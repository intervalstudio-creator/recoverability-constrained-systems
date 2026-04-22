"""
Public population view placeholder.

The public repository preserves only the statement that population-level risk
can be assessed. Aggregation mechanics, clustering thresholds, and cohort
inference internals are intentionally withheld.
"""

from collections import Counter


def summarise_population(states: list[str]) -> dict:
    counts = Counter(states)
    return {
        "counts": dict(counts),
        "note": "Population risk can be assessed, but aggregation mechanics are intentionally excluded from the public repository.",
    }
