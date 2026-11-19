"""Helpers for the loop scheduler (probe comparison and rest decisions)."""
from __future__ import annotations


def compare_value(value: int, operator, threshold: int) -> bool:
    """Compare a probe value with the configured operator.

    ``operator`` may be a ``LoopCompare`` enum or its string value.
    """
    operation = getattr(operator, 'value', operator)
    match operation:
        case '>':
            return value > threshold
        case '>=':
            return value >= threshold
        case '<':
            return value < threshold
        case '<=':
            return value <= threshold
        case '==':
            return value == threshold
        case '!=':
            return value != threshold
    return False


def wait_after_poll(polls: int, interval: int, rest_every: int, rest_duration: int) -> int:
    """Return how long to sleep after the given number of failed probes."""
    if rest_every > 0 and polls % rest_every == 0:
        return max(rest_duration, 0)
    return max(interval, 0)
