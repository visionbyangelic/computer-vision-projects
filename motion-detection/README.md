# Motion Detection with OpenCV

A simple real-time motion detection program using OpenCV and Python. This project captures video from your webcam, detects moving objects by comparing consecutive frames, and highlights motion areas with bounding boxes.

---

## Features

- Real-time motion detection using frame differencing.
- Noise reduction with grayscale conversion and Gaussian blur.
- Thresholding and dilation to isolate moving regions.
- Contour detection to identify and highlight moving objects.
- Adjustable sensitivity by filtering small movements.
- Visual feedback with bounding rectangles around detected motion.

---

## How It Works

1. **Capture video frames** continuously from the webcam.
2. **Flip frames horizontally** for a mirror-like view.
3. **Calculate the absolute difference** between consecutive frames to detect changes.
4. **Convert the difference to grayscale** and apply Gaussian blur to reduce noise.
5. **Threshold the blurred image** to create a binary mask of motion areas.
6. **Dilate the mask** to fill gaps and make contours more prominent.
7. **Find contours** representing moving objects.
8. **Filter out small contours** to avoid false positives.
9. **Draw bounding rectangles** around detected motion on the frame.
10. **Display the processed video** with motion highlights.
11. **Exit the program** by pressing the 'q' key.

---

## Installation

### Requirements

- Python 3.x
- OpenCV (`opencv-python`)
- NumPy

### Install dependencies

```bash
pip install opencv-python numpy
```

---

## Usage

Run the script:

```bash
python motion_detector.py
```

- The webcam window will open.
- Move in front of the camera to see motion detection in action.
- Green rectangles highlight detected motion areas.
- Press `q` to quit the program.

---

## Code Snippet Overview

```python
# Compute difference between frames
diff = cv2.absdiff(frame1, frame2)

# Convert to grayscale and blur
gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Threshold and dilate
_, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
dilated = cv2.dilate(thresh, None, iterations=3)

# Find contours and draw rectangles
contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for contour in contours:
    if cv2.contourArea(contour) < 700:
        continue
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
```

---

## References

- [PyImageSearch: Basic Motion Detection and Tracking](https://pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/)
- [LearnOpenCV: Moving Object Detection](https://learnopencv.com/moving-object-detection-with-opencv/)
- Various OpenCV tutorials on contour detection and background subtraction.

---

## Contact

Created by [ANGELIC](https://github.com/visionbyangelic) (GitHub username: **visionbyangelic**).  
Feel free to open issues or reach out on GitHub for questions or feedback.

---
