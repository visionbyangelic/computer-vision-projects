import cv2
import mediapipe as mp
import numpy as np
import os

# Set the base folder path where header images are stored
base_path = r"C:/Users/charl/Desktop/python learn/cv/virtual drawing board main"

# Dictionary to store loaded header images
headers = {}

# Load all PNG images from the specified folder
for file in os.listdir(base_path):
    if file.endswith(".png"):  # Ensure only PNG files are loaded
        file_path = os.path.join(base_path, file)
        image = cv2.imread(file_path)
        
        if image is not None:
            headers[file] = image  # Store image without resizing
        else:
            print(f"Error loading: {file_path}")  # Debugging message for failed loads

# Expected headers to ensure all necessary tools are available
expected_headers = {
    "header_pink.png": "Pink",
    "header_green.png": "Green",
    "header_blue.png": "Blue",
    "header_eraser.png": "Eraser"
}

# Check if all required headers are present
for img_name in expected_headers.keys():
    if img_name not in headers:
        print(f"Missing Image: {img_name} in {base_path}")
        exit(1)  # Exit if any required image is missing

# Map loaded images to their respective tool names
header_images = {expected_headers[k]: headers[k] for k in expected_headers}
current_header = header_images["Pink"]  # Set default header

# Initialize Mediapipe Hand Tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

# Initialize webcam capture
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set width of webcam feed
cap.set(4, 720)   # Set height of webcam feed

# Create a blank canvas for drawing (same size as webcam feed)
canvas = np.zeros((720, 1280, 3), dtype=np.uint8)

# Define brush colors for different tools
colors = {
    "Pink": (255, 0, 255),  # Pink color
    "Green": (0, 255, 0),   # Green color
    "Blue": (0, 0, 255),    # Blue color
    "Eraser": (0, 0, 0)     # Black color acts as an eraser
}
brush_color = colors["Blue"]  # Set default brush color
brush_thickness = 5  # Default brush thickness
eraser_thickness = 50  # Thicker stroke for eraser

# Define header height for selection area
header_height = 125

# Define selection zones for different tools (based on x-coordinates)
selection_zones = {
    "Pink": (50, 350),
    "Green": (400, 700),
    "Blue": (750, 1050),
    "Eraser": (1100, 1280)
}

# Variables to track previous position for drawing smooth lines
prev_x, prev_y = None, None

# Main loop to process video feed
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  # Exit loop if frame is not read properly

    frame = cv2.flip(frame, 1)  # Flip frame horizontally for mirror effect
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB for Mediapipe

    # Detect hands using Mediapipe
    results = hands.process(rgb_frame)

    # Resize current header to match the frame width dynamically
    frame_height, frame_width, _ = frame.shape
    current_header_resized = cv2.resize(current_header, (frame_width, header_height))

    # Overlay the header image at the top of the frame
    frame[0:header_height, 0:frame_width] = current_header_resized

    # Process detected hand landmarks
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm_list = [(int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])) for lm in hand_landmarks.landmark]

            if lm_list:
                x, y = lm_list[8]  # Index finger tip coordinates

                # Check if index finger is touching the header (tool selection area)
                if y < header_height:
                    for tool, (x_min, x_max) in selection_zones.items():
                        if x_min < x < x_max:
                            brush_color = colors[tool]  # Change brush color
                            brush_thickness = eraser_thickness if tool == "Eraser" else 5  # Adjust thickness
                            current_header = header_images[tool]  # Update selected tool header
                            print(f"Tool selected: {tool}")  # Debugging output

                # If not selecting a tool, draw on the canvas
                elif prev_x is not None and prev_y is not None:
                    cv2.line(canvas, (prev_x, prev_y), (x, y), brush_color, brush_thickness)  # Draw line

                prev_x, prev_y = x, y  # Update previous position for continuous drawing
            
            # Draw hand landmarks on frame
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Merge canvas with frame for display (overlay effect)
    frame = cv2.addWeighted(frame, 0.7, canvas, 0.3, 0)

    # Display output window
    cv2.imshow("Virtual Drawing Board", frame)

    # Exit loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources after exiting the loop
cap.release()
cv2.destroyAllWindows()
