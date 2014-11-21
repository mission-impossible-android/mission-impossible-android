#!/usr/bin/env bash

BASEDIR=$(readlink -e pkg)

apk_files=( \
  org.torproject.android_124.apk \
  org.ethack.orwall_32.apk \
)

echo "--- Downloading F-Droid app market APK..."
cd ${BASEDIR}/system/app
wget --no-verbose --continue https://f-droid.org/repo/org.fdroid.fdroid_760.apk

echo "--- Downloading ${#apk_files[@]} F-Droid packages..."
echo "    This is parallel, but may still take awhile."
echo "    (Partially-downloaded files will be resumed.)"

cd ${BASEDIR}/data/app
printf "%s\n" "${apk_files[@]}" \
  | xargs --max-args=1 --max-procs=8 -i \
    wget --no-verbose --continue https://f-droid.org/repo/{}

echo "--- All packages downloaded!"
