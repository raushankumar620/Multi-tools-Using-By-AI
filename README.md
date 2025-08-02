
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

### Installation & Setup

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

# 🎤 AI Voice Assistant - Tool 6

A comprehensive voice assistant that works completely offline without any external APIs!

## ✨ Features

### 🎯 Core Capabilities
- **Speech Recognition** - Understands your voice commands
- **Text-to-Speech** - Responds with natural voice
- **Offline Operation** - No internet required
- **Multi-language Support** - English voice commands

### 📱 Available Commands

#### 🕐 Time & Date
- "What time is it?"
- "What's the date today?"
- "Current time"

#### 🌐 Web Browsing
- "Open Google"
- "Open YouTube" 
- "Open browser"

#### 📱 Application Control
- "Open calculator"
- "Open notepad"
- "Calculator"

#### 🔊 Volume Control
- "Volume up"
- "Volume down"
- "Mute"

#### 📷 Camera
- "Take photo"
- "Camera"
- "Take picture"

#### 🧮 Math Calculations
- "Calculate 15 plus 25"
- "What is 100 divided by 5?"
- "Math: 5 times 7"

#### 🔍 Web Search
- "Search for Python tutorials"
- "Find information about AI"

#### 😂 Entertainment
- "Tell me a joke"
- "Make me laugh"

#### ❓ Help & Control
- "Help" - Get list of commands
- "What can you do?"
- "Stop" - Exit assistant

## 🚀 Setup Instructions

### 1. Install Dependencies

Run the setup script:
```bash
python setup_voice_assistant.py
```

Or install manually:
```bash
pip install speechrecognition pyttsx3 pyaudio opencv-python
```

### 2. Run the Application

Start the Flask server:
```bash
python app.py
```

### 3. Access Voice Assistant

Open your browser and go to:
```
http://localhost:5000/tool6
```

## 🎮 How to Use

1. **Start the Assistant**: Click "Start Assistant" button
2. **Speak Commands**: Wait for the listening indicator and speak clearly
3. **Listen to Response**: The assistant will respond with voice and text
4. **Stop when Done**: Say "stop" or click "Stop Assistant"

## 🔧 Technical Details

### Dependencies
- **speechrecognition** - Voice input processing
- **pyttsx3** - Text-to-speech conversion
- **opencv-python** - Camera functionality
- **pyaudio** - Microphone access (optional but recommended)

### Architecture
- **Frontend**: HTML/CSS/JavaScript with Bootstrap
- **Backend**: Flask web server
- **Voice Processing**: Local speech recognition
- **TTS Engine**: System text-to-speech

### Offline Capabilities
- Works without internet connection
- No external API calls
- Local speech processing
- System-level integrations

## 🛠️ Troubleshooting

### Common Issues

**Microphone not working:**
- Check microphone permissions
- Install pyaudio: `pip install pyaudio`
- Test microphone in other applications

**TTS not working:**
- Check system audio settings
- Install TTS voices (Windows/macOS)
- Verify speaker/headphone connection

**Import errors:**
- Run: `pip install -r requirements.txt`
- Check Python version (3.7+ required)

### Performance Tips

1. **Clear Environment**: Minimize background noise
2. **Speak Clearly**: Use normal speaking pace
3. **Wait for Indicator**: Wait for listening animation
4. **Close Other Audio Apps**: Reduce microphone conflicts

## 🎯 Advanced Features

### Custom Commands
You can extend the voice assistant by adding new commands in `tool6_voice_assistance.py`:

```python
# Add to commands dictionary
'your_command': ['keyword1', 'keyword2'],

# Add processing logic
elif any(word in command for word in self.commands['your_command']):
    return self.your_custom_function()
```

### Integration
The voice assistant integrates seamlessly with other tools in the Multi-Tools project.

## 📝 Development

### File Structure
```
tools/tool6_voice_assistance.py    # Main voice assistant code
templates/tool6.html               # Web interface
setup_voice_assistant.py           # Setup script
test_voice_assistant.py           # Test script
```

### Adding New Features
1. Add command keywords to `self.commands`
2. Implement processing function
3. Add to `process_command()` method
4. Update HTML interface if needed

## 🎉 Demo Commands

Try these commands to test the assistant:

```
"Hello, how are you?"
"What time is it?"
"Open Google"
"Tell me a joke"
"Calculate 25 plus 75"
"Take a photo"
"Volume up"
"Search for artificial intelligence"
"Help"
"Stop"
```

## 📞 Support

For issues or feature requests, check the main project documentation or create an issue in the repository.

---

**Enjoy your offline AI voice assistant! 🎤🤖**
