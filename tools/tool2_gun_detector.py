import cv2
from cvzone.HandTrackingModule import HandDetector
from playsound import playsound
import threading

# Function to play sound
def play_fire_sound():
    threading.Thread(target=playsound, args=("Sound.mp3",), daemon=True).start()

# Video capture setup
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Gun fire effect flag
fire_effect = False
fire_counter = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Mirror the image

    # Detect hands
    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        lmList = hand['lmList']  # List of 21 landmarks

        # Check for gun gesture (thumb and index finger extended)
        thumb_tip = lmList[4]  # Thumb tip
        index_tip = lmList[8]  # Index finger tip
        middle_tip = lmList[12]  # Middle finger tip

        # Check conditions for gun gesture
        thumb_up = thumb_tip[1] < lmList[3][1]  # Thumb agutha hai jo faila hona chaiye 
        index_up = index_tip[1] < lmList[6][1]  # Index finger is extended
        middle_down = middle_tip[1] > lmList[10][1]  # Middle finger is down

        if thumb_up and index_up and middle_down:
            fire_effect = True
            fire_counter = 5  # Show fire effect for a few frames
            play_fire_sound()  # Play fire sound

    # Draw fire effect
    if fire_effect:
        fire_counter -= 1
        cv2.putText(img, "FIRE!", (600, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
        if fire_counter <= 0:
            fire_effect = False

    # Display the image
    cv2.imshow("Gun Gesture Detection", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
