# Task 8: integration checkpoint: function, NumPy and evidence of testing.
import numpy as np


def measurement_report(readings, limit=13.0):
    """Return count, mean, peak and strict over-limit count."""
    values = np.asarray(readings, dtype=float)
    # Handle an empty array, then calculate the report with NumPy.
    pass


for data in ([12.1, 11.8, 14.2, 13.0, 12.7],
             [-5.0, -2.0, -8.0],
             []):
    print(measurement_report(data))

# Add assertions for the original, negative and empty cases.
