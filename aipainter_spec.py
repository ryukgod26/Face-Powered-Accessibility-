import sys
import os
import tempfile
import shutil

def _extract_mediapipe_resources():
    if not getattr(sys, "frozen", False):
        return
    base = getattr(sys, "_MEIPASS", None)
    if not base:
        return
    src = os.path.join(base, "mediapipe")
    if not os.path.isdir(src):
        return
    dest_root = tempfile.mkdtemp(prefix="mediapipe_")
    dest = os.path.join(dest_root, "mediapipe")
    try:
        shutil.copytree(src, dest, dirs_exist_ok=True)
    except TypeError:
        if os.path.exists(dest):
            shutil.rmtree(dest, ignore_errors=True)
        shutil.copytree(src, dest)
    sys.path.insert(0, dest_root)

if __name__ == "__main__":
    _extract_mediapipe_resources()
    try:
        import aiPainter
    except Exception as e:
        print("Error importing aipainter:", e)
        sys.exit(1)
    if hasattr(aiPainter, "main"):
        aiPainter.main()
    else:
        # If module uses class-based API, call appropriate function/instantiate
        print("aipainter has no main() - ensure it exposes a main() function.")
        sys.exit(1)