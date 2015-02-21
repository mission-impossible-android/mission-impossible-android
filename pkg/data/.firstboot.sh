#!/system/bin/sh
# One time fixup script to fix installed APP permissions

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

# Fix orwall's config UIDs
BROWSER_UID=$( $CAT /data/system/packages.xml | $EGREP "^[ ]*<package.*serId" | $GREP -v framework-res.apk | $GREP -v com.htc.resources.apk | $GREP -i $BROWSER_APP | $SED 's%.*serId="\(.*\)".*%\1%' |  $CUT -d '"' -f1) 
SIP_UID=$( $CAT /data/system/packages.xml | $EGREP "^[ ]*<package.*serId" | $GREP -v framework-res.apk | $GREP -v com.htc.resources.apk | $GREP -i $SIP_APP | $SED 's%.*serId="\(.*\)".*%\1%' |  $CUT -d '"' -f1)

$SED -i /data/data/org.ethack.orwall/shared_prefs/org.ethack.orwall_preferences.xml -e "s/REPLACE_WITH_BROWSER_UID/$BROWSER_UID/"
$SED -i /data/data/org.ethack.orwall/shared_prefs/org.ethack.orwall_preferences.xml -e "s/REPLACE_WITH_SIP_UID/$SIP_UID/"

# Fix permissions for all apps
for APP in ${APPS[@]}
do
  PKG_LINE=$( $CAT /data/system/packages.xml | $EGREP "^[ ]*<package.*serId" | $GREP -v framework-res.apk | $GREP -v com.htc.resources.apk | $GREP -i $APP )
  APP_UID=$( $ECHO $PKG_LINE | $SED 's%.*serId="\(.*\)".*%\1%' |  $CUT -d '"' -f1)
  echo "Fixup for app $APP uid $APP_UID: " >> /sdcard/init.log
  $FIND /data/data/$APP -type d -exec $CHOWN $APP_UID:$APP_UID {} \;
  $FIND /data/data/$APP -type d -exec $CHMOD 0771 {} \;
  $FIND /data/data/$APP -type f -exec $CHOWN $APP_UID:$APP_UID {} \;
  $FIND /data/data/$APP -type f -exec $CHMOD 0660 {} \;
done

# XXX: enablecrypto?? Seems to fail?
#/system/bin/vdc cryptfs enablecrypto inplace thisisapassword

rm $0 >> /sdcard/init.log
