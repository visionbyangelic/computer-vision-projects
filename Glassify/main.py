import cv2 as cv
import numpy as np
import mediapipe as mp
import time


# Step 1: Open camera and allow it to warm up
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

time.sleep(2)

# Step 2: initialize MediaPipe Face Mesh

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False,
                                max_num_faces=1,
                                min_detection_confidence=0.5,
                                min_tracking_confidence=0.5)

#step 3: load the glasses image
glasses_image = cv.imread('glasses.png', cv.IMREAD_UNCHANGED)
if glasses_image is None:
    print("Error: Glasses image not found.")
    exit()

while cap.isOpened():   
    # Step 4: detect landmarks, get eye points
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv.flip(frame, 1)
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            ih, iw, _ = frame.shape

            # Use outer eye landmarks for max width
            left_eye_outer = face_landmarks.landmark[33]
            right_eye_outer = face_landmarks.landmark[263]
            y = int(left_eye_outer.y * ih)

            # Calculate glasses position and size with big padding
            x1 = int(left_eye_outer.x * iw)
            x2 = int(right_eye_outer.x * iw)

            glasses_width = x2 - x1
            padding = int(glasses_width * 0.5)  # 50% padding, less than before

            x1 = max(0, x1 - padding // 2)
            x2 = min(iw, x2 + padding // 2)
            glasses_width = x2 - x1

            # Maintain aspect ratio, make glasses taller (1.5x)
            aspect_ratio = glasses_image.shape[0] / glasses_image.shape[1]
            glasses_height = int(glasses_width * aspect_ratio * 1.1)  # 10% taller than before

            # Lower glasses more vertically
            y_offset = int(y - glasses_height / 2) + 10
            x_offset = x1

            # Resize the glasses
            resized_glasses = cv.resize(glasses_image, (glasses_width, glasses_height))

            # Overlay with transparency (alpha blending)
            for i in range(glasses_height):
                for j in range(glasses_width):
                    if y_offset + i >= ih or x_offset + j >= iw or y_offset + i < 0 or x_offset + j < 0:
                        continue
                    alpha = resized_glasses[i, j, 3] / 255.0  # Alpha channel
                    if alpha > 0:
                        for c in range(3):
                            frame[y_offset + i, x_offset + j, c] = (
                                alpha * resized_glasses[i, j, c] +
                                (1 - alpha) * frame[y_offset + i, x_offset + j, c]
                            )

    cv.imshow('Face Filter - Glasses', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv.destroyAllWindows()
