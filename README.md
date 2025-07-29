# Multi Tool Project

This project is a multi-tool web application built with Python (Flask). It includes gesture launcher and gun detector tools, with a simple web interface.

## Project Structure

- `app.py` - Main Flask application
- `tools/` - Python scripts for each tool
    - `tool1_gesture_launcher.py` - Gesture launcher tool
    - `tool2_gun_detector.py` - Gun detector tool
- `templates/` - HTML templates
    - `index.html` - Home page
    - `tool1.html` - Gesture launcher UI
    - `tool2.html` - Gun detector UI
- `static/` - Static files (CSS, JS, images)
    - `css/style.css` - Stylesheet
    - `js/script.js` - JavaScript
- `sound.mp3` - Example sound file

## How to Run

1. Install dependencies:
   ```bash
   pip install flask
   ```
2. Run the app:
   ```bash
   python app.py
   ```
3. Open your browser and go to `http://127.0.0.1:5000/`

## Features
- Gesture launcher tool
- Gun detector tool
- Simple web interface

---

Feel free to extend the tools or UI as needed!
