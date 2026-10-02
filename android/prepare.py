"""Apply the experimental APK additions after the existing Android port patches."""
import argparse
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('blender', type=Path)
args = parser.parse_args()
root = args.blender.resolve()
here = Path(__file__).resolve().parent
patch = here / 'native.patch'
reverse = subprocess.run(['git', '-C', str(root), 'apply', '--reverse', '--check', str(patch)],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if reverse.returncode:
    subprocess.run(['git', '-C', str(root), 'apply', '--check', str(patch)], check=True)
    subprocess.run(['git', '-C', str(root), 'apply', str(patch)], check=True)
platform = root / 'build_files/cmake/platform/platform_android.cmake'
marker = '# Experimental APK dependencies (android/prepare.py).'
text = platform.read_text()
if marker not in text:
    platform.write_text(text + '\n' + marker + '\nif(BLENDER_ANDROID_APK)\n'
                        + '  include("${BLENDER_ANDROID_SUPPORT}/dependencies.cmake")\nendif()\n')
