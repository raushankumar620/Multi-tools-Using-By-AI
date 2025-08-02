
# 🚀 Smart AI Tools - Multi-Tool Project

> **✅ Status**: Fully Functional & Python 3.13 Compatible!

This project is a modern multi-tool web application built using Python, Flask, and console-based AI tools. It provides an intuitive web interface to access multiple AI-powered tools with real-time console interaction capabilities.

## ⚡ Quick Start

**Double-click `start_app.bat` to launch instantly!**

Or run manually:
```bash
python app.py
```
Then visit: `http://localhost:5000`

## ✨ Features

### 🖐️ Gesture Launcher (Tool 1)
- **Live camera feed** with keyboard-based website launching
- **Quick website access** via keyboard shortcuts:
  - Press 1 → Open Google
  - Press 2 → Open YouTube  
  - Press 3 → Open Amazon
  - Press 5 → Open WhatsApp Web
- **Real-time visual feedback** with camera display
- **Easy start/stop controls** from web interface

### 🔫 Gun Detector (Tool 2)
- **Interactive fire effects** triggered by keyboard
- **Visual explosion effects** with colorful animations
- **Real-time camera processing** with instant feedback
- **Sound effect notifications** in console
- **Responsive web controls** for starting/stopping detection

### 🌐 Modern Web Interface
- **Beautiful gradient animations** and glass-morphism design
- **Responsive layout** that works on all devices
- **Real-time status updates** with emoji indicators
- **Intuitive navigation** between different tools
- **Professional styling** with smooth transitions

## 🛠️ Technology Stack

- **Backend**: Python 3.13, Flask 2.3.3
- **Computer Vision**: OpenCV 4.10.0 (NumPy 2.x compatible)
- **Frontend**: HTML5, CSS3, JavaScript (ES6)
- **Styling**: Modern CSS with gradients, animations, and backdrop filters
- **Compatibility**: Optimized for Python 3.13 with keyboard-based controls

## 📁 Project Structure

```
Multi-tools-Using-By-AI/
│
├── app.py                  # Main Flask application with all routes
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── sound.mp3              # Sound effect file
│
├── templates/             # HTML templates
│   ├── index.html         # Main landing page
│   ├── tool1.html         # Gesture Launcher interface
│   ├── tool2.html         # Gun Detector interface  
│   ├── about.html         # About page
│   ├── features.html      # Features showcase
│   └── contact.html       # Contact information
│
├── static/               # Static assets
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   └── js/
│       └── script.js     # Client-side JavaScript
│
└── tools/                # Core AI tools
    ├── tool1_gesture_launcher.py  # Gesture recognition engine
    └── tool2_gun_detector.py      # Gun gesture detector
## 🚀 Quick Start

### Prerequisites
- **Python 3.7+** (Python 3.13+ recommended)
- **Webcam/Camera** for gesture recognition
- **pip** (Python package manager)

### Installation & Setups

1. **Clone the repository:**
```bash
git clone https://github.com/raushankumar620/Multi-tools-Using-By-AI.git
cd Multi-tools-Using-By-AI
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python app.py
```

4. **Open your browser and visit:**
```
http://localhost:5000
```

### 🎯 Usage Instructions

#### Gesture Launcher (Tool 1):
1. Click **"Tool 1"** from the main page
2. Click **"🚀 Start Camera"** to begin camera feed
3. Use keyboard shortcuts for quick website access:
   - Press **1** = Opens Google
   - Press **2** = Opens YouTube
   - Press **3** = Opens Amazon
   - Press **5** = Opens WhatsApp Web
   - Press **ESC** = Stop detection
4. Click **"🛑 Stop Camera"** when done

#### Gun Detector (Tool 2):
1. Click **"Tool 2"** from the main page  
2. Click **"🚀 Start Camera"** to begin detection
3. Use keyboard shortcuts for fire effects:
   - Press **G** = Trigger gun fire effect with visual explosions
   - Press **Q** or **ESC** = Stop detection
4. Watch for colorful fire effects on screen!
5. Click **"🛑 Stop Camera"** when done

> **Note**: Due to Python 3.13 compatibility limitations with MediaPipe and CVZone, this version uses keyboard shortcuts instead of hand gesture recognition. This ensures the application works reliably on the latest Python version.

## 🔧 Configuration

### Camera Settings
- Default camera index: `0` (first camera)
- Resolution: 1280x720 for gun detector, auto for gesture launcher
- Detection confidence: 80%

### Customizing Gestures
Edit `tools/tool1_gesture_launcher.py` to modify:
- Gesture patterns (finger combinations)
- Target websites/applications
- Detection sensitivity

### Adding New Tools
1. Create new Python script in `tools/` folder
2. Add route in `app.py`
3. Create corresponding HTML template
4. Update navigation in `index.html`

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit changes** (`git commit -m 'Add AmazingFeature'`)
4. **Push to branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues:

**Camera not detected:**
- Ensure no other applications are using the camera
- Check camera permissions
- Try different camera index (change `0` to `1`, `2`, etc.)

**Installation issues:**
- Use Python 3.7+ (3.13+ recommended)
- Install Visual C++ Build Tools if on Windows
- Try: `pip install --upgrade pip`

**Gesture not recognized:**
- Ensure good lighting
- Keep hand clearly visible to camera
- Maintain proper distance from camera
- Check detection confidence settings

## 🌟 Acknowledgments

- **MediaPipe** for robust hand tracking
- **OpenCV** for computer vision capabilities  
- **CVZone** for simplified hand detection
- **Flask** for the web framework

---

**Made with ❤️ by [Raushan Kumar](https://github.com/raushankumar620)**

*If you found this project helpful, please give it a ⭐!*
