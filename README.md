# Mission Impossible Android Hardening

This project is a attempting to streamline the process of following [Mike
Perry's Android hardening tutorial on the Tor
blog](https://blog.torproject.org/blog/mission-impossible-hardening-android-security-and-privacy).

It is currently a collection of scripts that require developer tools,
that will build and deploy an `update.zip` file to your connected
device. It aspires for be the basis for an installer for a custom
Android ROM based on Cyanogenmod.

Please keep in mind that this is experimental, and may not be functional
at any given moment. Also, it will likely wipe your Android device, and
this is by design!

### Usage

* [Install](http://teamw.in/project/twrp2) Team Win Recovery Project bootloader. (Follow instructions for your device.)
* [Enable](https://developer.android.com/tools/device.html#developer-device-options) on-device developer options.
- [Enable](https://developer.android.com/tools/device.html#setting-up) USB debugging.
* Connect your device via USB, authorizing as neccessary.
* Provide **temporary root access via ADB**. (We will revoke later.)

```
make cm_dl_link # Follow instructions
make push_cm_zip
make build_deploy
```

### Compatibility

Currently, project is being tested on the wifi-only Nexus 7, 2012 version (`grouper`).

### Links

- [updater-script syntax](http://forum.xda-developers.com/wiki/Edify_script_language)
- [TWRP emulator](http://teamw.in/project/twrp2/169)
