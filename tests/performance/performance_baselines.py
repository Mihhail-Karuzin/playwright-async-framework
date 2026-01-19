class PerformanceBaseline:
    """
    Performance baselines (seconds).
    Values represent p75–p90 real measurements, not SLA.
    """

    INVENTORY_LOAD = {
        "standard_user": 1.8,
        "performance_glitch_user": 5.0,
    }

    DEFAULT_MULTIPLIER = 1.5
    DEFAULT_BUFFER = 0.5

