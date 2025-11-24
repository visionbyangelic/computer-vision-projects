
# 🎭 Real-Time Face Pixelation Tool

This project is a **privacy-focused real-time face blurring tool** using a webcam. It leverages **MediaPipe's face detection** and **OpenCV** for image processing to pixelate detected faces in live video.

---

## 📁 File

* `main.py` — The main script for running the tool.

---

## 📸 How It Works

1. Opens the webcam.
2. Uses MediaPipe to detect faces in real-time.
3. For each detected face:

   * Calculates bounding box.
   * Extracts the face region.
   * Downscales and then upscales the face region to pixelate it.
4. Replaces the original face region with the pixelated version.
5. Displays the video feed with pixelated faces.
6. Press `q` to quit the application.

---

## 🔧 Requirements

Install the following Python packages:

```bash
pip install opencv-python mediapipe numpy
```

---

## 🚀 Run It

```bash
python main.py
```

Make sure your webcam is connected and accessible.

---

## 🧠 Tech Stack

* **OpenCV** — For video capture and image processing.
* **MediaPipe** — For real-time face detection.
* **NumPy** — For efficient array and image manipulation.

---

## ✅ Features

* Fast and light-weight.
* Real-time face pixelation for privacy.
* Uses short-range detection model optimized for webcams.
* Mirror-style video for natural camera alignment.

---
## Contact

Created by [ANGELIC](https://github.com/visionbyangelic) (GitHub username: **visionbyangelic**).  
Feel free to open issues or reach out on GitHub for questions or feedback.

---
