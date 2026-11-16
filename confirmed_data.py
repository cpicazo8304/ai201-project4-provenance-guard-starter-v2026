import math
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping

import pandas as pd
import numpy as np


DATASET_PATH = Path(__file__).resolve().parent / "data" / "data.csv"
LABELS = {"human", "ai"}
LABEL_SOURCES = {"reviewer", "resolved_appeal", "author_disclosure"}
FEATURE_COLUMNS = ("spread", "ttr", "punct")
SCORE_COLUMNS = (*FEATURE_COLUMNS, "model_score", "style_score", "combined_score")
DATASET_COLUMNS = (
    "content_id",
    "text",
    "label",
    "labermed_at",
    *SCOREl_source",
    "confi_COLUMNS,
)
DEFAULT_CALIBRATION = {
    "spread": {"spread_cutoff": 0.8},
    "ttr":    {"ttr_base": 0.75, "ttr_span": 0.20},   # redo if you change the window size
    "punc":   {"punct_div": 15},
}
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
    admin_id: str,
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
    admin_id = str(admin_id).strip()
    if not content_id:
        raise ValueError("content_id must not be empty")
    if not admin_id:
        raise ValueError("admin_id must not be empty")
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
        "admin_id": admin_id,
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


def fit_calibration(examples: pd.DataFrame) -> dict:
    """Derive exploratory per-feature cutoffs from labeled training examples.
    """
    _validate_examples(examples)
    feature_cutoffs = {f: dict(v) for f, v in DEFAULT_CALIBRATION.items()}

    counts = examples["label"].value_counts()
    if any(counts.get(label, 0) < MIN_EXAMPLES_PER_LABEL for label in LABELS):
        return feature_cutoffs  # not enough data: all defaults

    for feature in FEATURE_COLUMNS:
        available = examples.dropna(subset=[feature])
        human_values = available.loc[available["label"] == "human", feature]
        ai_values = available.loc[available["label"] == "ai", feature]

        if min(len(human_values), len(ai_values)) < MIN_EXAMPLES_PER_LABEL:
            continue  # keep default

        # Direction check: spread and ttr higher for human, punc higher for AI.
        expected_human_higher = feature in ("spread", "ttr")
        if (human_values.mean() > ai_values.mean()) != expected_human_higher:
            continue  # reversed or flat: keep default

        if feature == "spread":
            feature_cutoffs[feature] = {
                "spread_cutoff": np.percentile(human_values, 90)
            }
        elif feature == "ttr":
            ttr_base = np.percentile(ai_values, 10)
            ttr_span = np.percentile(human_values, 90) - ttr_base
            if ttr_span <= 0:
                continue  # groups overlap too much: keep default
            feature_cutoffs[feature] = {"ttr_base": ttr_base, "ttr_span": ttr_span}
        elif feature == "punc":
            punct_div = np.percentile(ai_values, 90)
            if punct_div <= 0:
                continue
            feature_cutoffs[feature] = {"punct_div": punct_div}

    return feature_cutoffs


def bound(x: float) -> float:
    return min(max(x, 0.0), 1.0)


def calculate_transformed_values(spread, ttr, punct, cutoffs) -> tuple[float, float, float]:
    """Turn raw measures into 0-1 transformed sub-scores (higher = more AI-like)."""
    # NaN spread (fewer than two sentences) -> neutral
    if spread != spread:
        spread_transformed = 0.5
    else:
        spread_transformed = bound(1.0 - spread / cutoffs["spread"]["spread_cutoff"])

    ttr_transformed = bound(
        1.0 - (ttr - cutoffs["ttr"]["ttr_base"]) / cutoffs["ttr"]["ttr_span"]
    )
    punct_transformed = bound(punct / cutoffs["punc"]["punct_div"])

    return spread_transformed, ttr_transformed, punct_transformed


DEFAULT_WEIGHTS = (0.5, 0.3, 0.2)

def fit_weights(examples: pd.DataFrame) -> tuple[float, float, float]:
    """Weight each feature by how well its raw values separate human from AI."""
    is_ai = examples["label"] == "ai"
    # direction: spread/ttr are higher for human, punc is higher for AI
    sign = {"spread": -1, "ttr": -1, "punc": 1}

    separations = []
    for feature in ["spread", "ttr", "punc"]:
        ai_vals = examples.loc[is_ai, feature].dropna()
        human_vals = examples.loc[~is_ai, feature].dropna()
        spread_sum = ai_vals.std() + human_vals.std()
        if not spread_sum:                      # zero or NaN: can't measure
            separations.append(0.0)
            continue
        gap = sign[feature] * (ai_vals.mean() - human_vals.mean())
        separations.append(max(gap, 0.0) / spread_sum)   # reversed feature -> 0

    total = sum(separations)
    if total <= 0:
        return DEFAULT_WEIGHTS
    return tuple(s / total for s in separations)