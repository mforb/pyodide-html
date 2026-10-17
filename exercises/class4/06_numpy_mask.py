# Task 6: select engineering data with a NumPy mask.
import numpy as np

wind_speed_ms = np.array([12.0, 20.0, 24.5, 18.0, 31.0, 20.0])
limit_ms = 20.0

# Select only values strictly above the limit.
# Print the number selected, their mean to one decimal place,
# and whether the original value at the limit was selected.
