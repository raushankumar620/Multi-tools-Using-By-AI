# tools/tool1_gesture_launcher.py
import os
import cv2
import time
from cvzone.HandTrackingModule import HandDetector
import sys
import signal

cap = None

def cleanup(signum, frame):
    global cap
    print(f"Received signal {signum}, cleaning up...", file=sys.stderr)
    if cap is not None:
        try:
            cap.release()
        except Exception:
            pass
    try:
        cv2.destroyAllWindows()
    except Exception:
        pass
    sys.exit(0)

signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)

def start_gesture_detection():
    global cap
    print("=== Gesture detection script started ===", file=sys.stderr)
    import time
    max_retries = 5
    retry_delay = 1  # seconds

    cap = None
    for attempt in range(max_retries):
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            break
        print(f"Camera not available (attempt {attempt+1}/{max_retries}), retrying...", file=sys.stderr)
        time.sleep(retry_delay)
    else:
        print("Error: Could not open video stream after several attempts. Camera may be in use by another process.", file=sys.stderr)
        return

    detector = HandDetector(detectionCon=0.8, maxHands=1)
    print("Gesture detection loop started.", file=sys.stderr)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to read from camera. Breaking loop.", file=sys.stderr)
                break

            img, hands = detector.findHands(frame, draw=True)

            if isinstance(hands, list) and len(hands) > 0:
                hand = hands[0]
                if isinstance(hand, dict) and 'lmList' in hand:
                    fingers = detector.fingersUp(hand)
                    print(f"DEBUG: Detected fingers pattern: {fingers}", file=sys.stderr)

                    # 1 Finger (Index Finger Up)
                    if fingers == [0,1,0,0,0]:
                        print("ACTION: Single finger detected - Opening Google.", file=sys.stderr)
                        open_browser("https://www.google.com")
                        break
                    # 2 Fingers (Index and Middle Finger Up)
                    elif fingers == [0,1,1,0,0]:
                        print("ACTION: Two fingers detected - Opening YouTube.", file=sys.stderr)
                        open_browser("https://www.youtube.com")
                        break
                    # 3 Fingers (Index, Middle, Ring Finger Up)
                    elif fingers == [0,1,1,1,0]:
                        print("ACTION: Three fingers detected - Opening Amazon.", file=sys.stderr)
                        open_browser("https://www.amazon.com")
                        break
                    # 5 Fingers (All Fingers Up - Open Palm)
                    elif fingers == [1,1,1,1,1]:
                        print("ACTION: All five fingers detected - Opening WhatsApp Web.", file=sys.stderr)
                        os.system("start chrome https://web.whatsapp.com")
                        break
                    # MyGyanVihar (Currently assigned to [0,1,1,1,1])
                    elif fingers == [0,1,1,1,1]:
                        print("ACTION: Four fingers (thumb down) detected - Opening MyGyanVihar.", file=sys.stderr)
                        open_browser("https://mygyanvihar.com")
                        break

            # Ensure img is a numpy array before showing
            import numpy as np
            if not isinstance(img, np.ndarray):
                img = frame

            try:
                cv2.imshow("Gesture Detection", img)
            except cv2.error as e:
                print("cv2.imshow failed. This process may not have access to the desktop GUI. Exiting.", file=sys.stderr)
                break
            key = cv2.waitKey(1)
            if key == 27:  # ESC to exit
                print("Exiting gesture detection loop via ESC key.", file=sys.stderr)
                break
    except Exception as e:
        print(f"An error occurred in gesture detection loop: {e}", file=sys.stderr)
    finally:
        if cap is not None:
            cap.release()
        cv2.destroyAllWindows()
        print("Camera released and windows destroyed.", file=sys.stderr)

# Helper function for cross-platform browser opening (unchanged)
def open_browser(url):
    if sys.platform == "win32":
        os.system(f"start chrome {url}")
    elif sys.platform == "darwin":  # macOS
        os.system(f"open -a 'Google Chrome' {url}")
    else:  # Linux and other Unix-like
        os.system(f"xdg-open {url}")

if __name__ == '__main__':
    start_gesture_detection()