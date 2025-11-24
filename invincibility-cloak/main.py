import cv2 as cv
import numpy as np
import time

# Step 1: Open camera and allow it to warm up
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

time.sleep(2)

# Step 2: Capture background frame
for i in range(30):
    ret, background = cap.read()
    if not ret:
        continue
background = cv.flip(background, 1)
print("Background captured.")

while cap.isOpened():
    # Step 3: Read and flip the frame
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv.flip(frame, 1)

    # Step 4: Convert to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Step 4: Define HSV color ranges
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])

    lower_pink = np.array([140, 50, 50])
    upper_pink = np.array([170, 255, 255])

    # Step 4: Create individual masks
    mask_green = cv.inRange(hsv, lower_green, upper_green)
    mask_pink = cv.inRange(hsv, lower_pink, upper_pink)

    # Step 4: Combine all cloak masks
    cloak_mask = mask_green + mask_pink

    # Step 4: Clean the combined mask
    kernel = np.ones((3, 3), np.uint8)
    cloak_mask = cv.morphologyEx(cloak_mask, cv.MORPH_OPEN, kernel, iterations=2)
    cloak_mask = cv.dilate(cloak_mask, kernel, iterations=1)

    # Step 5: Segment cloak and non-cloak areas
    cloak_area = cv.bitwise_and(background, background, mask=cloak_mask)
    inverse_mask = cv.bitwise_not(cloak_mask)
    visible_area = cv.bitwise_and(frame, frame, mask=inverse_mask)

    # Step 6: Combine both to create final output
    final_output = cv.addWeighted(cloak_area, 1, visible_area, 1, 0)

    # Step 7: Display result
    cv.imshow('Invisibility Cloak', final_output)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv.destroyAllWindows()
