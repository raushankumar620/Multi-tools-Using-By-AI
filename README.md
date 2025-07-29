
# Multi Tool Project

This project is a multi-tool web application built using Python and Flask. It provides a simple web interface to access multiple AI-powered tools, including a gesture launcher and a gun detector. The project is modular and easy to extend with additional tools.

## Table of Contents

- [Project Structure](#project-structure)
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Project Structure

```
multi_tool_project/
│
├── app.py                  # Main Flask application
├── sound.mp3               # Example sound file
│
├── tools/                  # Python scripts for each tool
│   ├── tool1_gesture_launcher.py  # Gesture launcher tool
│   └── tool2_gun_detector.py      # Gun detector tool
│
├── templates/              # HTML templates
│   ├── index.html          # Home page
│   ├── tool1.html          # Gesture launcher UI
│   └── tool2.html          # Gun detector UI
│
└── static/                 # Static files (CSS, JS, images)
    ├── css/
    │   └── style.css       # Stylesheet
    └── js/
        └── script.js       # JavaScript
```

## Features

- **Gesture Launcher Tool:** Launches actions based on hand gestures.
- **Gun Detector Tool:** Detects guns in images or video streams.
- **Simple Web Interface:** Easy-to-use UI for accessing tools.
- **Modular Design:** Easily add more tools as needed.

## Getting Started

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd multi_tool_project
   ```
2. Install dependencies:
   ```bash
   pip install flask
   ```

## Usage

1. Start the Flask application:
   ```bash
   python app.py
   ```
2. Open your browser and go to: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
3. Use the web interface to access the available tools.

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests.

## License

This project is licensed under the MIT License.

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
