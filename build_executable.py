import os
import sys
import subprocess
import shutil
import importlib
from pathlib import Path

class ShareifyExecutableBuilder:

    def __init__(self):
        self.script_dir = Path(__file__).parent.absolute()
        self.dist_dir = self.script_dir / 'dist'
        self.build_dir = self.script_dir / 'build'
        self._mediapipe_bundle = self.script_dir / '_mediapipe_resources'
        self.target_script = None
        self.exe_name = None

    def log(self, message, level='INFO'):
        print(f'[{level}] {message}')

    def ensure_pyinstaller(self):
        try:
            __import__('PyInstaller')
            self.log('✓ PyInstaller is available')
            return True
        except ImportError:
            self.log('Installing PyInstaller...')
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
                self.log('✓ PyInstaller installed')
                return True
            except subprocess.CalledProcessError:
                self.log('✗ Failed to install PyInstaller', 'ERROR')
                return False

    def collect_mediapipe_resources(self):
        """
        Copy required mediapipe resource folders (modules, graphs, protobufs) into
        a local bundle directory so PyInstaller will include them intact.
        """
        try:
            mp = importlib.import_module('mediapipe')
        except Exception as e:
            self.log(f'Mediapipe not importable: {e} — skipping resource collection', 'WARNING')
            return None

        # mediapipe package root
        try:
            mp_root = Path(mp.__file__).parent
        except Exception:
            self.log('Could not determine mediapipe package path', 'WARNING')
            return None

        # Candidate resource folders inside mediapipe package to include
        candidates = ['modules', 'graphs', 'python', 'framework']
        # Create/clean bundle dir
        if self._mediapipe_bundle.exists():
            shutil.rmtree(self._mediapipe_bundle, ignore_errors=True)
        self._mediapipe_bundle.mkdir(parents=True, exist_ok=True)

        included = []
        for name in candidates:
            src = mp_root / name
            if src.exists():
                dest = self._mediapipe_bundle / name
                try:
                    # copytree with dirs_exist_ok for Python >=3.8
                    shutil.copytree(src, dest, dirs_exist_ok=True)
                except TypeError:
                    # fallback for older Python versions
                    if dest.exists():
                        shutil.rmtree(dest, ignore_errors=True)
                    shutil.copytree(src, dest)
                included.append((str(dest), f'mediapipe/{name}'))
                self.log(f'✓ Collected mediapipe resource: {src} -> {dest}')
        if not included:
            self.log('No mediapipe resource folders were found to collect', 'WARNING')
            return None
        return included

    def create_main_script(self):
        # Entry script that launches the target python file using runpy
        # This approach executes the provided script as __main__ so the
        # bundled executable behaves like running `python your_script.py`.
        target = self.target_script or 'face_detection.py'
        main_script = f'''import runpy
import sys
import os

if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

# Ensure application path is first on sys.path for bundled imports
sys.path.insert(0, application_path)

if __name__ == "__main__":
    script_path = os.path.join(application_path, {repr(os.path.basename(str(target)))})
    try:
        runpy.run_path(script_path, run_name='__main__')
    except Exception as e:
        print(f"Error running {{script_path}}: {{e}}")
        raise
'''
        entry_script_path = self.script_dir / 'face_entry.py'
        with open(entry_script_path, 'w', encoding='utf-8') as f:
            f.write(main_script)
        self.log(f'✓ Created entry script: {entry_script_path}')
        return entry_script_path

    def create_spec_file(self, entry_script):
        # Prepare datas list: include common folders + mediapipe resources if collected
        datas = []
        # Include project data dirs if present
        for folder_name in ('assets', 'models', 'Face_detection_testing_videos'):
            folder = self.script_dir / folder_name
            if folder.exists():
                datas.append((str(folder), folder_name))
                self.log(f'✓ Will include data folder: {folder}')

        # Collect mediapipe resources and add to datas
        mediapipe_datas = self.collect_mediapipe_resources()
        if mediapipe_datas:
            for src, target in mediapipe_datas:
                datas.append((src, target))
        # Also include face_detection.py explicitly (not strictly required but explicit)
        face_file = self.script_dir / 'face_detection.py'
        if face_file.exists():
            datas.append((str(face_file), '.'))

        # Build spec content
        # Use repr on paths to ensure correct escaping in spec file
        datas_repr = ",\n        ".join(f"({repr(s)}, {repr(t)})" for s, t in datas)

        exe_basename = self.exe_name or 'face_detection'
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path
block_cipher = None

a = Analysis(
    [{repr(str(entry_script))}],
    pathex=[{repr(str(self.script_dir))}],
    binaries=[],
    datas=[
        {datas_repr}
    ],
    hiddenimports=[
        'cv2',
        'mediapipe',
        'mediapipe.python',
        'pyautogui',
        'numpy',
        'google.protobuf'
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name={repr(exe_basename)},
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name={repr(exe_basename)},
)
'''
        spec_path = self.script_dir / f'{exe_basename}.spec'
        with open(spec_path, 'w', encoding='utf-8') as f:
            f.write(spec_content)
        self.log(f'✓ Created spec file: {spec_path}')
        return spec_path

    def build_executable(self, spec_path):
        # Build a single-file executable and include collected mediapipe resources
        exe_basename = self.exe_name or 'face_detection'
        self.log('Building single-file executable (onefile)...')
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)

        # Prepare add-data args from mediapipe bundle if present
        add_data_args = []
        if self._mediapipe_bundle.exists():
            # include each top-level folder under the bundle
            for child in self._mediapipe_bundle.iterdir():
                # target path inside the extracted runtime should be 'mediapipe/<name>'
                src = str(child)
                target = f"mediapipe/{child.name}"
                # PyInstaller on Windows uses ';' as separator for add-data
                add_data_args.extend(['--add-data', f"{src};{target}"])
                self.log(f'✓ Will bundle mediapipe resource: {src} -> {target}')

        # Make sure we have an entry script
        entry = self.script_dir / 'face_entry.py'
        if not entry.exists():
            self.log('Entry script not found: face_entry.py', 'ERROR')
            return False

        cmd = [
            sys.executable, '-m', 'PyInstaller',
            '--onefile',
            '--clean',
            '--name', exe_basename,
            '--console'
        ]

        # hidden imports
        hidden = ['mediapipe', 'google.protobuf', 'cv2', 'pyautogui']
        for hi in hidden:
            cmd.extend(['--hidden-import', hi])

        # attach add-data arguments
        cmd.extend(add_data_args)

        # finally the entry script
        cmd.append(str(entry))

        try:
            self.log('Running: ' + ' '.join(cmd))
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.script_dir)
            if result.returncode == 0:
                self.log('✓ Single-file executable built successfully!')
                return True
            else:
                self.log('✗ PyInstaller onefile build failed', 'ERROR')
                self.log(f'STDOUT: {result.stdout}')
                self.log(f'STDERR: {result.stderr}')
                return False
        except Exception as e:
            self.log(f'✗ Error during onefile build: {e}', 'ERROR')
            return False

    def cleanup_temp_files(self):
        exe_basename = self.exe_name or 'face_detection'
        temp_files = ['face_entry.py', f'{exe_basename}.spec']
        for file_name in temp_files:
            file_path = self.script_dir / file_name
            if file_path.exists():
                try:
                    file_path.unlink()
                except Exception:
                    pass

        # Remove mediapipe bundle if present
        if self._mediapipe_bundle.exists():
            try:
                shutil.rmtree(self._mediapipe_bundle, ignore_errors=True)
                self.log(f'✓ Removed temporary mediapipe bundle {self._mediapipe_bundle}')
            except Exception:
                pass

        if self.build_dir.exists():
            try:
                shutil.rmtree(self.build_dir)
            except Exception:
                pass

    def build(self):
        exe_basename = self.exe_name or 'face_detection'
        self.log(f'Starting {exe_basename} executable build...')
        self.log('=' * 50)

        if not self.ensure_pyinstaller():
            return False

        # create entry script for the requested target
        entry_script = self.create_main_script()
        spec_path = self.create_spec_file(entry_script)

        if not self.build_executable(spec_path):
            return False

        self.cleanup_temp_files()

        self.log('=' * 50)
        self.log('✓ Executable build completed!')

        # Report paths (onefile exe placed directly in dist/)
        shareify_dist = self.dist_dir
        if os.name == 'nt':
            exe_path = shareify_dist / f'{exe_basename}.exe'
        else:
            exe_path = shareify_dist / exe_basename

        if exe_path.exists():
            self.log(f'✓ Executable: {exe_path}')

        self.log(f'✓ Distribution folder: {shareify_dist}')
        self.log('✓ Ready to zip and deploy!')

        return True

def main():
    builder = ShareifyExecutableBuilder()
    # CLI: python build_executable.py [--clean] <target_script.py>
    if len(sys.argv) > 1:
        if sys.argv[1] == '--clean':
            if builder.dist_dir.exists():
                shutil.rmtree(builder.dist_dir)
                print('Cleaned dist directory')
            if builder.build_dir.exists():
                shutil.rmtree(builder.build_dir)
                print('Cleaned build directory')
            return

    target = None
    if len(sys.argv) > 1:
        target = sys.argv[1]

    if target:
        builder.target_script = Path(target)
        if not builder.target_script.exists():
            print(f"Target script not found: {target}")
            sys.exit(2)
        builder.exe_name = builder.target_script.stem

    success = builder.build()
    if not success:
        sys.exit(1)

if __name__ == '__main__':
    main()