#!/system/bin/sh

# @TODO: Make sure this script is ran just once.
# @TODO: Split into multiple files inside `/data/local/miainit.d/`. `/data/local/userinit.d/` is deprecated.

# A short command for adding log entries.
# To view these log entries you can run this command on your computer:
#   $ adb logcat -s MIA
# You can clear the logcat by running on your computer:
#   $ adb logcat -c
LOG="log -p I -t MIA"
$LOG "Running MIA init script: $0"
$LOG "Environment PATH variable: ${PATH}"


# GH-94: Enable Airplane Mode and broadcast the event.
settings put global airplane_mode_on 1
am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true
AIRPLANE_MODE=`settings get global airplane_mode_on`
$LOG "The global airplane_mode_on setting is set to: ${AIRPLANE_MODE}"


# Check the android debugging status once again.
ADB_STATUS=`settings get global adb_enabled`
$LOG "The global adb_enabled setting is set to: ${ADB_STATUS}"


# Change the device hostname.
$LOG "Change the secure device_hostname setting to: localhost"
DEVICE_HOSTNAME=`/system/bin/settings get secure device_hostname`
$LOG "The device hostname was: ${DEVICE_HOSTNAME}"
settings put secure device_hostname "localhost"
# Change the hostname for the current session.
setprop net.hostname localhost
echo localhost > /proc/sys/kernel/hostname


# @see https://developer.android.com/reference/android/provider/Settings.Secure.html#LOCATION_PROVIDERS_ALLOWED
# @deprecated in API level 19
settings put secure location_providers_allowed ''
# For API level 19
# @see https://developer.android.com/reference/android/provider/Settings.Secure.html#LOCATION_MODE
#settings put secure location_mode 0
#am broadcast -a android.location.MODE_CHANGED


# Do not automatically fetch time from the network.
# @see https://developer.android.com/reference/android/provider/Settings.Global.html#AUTO_TIME
settings put global auto_time 0
AUTO_TIME=`settings get global auto_time`
$LOG "The global auto_time setting is set to: ${AUTO_TIME}"


# The Tor binary does not start until RECEIVE_BOOT_COMPLETED is broadcast. We
# need the supporting data files created in the org.torproject.android
# directory prior to that.  Starting this service happens to check for these
# directories and generate them if missing (which they are on first boot).
#
# This is a hack, and race conditions might occur if the .firstboot.sh script gets to long.
am startservice org.torproject.android/org.torproject.android.service.TorService

# Fake BOOT_COMPLETE to force orwall to apply rules in background.
# TODO: Investigate why this doesn't happen on its own.
am broadcast -a android.intent.action.BOOT_COMPLETED -n org.ethack.orwall/.BootBroadcast


####################
# Old script based on:
# https://raw.githubusercontent.com/CyanogenMod/android_vendor_cyanogen/a013434bb46bb06bf0b7c83817cbcfaf040c5874/prebuilt/common/bin/fix_permissions
# and http://forum.xda-developers.com/showthread.php?t=1441378

APPS=( \
com.android.inputmethod.latin \
com.android.nfc \
com.android.settings \
com.xabber.androiddev \
org.ethack.orwall \
org.torproject.android \
)

SIP_APP=com.csipsimple
BROWSER_APP=org.mozilla.fennec_fdroid
ORWALL_APP=org.ethack.orwall
#
## Programs needed
#ECHO="busybox echo"
#GREP="busybox grep"
#EGREP="busybox egrep"
#CAT="busybox cat"
#CHOWN="busybox chown"
#CHMOD="busybox chmod"
#CUT="busybox cut"
#FIND="busybox find"
#SED="busybox sed"
#
#MISC_DIR=/sdcard/misc
#source $MISC_DIR/library.sh
#
## Get important UIDs for later
#BROWSER_UID=$(get_app_uid $BROWSER_APP)
#SIP_UID=$(get_app_uid $SIP_APP)
#ORWALL_UID=$(get_app_uid $ORWALL_APP)
#
## Fix orwall's config UIDs
#$SED -i /data/data/org.ethack.orwall/shared_prefs/org.ethack.orwall_preferences.xml -e "s/REPLACE_WITH_BROWSER_UID/$BROWSER_UID/"
#$SED -i /data/data/org.ethack.orwall/shared_prefs/org.ethack.orwall_preferences.xml -e "s/REPLACE_WITH_SIP_UID/$SIP_UID/"
#
## Give OrWall full, permanent root access
#echo "Importing Superuser database with orWall uid $APP_UID pre-authorized." >> /sdcard/init.log
#mkdir -p /data/data/com.android.settings/databases
#$SED -i $MISC_DIR/com.android.settings_su.sql -e "s/REPLACE_WITH_ORWALL_UID/$ORWALL_UID/"
#/system/xbin/sqlite3 /data/data/com.android.settings/databases/su.sqlite < $MISC_DIR/com.android.settings_su.sql
#
## Generate SQL to create orWall app DB
#SQL_FRAGMENT=""
#while read APP_DATA; do
#  APP_NAME=$(echo $APP_DATA | $CUT -f'1' -d':')
#  APP_UID=$(get_app_uid $APP_NAME)
#  APP_PORT_TYPE=$(echo $APP_DATA | $CUT -f'2' -d':')
#  APP_PORT_TYPE=${APP_PORT_TYPE:-TransProxy} # Default port type
#  SQL_LINE="INSERT INTO rules VALUES($APP_UID,'$APP_NAME','Tor',9040,'$APP_PORT_TYPE');"
#  SQL_FRAGMENT="$SQL_LINE\n$SQL_FRAGMENT"
#done < $MISC_DIR/app-list-orwall.txt
#$SED -i $MISC_DIR/org.ethack.orwall_nat.sql -e "s/{{REPLACE_WITH_GENERATED_SQL}}/$SQL_FRAGMENT/"
#mkdir -p /data/data/org.ethack.orwall/databases
#/system/xbin/sqlite3 /data/data/org.ethack.orwall/databases/nat.s3db < $MISC_DIR/org.ethack.orwall_nat.sql
#
## Fix permissions for all apps
#for APP in ${APPS[@]}
#do
#  PKG_LINE=$( $CAT /data/system/packages.xml | $EGREP "^[ ]*<package.*serId" | $GREP -v framework-res.apk | $GREP -v com.htc.resources.apk | $GREP -i $APP )
#  APP_UID=$( $ECHO $PKG_LINE | $SED 's%.*serId="\(.*\)".*%\1%' |  $CUT -d '"' -f1)
#  echo "Fixup for app $APP uid $APP_UID: " >> /sdcard/init.log
#  $FIND /data/data/$APP -type d -exec $CHOWN $APP_UID:$APP_UID {} \;
#  $FIND /data/data/$APP -type d -exec $CHMOD 0771 {} \;
#  $FIND /data/data/$APP -type f -exec $CHOWN $APP_UID:$APP_UID {} \;
#  $FIND /data/data/$APP -type f -exec $CHMOD 0660 {} \;
#done

# Remove setup MISC_DIR
rm -rf $MISC_DIR

# Remove self
rm $0 >> /sdcard/init.log


$LOG "Finished MIA init script: $0"
