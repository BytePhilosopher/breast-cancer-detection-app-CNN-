import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint

DATA_DIR = "../dataset"
IMAGE_SIZE = (50, 50)
BATCH_SIZE = 32
EPOCHS = 10
MODEL_PATH = "../backend/model/model.h5"

def build_model(input_shape):
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D(2, 2),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.3),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def train():
    datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

    train_gen = datagen.flow_from_directory(
        DATA_DIR,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary',
        subset='training'
    )

    val_gen = datagen.flow_from_directory(
        DATA_DIR,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary',
        subset='validation'
    )

    input_shape = (IMAGE_SIZE[0], IMAGE_SIZE[1], 3)
    model = build_model(input_shape)

    checkpoint = ModelCheckpoint(MODEL_PATH, monitor='val_accuracy', save_best_only=True)

    model.fit(train_gen, validation_data=val_gen, epochs=EPOCHS, callbacks=[checkpoint])
    print(f"✅ Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train()
