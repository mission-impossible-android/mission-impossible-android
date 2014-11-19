# Mission Impossible Android Hardening

This project is a attempting to streamline the process of following [Mike
Perry's Android hardening tutorial on the Tor
blog](https://blog.torproject.org/blog/mission-impossible-hardening-android-security-and-privacy).

It is currently a collection of scripts that require developer tools. It
aspires for be the basis for an installer for a custom Android ROM based
on Cyanogenmod.

Please keep in mind that this is experimental, and may not be functional
at any given moment. Also, it will likely wipe your Android device, and
this is by design!

### Usage

* [Enable](https://developer.android.com/tools/device.html#developer-device-options) on-device developer options.
- [Enable](https://developer.android.com/tools/device.html#setting-up) USB debugging.
* Connect your device via USB, authorizing as neccessary.
* Provide **temporary root access via ADB**. (We will revoke later.)

```
make cm_dl_link # Follow instructions
adb push path/to/cm-11-<TIMESTAMP>-SNAPSHOT-<VERSION>-<DEVICE_CODENAME>.zip /sdcard/
make build_deploy


### Links

- [updater-script syntax](http://forum.xda-developers.com/wiki/Edify_script_language)
- [TWRP emulator](http://teamw.in/project/twrp2/169)
