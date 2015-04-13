
## Usage example: Google Nexus 4 (mako) and CyanogenMod

### Requirements
For best chances of success you might want to download and install a fresh
standard image from the Google [Factory Images for Nexus Devices](https://developers.google.com/android/nexus/images)
page.

For this example we are going to use Android KitKat (v4.4.4) and CyanogenMod 11
since, at the moment, there is no stable snapshot of CyanogenMod 12 based on
Android Lollipop (v5.0.x).

**NOTE: It is best if this is not the first time you have installed
[CyanogenMod](http://wiki.cyanogenmod.org/w/Install_CM_for_mako?setlang=en)
onto your device. This way you can know for sure that things work.**


# Reset the device
[Download](https://developers.google.com/android/nexus/images) and extract the
factory image zip for the device and follow the instructions provided on the download page. Here's a summary:

1.  Reboot the device into the bootloader. You can press and hold `VolumeDown + Power` until you see the bootloader or You can use `adb reboot bootloader`.
2.  Once in recovery run the `flash-all.sh` script extracted from the downloaded
    image zip and wait for it to finish reinstalling the OS (about 90s).
3.  Boot into the OS and make sure everything is OK.


# Install the TWRP
Team Win Recovery Project is custom recovery that is needed in order to install
the custom ROM.

1.  Go to the [TWRP page](http://www.teamw.in/project/twrp2) and download the
    recovery image for the device.
2.  Reboot the device into recovery.
3.  Flash the TWRP recovery image onto the device.
    ```bash
    fastboot flash recovery twrp-*-mako.img
    ```
4.  Reboot into recovery mode in order to root the devices.
5.  Simply select "Reboot > System" and you will be notified that the devices
    is not rooted and you will have the option to install "SuperSu".
6.  Confirm the SuperSu installation
7.  Wait for the reboot and continue with the next section.


# Generate and install an update.zip
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
