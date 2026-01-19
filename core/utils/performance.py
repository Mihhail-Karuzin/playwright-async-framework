class PerformanceChecker:
    """
    Centralized performance validation logic.
    Used by performance tests to compare
    actual timings against defined baselines.
    """

    def __init__(
        self,
        actual_seconds: float,
        baseline_seconds: float,
        tolerance: float = 0.0,
    ):
        self.actual_seconds = actual_seconds
        self.baseline_seconds = baseline_seconds
        self.tolerance = tolerance

    def threshold(self) -> float:
        """
        Calculates the maximum allowed time.
        """
        return self.baseline_seconds + self.tolerance

    def is_within_threshold(self) -> bool:
        """
        Returns True if performance is acceptable.
        """
        return self.actual_seconds <= self.threshold()

    def failure_message(self, metric: str, user: str) -> str:
        """
        Human-readable assertion message.
        """
        return (
            f"{metric} for user '{user}' took {self.actual_seconds:.2f}s, "
            f"which exceeds allowed threshold of {self.threshold():.2f}s "
            f"(baseline={self.baseline_seconds:.2f}s, tolerance={self.tolerance:.2f}s)"
        )

