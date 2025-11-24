import cv2 as cv
import mediapipe as mp
import numpy as np

# Open webcam
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(
    model_selection=0,  # 0 = short range (webcam), 1 = long range (camera >2m)
    min_detection_confidence=0.5
)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv.flip(frame, 1)
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = face_detection.process(rgb_frame)

    if results.detections:
        for detection in results.detections:
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = frame.shape
            x = int(bboxC.xmin * iw)
            y = int(bboxC.ymin * ih)
            w = int(bboxC.width * iw)
            h = int(bboxC.height * ih)

            # Clamp to image bounds
            x = max(0, x)
            y = max(0, y)
            w = min(w, iw - x)
            h = min(h, ih - y)

            face_roi = frame[y:y+h, x:x+w]

            h, w = face_roi.shape[:2]
            small = cv.resize(face_roi, (w//10, h//10), interpolation=cv.INTER_LINEAR)
            pixelated = cv.resize(small, (w, h), interpolation=cv.INTER_NEAREST)
            frame[y:y+h, x:x+w] = pixelated


    cv.imshow("Face Blur Tool", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
