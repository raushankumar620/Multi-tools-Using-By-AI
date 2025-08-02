"""
Setup script for AI Voice Assistant
This script helps install the required dependencies for the voice assistant to work properly.
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def check_package(package):
    """Check if a package is already installed"""
    try:
        __import__(package)
        return True
    except ImportError:
        return False

def main():
    print("🎤 AI Voice Assistant Setup")
    print("=" * 50)
    
    # Required packages for voice assistant
    packages = {
        'speech_recognition': 'speechrecognition',
        'pyttsx3': 'pyttsx3',
        'cv2': 'opencv-python',
        'numpy': 'numpy',
        'flask': 'flask'
    }
    
    # Optional packages
    optional_packages = {
        'pyaudio': 'pyaudio'  # For better microphone support
    }
    
    print("Checking required packages...")
    missing_packages = []
    
    for import_name, pip_name in packages.items():
        if check_package(import_name):
            print(f"✅ {pip_name} is already installed")
        else:
            print(f"❌ {pip_name} is not installed")
            missing_packages.append(pip_name)
    
    if missing_packages:
        print(f"\n📦 Installing {len(missing_packages)} missing packages...")
        for package in missing_packages:
            install_package(package)
    
    # Try to install optional packages
    print("\n🔧 Installing optional packages for better performance...")
    for import_name, pip_name in optional_packages.items():
        if not check_package(import_name):
            print(f"Installing {pip_name} (optional)...")
            if not install_package(pip_name):
                print(f"⚠️  {pip_name} installation failed. Voice assistant will work but microphone quality may be reduced.")
    
    print("\n🎉 Setup complete!")
    print("\n📖 To use the voice assistant:")
    print("1. Run the Flask app: python app.py")
    print("2. Open your browser and go to http://localhost:5000/tool6")
    print("3. Click 'Start Assistant' and start speaking!")
    
    print("\n🎤 Supported voice commands:")
    print("- 'Hello' - Greeting")
    print("- 'What time is it?' - Get current time")
    print("- 'Open Google' - Open Google in browser")
    print("- 'Tell me a joke' - Get a random joke")
    print("- 'Calculate 5 plus 3' - Perform math")
    print("- 'Take photo' - Capture photo from webcam")
    print("- 'Volume up/down' - Control system volume")
    print("- 'Help' - Get list of all commands")
    print("- 'Stop' - Stop the assistant")

if __name__ == "__main__":
    main()
