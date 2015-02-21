#!/usr/bin/env bash

BASEDIR=$(readlink -e pkg)

# FIXME: Can we get a better interface from F-Droid to get the latest apk
# version? Maybe just a symlink on their side? It's either that, or we
# write some sketch regex scraper for app URLs, which are regular
# (ex: https://f-droid.org/repository/browse/?fdid=org.ethack.orwall)
apk_files=( \
  org.torproject.android_133.apk \
  org.ethack.orwall_35.apk \
  org.nick.cryptfs.passwdmanager_1230.apk \
  com.fsck.k9_22002.apk \
  org.sufficientlysecure.keychain_31200.apk \
  net.osmand.plus_197.apk \
  com.csipsimple_2417.apk \
  com.projectsexception.myapplist.open_16.apk \
  fr.kwiatkowski.ApkTrack_1.apk \
  org.coolreader_875.apk \
  com.artifex.mupdfdemo_55.apk \
  org.mozilla.fennec_fdroid_350010.apk \
  fennec-35.0.multi.android-arm.apk \
  de.schildbach.wallet_209.apk \
  org.mariotaku.twidere_98.apk \
  com.morlunk.mumbleclient_72.apk \
  indrora.atomic_19.apk \
  com.xabber.androiddev_120.apk \
  org.videolan.vlc_10104.apk \
  org.sufficientlysecure.localcalendar_6.apk
)

echo "--- Downloading F-Droid app market APK..."
cd ${BASEDIR}/system/priv-app
wget --no-verbose --continue https://f-droid.org/repo/org.fdroid.fdroid_780.apk

echo "--- Downloading Orfox browser debug APK..."
cd ${BASEDIR}/data/app
wget --no-verbose --continue "https://guardianproject.info/builds/OrfoxFennec/latest/OrfoxFennec-debug.apk"

echo "--- Downloading ${#apk_files[@]} F-Droid packages..."
echo "    This is parallel, but may still take awhile."
echo "    (Partially-downloaded files will be resumed.)"

cd ${BASEDIR}/data/app
printf "%s\n" "${apk_files[@]}" \
  | xargs --max-args=1 --max-procs=8 -i \
    wget --no-verbose --continue https://f-droid.org/repo/{}

echo "--- All packages downloaded!"
