# Invincibility Cloak


**Invincibility Cloak** is a fun computer vision project that uses OpenCV and NumPy to create a real-time invisibility effect using your webcam. By wearing a cloak of specific colors (green or pink), the program replaces the cloak area with the background, making it appear as if you are invisible.

---

## Features

- Real-time video processing using your webcam.
- Detects green and pink colored cloaks.
- Creates a seamless invisibility effect by replacing cloak pixels with the background.
- Easy to run and experiment with.

---

## Requirements

- Python 3.6 or higher
- OpenCV (`opencv-python`)
- NumPy

---

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/nerdyalgorithm/invincibility-cloak.git
cd invincibility-cloak
```

2. **Install dependencies:**

```bash
pip install opencv-python numpy
```

---

## Usage

Run the main script:

```bash
python main.py
```

### How it works:

1. The program opens your webcam and captures the background for a few seconds.
2. It then detects green and pink colors in the video feed (you can wear a cloak or cloth of these colors).
3. The cloak area is replaced with the captured background, creating an invisibility effect.
4. Press **`q`** to quit the application.

---

## Notes

- Make sure you have good lighting conditions for better color detection.
- The cloak colors are set for green and pink but can be adjusted in the code by changing HSV ranges.
- The program flips the video feed horizontally for a mirror-like experience.

---

## Contributing

Feel free to fork the repo and submit pull requests! Suggestions and improvements are welcome.

---

## License

This project is licensed under the MIT License.

---

## Contact

Created by [ANGELIC](https://github.com/visionbyangelic) (GitHub username: **visionbyangelic**).  
Feel free to open issues or reach out on GitHub for questions or feedback.

---
