"""
Performance baselines for critical user flows.

These values define expected performance
characteristics and allowed tolerances.
"""

INVENTORY_LOAD_BASELINES = {
    "standard_user": {
        "expected_seconds": 3.0,
        "tolerance": 0.5,
    },
    "performance_glitch_user": {
        "expected_seconds": 3.0,
        "tolerance": 2.5,
    },
}


