"""Package a previously built libmain.so with SDL's matching Java sources.

Produces a development APK, not a claim of device compatibility.
"""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import zipfile

p = argparse.ArgumentParser()
p.add_argument('--sdk', type=Path, required=True)
p.add_argument('--sdl', type=Path, required=True)
p.add_argument('--blender', type=Path, required=True)
p.add_argument('--library', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
args = p.parse_args()
here = Path(__file__).resolve().parent
out = args.output.resolve()
out.mkdir(parents=True, exist_ok=True)
tools = args.sdk / 'build-tools/35.0.0'
android_jar = args.sdk / 'platforms/android-35/android.jar'

def run(*command):
    subprocess.run([str(x) for x in command], check=True)

classes = out / 'classes'
dex = out / 'dex'
classes.mkdir(exist_ok=True)
dex.mkdir(exist_ok=True)
java_sources = list((args.sdl / 'android-project/app/src/main/java').rglob('*.java'))
if not java_sources:
    raise RuntimeError('Matching SDL Java sources are required')
run('javac', '-source', '17', '-target', '17', '-classpath', android_jar,
    '-d', classes, *java_sources, *sorted(here.glob('*.java')))
run('jar', 'cf', out / 'classes.jar', '-C', classes, '.')
run(tools / 'd8', '--min-api', '26', '--lib', android_jar,
    '--output', dex, out / 'classes.jar')
run(tools / 'aapt2', 'link', '-I', android_jar, '--manifest', here / 'AndroidManifest.xml',
    '--min-sdk-version', '26', '--target-sdk-version', '35', '-o', out / 'unsigned.apk')
library = out / 'libmain.so'
shutil.copyfile(args.library, library)
strip = Path(os.environ.get('ANDROID_NDK_HOME', '/opt/android-ndk-r27c')) / 'toolchains/llvm/prebuilt/linux-x86_64/bin/llvm-strip'
run(strip, '--strip-debug', library)
with zipfile.ZipFile(out / 'unsigned.apk', 'a', compression=zipfile.ZIP_DEFLATED) as apk:
    apk.write(library, 'lib/arm64-v8a/libmain.so')
    for f in dex.glob('*.dex'):
        apk.write(f, f.name)
    data = args.blender / 'release/datafiles'
    for f in sorted(data.rglob('*')):
        if f.is_file() and f.suffix not in {'.cc', '.h', '.py', '.txt'} and f.name != 'CMakeLists.txt':
            apk.write(f, 'assets/blender/datafiles/' + f.relative_to(data).as_posix())
run(tools / 'zipalign', '-P', '16', '-f', '4', out / 'unsigned.apk', out / 'aligned.apk')
key = Path.home() / '.android/blender-development.keystore'
key.parent.mkdir(exist_ok=True)
if not key.exists():
    run('keytool', '-genkeypair', '-keystore', key, '-storepass', 'android',
        '-keypass', 'android', '-alias', 'androiddebugkey', '-keyalg', 'RSA',
        '-keysize', '2048', '-validity', '10000', '-dname', 'CN=Blender Development')
apk = out / 'blender-arm64-experimental.apk'
run(tools / 'apksigner', 'sign', '--ks', key, '--ks-pass', 'pass:android',
    '--key-pass', 'pass:android', '--out', apk, out / 'aligned.apk')
run(tools / 'apksigner', 'verify', '--verbose', apk)
print(apk)
