# VoiceChanger – Real-Time Audio Processing App

**VoiceChanger** is a simple yet powerful Python application that lets you **modify your voice in real-time** using sliders to control pitch, volume, distortion, and compression.

Built with:
-  **Python**
-  **SoundDevice** for real-time audio I/O
-  **Kivy** for the graphical user interface (GUI)
-  **NumPy** for efficient signal processing

---

## Features

- **Real-Time Audio Processing:** Hear changes instantly as you adjust sliders.  
- **Pitch Shifting:** Alters the pitch by changing the sample rate.  
- **Volume Control:** Amplifies or reduces volume dynamically.  
- **Distortion Effect:** Adds random noise to simulate a “radio” or “grunge” effect.  
- **Dynamic Compression:** Smooths loud peaks to create balanced sound output.  
- **Interactive GUI:** Built using Kivy’s sliders, buttons, and labels.  
- **Customizable Parameters:** All values can be tuned while the app runs.  

---

## How It Works

The app records input from your **microphone**, processes the sound in real-time through several stages:
1. **Pitch Shift** → Resamples the waveform to modify tone.  
2. **Volume Adjustment** → Scales signal amplitude.  
3. **Distortion** → Adds controlled Gaussian noise.  
4. **Compression** → Reduces dynamic range for consistent loudness.  

Finally, it plays the processed sound back through your **output device**.

---

## Interface Overview

| Control | Description |
|----------|-------------|
| 🎚️ **Pitch Factor** | Changes voice pitch (1.0 = normal, 2.0 = double pitch) |
| 🔊 **Volume Factor** | Adjusts volume intensity |
| ⚡ **Distortion Factor** | Adds a noise-based distortion effect |
| 🎛️ **Compression Factor** | Controls the level of dynamic compression |
| ▶️ **Start Button** | Starts live voice processing |
| ⏹️ **Stop Button** | Stops the processing stream |

---

## ⚙️ Installation

1. **Clone this repository**
   ```bash
   python main.py

   
## Author
   Ali Emad (asgard)
   
