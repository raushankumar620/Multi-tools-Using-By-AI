"""
AI Voice Assistant - Tool 6
A comprehensive voice assistant that can perform various tasks without external APIs
"""

import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import sys
import json
import random
import subprocess
import threading
import time
import math
import cv2
import numpy as np
from playsound import playsound

class VoiceAssistant:
    def __init__(self):
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self.setup_tts()
        
        # Assistant settings
        self.assistant_name = "AI Assistant"
        self.listening = False
        self.running = False
        
        # Commands dictionary
        self.commands = {
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening'],
            'time': ['time', 'what time is it', 'current time'],
            'date': ['date', 'what date is it', 'today date', 'current date'],
            'weather': ['weather', 'temperature', 'climate'],
            'open_browser': ['open browser', 'browser', 'internet'],
            'open_youtube': ['open youtube', 'youtube'],
            'open_google': ['open google', 'google'],
            'open_calculator': ['calculator', 'calc', 'calculate'],
            'open_notepad': ['notepad', 'text editor', 'note'],
            'play_music': ['play music', 'music', 'song'],
            'tell_joke': ['joke', 'tell me a joke', 'funny'],
            'stop': ['stop', 'exit', 'quit', 'bye', 'goodbye'],
            'help': ['help', 'commands', 'what can you do'],
            'camera': ['camera', 'take photo', 'picture'],
            'volume_up': ['volume up', 'increase volume', 'louder'],
            'volume_down': ['volume down', 'decrease volume', 'quieter'],
            'mute': ['mute', 'silent', 'no sound'],
            'search': ['search', 'find', 'look for'],
            'math': ['calculate', 'math', 'plus', 'minus', 'multiply', 'divide']
        }
        
        # Jokes database
        self.jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a fake noodle? An impasta!",
            "Why did the math book look so sad? Because it was full of problems!",
            "What's the best thing about Switzerland? I don't know, but the flag is a big plus!",
            "Why don't programmers like nature? It has too many bugs!",
            "What do you call a bear with no teeth? A gummy bear!"
        ]
        
        print("🎤 AI Voice Assistant initialized successfully!")
    
    def setup_tts(self):
        """Setup text-to-speech engine"""
        try:
            # Get available voices
            voices = self.tts_engine.getProperty('voices')
            
            # Set voice (prefer female voice if available)
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            
            # Set speech rate and volume
            self.tts_engine.setProperty('rate', 180)  # Speed of speech
            self.tts_engine.setProperty('volume', 0.8)  # Volume level (0.0 to 1.0)
            
        except Exception as e:
            print(f"TTS setup error: {e}")
    
    def speak(self, text):
        """Convert text to speech"""
        try:
            print(f"🤖 {self.assistant_name}: {text}")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"Speech error: {e}")
    
    def listen(self):
        """Listen for voice commands"""
        try:
            with self.microphone as source:
                print("🎧 Listening...")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for audio with timeout
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
                print("🔄 Processing...")
                # Recognize speech using Google Speech Recognition (offline mode)
                try:
                    command = self.recognizer.recognize_google(audio, language='en-US')
                    print(f"👤 You said: {command}")
                    return command.lower()
                except sr.RequestError:
                    # Fallback to offline recognition if available
                    try:
                        command = self.recognizer.recognize_sphinx(audio)
                        print(f"👤 You said (offline): {command}")
                        return command.lower()
                    except:
                        return "recognition_error"
                        
        except sr.WaitTimeoutError:
            return "timeout"
        except sr.UnknownValueError:
            return "unknown"
        except Exception as e:
            print(f"Listening error: {e}")
            return "error"
    
    def get_current_time(self):
        """Get current time"""
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")
        return f"The current time is {current_time}"
    
    def get_current_date(self):
        """Get current date"""
        now = datetime.datetime.now()
        current_date = now.strftime("%A, %B %d, %Y")
        return f"Today is {current_date}"
    
    def tell_joke(self):
        """Tell a random joke"""
        joke = random.choice(self.jokes)
        return joke
    
    def open_application(self, app_name):
        """Open various applications"""
        try:
            if app_name in ['browser', 'internet']:
                webbrowser.open('https://www.google.com')
                return "Opening web browser"
            
            elif app_name == 'youtube':
                webbrowser.open('https://www.youtube.com')
                return "Opening YouTube"
            
            elif app_name == 'google':
                webbrowser.open('https://www.google.com')
                return "Opening Google"
            
            elif app_name in ['calculator', 'calc']:
                if sys.platform == "win32":
                    subprocess.Popen(['calc.exe'])
                elif sys.platform == "darwin":
                    subprocess.Popen(['open', '-a', 'Calculator'])
                else:
                    subprocess.Popen(['gnome-calculator'])
                return "Opening calculator"
            
            elif app_name in ['notepad', 'text editor']:
                if sys.platform == "win32":
                    subprocess.Popen(['notepad.exe'])
                elif sys.platform == "darwin":
                    subprocess.Popen(['open', '-a', 'TextEdit'])
                else:
                    subprocess.Popen(['gedit'])
                return "Opening text editor"
            
            else:
                return f"Sorry, I don't know how to open {app_name}"
                
        except Exception as e:
            return f"Error opening {app_name}: {str(e)}"
    
    def control_volume(self, action):
        """Control system volume"""
        try:
            if sys.platform == "win32":
                # Windows volume control
                if action == "up":
                    subprocess.run(['powershell', '-c', 
                                   '(New-Object -comObject WScript.Shell).SendKeys([char]175)'])
                    return "Volume increased"
                elif action == "down":
                    subprocess.run(['powershell', '-c', 
                                   '(New-Object -comObject WScript.Shell).SendKeys([char]174)'])
                    return "Volume decreased"
                elif action == "mute":
                    subprocess.run(['powershell', '-c', 
                                   '(New-Object -comObject WScript.Shell).SendKeys([char]173)'])
                    return "Volume muted"
            else:
                return "Volume control not available on this platform"
        except Exception as e:
            return f"Volume control error: {str(e)}"
    
    def take_photo(self):
        """Take a photo using webcam"""
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                return "Camera not available"
            
            ret, frame = cap.read()
            if ret:
                # Save photo with timestamp
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                photo_path = f"photo_{timestamp}.jpg"
                cv2.imwrite(photo_path, frame)
                cap.release()
                return f"Photo saved as {photo_path}"
            else:
                cap.release()
                return "Failed to capture photo"
                
        except Exception as e:
            return f"Camera error: {str(e)}"
    
    def calculate_math(self, expression):
        """Perform basic math calculations"""
        try:
            # Clean and prepare expression
            expression = expression.replace("plus", "+")
            expression = expression.replace("minus", "-")
            expression = expression.replace("multiply", "*")
            expression = expression.replace("times", "*")
            expression = expression.replace("divided by", "/")
            expression = expression.replace("divide", "/")
            
            # Extract numbers and operators
            allowed_chars = "0123456789+-*/.() "
            clean_expr = ''.join(c for c in expression if c in allowed_chars)
            
            if clean_expr.strip():
                result = eval(clean_expr)
                return f"The answer is {result}"
            else:
                return "Sorry, I couldn't understand the math expression"
                
        except Exception as e:
            return "Sorry, I couldn't calculate that"
    
    def web_search(self, query):
        """Perform web search"""
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            return f"Searching for {query} on Google"
        except Exception as e:
            return f"Search error: {str(e)}"
    
    def get_help(self):
        """Get list of available commands"""
        help_text = """
        Here are the things I can help you with:
        
        🕐 Time and Date - Ask for current time or date
        🌐 Web Browsing - Open browser, Google, YouTube
        📱 Applications - Open calculator, notepad
        🔊 Volume Control - Increase, decrease, or mute volume
        📷 Camera - Take photos
        🧮 Math - Perform calculations
        🔍 Search - Search the web
        😂 Entertainment - Tell jokes
        ❓ Help - Get this help message
        
        Just speak naturally and I'll try to help!
        """
        return help_text
    
    def process_command(self, command):
        """Process voice command and return response"""
        if not command or command in ['timeout', 'unknown', 'error', 'recognition_error']:
            if command == 'timeout':
                return "I didn't hear anything. Please try again."
            elif command == 'unknown':
                return "Sorry, I didn't understand that. Please speak clearly."
            else:
                return "Sorry, there was an error processing your command."
        
        # Check for greeting
        if any(word in command for word in self.commands['greeting']):
            return f"Hello! I'm your {self.assistant_name}. How can I help you today?"
        
        # Check for time
        elif any(word in command for word in self.commands['time']):
            return self.get_current_time()
        
        # Check for date
        elif any(word in command for word in self.commands['date']):
            return self.get_current_date()
        
        # Check for browser commands
        elif any(word in command for word in self.commands['open_browser']):
            return self.open_application('browser')
        
        elif any(word in command for word in self.commands['open_youtube']):
            return self.open_application('youtube')
        
        elif any(word in command for word in self.commands['open_google']):
            return self.open_application('google')
        
        elif any(word in command for word in self.commands['open_calculator']):
            return self.open_application('calculator')
        
        elif any(word in command for word in self.commands['open_notepad']):
            return self.open_application('notepad')
        
        # Volume controls
        elif any(word in command for word in self.commands['volume_up']):
            return self.control_volume('up')
        
        elif any(word in command for word in self.commands['volume_down']):
            return self.control_volume('down')
        
        elif any(word in command for word in self.commands['mute']):
            return self.control_volume('mute')
        
        # Camera
        elif any(word in command for word in self.commands['camera']):
            return self.take_photo()
        
        # Jokes
        elif any(word in command for word in self.commands['tell_joke']):
            return self.tell_joke()
        
        # Math calculations
        elif any(word in command for word in self.commands['math']) or any(op in command for op in ['+', '-', '*', '/', 'plus', 'minus', 'multiply', 'divide']):
            return self.calculate_math(command)
        
        # Web search
        elif any(word in command for word in self.commands['search']):
            query = command.replace('search for', '').replace('search', '').replace('find', '').strip()
            if query:
                return self.web_search(query)
            else:
                return "What would you like me to search for?"
        
        # Help
        elif any(word in command for word in self.commands['help']):
            return self.get_help()
        
        # Stop command
        elif any(word in command for word in self.commands['stop']):
            return "stop_assistant"
        
        # Default response for unrecognized commands
        else:
            return "I'm not sure how to help with that. Say 'help' to see what I can do."
    
    def start_listening(self):
        """Start the voice assistant"""
        self.running = True
        self.speak(f"Hello! I'm your {self.assistant_name}. I'm ready to help you!")
        
        while self.running:
            try:
                # Listen for wake word or direct command
                print("\n🎤 Say something or say 'stop' to exit...")
                command = self.listen()
                
                if command:
                    response = self.process_command(command)
                    
                    if response == "stop_assistant":
                        self.speak("Goodbye! Have a great day!")
                        self.running = False
                        break
                    else:
                        self.speak(response)
                
                # Small delay between listening sessions
                time.sleep(0.5)
                
            except KeyboardInterrupt:
                self.speak("Goodbye!")
                self.running = False
                break
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(1)
    
    def stop(self):
        """Stop the voice assistant"""
        self.running = False
        self.listening = False

# Web interface functions for Flask integration
assistant_instance = None
assistant_thread = None

def start_voice_assistant():
    """Start voice assistant in a separate thread"""
    global assistant_instance, assistant_thread
    
    if assistant_instance is None or not assistant_instance.running:
        assistant_instance = VoiceAssistant()
        assistant_thread = threading.Thread(target=assistant_instance.start_listening)
        assistant_thread.daemon = True
        assistant_thread.start()
        return True
    return False

def stop_voice_assistant():
    """Stop voice assistant"""
    global assistant_instance
    
    if assistant_instance and assistant_instance.running:
        assistant_instance.stop()
        return True
    return False

def is_assistant_running():
    """Check if assistant is running"""
    global assistant_instance
    return assistant_instance is not None and assistant_instance.running

# Main function for standalone execution
def main():
    """Main function to run the voice assistant"""
    try:
        assistant = VoiceAssistant()
        assistant.start_listening()
    except Exception as e:
        print(f"Error starting voice assistant: {e}")
        print("Please make sure you have the required dependencies installed:")
        print("pip install speechrecognition pyttsx3 pyaudio opencv-python")

if __name__ == "__main__":
    main()
