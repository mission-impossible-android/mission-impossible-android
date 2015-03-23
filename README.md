
# MIA - Mission Impossible: Android hardening

This project is a attempting to streamline the process of following the
guidelines from Mike Perry's post "Mission Impossible: Hardening Android for
Security and Privacy" on the [Tor Project Blog](https://blog.torproject.org/blog/mission-impossible-hardening-android-security-and-privacy).

It is currently a collection of scripts that require developer tools, that will
build and deploy an `update.zip` file to your connected device. It aspires for
be the basis for an installer for a custom Android ROM based on CyanogenMod.

Please keep in mind that this is experimental, and may not be functional at any
given moment. Also, it will likely wipe your Android device, and this is by
design!

**These tools come with no warranty. Test them on your own risk.**


## Requirements
* A supported device - see the compatibility table bellow.
* A linux/unix operating system - tested on: openSUSE and Ubuntu
* [Android SDK Tools](https://developer.android.com/sdk/index.html#Other) - with `adb` working globally.
* [Team Win Recovery Project](http://teamw.in/project/twrp2) bootloader installed onto your device.
* [Developer Options](https://developer.android.com/tools/device.html#developer-device-options) enabled on your device.
* [USB debugging](https://developer.android.com/tools/device.html#setting-up) enabled on your device.
* The MIA CLI tool - follow the setup instructions bellow.


## Usage
1.  Connect your device via USB, authorizing as necessary.

2.  Provide **temporary root access via ADB**, can be revoked later.
    ```
    mia definition create my-phone --yes
    mia build my-phone
    mia install my-phone
    ```

3.  After the installation completed open F-Droid and update the applications
    list.

4.  Open the *My App List* app, and install any desired applications from
    `misc-apps.xml`.


## MIA - CLI Tool
### Requirements:

* Python 3
* [docopt](https://github.com/docopt/docopt)
* [PyYAML](http://pyyaml.org/wiki/PyYAML)


### Setup instructions:

1. Install Python 3 if not already installed. Test using: `python3 --version`

2. Install the docopt and PyYAML modules:

    * Using Python Package Index [pip](https://pip.pypa.io/en/latest/index.html):
      `pip install docopt pyyaml`

    * Or using apt-get on Ubuntu:
      `apt-get install python3-docopt python3-yaml`

    * Or using zypper on openSUSE:
      `zypper install python3-docopt python3-PyYAML`

3. Clone the repository:
    ```
    git clone https://github.com/patcon/mission-impossible-android.git
    ```

4. (optional) Add the tools folder to the PATH environment variable. This will
   let you run the tool from any folder in your system.
    `export PATH=$PATH:$HOME/mission-impossible-android/tools`

    * Make sure to replace `$HOME/mission-impossible-android/tools` with the
      actual path of the tools folder.
    * If you skip this step you will need to use an absolute or relative
      path to the CLI Tool. Eg: `./tools/mia` or
      `~/mission-impossible-android/tools/mia` instead of `mia`

5. Test if the tool is working properly.
    ```
    mia --help
    ```

## Compatibility
Devices currently available for testing:

| Device | Codename | Testers | Actively tested? |
|--------|:--------:|:-------:|:----------------:|
| LG Nexus 4 | mako | patcon | no |
| LG Nexus 4 | mako | SchnWalter | yes |
| Asus Nexus 7 (wifi, 2012) | grouper | patcon | yes |
| Asus Nexus 7 (wifi, 2013) | flo | mikeperry-tor | yes |
| Motorola Moto G 4G | peregrine | mikeperry-tor | no |
| Samsung Galaxy S II | i9100 | SchnWalter | no |
| OnePlus One | bacon | SchnWalter | no |
| Sony Xperia Tablet Z (wifi) | pollux_windy | SchnWalter | yes |

NOTE: Other devices supported by CyanogenMod might also be compatible. If you
      test one, please report it in the [issue queue](https://github.com/patcon/mission-impossible-android/issues).


## Links
* [updater-script syntax](http://forum.xda-developers.com/wiki/Edify_script_language)
* [TWRP for Android Emulator](http://teamw.in/project/twrp2/169)
