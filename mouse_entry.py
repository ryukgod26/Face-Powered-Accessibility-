import sys
import os
import shutil
import tempfile

def _extract_mediapipe_resources():
    if not getattr(sys, "frozen", False):
        return None
    base = getattr(sys, "_MEIPASS", None)
    if not base:
        return None
    src = os.path.join(base, "mediapipe")
    if not os.path.isdir(src):
        return None
    dest_root = tempfile.mkdtemp(prefix="mediapipe_")
    dest = os.path.join(dest_root, "mediapipe")
    try:
        shutil.copytree(src, dest, dirs_exist_ok=True)
    except TypeError:
        if os.path.exists(dest):
            shutil.rmtree(dest, ignore_errors=True)
        shutil.copytree(src, dest)
    except Exception:
        os.makedirs(dest, exist_ok=True)
        for name in os.listdir(src):
            s = os.path.join(src, name)
            d = os.path.join(dest, name)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copy2(s, d)
    sys.path.insert(0, dest_root)
    return dest_root

if __name__ == "__main__":
    _extract_mediapipe_resources()
    try:
        import mousecontrol
    except Exception as e:
        print("Error importing mousecontrol:", e)
        sys.exit(1)
    if hasattr(mousecontrol, "main"):
        mousecontrol.main()
    else:
        # adjust this call if your module uses a different entry point
        print("mousecontrol has no main()")
        sys.exit(1)