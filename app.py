# app.py
from flask import Flask, render_template, jsonify, request
import subprocess
import os
import signal
import sys
import threading # Use threading for better control over the subprocess
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)

# Use a dictionary to store process objects, if you plan for multiple tools to run concurrently
# For now, let's stick to one gesture_process for simplicity.
gesture_process = None
gesture_thread = None # To manage the lifecycle of the gesture detection in a separate thread

# Define a lock to prevent race conditions when modifying gesture_process
import threading
process_lock = threading.Lock()

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# For tool3 hand tracking zoom
tool3_zoom_scale = 1.0
tool3_zoom_thread = None
tool3_zoom_running = False

@app.route('/')
def home():
    # Assuming your index.html is your main landing page
    return render_template('index.html', active_page='home')

@app.route('/about')
def about():
    return render_template('about.html', active_page='about')

@app.route('/features')
def features():
    return render_template('features.html', active_page='features')

@app.route('/contact')
def contact():
    return render_template('contact.html', active_page='contact')

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
    global gesture_process, gesture_thread
    with process_lock:
        if gesture_process is None or gesture_process.poll() is not None:
            # If the process is not running, or has finished
            gesture_thread = threading.Thread(target=run_gesture_script)
            gesture_thread.daemon = True # Allow main program to exit even if thread is running
            gesture_thread.start()
            return jsonify({'status': 'success', 'msg': '🟢 Gesture detection starting... (Check desktop for camera feed)'})
        else:
            return jsonify({'status': 'running', 'msg': '🟡 Gesture detection already running.'})

@app.route('/stop_gesture', methods=['POST'])
def stop_gesture():
    global gesture_process, gesture_thread
    with process_lock:
        if gesture_process and gesture_process.poll() is None:
            print(f"Terminating gesture process with PID: {gesture_process.pid}", file=sys.stderr)
            try:
                # For cross-platform termination:
                if sys.platform == "win32":
                    # On Windows, terminate() might not close the GUI window properly,
                    # so taskkill is more robust for GUI applications.
                    # However, simple terminate() usually works for Python processes.
                    # If issues persist, consider: subprocess.call(['taskkill', '/F', '/T', '/PID', str(gesture_process.pid)])
                    gesture_process.terminate()
                else:
                    gesture_process.send_signal(signal.SIGINT) # Send Ctrl+C
                gesture_process.wait(timeout=5) # Wait for it to terminate gracefully
                print("Gesture process terminated.", file=sys.stderr)
            except subprocess.TimeoutExpired:
                print("Gesture process did not terminate gracefully, killing it.", file=sys.stderr)
                gesture_process.kill() # Force kill if terminate() fails
            except Exception as e:
                print(f"Error during termination: {e}", file=sys.stderr)
            
            gesture_process = None
            gesture_thread = None
            return jsonify({'status': 'success', 'msg': '🔴 Gesture detection stopped.'})
        else:
            return jsonify({'status': 'stopped', 'msg': '🔵 Gesture detection is not running.'})

@app.route('/run_tool2', methods=['POST'])
def run_tool2():
    try:
        script_path = os.path.join(os.path.dirname(__file__), 'tools', 'tool2_gun_detector.py')
        # Similar considerations for tool2: if it has a GUI, it might not show up.
        # For simplicity, keeping it as is, but be aware.
        subprocess.Popen(['python', script_path])
        return jsonify({'status': 'success', 'msg': 'Gun Detector started.'})
    except Exception as e:
        print(f"Error running tool2: {e}", file=sys.stderr)
        return jsonify({'status': 'error', 'msg': f'Error: {str(e)}'})

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

if __name__ == '__main__':
    # Ensure all OpenCV windows are closed if the server is stopped
    def shutdown_server(signal, frame):
        global gesture_process
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