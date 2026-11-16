"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics
import traceback
import audit


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies. ← TODO

    Returns:
        A float. Decide yourself what scale it's on and which direction means
        "more human" — then write that down, because your combining rule
        depends on knowing it.

        Scale: coefficient of variation (stdev / mean of sentence lengths in
        words). Higher = lumpier = more human. Returns NaN when there are
        fewer than two sentences, because spread is undefined there and the
        caller should treat it as "no evidence", not as "very even".

    A hint on what you're reaching for: the standard deviation of sentence
    lengths, probably divided by the mean so a long text and a short one are
    comparable. `statistics.stdev` is imported for you.

    Watch the edge case: a one-sentence submission has no spread at all, and
    `stdev` raises on fewer than two values. Decide what that should return
    before the attack set decides for you.
    """
    s_lengths = [len(words(sentence)) for sentence in sentences(text)]
    s_lengths = [n for n in s_lengths if n > 0]
    if len(s_lengths) < 2:
        return float("nan")
    mean_length = statistics.mean(s_lengths)
    if mean_length == 0:
        return float("nan")
    return statistics.stdev(s_lengths) / mean_length


def type_token_ratio(text: str, window_size: int = 25) -> float:
    """Moving-average type-token ratio; higher means more varied vocabulary."""
    word_list = words(text)
    if not word_list:
        return 0.0

    if len(word_list) <= window_size:
        return len(set(word_list)) / len(word_list)

    ratios = []
    for window_start in range(len(word_list) - window_size + 1):
        window = word_list[window_start:window_start + window_size]
        ratios.append(len(set(window)) / window_size)

    return statistics.mean(ratios)


def punctuation_density(text: str) -> float:
    """Selected punctuation marks per 100 words; descriptive, not directional.

    Hyphens are not counted: they mostly sit inside compound words
    ("early-career") rather than acting as punctuation between clauses.
    """
    word_count = len(words(text))
    if not word_count:
        return 0.0

    punctuation_count = sum(
        1 for character in text if character in ",;:!?—–"
    )
    return 100 * punctuation_count / word_count


# ── Combining them ───────────────────────────────────────────────────────────

def bound(x: float) -> float:
    return min(max(x, 0.0), 1.0)


def style_signal(text: str, content_id: str, creator_id: str) -> tuple[float, float, float, float]:
    """0-1, HIGHER = MORE LIKELY AI. Each measure becomes an AI-ness sub-score
    on 0-1 first, so none wins just because its raw numbers are bigger."""
    # No words means no evidence either way: stay neutral.
    if not words(text):
        return 0.5, 0.5, 0.5, 0.5

    try:
        cv = sentence_length_spread(text)
        ttr = type_token_ratio(text)
        punct = punctuation_density(text)

        audit.log_stylometry(
            content_id=content_id, 
            creator_id=creator_id,
            flipped=False,
            sentence_length_spread=cv,
            type_token_ratio=ttr,
            punctuation_density=punct,
            text=text,
        )

        
        # NaN (fewer than two sentences) -> neutral sub-score
        spread_ai = 0.5 if cv != cv else bound(1.0 - cv / 0.8)         # flipped
        # Window-based TTR sits higher (~0.7-0.95) than whole-text TTR, so the
        # baseline/span here are placeholders: recalibrate on your own samples.
        ttr_ai = bound(1.0 - (ttr - 0.75) / 0.20)   # flipped
        # Density is per 100 words (~5-15 typical), so divide by 15, not 0.15.
        # Direction (more punctuation = more AI) is an unverified assumption.
        punct_ai = bound(punct / 15) 
        
        main_score =  round(0.7 * spread_ai + 0.3 * ttr_ai, 4)

        audit.log_stylometry(
            content_id=content_id, 
            creator_id=creator_id,
            flipped=True,
            sentence_length_spread=cv,
            type_token_ratio=ttr,
            punctuation_density=punct,
            text=text,
            main_score=main_score,
        )

        return main_score, spread_ai, ttr_ai, punct_ai
    except Exception:
        # Log the real error instead of hiding it, then fall back to neutral.
        traceback.print_exc()
        return 0.5, 0.5, 0.5, 0.5  # neutral fallback


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")