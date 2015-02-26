#!/usr/bin/env bash

current_dir="$(dirname "$0")"
source $current_dir/common.sh

BASEDIR=$(readlink -e pkg)

# Convert file listing download filenames to array.
apk_files=()
i=0
while read filename; do
  apk_files[i]=$filename
  i=$(($i + 1))
done < $BASEDIR/misc/preinstalled.list.lock

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
