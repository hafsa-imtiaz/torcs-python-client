# ANN.py

import pandas as pd
import numpy as np
import joblib
import tensorflow as tf
from sklearn.preprocessing import RobustScaler
import logging
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, LayerNormalization
from tensorflow.keras.callbacks import EarlyStopping

# Configuration
DATA_DIR = "./"
SEQ_LENGTH = 5
BATCH_SIZE = 64
EPOCHS = 500
PATIENCE = 10

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def data_preprocessing():
    logger.info("Loading and preprocessing data...")

    df = pd.read_csv(f"{DATA_DIR}Dataset.csv")
    df.columns = df.columns.str.strip()

    base_features = ["RPM", "SpeedX", "SpeedY", "SpeedZ", "TrackPosition", "Z", 
                     "Steering", "Acceleration", "Braking"]
    track_features = [f"Track_{i}" for i in range(1, 20)]
    df = df[base_features + track_features].copy()

    df['Speed'] = np.sqrt(df['SpeedX']**2 + df['SpeedY']**2 + df['SpeedZ']**2)
    df['TrackWidth'] = df['Track_1'] + df['Track_2']
    df['UpcomingCurvature'] = df[['Track_3', 'Track_4', 'Track_5']].mean(axis=1)
    df['DistanceFromCenter'] = np.abs(df['TrackPosition'])
    df['TrackPositionSquared'] = df['TrackPosition'] ** 2

    scaler = RobustScaler()
    scaled_features = ['RPM', 'SpeedX', 'Speed', 'TrackWidth', 'UpcomingCurvature', 
                       'DistanceFromCenter', 'TrackPositionSquared']
    df[scaled_features] = scaler.fit_transform(df[scaled_features])
    joblib.dump(scaler, f"{DATA_DIR}racing_scaler.pkl")

    data = df.drop(columns=['Steering', 'Acceleration', 'Braking'])
    targets = df[['Steering', 'Acceleration', 'Braking']]

    X, y = [], []
    for i in range(SEQ_LENGTH, len(df)):
        X.append(data.iloc[i-SEQ_LENGTH:i].values)
        y.append(targets.iloc[i].values)

    X, y = np.array(X), np.array(y)
    split = int(0.8 * len(X))
    return X[:split], X[split:], y[:split], y[split:]

def model_training(X_train, X_val, y_train, y_val):
    inputs = tf.keras.Input(shape=(X_train.shape[1], X_train.shape[2]))
    x = tf.keras.layers.LSTM(128, return_sequences=True)(inputs)
    x = tf.keras.layers.LSTM(64)(x)
    x = tf.keras.layers.Dense(64, activation='relu')(x)
    x = tf.keras.layers.Dropout(0.2)(x)
    x = tf.keras.layers.Dense(32, activation='relu')(x)
    outputs = tf.keras.layers.Dense(3)(x)

    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mse', metrics=['mae'])

    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=[
            tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=PATIENCE, restore_best_weights=True),
            tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5)
        ]
    )

    model.save(f"{DATA_DIR}torcs_model.h5")

    # Convert to TFLite
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.target_spec.supported_ops = [
        tf.lite.OpsSet.TFLITE_BUILTINS,
        tf.lite.OpsSet.SELECT_TF_OPS
    ]
    converter._experimental_lower_tensor_list_ops = False
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_types = [tf.float16]

    try:
        tflite_model = converter.convert()
        with open(f"{DATA_DIR}torcs_model.tflite", 'wb') as f:
            f.write(tflite_model)
        print("TFLite model saved successfully!")
    except Exception as e:
        print(f"Error converting to TFLite: {e}")
        model.save(f"{DATA_DIR}torcs_model_saved", save_format='tf')

    return model, history

if __name__ == "__main__":
    X_train, X_val, y_train, y_val = data_preprocessing()
    model, history = model_training(X_train, X_val, y_train, y_val)
