import argparse
import subprocess
parser = argparse.ArgumentParser(description='This Program is Created Just to Convert face_detection files into Executables.')
parser.add_argument("--face", action="store_true", help="Compile face detection Python file into Executable.")
parser.add_argument("--mouse", action="store_true", help="Compile Mouse Control Python file into Executable.")
parser.add_argument("--hand", action="store_true", help="Compile face detection Python file into Executable.")
parser.add_argument("--painter", action="store_true", help="Compile face detection Python file into Executable.")
args = parser.parse_args()
MP = r"D:\face_accesibility\Face-Powered-Accessibility-\faceAccessibility\Lib\site-packages\mediapipe"

if args.face:
    command = [
    "pyinstaller",
    "--onefile",
    "--name", "face_detection",
    "--add-data", f"{MP}\\modules;mediapipe/modules",
    "--add-data", f"{MP}\\python;mediapipe/python",
    "--add-data", f"{MP}\\framework;mediapipe/framework",
    "--hidden-import", "mediapipe",
    "--hidden-import", "google.protobuf",
    "--hidden-import", "pyautogui",
    "--hidden-import", "cv2",
    "face_entry.py"
]
    subprocess.run(command,shell=True)

if args.mouse:
    command = [
    "pyinstaller",
    "--onefile",
    "--name", "mousecontrol",
    "--add-data", f"{MP}\\modules;mediapipe/modules",
    "--add-data", f"{MP}\\python;mediapipe/python",
    "--add-data", f"{MP}\\framework;mediapipe/framework",
    "--hidden-import", "mediapipe",
    "--hidden-import", "google.protobuf",
    "--hidden-import", "pyautogui",
    "--hidden-import", "cv2",
    "mouse_entry.py"
]
    subprocess.run(command,shell=True)

if args.hand:
    command = [
    "pyinstaller",
    "--onefile",
    "--name", "hand_detection",
    "--add-data", f"{MP}\\modules;mediapipe/modules",
    "--add-data", f"{MP}\\python;mediapipe/python",
    "--add-data", f"{MP}\\framework;mediapipe/framework",
    "--hidden-import", "mediapipe",
    "--hidden-import", "google.protobuf",
    "--hidden-import", "pyautogui",
    "--hidden-import", "cv2",
    "hand_entry.py"
]
    subprocess.run(command,shell=True)
    
if args.painter:
    command = [
    "pyinstaller",
    "--onefile",
    "--name", "aipainter",
    "--add-data", f"{MP}\\modules;mediapipe/modules",
    "--add-data", f"{MP}\\python;mediapipe/python",
    "--add-data", f"{MP}\\framework;mediapipe/framework",
    "--hidden-import", "mediapipe",
    "--hidden-import", "google.protobuf",
    "--hidden-import", "pyautogui",
    "--hidden-import", "cv2",
    "aipainter_spec.py"
]
    subprocess.run(command,shell=True)



    '''$MP = "D:\face_accesibility\Face-Powered-Accessibility-\faceAccessibility\Lib\site-packages\mediapipe"
>>
>> pyinstaller `
>>   --onefile `
>>   --name mousecontrol `
>>   --add-data "$MP\modules;mediapipe/modules" `
>>   --add-data "$MP\python;mediapipe/python" `
>>   --add-data "$MP\framework;mediapipe/framework" `
>>   --hidden-import mediapipe `
>>   --hidden-import "google.protobuf" `
>>   --hidden-import pyautogui `
>>   --hidden-import cv2 `
>>   mouse_entry.py'''
