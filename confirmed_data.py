import math
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping

import pandas as pd


DATASET_PATH = Path(__file__).resolve().parent / "data" / "data.csv"
LABELS = {"human", "ai"}
LABEL_SOURCES = {"reviewer", "resolved_appeal", "author_disclosure"}
FEATURE_COLUMNS = ("spread", "ttr", "punct")
SCORE_COLUMNS = (*FEATURE_COLUMNS, "model_score", "style_score", "combined_score")
DATASET_COLUMNS = (
    "content_id",
    "text",
    "label",
    "label_source",
    "confirmed_at",
    *SCORE_COLUMNS,
)
MIN_EXAMPLES_PER_LABEL = 5

_write_lock = threading.Lock()


def _validate_examples(examples: pd.DataFrame) -> None:
    """Reject invalid labels early so bad rows never silently train a model."""
    required = {"label", *FEATURE_COLUMNS}
    missing = required - set(examples.columns)
    if missing:
        raise ValueError(f"Dataset is missing columns: {', '.join(sorted(missing))}")

    invalid_labels = set(examples["label"].dropna()) - LABELS
    if invalid_labels:
        raise ValueError(f"Unknown labels: {', '.join(sorted(invalid_labels))}")


def add_confirmed_example(
    content_id: str,
    text: str,
    label: str,
    label_source: str,
    scores: Mapping[str, float | None],
    path: str | Path = DATASET_PATH,
) -> dict:
    """Add or replace one explicitly confirmed label and its raw scores.

    A content ID has one current dataset label; audit.py remains responsible
    for preserving the history of earlier decisions and appeal events.
    """
    content_id = str(content_id).strip()
    if not content_id:
        raise ValueError("content_id must not be empty")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text must be a non-empty string")
    if label not in LABELS:
        raise ValueError("label must be 'human' or 'ai'")
    if label_source not in LABEL_SOURCES:
        raise ValueError(
            "label_source must be 'reviewer', 'resolved_appeal', or "
            "'author_disclosure'"
        )
    if not isinstance(scores, Mapping):
        raise TypeError("scores must be a mapping of score names to values")

    unknown_scores = set(scores) - set(SCORE_COLUMNS)
    if unknown_scores:
        raise ValueError(f"Unknown scores: {', '.join(sorted(unknown_scores))}")

    row = {
        "content_id": content_id,
        "text": text,
        "label": label,
        "label_source": label_source,
        "confirmed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    for column in SCORE_COLUMNS:
        value = scores.get(column)
        if value is None or pd.isna(value):
            row[column] = None
            continue

        try:
            number = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{column} must be a finite number or None") from exc
        if not math.isfinite(number):
            raise ValueError(f"{column} must be a finite number or None")
        if column == "ttr" and not 0 <= number <= 1:
            raise ValueError("ttr must be between 0 and 1")
        if column in {"spread", "punct"} and number < 0:
            raise ValueError(f"{column} cannot be negative")
        if column in {"model_score", "style_score", "combined_score"} and not 0 <= number <= 1:
            raise ValueError(f"{column} must be between 0 and 1")
        row[column] = number

    if not any(row[column] is not None for column in FEATURE_COLUMNS):
        raise ValueError("At least one raw style feature score is required")

    dataset_path = Path(path)
    dataset_path.parent.mkdir(parents=True, exist_ok=True)
    with _write_lock:
        existing = load_confirmed_examples(dataset_path)
        # Reconfirming an item updates its current label; the audit log keeps
        # the previous decision and the events that led to this confirmation.
        existing = existing[existing["content_id"] != content_id]
        updated = pd.concat([existing, pd.DataFrame([row])], ignore_index=True)
        updated.to_csv(dataset_path, index=False)
    return row


def load_confirmed_examples(path: str | Path = DATASET_PATH) -> pd.DataFrame:
    """Load the current, confirmed dataset, preserving an empty schema."""
    dataset_path = Path(path)
    if not dataset_path.exists() or dataset_path.stat().st_size == 0:
        return pd.DataFrame(columns=DATASET_COLUMNS)

    examples = pd.read_csv(dataset_path, dtype={"content_id": "string"})
    missing = set(DATASET_COLUMNS) - set(examples.columns)
    if missing:
        raise ValueError(
            "Dataset has an older or incomplete schema; missing columns: "
            + ", ".join(sorted(missing))
        )

    _validate_examples(examples)
    invalid_sources = set(examples["label_source"].dropna()) - LABEL_SOURCES
    if invalid_sources:
        raise ValueError(f"Unknown label sources: {', '.join(sorted(invalid_sources))}")
    return examples.loc[:, DATASET_COLUMNS]


def summarize_by_label(examples: pd.DataFrame) -> pd.DataFrame:
    """Compare raw feature ranges by label before choosing any cutoffs."""
    _validate_examples(examples)
    if examples.empty:
        return pd.DataFrame()

    # Counts and medians expose both weak features and class overlap; a mean
    # alone can hide a few unusually long or punctuation-heavy texts.
    return examples.groupby("label")[list(FEATURE_COLUMNS)].agg(
        ["count", "median", "mean", "min", "max"]
    )


def fit_calibration(examples: pd.DataFrame) -> dict:
    """Derive exploratory per-feature cutoffs from labeled training examples.

    The midpoint between class medians is transparent and easy to inspect,
    but it is not a robust production model. Fit only on training data; use a
    separate held-out set with evaluate_calibration().
    """
    _validate_examples(examples)
    counts = examples["label"].value_counts()
    if any(counts.get(label, 0) < MIN_EXAMPLES_PER_LABEL for label in LABELS):
        raise ValueError(
            f"Need at least {MIN_EXAMPLES_PER_LABEL} examples of each label "
            "to fit exploratory cutoffs"
        )

    feature_cutoffs = {}
    for feature in FEATURE_COLUMNS:
        available = examples.dropna(subset=[feature])
        human_values = available.loc[available["label"] == "human", feature]
        ai_values = available.loc[available["label"] == "ai", feature]
        if min(len(human_values), len(ai_values)) < MIN_EXAMPLES_PER_LABEL:
            continue

        human_median = float(human_values.median())
        ai_median = float(ai_values.median())
        if human_median == ai_median:
            continue

        feature_cutoffs[feature] = {
            "threshold": (human_median + ai_median) / 2,
            "ai_direction": "higher" if ai_median > human_median else "lower",
            "human_median": human_median,
            "ai_median": ai_median,
        }

    if not feature_cutoffs:
        raise ValueError("No feature has distinct, sufficiently sampled class medians")

    return {
        "method": "midpoint_of_class_medians",
        "training_examples": int(len(examples)),
        "features": feature_cutoffs,
    }


def evaluate_calibration(examples: pd.DataFrame, calibration: dict) -> dict:
    """Report held-out accuracy and human false-positive rate for cutoffs.

    Each usable feature casts one vote. Ties remain 'unsure' rather than being
    forced into a human or AI label, since uncertainty is a valid outcome here.
    """
    _validate_examples(examples)
    features = calibration.get("features", {})
    if not features:
        raise ValueError("calibration has no feature cutoffs")
    if examples.empty:
        raise ValueError("examples must not be empty")

    labels = ("human", "ai", "unsure")
    confusion = {actual: {predicted: 0 for predicted in labels} for actual in LABELS}
    predictions = []

    for _, row in examples.iterrows():
        ai_votes = human_votes = 0
        for feature, cutoff in features.items():
            value = row.get(feature)
            if pd.isna(value):
                continue
            is_ai = (
                value >= cutoff["threshold"]
                if cutoff["ai_direction"] == "higher"
                else value <= cutoff["threshold"]
            )
            ai_votes += int(is_ai)
            human_votes += int(not is_ai)

        predicted = (
            "ai" if ai_votes > human_votes
            else "human" if human_votes > ai_votes
            else "unsure"
        )
        actual = row["label"]
        confusion[actual][predicted] += 1
        predictions.append({
            "content_id": row.get("content_id"),
            "actual": actual,
            "predicted": predicted,
        })

    total = len(predictions)
    human_count = sum(confusion["human"].values())
    ai_count = sum(confusion["ai"].values())
    return {
        "count": total,
        "accuracy": sum(confusion[label][label] for label in LABELS) / total,
        "human_false_positive_rate": (
            confusion["human"]["ai"] / human_count if human_count else None
        ),
        # An AI example labeled human or unsure was not successfully detected.
        "ai_miss_rate": (
            (confusion["ai"]["human"] + confusion["ai"]["unsure"]) / ai_count
            if ai_count else None
        ),
        "confusion": confusion,
        "predictions": predictions,
    }