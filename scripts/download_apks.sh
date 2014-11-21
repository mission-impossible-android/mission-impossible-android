#!/usr/bin/env bash

BASEDIR=$(readlink -e pkg)

apk_files=( \
  org.torproject.android_124.apk \
  org.ethack.orwall_33.apk \
)

echo "--- Downloading F-Droid app market APK..."
cd ${BASEDIR}/system/priv-app
wget --no-verbose --continue https://f-droid.org/repo/org.fdroid.fdroid_760.apk

echo "--- Downloading Orfox browser debug APK..."
cd ${BASEDIR}/data/app
wget --no-verbose --continue "https://guardianproject.info/builds/OrfoxFennec/latest/OrfoxFennec-debug.apk

echo "--- Downloading ${#apk_files[@]} F-Droid packages..."
echo "    This is parallel, but may still take awhile."
echo "    (Partially-downloaded files will be resumed.)"

cd ${BASEDIR}/data/app
printf "%s\n" "${apk_files[@]}" \
  | xargs --max-args=1 --max-procs=8 -i \
    wget --no-verbose --continue https://f-droid.org/repo/{}

echo "--- All packages downloaded!"
