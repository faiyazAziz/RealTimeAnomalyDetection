import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import random
import math

# EWMA Parameters
alpha = 0.2
mu_ewma = None
sigma_ewma = None
z_threshold = 1.77
normal_data_buffer = []

def data_stream():
    """
    Generator function to simulate a data stream with regular patterns,
    seasonal elements, random noise, and occasional anomalies.
    """
    t = 0
    while True:
        seasonal = 10 * np.sin(2 * np.pi * t / 50)
        trend = 0.02 * t
        noise = np.random.normal(0, 1)
        value = seasonal + trend + noise

        # Inject anomalies occasionally
        if random.randint(0, 100) == 50:
            value += random.choice([20, -20])

        t += 1
        yield value

def ewma(prev_ewma, value, alpha):
    """Calculates Exponentially Weighted Moving Average (EWMA)."""
    return value if prev_ewma is None else alpha * value + (1 - alpha) * prev_ewma

def detect_anomaly(value):
    """
    Detects anomalies using EWMA-based z-score.
    """
    global mu_ewma, sigma_ewma

    # Update EWMA for mean and variance
    mu_ewma = ewma(mu_ewma, value, alpha)
    sigma_ewma = ewma(sigma_ewma, (value - mu_ewma) ** 2, alpha) if sigma_ewma is not None else 0

    # Calculate standard deviation
    sigma = math.sqrt(sigma_ewma) if sigma_ewma else 1  # Avoid division by zero

    # Calculate z-score and flag as anomaly if it exceeds the threshold
    return abs((value - mu_ewma) / sigma) > z_threshold

def update(frame):
    """
    Updates the plot with new data, detects anomalies, and adjusts plot size.
    """
    t, value = frame

    # Update plot data
    xdata.append(t)
    ydata.append(value)
    ln.set_data(xdata, ydata)

    # Detect anomaly and update anomaly plot if detected
    if detect_anomaly(value):
        anomaly_x.append(t)
        anomaly_y.append(value)
        an_ln.set_data(anomaly_x, anomaly_y)

    # Dynamically adjust plot limits
    ax.set_xlim(0, xdata[-1] + 10)
    ax.set_ylim(min(ydata) - 10, max(ydata) + 10)

    return ln, an_ln

def data_gen():
    """
    Generates data points with timestamps for animation.
    """
    t = 0
    for value in data_stream():
        yield t, value
        t += 1

# Initialize plot
fig, ax = plt.subplots()
xdata, ydata = [], []
anomaly_x, anomaly_y = [], []  # Initialize both lists properly
ln, = plt.plot([], [], 'b-', label='Data Stream')
an_ln, = plt.plot([], [], 'ro', label='Anomalies')
plt.title('Anomaly detection using exponential weighted moving average')
plt.legend()


def init():
    ax.set_xlim(0, 100)
    ax.set_ylim(-30, 30)
    return ln, an_ln

# Run the animation to show frame by frame
ani = animation.FuncAnimation(fig, update, data_gen, init_func=init, blit=True, interval=100)

plt.show()
