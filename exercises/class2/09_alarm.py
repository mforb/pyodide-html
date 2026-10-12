# Task 9: combine a sensor reading with an active-site check.
site = {"active": True, "low_c": -20.0, "high_c": 0.0}
temp_c = -25.0

# Print ALARM only when the site is active AND the reading is outside the range.
# Both endpoints (-20.0 and 0.0) are inside the range.
# Otherwise print NO ALARM.
# Use and, or, and dictionary lookups.
