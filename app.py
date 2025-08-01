# app.py
from flask import Flask, render_template, jsonify, request, Response

import subprocess
import os
import signal
import sys
import threading # Use threading for better control over the subprocess
from werkzeug.utils import secure_filename
import time

# For tool2 gun detector
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import threading as py_threading
from playsound import playsound

app = Flask(__name__)

gesture_process = None
gesture_thread = None # To manage the lifecycle of the gesture detection in a separate thread

# Define a lock to prevent race conditions when modifying gesture_process
import threading
process_lock = threading.Lock()

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# For tool5 volume control
tool5_volume_thread = None
tool5_volume_running = False
current_volume = 50.0  # Default volume percentage

# For tool3 zoom control
tool3_zoom_scale = 1.0  # Default zoom scale
tool3_zoom_thread = None
tool3_zoom_running = False

def run_tool5_volume_control():
    global tool5_volume_running, current_volume
    script_path = os.path.join(os.path.dirname(__file__), 'tools', 'tool5_volume_control.py')
    try:
        if sys.platform == "win32":
            subprocess.run(['python', script_path])
        else:
            subprocess.run(['python', script_path])
    except Exception as e:
        print(f"Error running volume control script: {e}", file=sys.stderr)
    finally:
        tool5_volume_running = False

# For tool4 face detection
tool4_face_process = None
tool4_face_thread = None

def run_tool4_face_detection():
    global tool4_face_process
    script_path = os.path.join(os.path.dirname(__file__), 'tools', 'tool4_facedetection.py')
    try:
        if sys.platform == "win32":
            tool4_face_process = subprocess.Popen(['python', script_path])
        else:
            tool4_face_process = subprocess.Popen(['python', script_path])
        
        print(f"Face detection process started with PID: {tool4_face_process.pid}", file=sys.stderr)
        tool4_face_process.wait()
        print("Face detection process finished.", file=sys.stderr)
    except Exception as e:
        print(f"Error running face detection script: {e}", file=sys.stderr)
    finally:
        tool4_face_process = None

# For tool1 gesture detection with web streaming
tool1_gesture_running = False
tool1_gesture_lock = py_threading.Lock()
tool1_last_action_time = 0
tool1_action_cooldown = 3  # 3 seconds cooldown between actions

def open_browser_app(url):
    """Cross-platform browser opening function"""
    import webbrowser
    try:
        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"Error opening browser: {e}", file=sys.stderr)
        return False

def gen_tool1_gesture_frames():
    global tool1_gesture_running, tool1_last_action_time
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    detector = HandDetector(detectionCon=0.8, maxHands=1)
    tool1_gesture_running = True
    
    while tool1_gesture_running:
        success, img = cap.read()
        if not success:
            continue
            
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img)
        current_time = time.time()
        
        if hands:
            hand = hands[0]
            fingers = detector.fingersUp(hand)
            
            # Display current finger pattern on screen
            cv2.putText(img, f"Fingers: {fingers}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            # Check if enough time has passed since last action
            if current_time - tool1_last_action_time > tool1_action_cooldown:
                action_taken = False
                action_text = ""
                
                # 1 Finger (Index Finger Up) - Google
                if fingers == [0,1,0,0,0]:
                    action_text = "Opening Google..."
                    action_taken = open_browser_app("https://www.google.com")
                    
                # 2 Fingers (Index and Middle Finger Up) - YouTube
                elif fingers == [0,1,1,0,0]:
                    action_text = "Opening YouTube..."
                    action_taken = open_browser_app("https://www.youtube.com")
                    
                # 3 Fingers (Index, Middle, Ring Finger Up) - Amazon
                elif fingers == [0,1,1,1,0]:
                    action_text = "Opening Amazon..."
                    action_taken = open_browser_app("https://www.amazon.com")
                    
                # 5 Fingers (All Fingers Up) - WhatsApp
                elif fingers == [1,1,1,1,1]:
                    action_text = "Opening WhatsApp..."
                    action_taken = open_browser_app("https://web.whatsapp.com")
                    
                # 4 Fingers (Thumb down) - MyGyanVihar
                elif fingers == [0,1,1,1,1]:
                    action_text = "Opening MyGyanVihar..."
                    action_taken = open_browser_app("https://mygyanvihar.com")
                
                if action_taken:
                    tool1_last_action_time = current_time
                    cv2.putText(img, action_text, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    print(f"Gesture Action: {action_text}", file=sys.stderr)
                elif action_text:
                    cv2.putText(img, "Action failed!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                remaining_time = tool1_action_cooldown - (current_time - tool1_last_action_time)
                cv2.putText(img, f"Cooldown: {remaining_time:.1f}s", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        
        # Add gesture guide on the frame
        guide_text = [
            "Gesture Guide:",
            "1 finger: Google",
            "2 fingers: YouTube", 
            "3 fingers: Amazon",
            "4 fingers: MyGyanVihar",
            "5 fingers: WhatsApp"
        ]
        
        for i, text in enumerate(guide_text):
            y_pos = img.shape[0] - 150 + (i * 25)
            cv2.putText(img, text, (50, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    cap.release()

# For tool2 gun detector video stream
tool2_video_running = False
tool2_video_lock = py_threading.Lock()
tool2_fire_effect = False
tool2_fire_counter = 0

def play_fire_sound():
    sound_path = os.path.join(os.path.dirname(__file__), 'static', 'sound.mp3')
    py_threading.Thread(target=playsound, args=(sound_path,), daemon=True).start()

def gen_tool2_frames():
    global tool2_video_running, tool2_fire_effect, tool2_fire_counter
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    detector = HandDetector(detectionCon=0.8, maxHands=1)
    tool2_video_running = True
    while tool2_video_running:
        success, img = cap.read()
        if not success:
            continue
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img)
        if hands:
            hand = hands[0]
            lmList = hand['lmList']
            thumb_tip = lmList[4]
            index_tip = lmList[8]
            middle_tip = lmList[12]
            thumb_up = thumb_tip[1] < lmList[3][1]
            index_up = index_tip[1] < lmList[6][1]
            middle_down = middle_tip[1] > lmList[10][1]
            if thumb_up and index_up and middle_down:
                tool2_fire_effect = True
                tool2_fire_counter = 5
                play_fire_sound()
        if tool2_fire_effect:
            tool2_fire_counter -= 1
            cv2.putText(img, "FIRE!", (600, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
            if tool2_fire_counter <= 0:
                tool2_fire_effect = False
        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()

@app.route('/')
def home():
    # Assuming your index.html is your main landing page
    return render_template('index.html', active_page='home')

@app.route('/about')
def about():
    try:
        return render_template('about.html', active_page='about')
    except Exception as e:
        return f"Template not found: {e}", 404

@app.route('/features')
def features():
    try:
        return render_template('features.html', active_page='features')
    except Exception as e:
        return f"Template not found: {e}", 404

@app.route('/contact')
def contact():
    try:
        return render_template('contact.html', active_page='contact')
    except Exception as e:
        return f"Template not found: {e}", 404

# Pointing to the correct HTML file for the gesture launcher
@app.route('/tool1')
def tool1():
    return render_template('tool1.html') # This should be the HTML provided in the prompt

@app.route('/tool2')
def tool2():
    return render_template('tool2.html')

@app.route('/tool3')
def tool3():
    return render_template('tool3.html')

@app.route('/tool4')
def tool4():
    return render_template('tool4.html')

@app.route('/tool5')
def tool5():
    return render_template('tool5.html')

def run_gesture_script():
    """Function to be run in a separate thread to manage the subprocess."""
    global gesture_process
    script_path = os.path.join(os.path.dirname(__file__), 'tools', 'tool1_gesture_launcher.py')
    print(f"Attempting to start gesture script: {script_path}", file=sys.stderr)
    try:

        if sys.platform == "win32":
            gesture_process = subprocess.Popen(['python', script_path])
        else:
            gesture_process = subprocess.Popen(['python', script_path])
        
        print(f"Gesture process started with PID: {gesture_process.pid}", file=sys.stderr)
        gesture_process.wait() # Wait for the subprocess to complete
        print("Gesture process finished.", file=sys.stderr)
    except Exception as e:
        print(f"Error running gesture script: {e}", file=sys.stderr)
    finally:
        with process_lock:
            gesture_process = None # Reset process handle when it's done

@app.route('/start_gesture', methods=['POST'])
def start_gesture():
    global tool1_gesture_running
    with tool1_gesture_lock:
        if not tool1_gesture_running:
            tool1_gesture_running = True
            return jsonify({'status': 'success', 'msg': '🟢 Gesture detection started! Show your hand gestures to the camera.'})
        else:
            return jsonify({'status': 'running', 'msg': '🟡 Gesture detection already running.'})

@app.route('/stop_gesture', methods=['POST'])
def stop_gesture():
    global tool1_gesture_running
    with tool1_gesture_lock:
        tool1_gesture_running = False
    return jsonify({'status': 'success', 'msg': '🔴 Gesture detection stopped.'})

# Route to stream the video feed for tool1 gesture detection
@app.route('/gesture_video_feed')
def gesture_video_feed():
    global tool1_gesture_running
    with tool1_gesture_lock:
        if not tool1_gesture_running:
            tool1_gesture_running = True
    return Response(gen_tool1_gesture_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/run_tool2', methods=['POST'])
def run_tool2():
    global tool2_video_running
    with tool2_video_lock:
        if not tool2_video_running:
            tool2_video_running = True
            return jsonify({'status': 'success', 'msg': 'Gun Detector started. Camera feed below.'})
        else:
            return jsonify({'status': 'running', 'msg': 'Gun Detector already running.'})



# Route to stream the video feed for tool2
@app.route('/tool2_video_feed')
def tool2_video_feed():
    global tool2_video_running
    with tool2_video_lock:
        if not tool2_video_running:
            tool2_video_running = True
    return Response(gen_tool2_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route to stop the video feed for tool2
@app.route('/stop_tool2', methods=['POST'])
def stop_tool2():
    global tool2_video_running
    with tool2_video_lock:
        tool2_video_running = False
    return jsonify({'status': 'stopped', 'msg': 'Gun Detector stopped.'})

@app.route('/tool3_upload', methods=['POST'])
def tool3_upload():
    if 'image' not in request.files:
        return jsonify({'status': 'error', 'msg': 'No file part'})
    file = request.files['image']
    if file.filename == '':
        return jsonify({'status': 'error', 'msg': 'No selected file'})
    filename = secure_filename(file.filename)
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)
    # No need to launch the zoom tool script anymore
    return jsonify({'status': 'success', 'msg': '🟢 Image uploaded and previewed below. Use the zoom controls.'})

def run_tool3_hand_tracking():
    global tool3_zoom_scale, tool3_zoom_running
    from cvzone.HandTrackingModule import HandDetector
    import cv2
    import numpy as np

    cap = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon=0.8, maxHands=1)
    tool3_zoom_running = True
    while tool3_zoom_running:
        success, img = cap.read()
        if not success:
            continue
        img = cv2.flip(img, 1)
        hands, _ = detector.findHands(img)
        if hands:
            hand = hands[0]
            lmList = hand['lmList']
            x1, y1 = lmList[4][0], lmList[4][1]
            x2, y2 = lmList[8][0], lmList[8][1]
            length, _, _ = detector.findDistance((x1, y1), (x2, y2), img)
            scale = np.interp(length, [50, 300], [0.5, 3.0])
            tool3_zoom_scale = float(scale)
        time.sleep(0.05)
    cap.release()

@app.route('/tool3_zoom_scale')
def tool3_zoom_scale_api():
    return jsonify({'scale': tool3_zoom_scale})

@app.route('/tool3_start_zoom', methods=['POST'])
def tool3_start_zoom():
    global tool3_zoom_thread, tool3_zoom_running
    if tool3_zoom_thread is None or not tool3_zoom_thread.is_alive():
        tool3_zoom_running = True
        tool3_zoom_thread = threading.Thread(target=run_tool3_hand_tracking)
        tool3_zoom_thread.daemon = True
        tool3_zoom_thread.start()
        return jsonify({'status': 'started'})
    else:
        return jsonify({'status': 'already running'})

@app.route('/tool3_stop_zoom', methods=['POST'])
def tool3_stop_zoom():
    global tool3_zoom_running
    tool3_zoom_running = False
    return jsonify({'status': 'stopped'})

# Tool4 Face Detection Routes
@app.route('/start_face_detection', methods=['POST'])
def start_face_detection():
    global tool4_face_process, tool4_face_thread
    if tool4_face_process is None or tool4_face_process.poll() is not None:
        tool4_face_thread = threading.Thread(target=run_tool4_face_detection)
        tool4_face_thread.daemon = True
        tool4_face_thread.start()
        return jsonify({'status': 'success', 'msg': '🟢 Face detection starting... (Check desktop for camera feed)'})
    else:
        return jsonify({'status': 'running', 'msg': '🟡 Face detection already running.'})

@app.route('/stop_face_detection', methods=['POST'])
def stop_face_detection():
    global tool4_face_process
    if tool4_face_process and tool4_face_process.poll() is None:
        try:
            if sys.platform == "win32":
                tool4_face_process.terminate()
            else:
                tool4_face_process.send_signal(signal.SIGINT)
            tool4_face_process.wait(timeout=5)
            print("Face detection process terminated.", file=sys.stderr)
        except subprocess.TimeoutExpired:
            tool4_face_process.kill()
        except Exception as e:
            print(f"Error during face detection termination: {e}", file=sys.stderr)
        
        tool4_face_process = None
        return jsonify({'status': 'success', 'msg': 'Face detection stopped.'})
    else:
        return jsonify({'status': 'stopped', 'msg': 'Face detection is not running.'})

# Tool5 Volume Control Routes
@app.route('/start_volume_control', methods=['POST'])
def start_volume_control():
    global tool5_volume_thread, tool5_volume_running
    if not tool5_volume_running:
        tool5_volume_running = True
        tool5_volume_thread = threading.Thread(target=run_tool5_volume_control)
        tool5_volume_thread.daemon = True
        tool5_volume_thread.start()
        return jsonify({'status': 'success', 'msg': '🟢 Volume control starting... Use hand gestures!'})
    else:
        return jsonify({'status': 'running', 'msg': '🟡 Volume control already running.'})

@app.route('/stop_volume_control', methods=['POST'])
def stop_volume_control():
    global tool5_volume_running
    tool5_volume_running = False
    return jsonify({'status': 'stopped', 'msg': 'Volume control stopped.'})

@app.route('/get_volume_level')
def get_volume_level():
    global current_volume
    # In a real implementation, you would get the actual system volume
    # For now, return a simulated value
    return jsonify({'volume': current_volume})

# Add error handler for 404
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404 if os.path.exists('templates/404.html') else ('Page not found', 404)

if __name__ == '__main__':
    # Ensure all OpenCV windows are closed if the server is stopped

    def shutdown_server(signal, frame):
        global gesture_process, tool1_gesture_running, tool2_video_running, tool4_face_process, tool5_volume_running
        
        # Stop tool1 gesture detection
        tool1_gesture_running = False
        
        with process_lock:
            if gesture_process and gesture_process.poll() is None:
                print("Server shutting down, attempting to terminate gesture process.", file=sys.stderr)
                try:
                    if sys.platform == "win32":
                        gesture_process.terminate()
                    else:
                        gesture_process.send_signal(signal.SIGINT)
                    gesture_process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    gesture_process.kill()
                except Exception as e:
                    print(f"Error during server shutdown termination: {e}", file=sys.stderr)
            
            # Stop face detection process
            if tool4_face_process and tool4_face_process.poll() is None:
                print("Terminating face detection process.", file=sys.stderr)
                try:
                    if sys.platform == "win32":
                        tool4_face_process.terminate()
                    else:
                        tool4_face_process.send_signal(signal.SIGINT)
                    tool4_face_process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    tool4_face_process.kill()
                except Exception as e:
                    print(f"Error during face detection shutdown: {e}", file=sys.stderr)
        
        # Also stop tool2 video stream and tool5 volume control on shutdown
        tool2_video_running = False
        tool5_volume_running = False
        print("Flask server shutting down.", file=sys.stderr)
        sys.exit(0)

    # Register signal handlers for graceful shutdown
    if sys.platform == "win32":
        # On Windows, SIGINT (Ctrl+C) is usually handled by the console,
        # but setting a handler can catch programmatically.
        # signal.SIGBREAK is also an option for Ctrl+Break
        signal.signal(signal.SIGINT, shutdown_server)
    else:
        signal.signal(signal.SIGINT, shutdown_server)
        signal.signal(signal.SIGTERM, shutdown_server) # For more general termination signals

    app.run(debug=True)