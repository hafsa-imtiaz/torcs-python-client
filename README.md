# README - Python Client for TORCS Telemetry

## Overview

This project is a Python client for **TORCS (The Open Racing Car Simulator)**, designed to collect telemetry data from the racing simulation. The collected data is stored in a CSV file for further **AI-based controller training**.

### Features:

- Real-time telemetry data collection from TORCS.
- Storage of relevant vehicle and track data for analysis.
- CSV logging for AI-based training and performance evaluation.
- Noisy sensors (`focus`, `opponent`, and `track`) are **disabled** for clean data collection.

## **Stored Data in CSV**

The script stores **relevant telemetry data** from the TORCS simulation for AI model training. Below is a breakdown of what is stored and what is ignored.

### **Stored Data:**

#### **1. Core Vehicle State (Single-Value Sensors)**

| Field           | Description                                           |
| --------------- | ----------------------------------------------------- |
| `curLapTime`    | Current lap time in seconds.                          |
| `distFromStart` | Distance from the start line (meters).                |
| `distRaced`     | Total distance raced (meters).                        |
| `fuel`          | Remaining fuel (**irrelevant as fuel is unlimited**). |
| `gear`          | Current gear in use.                                  |
| `lastLapTime`   | Time taken for the last completed lap.                |
| `racePos`       | Current position in the race.                         |
| `rpm`           | Engine revolutions per minute (RPM).                  |
| `speedX`        | Forward speed of the car.                             |
| `speedY`        | Sideways speed.                                       |
| `speedZ`        | Vertical speed.                                       |
| `trackPos`      | Position relative to the center of the track.         |
| `angle`         | Angle between the car's heading and the track axis.   |
| `z`             | Car's altitude above the track.                       |

#### **2. Wheel Spin Velocity (4 Values)**

| Field Format    | Description                              |
| --------------- | ---------------------------------------- |
| `wheelSpin_0-3` | Measures wheel slip/spin for each wheel. |

- Useful for detecting oversteering or traction loss.

### **Data NOT Stored:**

1. **Noisy Sensors** (disabled as per requirements):

   - `focus` (Focus Sensors)
   - `opponent` (Opponent Sensors)
   - `track` (Edge-Distance Sensors)

2. **Car Damage**

   - The `damage` field is ignored as car damage is disabled.

3. **Fuel Level**

   - The `fuel` field is ignored since the project requirements state that fuel is unlimited.

## **Telemetry Implementation**

The telemetry data collection is implemented in a file called `telemetry.py`, which is responsible for the storage of the telemetry data recieved from the TORCS simulator. This file is imported and executed by `msgParser`, which processes and formats the received data before logging it.

## License

This project is part of the **Artificial Intelligence AI-2002 Spring-2025** course and is intended for academic purposes only.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```
2. Run the TORCS Simulator in the background.
3. Run the pyClient.py file.

## **Original Code Source**

The original Python 2 code for `pyClient` is from: [http://games.ws.dei.polimi.it/competitions/scr/](http://games.ws.dei.polimi.it/competitions/scr/) and has been converted to Python 3 with telemetry updates.

