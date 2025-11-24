# Virtual Drawing Board

A hand-gesture controlled virtual drawing board using OpenCV and MediaPipe. This project allows you to draw on a digital canvas by moving your index finger in front of your webcam, and select different brush colors or an eraser by hovering over a tool header area.

---

## Features

- Real-time hand tracking with MediaPipe.
- Select brush colors (Pink, Green, Blue) or Eraser by touching header icons.
- Draw smooth lines on a virtual canvas using your index finger.
- Overlay drawing on webcam feed with a transparent effect.
- Intuitive tool selection area displayed as a header image.
- Adjustable brush and eraser thickness.

---

## How It Works

1. **Load header images** for each tool (Pink, Green, Blue, Eraser) from a specified folder.
2. **Initialize webcam** and set resolution to 1280x720.
3. **Create a blank canvas** to draw on.
4. **Use MediaPipe Hands** to detect hand landmarks in each video frame.
5. **Detect index finger tip position** and check if it’s touching the header area to select a tool.
6. **Draw lines on the canvas** by connecting the previous and current finger positions.
7. **Overlay the canvas on the webcam feed** with transparency for a smooth visual effect.
8. **Display the combined image** with the header on top.
9. **Exit the program** by pressing the 'q' key.

---

## Installation

### Requirements

- Python 3.x
- OpenCV (`opencv-python`)
- MediaPipe
- NumPy

### Install dependencies

```bash
pip install opencv-python mediapipe numpy
```

---

## Setup

1. Prepare a folder containing the header PNG images named:

   - `header_pink.png`
   - `header_green.png`
   - `header_blue.png`
   - `header_eraser.png`

2. Update the `base_path` variable in the script to point to your header images folder.

---

## Usage

Run the script:

```bash
python virtualboard.py
```

- The webcam window will open with the header at the top.
- Hover your index finger over a color or eraser icon in the header to select the tool.
- Move your index finger on the screen to draw.
- Press `q` to quit.

---

## Code Highlights

- **Header Loading:** Loads all PNG images from the specified folder and ensures required tools are available.
- **Hand Tracking:** Uses MediaPipe to detect hand landmarks with high confidence.
- **Tool Selection:** Detects finger position in the header area to switch brush color or eraser.
- **Drawing:** Draws lines on a separate canvas to avoid losing previous strokes when refreshing frames.
- **Overlay:** Combines the drawing canvas with the webcam feed using weighted addition for transparency.

---

## Troubleshooting

- Ensure your webcam is connected and accessible.
- Verify header images exist and are correctly named in the specified folder.
- Adjust `min_detection_confidence` or camera resolution if detection is unstable.

---

## References

- MediaPipe Hands documentation
- OpenCV tutorials on drawing and video processing
- Inspired by AI Virtual Painter projects on YouTube and OpenCV community guides

---

## Contact

Created by [ANGELIC](https://github.com/visionbyangelic) (GitHub username: **visionbyangelic**).  
Feel free to open issues or reach out on GitHub for questions or feedback.

---
