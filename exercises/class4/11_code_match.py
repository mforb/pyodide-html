# Optional Task 11: compare a received code with a circularly shifted register.
# One sample per chip, known code, no noise or frequency offset.
import numpy as np

register = np.array([1, 1, 1, -1, 1, -1, -1])
received = np.array([-1, -1, 1, 1, 1, -1, 1])


def match_score(received, trial):
    # Same signs multiply to +1; different signs multiply to -1.
    # TODO: return np.sum(received * trial).
    pass


for shift in range(len(register)):
    trial = np.roll(register, shift)  # positive = circular shift to the right
    print(f"Shift {shift}: score {match_score(received, trial)}")

# Which shift scores highest? This is a toy code-phase search, not a PRN generator.
