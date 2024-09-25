---

# EWMA Anomaly Detection

This project implements real-time anomaly detection using Exponentially Weighted Moving Average (EWMA) on a synthetic data stream with seasonal, trend, and noise components.

## Features

- **Real-time data stream** with periodic and random noise.
- **EWMA-based anomaly detection** using z-score.
- **Live plot** highlighting detected anomalies in red.

## Prerequisites

Ensure Python 3.x and the following libraries are installed:

```bash
pip install numpy matplotlib
```

## Running the Project

To run the project:

```bash
python anomaly_detection.py
```

## Customization

- `alpha`: EWMA smoothing factor (default: 0.2)
- `z_threshold`: Z-score threshold for anomaly detection (default: 1.77)
