# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['mouse_entry.py'],
    pathex=[],
    binaries=[],
    datas=[('D:\\face_accesibility\\Face-Powered-Accessibility-\\faceAccessibility\\Lib\\site-packages\\mediapipe\\modules', 'mediapipe/modules'), ('D:\\face_accesibility\\Face-Powered-Accessibility-\\faceAccessibility\\Lib\\site-packages\\mediapipe\\python', 'mediapipe/python'), ('D:\\face_accesibility\\Face-Powered-Accessibility-\\faceAccessibility\\Lib\\site-packages\\mediapipe\\framework', 'mediapipe/framework')],
    hiddenimports=['mediapipe', 'google.protobuf', 'pyautogui', 'cv2'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='mousecontrol',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
