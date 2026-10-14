# Optional: stop a calculation that cannot reach the requested tolerance.
x = 2.0
tolerance = 1e-16
max_updates = 20
guess = x / 2
updates = 0

# Plan a square-root loop with two conditions combined using and:
# error is still above tolerance AND updates is below max_updates.
# Count each completed update.
# After the loop, report CONVERGED only if the error is within tolerance.
# Otherwise report NOT CONVERGED. Always print Updates.
# Try tolerance = 1e-6, then max_updates = 2.
# This version assumes positive x, tolerance and max_updates.
