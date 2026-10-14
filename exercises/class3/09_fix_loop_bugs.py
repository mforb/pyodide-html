# Task 9: two deliberate loop bugs. Predict them before running.
# The table should include 50 kN, not finish at 40 kN.
for load in range(0, 50, 10):
    print(load)

# This loop should add 1 + 2 + 3, then finish.
# It deliberately omits an update, so the runner will stop it after 5 seconds.
step = 1
total = 0
while step <= 3:
    total += step

print(f"Step total: {total}")
