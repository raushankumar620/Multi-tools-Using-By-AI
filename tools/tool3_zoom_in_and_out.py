# Use the /tool3 page in your web app and click "Finger Zoom" to control zoom with your hand.

import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import sys
import os

# Get image path from command-line argument or use default
if len(sys.argv) > 1:
    image_path = sys.argv[1]
else:
    image_path = "photo@.jpg"  # Default fallback

# Video capture setup
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Load an image
image = cv2.imread(image_path)
if image is None:
    raise FileNotFoundError(f"The image file '{image_path}' was not found. Check the path.")
scale = 1.0  # Initial scale factor
center_x, center_y = image.shape[1] // 2, image.shape[0] // 2

while True:
    success, frame = cap.read()
    if not success:
        continue
    frame = cv2.flip(frame, 1)  # Mirror the webcam frame

    # Detect hands
    hands, _ = detector.findHands(frame)

    # Check if hand is detected
    if hands:
        hand = hands[0]
        lmList = hand['lmList']  # List of 21 landmarks

        # Get the distance between thumb tip (4) and index finger tip (8)
        x1, y1 = lmList[4][0], lmList[4][1]  # Thumb tip
        x2, y2 = lmList[8][0], lmList[8][1]  # Index finger tip
        length, _, _ = detector.findDistance((x1, y1), (x2, y2), frame)

        # Map the distance to scale (adjust values as needed)
        scale = float(np.clip(np.interp(length, [50, 300], [0.5, 3.0]), 0.2, 5.0))

    # Resize the image based on scale
    resized_img = cv2.resize(image, None, fx=scale, fy=scale)

    # Center crop or pad the resized image to 1280x720
    target_w, target_h = 1280, 720
    h, w, _ = resized_img.shape
    if w > target_w:
        x_start = (w - target_w) // 2
        x_end = x_start + target_w
        cropped_img = resized_img[:, x_start:x_end]
    else:
        # Pad left/right
        pad_left = (target_w - w) // 2
        pad_right = target_w - w - pad_left
        cropped_img = cv2.copyMakeBorder(resized_img, 0, 0, pad_left, pad_right, cv2.BORDER_CONSTANT, value=[0,0,0])
    if h > target_h:
        y_start = (h - target_h) // 2
        y_end = y_start + target_h
        cropped_img = cropped_img[y_start:y_end, :]
    else:
        # Pad top/bottom
        pad_top = (target_h - h) // 2
        pad_bottom = target_h - h - pad_top
        cropped_img = cv2.copyMakeBorder(cropped_img, pad_top, pad_bottom, 0, 0, cv2.BORDER_CONSTANT, value=[0,0,0])

    # Show only the zoomed image (not overlayed on webcam)
    cv2.imshow("Zoom In/Out", cropped_img)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()