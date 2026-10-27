# Task 7: estimate one chip's duration from an idealised signal.
# Each sample is 0.5 ms apart. Adjacent chips can have the same sign.
import matplotlib.pyplot as plt
import numpy as np

time_ms = np.arange(17) * 0.5
signal = np.array([1, 1, -1, -1, -1, -1, 1, 1,
                   -1, -1, 1, 1, 1, 1, -1, -1, -1])

# The step plot holds each sample until the next sample time.
plt.figure(figsize=(6, 3))  # Start a fresh plot each time you run the code.
plt.step(time_ms, signal, where="post")
plt.ylim(-1.5, 1.5)
plt.yticks([-1, 1])
# TODO: add title, xlabel, ylabel (signal is unitless), grid and plt.show().
# Read the shortest gap between visible changes; print your estimate in ms.
