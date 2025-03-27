import csv
import os
from datetime import datetime


filename = f"telemetry_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

headers = [
    "Current Lap Time", "Distance From Start", "Distance Raced", "Gear", "Last Lap Time", 
    "Race Position", "RPM", "SpeedX", "SpeedY", "SpeedZ", "Track Position", "Angle",
    "Z (Altitude)" #, "Fuel", "Damage"
]

extra_headers = [f"Wheel_#{str(i)}_Spin" for i in range(4)] # + ["Track_#" + str(i) for i in range(19)] + ["Opponent_#" + str(i) for i in range(36)]

headers.extend(extra_headers)
file_exists = os.path.isfile(filename)

def save_telemetry(data):
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        
        if not file_exists:
            writer.writerow(headers)

        row = [
            data["curLapTime"][0], data["distFromStart"][0], data["distRaced"][0], 
            data["gear"][0], data["lastLapTime"][0], 
            data["racePos"][0], data["rpm"][0], data["speedX"][0], data["speedY"][0], 
            data["speedZ"][0], data["trackPos"][0], data["angle"][0], 
            data["z"][0] #, data["fuel"][0], data["damage"][0]
        ]
        row.extend(data["wheelSpinVel"])
        
        #row.extend(data["track"])
        #row.extend(data["opponents"])
        # data not written ---> noisy sensors (focus values, opponent values (always 200 so i didnt save) and track edges values), damage, fuel

        writer.writerow(row)
        print(f"Telemetry data for saved to: {filename}")
