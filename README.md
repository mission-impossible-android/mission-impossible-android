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
