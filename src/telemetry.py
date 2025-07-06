import csv
import os
from datetime import datetime
import carControl 

# Generate a timestamp-based filename
filename = f"telemetry_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S').replace(':', '-')}.csv"

# Define headers for telemetry data
headers = [
    "Current Lap Time", "Distance From Start", "Distance Raced", "SensorGear", "Last Lap Time", 
    "Race Position", "RPM", "SpeedX", "SpeedY", "SpeedZ", "Track Position", "Angle", 
    "Z (Altitude)"  
]

# Define extra headers for wheel spins, track, and opponent data
extra_headers = [f"Wheel_#{str(i)}_Spin" for i in range(4)] + ["Track_#" + str(i) for i in range(19)] + ["Opponent_#" + str(i) for i in range(36)]
headers.extend(extra_headers)
headers.extend(["Steering", "Acceleration", "ControlGear", "Brake", "Clutch"])  

# Flag for checking if the file already exists
file_exists = os.path.isfile(filename)

def save_telemetry(state_data, car_output):
    """Save telemetry state_data to a CSV file, including car control values."""
    
    # Helper function to safely extract state_data from the dictionary
    def get_value_or_default(state_data, key, default=None):
        return state_data.get(key, [default])[0]
    
    # Open the file for appending state_data
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)

        # Write the header if the file is new
        if not file_exists:
            writer.writerow(headers)
        
        # Create a row of state_data
        row = [
            get_value_or_default(state_data, "curLapTime", 0), 
            get_value_or_default(state_data, "distFromStart", 0), 
            get_value_or_default(state_data, "distRaced", 0),
            get_value_or_default(state_data, "gear", 0), 
            get_value_or_default(state_data, "lastLapTime", 0),
            get_value_or_default(state_data, "racePos", 0), 
            get_value_or_default(state_data, "rpm", 0),
            get_value_or_default(state_data, "speedX", 0), 
            get_value_or_default(state_data, "speedY", 0),
            get_value_or_default(state_data, "speedZ", 0), 
            get_value_or_default(state_data, "trackPos", 0),
            get_value_or_default(state_data, "angle", 0),
            get_value_or_default(state_data, "z", 0) 
        ]
        
        # Add the wheel spin velocities
        row.extend(state_data.get("wheelSpinVel", [0, 0, 0, 0]))
        
        row.extend(state_data.get("track", [0] * 19))

        # Optional: Add opponent state_data
        row.extend(state_data.get("opponents", [200] * 36))  

        # car control values aka output
        row.extend(car_output.get("steer"))
        row.extend(car_output.get("accel"))
        row.extend(car_output.get("gear"))
        row.extend(car_output.get("brake"))
        row.extend(car_output.get("clutch"))
        
        writer.writerow(row)
        print(f"Telemetry data saved to: {filename}")
