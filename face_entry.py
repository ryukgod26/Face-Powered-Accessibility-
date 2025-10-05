import sys
import os
import shutil
import tempfile

def _extract_mediapipe_resources():
    """When running from a onefile exe, resources added with --add-data
    are extracted into sys._MEIPASS. Copy the mediapipe resource tree
    to a temporary folder and prepend it to sys.path so imports find it.
    """
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
        # shutil.copytree with dirs_exist_ok requires Python >= 3.8
        shutil.copytree(src, dest, dirs_exist_ok=True)
    except TypeError:
        # fallback for older shutil.copytree signature
        if os.path.exists(dest):
            shutil.rmtree(dest, ignore_errors=True)
        shutil.copytree(src, dest)
    except Exception:
        # best-effort: copy children
        os.makedirs(dest, exist_ok=True)
        for name in os.listdir(src):
            s = os.path.join(src, name)
            d = os.path.join(dest, name)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copy2(s, d)

    # Prepend the temp folder so `import mediapipe` loads from the extracted copy
    sys.path.insert(0, dest_root)
    return dest_root

if __name__ == "__main__":
    _extract_mediapipe_resources()
    # Now import and run your script as __main__
    try:
        import face_detection
    except Exception as e:
        print("Error importing face_detection:", e)
        sys.exit(1)

    if hasattr(face_detection, "main"):
        face_detection.main()
    else:
        print("face_detection has no main()")
        sys.exit(1)