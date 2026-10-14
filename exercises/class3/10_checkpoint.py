# Task 10: draw the flow chart, trace it, then write the full report.
readings = [12.1, None, 11.8, 14.2, 13.0, None, 12.7]
limit = 13.0

# Initialise total, count, skipped and above to zero; peak to None.
# Use a for loop. Missing readings increment skipped, then continue.
# Valid readings update total, count, peak and the count above the limit.
# Initialise peak from the first valid reading (not from zero).
# Print Valid readings and Skipped for every test.
# If count == 0, print No valid readings and do not calculate a mean.
# Otherwise print Mean (two decimals), Peak (one decimal), and Above 13.0.
# No sum(), len(), max(), comprehensions or NumPy for the calculation.
# Test the original list, all missing, empty, negative and boundary data.
