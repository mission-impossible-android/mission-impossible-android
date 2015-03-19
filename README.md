# Mission Impossible Android Hardening

This project is a attempting to streamline the process of following [Mike
Perry's Android hardening tutorial on the Tor
blog](https://blog.torproject.org/blog/mission-impossible-hardening-android-security-and-privacy).

It is currently a collection of scripts that require developer tools,
that will build and deploy an `update.zip` file to your connected
device. It aspires for be the basis for an installer for a custom
Android ROM based on CyanogenMod.

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
make TEMPLATE=mia-default DEFINITION=my-phone definition
make DEFINITION=my-phone build_deploy
```

After you generate the definition you can add a `cm_device_name=NAME_GOES_HERE` entry to the definition settings.ini file so that the phone phone won't be queried each time you the device name is needed.


* Open F-Droid and update the app list.
* Open the *My App List* app, and install any desired apps from
  `misc-apps.xml`.

### Updating Pre-installed Apps

The names of pre-installed apps are specified in `settings.ini`. These names
are resolved to their most recent download targets, or to the version specified.
Every so often, these can be updated so that new installs give the most recent
versions:

This process relies on the `xpath` command in the `libxml-xpath-perl` package.

```
sudo apt-get install libxml-xpath-perl
make download_apks
```

The above process does **NOT** delete previous APKs, and so you'll need
to manually delete duplicates and removed apps from `data/app`. (You
could also run `make clean` to remove all APKs before running the above.)

### Compatibility

Currently, project is being tested on the wifi-only Nexus 7, 2012 version
(`grouper`) and 2013 version (`flo`).

Devices currently available for testing:

| Device | Codename | Testers | Actively tested? |
|--------|:--------:|:-------:|:----------------:|
| LG Nexus 4 | mako | patcon | no |
| LG Nexus 4 | mako | SchnWalter | yes |
| Google/Asus Nexus 7 (wifi, 2012) | grouper | patcon | yes |
| Google/Asus Nexus 7 (wifi, 2013) | flo | mikeperry-tor | yes |
| Motorola Moto G 4G | peregrine | mikeperry-tor | no |
| Samsung Galaxy S II | i9100 | SchnWalter | no |
| OnePlus One | bacon | SchnWalter | no |
| Sony Xperia Tablet Z (wifi) | pollux_windy | SchnWalter | yes | 


### Links

- [updater-script syntax](http://forum.xda-developers.com/wiki/Edify_script_language)
- [TWRP emulator](http://teamw.in/project/twrp2/169)
