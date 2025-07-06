# carANN.py

import numpy as np
import joblib
import tensorflow as tf

SEQ_LENGTH = 5

class CarControllerANN:
    def __init__(self):
        self.scaler = joblib.load("racing_scaler.pkl")
        self.interpreter = tf.lite.Interpreter("torcs_model.tflite")
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.buffer = []

    def preprocess(self, state):
        speed = np.sqrt(state['SpeedX']**2 + state['SpeedY']**2 + state['SpeedZ']**2)
        twidth = state['Track_1'] + state['Track_2']
        curve = np.mean([state[f'Track_{i}'] for i in [3, 4, 5]])
        center_dist = np.abs(state['TrackPosition'])
        tpos_squared = state['TrackPosition'] ** 2

        scaled_input = [
            state['RPM'],
            state['SpeedX'],
            speed,
            twidth,
            curve,
            center_dist,
            tpos_squared
        ]

        scaled_vals = self.scaler.transform([scaled_input])[0]

        model_input = [
            state['RPM'],
            state['SpeedX'],
            state['SpeedY'],
            state['SpeedZ'],
            state['TrackPosition'],
            state['Z'],
            *[state[f'Track_{i}'] for i in range(1, 20)],
            # engineered walay here
            speed,  
            twidth, 
            curve,  
            center_dist, 
            tpos_squared                                           
        ]

        model_input[0] = scaled_vals[0]
        model_input[1] = scaled_vals[1]
        model_input[25] = scaled_vals[2]
        model_input[26] = scaled_vals[3]
        model_input[27] = scaled_vals[4]
        model_input[28] = scaled_vals[5]
        model_input[29] = scaled_vals[6]

        return model_input

    def predict(self, sensor_data):
        self.buffer.append(self.preprocess(sensor_data)) # keeping out lstm seq

        if len(self.buffer) > SEQ_LENGTH: # fixed seq_length
            self.buffer.pop(0)

        if len(self.buffer) < SEQ_LENGTH: # initial stages
            return {'steer': 0.0, 'accel': 0.6, 'brake': 0.0}

        input_data = np.array(self.buffer, dtype=np.float32).reshape(1, SEQ_LENGTH, -1)
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        prediction = self.interpreter.get_tensor(self.output_details[0]['index'])[0]

        # ensure valid values - sab values in correct range warna wo weird error
        steering = np.clip(prediction[0], -1, 1)
        accel = np.clip(prediction[1], 0, 1)
        brake = np.clip(prediction[2], 0, 1)

        if brake > 0.3:
            accel = 0.0

        return {'steer': float(steering), 'accel': float(accel), 'brake': float(brake)}