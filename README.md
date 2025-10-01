# Face-Powered Accessibility System

A comprehensive computer vision-based accessibility solution that enables hands-free computer interaction using facial expressions and hand gestures. This system is designed to help users with limited mobility control their computer using only facial movements and gestures.

## 🌟 Features

### 🎯 Nose-Based Mouse Control
- **Directional Movement**: Control mouse cursor by moving your nose - cursor moves in the direction of nose movement rather than direct positioning
- **Dead Zone Control**: Center dead zone prevents jittery movements when your nose is near the center
- **Smooth Movement**: Integrated smoothing algorithm for stable and precise cursor control
- **Adjustable Sensitivity**: Customizable movement speed and sensitivity settings
- **Screen Boundary Protection**: Automatic boundary clamping to prevent cursor from going off-screen

### 👄 Facial Expression Controls  
- **Lip Movement Detection**: Advanced lip closure detection using MediaPipe facial landmarks
- **Click Actions**: Right-click functionality triggered by lip movements
- **Real-time Processing**: Fast and accurate facial expression recognition
- **Customizable Thresholds**: Adjustable sensitivity for different users and lighting conditions

### 🖐️ Hand Gesture Recognition
- **Multi-Hand Detection**: Support for up to 4 hands simultaneously
- **Finger Counting**: Real-time finger counting and gesture recognition
- **Hand Landmark Tracking**: Precise 21-point hand landmark detection
- **Finger State Detection**: Individual finger up/down state recognition

### 🎨 AI Painter (In Development)
- **Gesture-Based Drawing**: Paint and draw using hand gestures
- **Color Selection**: Choose colors using different finger combinations
- **Mode Selection**: Switch between different drawing modes with gestures

## 🔧 Technical Specifications

### Core Technologies
- **Computer Vision**: OpenCV for image processing and video capture
- **Machine Learning**: MediaPipe for real-time face and hand detection
- **GUI Automation**: PyAutoGUI for mouse control and system interaction
- **Mathematical Processing**: NumPy for efficient numerical computations

### Performance Features
- **Real-time Processing**: Optimized for low-latency real-time operation
- **FPS Monitoring**: Built-in frame rate monitoring and display
- **Memory Efficient**: Lightweight implementation suitable for various hardware
- **Fail-safe Protection**: Built-in safety mechanisms to prevent system lockup

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- Webcam or video input device
- Windows/macOS/Linux operating system

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/ryukgod26/Face-Powered-Accessibility-.git
   cd Face-Powered-Accessibility-
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv faceAccessibility
   # Windows
   faceAccessibility\Scripts\activate
   # macOS/Linux
   source faceAccessibility/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 📋 Dependencies

```
opencv-python    # Computer vision library
mediapipe       # Google's ML framework for perception tasks
pyautogui       # Cross-platform GUI automation
numpy           # Numerical computing library
```

## 🎮 Usage

### Nose Mouse Control
```bash
python mousecontrol.py
```
**Controls:**
- Move your nose to control the cursor direction
- Keep nose in center to stop movement
- Lip movements trigger right-click actions
- Press 'q' to quit the application

### Face Detection Demo
```bash
python face_detection.py
```
**Features:**
- Real-time face mesh visualization
- Lip closure detection with visual feedback
- Nose position tracking
- FPS performance monitoring

### Hand Gesture Recognition
```bash
python hand_detection.py
```
**Features:**
- Multi-hand tracking and visualization
- Finger counting display
- Hand landmark visualization
- Real-time gesture recognition

### Main Application (Integration)
```bash
python main.py
```
**Features:**
- Combined face and hand detection
- Integrated accessibility controls
- Multi-modal interaction support

## ⚙️ Configuration

### Mouse Control Settings
```python
# In noseController class
self.moveSpeed = 10      # Cursor movement speed
self.deadZone = 50       # Center dead zone radius
self.sensitivity = 2.0   # Movement sensitivity
self.smoothFactor = 5    # Movement smoothing factor
```

### Face Detection Settings
```python
# In faceDetector class
max_faces = 2                    # Maximum faces to detect
minDetectionCon = 0.5           # Detection confidence threshold
minTrackCon = 0.5               # Tracking confidence threshold
lip_threshold = 0.05            # Lip closure sensitivity
```

### Hand Detection Settings
```python
# In handDetector class
max_hands = 4                   # Maximum hands to detect
minDetectionCon = 0.5          # Detection confidence threshold
minTrackingCon = 0.5           # Tracking confidence threshold
```

## 🔍 File Structure

```
Face-Powered-Accessibility-/
├── main.py                 # Main application entry point
├── mousecontrol.py         # Nose-based mouse control system
├── face_detection.py       # Face detection and analysis
├── hand_detection.py       # Hand gesture recognition
├── aiPainter.py           # AI-powered drawing application
├── requirements.txt        # Project dependencies
├── README.md              # Project documentation
├── Face_detection_testing_videos/  # Test video files
│   ├── hands.mp4
│   ├── test1.mp4
│   └── ...
└── output/                # Compiled executables
    ├── face_detection.exe
    ├── hand_detection.exe
    └── mousecontrol.exe
```

## 🛠️ Troubleshooting

### Common Issues

**Camera Access Issues:**
```python
# Try different camera indices
cap = cv2.VideoCapture(0)  # Default camera
cap = cv2.VideoCapture(1)  # External camera
```

**Performance Issues:**
- Ensure good lighting conditions
- Close unnecessary applications
- Lower video resolution if needed
- Adjust detection confidence thresholds

**Mouse Control Issues:**
- Disable PyAutoGUI fail-safe: `pyautogui.FAILSAFE = False`
- Adjust sensitivity and dead zone settings
- Check screen resolution compatibility

## 🎯 Use Cases

- **Accessibility Support**: Assist users with limited hand mobility
- **Hands-free Computing**: Control computers without physical contact
- **Gaming Applications**: Novel game control mechanisms
- **Presentation Tools**: Hands-free presentation navigation
- **Educational Tools**: Interactive learning experiences
- **Rehabilitation**: Motor skill training and assessment

## 🔬 Technical Details

### Face Mesh Detection
- Uses MediaPipe's 468 facial landmarks
- Real-time face mesh visualization with FACEMESH_TESSELATION
- Nose tip tracking using landmark index 1
- Lip closure detection using multiple landmark pairs

### Hand Landmark Detection
- 21-point hand landmark detection per hand
- Finger tip tracking using landmark indices [4,8,12,16,20]
- Real-time hand connection visualization
- Multi-hand support with individual hand tracking

### Mouse Control Algorithm
- Directional movement based on nose displacement from center
- Dead zone implementation to prevent jitter
- Smooth movement interpolation for natural cursor flow
- Screen boundary protection with fail-safe mechanisms

## 🚧 Future Enhancements

- [ ] Voice command integration
- [ ] Eye tracking for additional control options
- [ ] Gesture-based keyboard input
- [ ] Customizable gesture mappings
- [ ] Multi-user support
- [ ] Mobile app integration
- [ ] Cloud-based model improvements
- [ ] Real-time calibration system

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**ryukgod26**
- GitHub: [@ryukgod26](https://github.com/ryukgod26)

## 🙏 Acknowledgments

- **MediaPipe Team** for the excellent computer vision framework
- **OpenCV Community** for the comprehensive computer vision library
- **PyAutoGUI Developers** for the cross-platform automation tools
- **Accessibility Community** for inspiration and feedback

---

*This project aims to make computer interaction more accessible for everyone. Your feedback and contributions help make technology more inclusive.*