import cv2  # Import OpenCV for computer vision
import numpy as np  # Import NumPy for numerical operations

# Open webcam (0 is the default camera)
cap = cv2.VideoCapture(0)

# Read the first frame from the webcam and flip it horizontally
ret, frame1 = cap.read()  # Capture the first frame
frame1 = cv2.flip(frame1, 1)  # Flip the frame to correct camera inversion

# Read the second frame (to compare motion) and flip it
ret, frame2 = cap.read()
frame2 = cv2.flip(frame2, 1)

# Loop to process video frames continuously
while cap.isOpened():
    # Compute the absolute difference between two consecutive frames
    diff = cv2.absdiff(frame1, frame2)

    # Convert the difference frame to grayscale
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise and smoothen the frame
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply thresholding to convert the blurred frame into a binary image
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    # Dilate the thresholded image to fill in gaps and make objects more visible
    dilated = cv2.dilate(thresh, None, iterations=3)

    # Find contours (edges) of the moving objects
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Loop through each detected contour
    for contour in contours:
        # Ignore small movements by filtering out small contour areas
        if cv2.contourArea(contour) < 700:
            continue  # Skip this contour if it's too small

        # Get bounding box coordinates for the detected movement
        x, y, w, h = cv2.boundingRect(contour)

        # Draw a green rectangle around the moving object
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the processed frame with motion detection
    cv2.imshow("Motion Detector", frame1)

    # Update frames for the next iteration
    frame1 = frame2  # Set current frame as the previous frame
    ret, frame2 = cap.read()  # Capture a new frame from the webcam
    frame2 = cv2.flip(frame2, 1)  # Flip new frame to correct inversion

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(10) == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()