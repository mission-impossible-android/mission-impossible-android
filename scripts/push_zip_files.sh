#!/usr/bin/env bash

CURRENT_DIR="$(dirname "$0")"
source $CURRENT_DIR/common.sh
BASE_DIR=$(readlink -e "${CURRENT_DIR}/..")

DEFINITION=$1
DEFINITION_DIR="${BASE_DIR}/definitions/${DEFINITION}"
if [ ! -d $DEFINITION_DIR ]; then
  echo "ERROR: definition not found!"
  exit
fi
echo "The definition found at:"
echo " - ${DEFINITION_DIR}"

ZIP=$2
if [ "$ZIP" != "cm" ] && [ "$ZIP" != "update" ]; then
  echo "ERROR: ZIP must must be either 'cm' or 'update'."
  exit
fi

# Read the general settings.
declare -A GENERAL_SETTINGS
SETTINGS_FILE="${DEFINITION_DIR}/settings.ini"
get_settings_section $SETTINGS_FILE general GENERAL_SETTINGS

cm_device_name=
if [ ! -z "${GENERAL_SETTINGS[cm_device_name]}" ]; then
  cm_device_name=${GENERAL_SETTINGS[cm_device_name]}
else
  echo "Attach your device with debug enabled, unlock and allow USB debugging."
  echo "NOTE: You can also add a 'cm_device_name' entry in the settings file."
  read -p "Press enter to continue." -r
  connect_adb

  echo # Move to a new line.
  echo "Trying to detect the device_name... If stuck press CTRL+C to cancel"
  echo "And test if the device is online by running 'adb devices -l'"
  cm_device_name=$(get_cm_device_name 2>/dev/null)
fi
echo "Device name: $cm_device_name"

cm_release_version="M12"
if [ ! -z "${GENERAL_SETTINGS[cm_release_version]}" ]; then
  cm_release_version=${GENERAL_SETTINGS[cm_release_version]}
fi

cm_release_type="snapshot"
if [ ! -z "${GENERAL_SETTINGS[cm_release_type]}" ]; then
  cm_release_type=${GENERAL_SETTINGS[cm_release_type]}
fi

if [ "$ZIP" == "cm" ]; then
  ZIP_FILE_PATH="${BASE_DIR}/resources/cm-11-${cm_release_type}-${cm_release_version}-${cm_device_name}.zip"
elif [ "$ZIP" == "update" ]; then
  ZIP_FILE_PATH="${BASE_DIR}/build/${DEFINITION}/mia-update.zip"
fi

echo # Move to a new line.
echo "Pushing file to /sdcard:"
echo " - $ZIP_FILE_PATH"
adb push $ZIP_FILE_PATH /sdcard/
