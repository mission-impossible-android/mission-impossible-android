#!/usr/bin/env bash

if [ -z "$1" ]; then
  echo "ERROR: Please provide a template to use."
  exit 1;
fi

if [ -z "$2" ]; then
  echo "ERROR: Please provide a name for the new definition."
  exit 1;
fi

CURRENT_DIR="$(dirname "$0")"
source $CURRENT_DIR/common.sh
BASE_DIR=$(readlink -e "${CURRENT_DIR}/..")

# Determine the template folder.
TEMPLATE=$1
TEMPLATE_DIR="${BASE_DIR}/templates/${TEMPLATE}"
if [ ! -d "$TEMPLATE_DIR" ]; then
  echo "ERROR: Template not found."
  exit 1;
fi
echo "Template found:"
echo " - ${TEMPLATE_DIR}"

# Determine the definition to create.
DEFINITION=$2
DEFINITION_DIR="${BASE_DIR}/definitions/${DEFINITION}"
echo "The definition will be created at:"
echo " - ${DEFINITION_DIR}"
mkdir -p $DEFINITION_DIR

# Create the definition.
# NOTE: dot files are not copied!
cp --recursive $TEMPLATE_DIR/* $DEFINITION_DIR
echo " - Definition has been created."

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

echo
echo "Please download the snapshot (${cm_release_version} recommended) from this page:"
echo " - Please save the downloaded file to the resources folder!"
echo "  xdg-open https://download.cyanogenmod.org/?device=${cm_device_name}&type=${cm_release_type}"
echo
echo "Download the file and verify the provided checksum against the local file:"
echo "  md5sum resources/cm-11-*-${cm_release_type}-${cm_release_version}-${cm_device_name}.zip"
echo
echo "When you are done move the downloaded file to the 'resources' folder:"
echo "  mv resources/cm-11-*-${cm_release_type}-${cm_release_version}-${cm_device_name}.zip resources/cm-11-${cm_release_type}-${cm_release_version}-${cm_device_name}.zip"
echo

# read -p "Do you want to configure the definition now?" -r
# echo # Move to a new line.
# if [[ ! $REPLY =~ ^[Yy]$ ]]
# then
#     exit 0
# fi


echo # Move to a new line.
echo "You can now customize your definition."
# @TODO: Add configuration questionnaire?
