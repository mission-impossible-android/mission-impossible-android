
# Usage example: Google Nexus 4 (mako) and CyanogenMod

For this example we are going to use Android KitKat (v4.4.4) and CyanogenMod 11
since, at the moment, there is no stable snapshot of CyanogenMod 12 based on
Android Lollipop (v5.0.x).


### Notes
 *  It is best if this is not the first time you have installed
    [CyanogenMod](http://wiki.cyanogenmod.org/w/Install_CM_for_mako?setlang=en)
    onto your device. This way you can know for sure that things work.
 *  For best chances of success you might want to download and install a fresh
    standard image from the Google [Factory Images for Nexus Devices](https://developers.google.com/android/nexus/images)
    page and then follow the [Flashing Instructions](https://developers.google.com/android/nexus/images#instructions)


## Install the TWRP and Root
[Team Win Recovery Project](http://www.teamw.in/project/twrp2) is the custom
recovery that is needed in order to auto install the generated update.zip and
perform various tasks. Download TWRP for your device and follow the [install
instructions](http://twrp.me/devices/lgnexus4.html#fastboot-install).

Then Manually root the device or reboot into recovery and simply select
"Reboot > System" and you will be notified that the devices is not rooted and
you will have the option to install "SuperSu" in order to root the device. Just
confirm the installation and you are done.


## Generate and install an update.zip
Follow the instruction from this repo and use the installed tool to customize

1.  Install the `mia` tool. Test using:
    `mia --version`
2.  Create a definition and follow the instructions presented:
    ```bash
    mkdir ~/mia-workspace && cd ~/mia-workspace
    mia create definition mynexus
    ```
3.  Build the definition:
    ```bash
    mia build definition mynexus
    ```
4.  Reboot the phone into recovery.
5.  Install the generated update.zip file:
    ```bash
    mia install definition mynexus
    ```
    NOTE: It will take about 90s to push the zip files onto the devices and
          about 60s for the installation will be finished and you will see the
          OS boot screen.
6.  Wait a couple of minutes for OS to boot and then open Orbot and make sure
    you are connected to the Tor network.
7.  **Safe surfing!!!**
