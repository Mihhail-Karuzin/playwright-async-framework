def calculate_threshold(baseline: float, multiplier: float, buffer: float) -> float:
    """
    Calculate dynamic performance threshold.

    threshold = baseline * multiplier + buffer
    """
    return baseline * multiplier + buffer
