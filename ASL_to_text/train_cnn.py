# train_cnn.py
# Trains a CNN to recognize ASL A-Z plus 'del', 'space', 'nothing' (29 classes).

import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
import os

# Setup MediaPipe Hands—one hand, 70% confidence.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Data directory—expects subfolders A/, B/, ..., Z/, del/, space/, nothing/.
data_dir = "./asl_alphabet_train"

# 29 classes: A-Z + 3 extras.
letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + ["del", "space", "nothing"]
num_samples = 1000  # 1,000 per class = 29,000 total (adjust if less data).

X, y, valid_labels = [], [], set()
failed_loads = 0  # Fixed: Track failed loads.

# Load data dynamically.
valid_classes = []
for label, letter in enumerate(letters):
    folder = os.path.join(data_dir, letter)
    if not os.path.exists(folder):
        print(f"Error: {folder} missing—'{letter}' won’t be trained!")
        continue
    letter_files = [f for f in os.listdir(folder) if f.endswith(".jpg")]
    if len(letter_files) < 50:  # Fixed: Warn if too few samples.
        print(f"Warning: Only {len(letter_files)} samples for {letter}—need more data!")
    valid_classes.append((label, letter, letter_files))
    print(f"Found {len(letter_files)} images for {letter}")

for label, letter, letter_files in valid_classes:
    for i, img_name in enumerate(letter_files[:num_samples]):
        img_path = os.path.join(folder, img_name)
        img = cv2.imread(img_path)
        if img is None:
            print(f"Error loading {img_path}")
            failed_loads += 1
            continue
        
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        
        if results.multi_hand_landmarks:  # Hand detected—use landmarks.
            hand_landmarks = results.multi_hand_landmarks[0]
            landmark_array = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]).flatten()
            X.append(landmark_array)
            y.append(label)
            valid_labels.add(label)
        elif letter == "nothing":  # No hand = 'nothing' class.
            X.append(np.zeros(63))  # Zero vector for no landmarks.
            y.append(label)
            valid_labels.add(label)

print(f"Total valid samples: {len(X)}")
if failed_loads > 0:
    print(f"Total failed image loads: {failed_loads}")
hands.close()

if len(valid_labels) < 1:
    print(f"Error: No valid classes found—check your data!")
    exit()

num_classes = len(valid_labels)
print(f"Training on {num_classes} classes.")
X = np.array(X)
y = tf.keras.utils.to_categorical(y, num_classes=num_classes)  # Fixed: Dynamic num_classes.

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# CNN with dropout for robustness.
model = models.Sequential([
    layers.Input(shape=(63,)),  # 63 landmark values (21 points × [x, y, z]).
    layers.Dense(256, activation="relu"),
    layers.Dropout(0.3),  # Fixed: Added dropout.
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.3),
    layers.Dense(64, activation="relu"),
    layers.Dense(num_classes, activation="softmax")  # Fixed: Dynamic output.
])

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
model.fit(X_train, y_train, epochs=15, batch_size=32, validation_data=(X_test, y_test))

loss, accuracy = model.evaluate(X_test, y_test)
print(f"Accuracy: {accuracy*100:.2f}%")

model.save(f"asl_{num_classes}_model.keras")  # Fixed: Dynamic filename.