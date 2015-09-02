#!/system/bin/sh
# One time script to fix installed APP permissions and prepare the OS.
# TODO: Encrypt the user data on FirstBoot; @see GH-104
# TODO: Find a way to set the time zone.

# Based on:
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

MISC_DIR="/sdcard/misc"
FB_LOG="/sdcard/mia-firstboot.log"

# Load helper functions.
source $MISC_DIR/library.sh

# TODO: Use system log instead of a simple file?!?
fb_logger() {
  echo $(date +%s): $1 >> $FB_LOG
}
fb_logger "Running script: $0"


# Programs needed
ECHO="busybox echo"
GREP="busybox grep"
EGREP="busybox egrep"
CAT="busybox cat"
CHOWN="busybox chown"
CHMOD="busybox chmod"
CUT="busybox cut"
FIND="busybox find"
SED="busybox sed"

# Get important UIDs for later
BROWSER_UID=$(get_app_uid $BROWSER_APP)
SIP_UID=$(get_app_uid $SIP_APP)
ORWALL_UID=$(get_app_uid $ORWALL_APP)

# Fix orwall's config UIDs
fb_logger "Updating UIDs in the orwall preferences file."
$SED -i /data/data/org.ethack.orwall/shared_prefs/org.ethack.orwall_preferences.xml -e "s/REPLACE_WITH_BROWSER_UID/$BROWSER_UID/"
$SED -i /data/data/org.ethack.orwall/shared_prefs/org.ethack.orwall_preferences.xml -e "s/REPLACE_WITH_SIP_UID/$SIP_UID/"

# Give OrWall full, permanent root access
fb_logger "Importing Superuser database with orWall uid $APP_UID pre-authorized."
mkdir -p /data/data/com.android.settings/databases
$SED -i $MISC_DIR/com.android.settings_su.sql -e "s/REPLACE_WITH_ORWALL_UID/$ORWALL_UID/"
/system/xbin/sqlite3 /data/data/com.android.settings/databases/su.sqlite < $MISC_DIR/com.android.settings_su.sql

ORWALL_APP_DATA="${MISC_DIR}/app-list-orwall.txt"
fb_logger "Generating SQL to populate the orWall NAT database."
fb_logger "Using app data from file: ${ORWALL_APP_DATA}."
SQL_FRAGMENT=""
while read APP_DATA; do
  APP_NAME=$(echo $APP_DATA | $CUT -f'1' -d':')
  APP_UID=$(get_app_uid $APP_NAME)
  fb_logger "- preparing SQL for ${APP_NAME}; uid: ${APP_UID}"

  APP_PORT_TYPE=$(echo $APP_DATA | $CUT -f'2' -d':')
  APP_PORT_TYPE=${APP_PORT_TYPE:-TransProxy} # Default port type
  SQL_LINE="INSERT INTO rules VALUES($APP_UID,'$APP_NAME','Tor',9040,'$APP_PORT_TYPE');"
  SQL_FRAGMENT="$SQL_LINE\n$SQL_FRAGMENT"
done < ${ORWALL_APP_DATA}

fb_logger "Updating the orWall NAT database."
$SED -i $MISC_DIR/org.ethack.orwall_nat.sql -e "s/{{REPLACE_WITH_GENERATED_SQL}}/$SQL_FRAGMENT/"
mkdir -p /data/data/org.ethack.orwall/databases
/system/xbin/sqlite3 /data/data/org.ethack.orwall/databases/nat.s3db < $MISC_DIR/org.ethack.orwall_nat.sql

fb_logger "Fix application data owner and group:"
for APP in ${APPS[@]}
do
  PKG_LINE=$( $CAT /data/system/packages.xml | $EGREP "^[ ]*<package.*serId" | $GREP -v framework-res.apk | $GREP -v com.htc.resources.apk | $GREP -i $APP )
  APP_UID=$( $ECHO $PKG_LINE | $SED 's%.*serId="\(.*\)".*%\1%' |  $CUT -d '"' -f1)
  fb_logger "- fixing ownership of ${APP}; uid: ${APP_UID}"
  $FIND /data/data/$APP -type d -exec $CHOWN $APP_UID:$APP_UID {} \;
  $FIND /data/data/$APP -type d -exec $CHMOD 0771 {} \;
  $FIND /data/data/$APP -type f -exec $CHOWN $APP_UID:$APP_UID {} \;
  $FIND /data/data/$APP -type f -exec $CHMOD 0660 {} \;
done

fb_logger "Settings.Secure.ADB_ENABLED -- Disable ADB by default."
# NOTE: This does not prevent the system from asking to authorize the connection.
/system/bin/settings put global adb_enabled 0

fb_logger "Settings.Secure.LOCATION_PROVIDERS_ALLOWED -- Limit the list of location providers that activities may access."
/system/bin/settings put secure location_providers_allowed ''

fb_logger "Settings.Global.AUTO_TIME -- Do not update the date, time and time zone automatically from the network (NITZ)."
/system/bin/settings put global auto_time 0

# GH-94: Enable Airplane Mode and broadcast the event.
fb_logger "Settings.Global.AIRPLANE_MODE_ON -- Enable Airplane Mode and broadcast the event."
/system/bin/settings put global airplane_mode_on 1
/system/bin/am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true

fb_logger "Change hostname for subsequent reboots."
/system/bin/settings put secure device_hostname "localhost"

fb_logger "Change hostname for current boot."
setprop net.hostname localhost
echo localhost > /proc/sys/kernel/hostname

# The Tor binary does not start until RECEIVE_BOOT_COMPLETED is broadcast. We
# need the supporting data files created in the org.torproject.android
# directory prior to that.  Starting this service happens to check for these
# directories and generate them if missing (which they are on first boot).
#
# This is a hack, and race conditions might occur if the mia-firstboot.sh script gets to long.
am startservice org.torproject.android/org.torproject.android.service.TorService

# Fake BOOT_COMPLETE to force orwall to apply rules in background.
# TODO: Investigate why this doesn't happen on its own.
am broadcast -a android.intent.action.BOOT_COMPLETED -n org.ethack.orwall/.BootBroadcast

fb_logger "Remove setup directory: ${MISC_DIR}"
rm -rf $MISC_DIR


# We want this FirstBoot script to run only once.
fb_logger "Finished running script: $0"