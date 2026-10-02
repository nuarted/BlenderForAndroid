# Experimental Android APK

This is work in progress. The command-line Android binary has been built;
installation, graphics and interaction on a tablet are separate validation steps.
Do not present an untested APK as a working Blender application.

The existing OpenGL ES context is insufficient for Blender's OpenGL 4.3 backend.
This APK experiment adds an Android Vulkan surface to the existing Vulkan backend.
It requires a device satisfying Blender's Vulkan feature checks, not merely one
advertising Vulkan. Runtime Python remains disabled in this configuration, which
also limits Python-defined UI and functionality.

After the normal port and `without_python.patch` are applied:

1. Install `shaderc` and `vulkan-headers` with the repository's API 26 triplet.
2. Run `python3 android/prepare.py /path/to/blender`.
3. Reconfigure the existing Android build with:

   ```sh
   cmake -S /path/to/blender -B /path/to/build-android \
     -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
     -DBLENDER_ANDROID_APK=ON \
     -DBLENDER_ANDROID_SUPPORT=/absolute/path/to/repository/android \
     -DBLENDER_ANDROID_ENTRY=/absolute/path/to/repository/android/entry.cc \
     -DWITH_VULKAN_BACKEND=ON \
     -DSHADERC_ROOT_DIR=/opt/vcpkg/installed/arm64-android \
     -DVULKAN_ROOT_DIR=/opt/vcpkg/installed/arm64-android
   ninja -j8 -C /path/to/build-android blender
   ```

4. Run `package.py --help`. It needs SDK platform 35, build tools 35.0.0,
   Java 17, the matching SDL source directory, and the resulting `libmain.so`.
   It generates a development-signed ARM64 APK with minimum API 26.

Keep the development signing key outside the repository. The packaging script
uses `~/.android/blender-development.keystore`. Device logs are written to the
application's private `files/blender.log`; with this development APK they can be
retrieved with `adb shell run-as org.blender.android.experimental cat files/blender.log`.
Without USB, return to the launcher and tap «Поделиться журналом». The native
activity runs in a separate process so this launcher remains available after a crash.

Before declaring success, install on the intended device, launch the activity,
verify a visible usable interface, and inspect `adb logcat` for native crashes.
