#!/system/bin/sh

# @TODO: Make sure this script is ran just once.
# @TODO: Maybe split into files inside `/data/local/miainit.d/`? In CM12 `/data/local/userinit.d/` is deprecated.

# A short command for adding log entries.
# To view these log entries you can run this command on your computer:
#   $ adb logcat -s MIA
# You can clear the logcat by running on your computer:
#   $ adb logcat -c
LOG="log -p I -t MIA"
$LOG "Running MIA init script: $0"
$LOG "Environment PATH variable: ${PATH}"


# GH-19: Disable android USB debugging using ADB.
USB_CONFIG=$(getprop sys.usb.config)
$LOG "The sys.usb.config is: ${USB_CONFIG}"

# The `sys.usb.config` property has the following format: foo,adb,bar.
# In order to disable ADB, it needs to be removed from the `sys.usb.config` property.
# You can run this command on the device to see possible values:
#   $ grep sys.usb.config /*.usb.rc
USB_CONFIG=$(echo ${USB_CONFIG} | sed -e 's/,\?adb,\?/,/g' -e 's/^,//' -e 's/,$//')

$LOG "Updating sys.usb.config to disable android USB debugging using ADB."
setprop persist.sys.usb.config ${USB_CONFIG}
USB_CONFIG=`getprop sys.usb.config`
$LOG "The sys.usb.config is: ${USB_CONFIG}"


# Check DB dir.
DIRNAME='/data/data/com.android.settings/databases'
test -d $DIRNAME && $LOG "Directory exists: $DIRNAME" || $LOG "Directory does not exist: $DIRNAME"


# Check if ADB is enabled.
# We don't have a working JRE at this moment.
#ADB_STATUS=`settings get global adb_enabled`
#$LOG "ADB status is: ${ADB_STATUS}"


$LOG "Finished MIA init script: $0"
