# app.py
from flask import Flask, render_template, jsonify, request
import subprocess
import os
import signal
import sys
import threading # Use threading for better control over the subprocess

app = Flask(__name__)

# Use a dictionary to store process objects, if you plan for multiple tools to run concurrently
# For now, let's stick to one gesture_process for simplicity.
gesture_process = None
gesture_thread = None # To manage the lifecycle of the gesture detection in a separate thread

# Define a lock to prevent race conditions when modifying gesture_process
import threading
process_lock = threading.Lock()

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

def run_gesture_script():
    """Function to be run in a separate thread to manage the subprocess."""
    global gesture_process
    script_path = os.path.join(os.path.dirname(__file__), 'tools', 'tool1_gesture_launcher.py')
    print(f"Attempting to start gesture script: {script_path}", file=sys.stderr)
    try:
        # Use Popen directly, without creationflags for GUI visibility
        # On Windows, `DETACHED_PROCESS` can sometimes help with GUI apps launched in background
        # but you removed it, which is good for foreground visibility.
        # Consider a shell=True on Windows if you face issues, but be cautious with security.
        if sys.platform == "win32":
            # For Windows, creating a new console can sometimes help with GUI interaction,
            # but usually it's not needed if you want the window to appear.
            # subprocess.CREATE_NEW_CONSOLE might be an option, but often makes things worse for visibility.
            # Best is typically to just run it as-is without special flags beyond default.
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