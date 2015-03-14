#!/usr/bin/env bash

if [ -z `command -v xpath` ]; then
  echo "ERROR: xpath not found!"
  exit
fi

if [ -z `command -v wget` ]; then
  echo "ERROR: wget not found!"
  exit
fi

if [ -z "$1" ]
then
  echo "Error: You did not pass an definition name."
  exit 1
fi

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

WGET_COMMAND="wget --no-verbose --continue"
# For debug purposes use:
# WGET_COMMAND="echo wget --no-verbose --continue"
XARGS_COMMAND="xargs --max-args=1 --max-procs=8"

echo # Move to a new line.
echo "Downloading the F-Droid repository information."
$WGET_COMMAND --output-document=resources/fdroid-index.xml https://f-droid.org/repo/index.xml

# Read the general settings.
declare -A GENERAL_SETTINGS
SETTINGS_FILE="${DEFINITION_DIR}/settings.ini"
get_settings_section $SETTINGS_FILE general GENERAL_SETTINGS


# Get a list of APKs to download.
declare -A BASE_APPS
get_settings_section $SETTINGS_FILE apps BASE_APPS

# Create local directory to store the APKs.
mkdir -p "${DEFINITION_DIR}${GENERAL_SETTINGS[system_app_destination]}"

# Download the APKs.
echo # Move to a new line.
for APP_NAME in "${!BASE_APPS[@]}"
do
  echo "Downloading ${APP_NAME} APK..."
  APK_URI="${BASE_APPS[$APP_NAME]}"
  output_document="--output-document=${DEFINITION_DIR}${GENERAL_SETTINGS[system_app_destination]}/"`basename $APK_URI`
  $WGET_COMMAND $output_document $APK_URI
  echo ""
done


# Get a list of applications to download from F-Droid.
declare -A FDROID_APPS
get_settings_section $SETTINGS_FILE fdroid_apps FDROID_APPS

# Create local directory to store the APKs.
mkdir -p "${DEFINITION_DIR}${GENERAL_SETTINGS[user_app_destination]}"

FDROID_XML=$(readlink -e "${BASE_DIR}/resources/fdroid-index.xml")

# Prepare a list of APKs to download.
declare -a APK_FILES_LIST
for APP_NAME in "${!FDROID_APPS[@]}"
do
  APP_VERSION="${FDROID_APPS[$APP_NAME]}"
  echo "Adding $APP_NAME [$APP_VERSION] to download queue."

  # Test if a settings section has been provided.
  APK_NAME=
  if [ "$APP_VERSION" == 'latest' ]; then
    echo " - Trying to determine the latest $APP_NAME version and APK file."
    APK_NAME=$(get_app_apkname $FDROID_XML $APP_NAME $APP_VERSION)

    if [ -z "$APK_NAME" ]; then
      echo "ERROR: Could not determine latest version APK file for $APP_NAME"
      exit 1;
    fi
  else
    echo " - Trying to determine the $APP_NAME APK file for version $APP_VERSION."
    # APK_NAME=$()
    echo get_app_apkname $FDROID_XML $APP_NAME $APP_VERSION
    APK_NAME=$(get_app_apkname $FDROID_XML $APP_NAME $APP_VERSION)

    if [ -z "$APK_NAME" ]; then
      echo "ERROR: Could not determine the APK file for $APP_NAME version $APP_VERSION"
      exit 1;
    fi
  fi

  # Add to the list of determined files.
  echo " - Using: https://f-droid.org/repo/$APK_NAME"
  APK_FILES_LIST+=("$APK_NAME")
  echo ""
done

# The download destination directory.
DEST_DIR="${DEFINITION_DIR}${GENERAL_SETTINGS[user_app_destination]}"

echo # Move to a new line.
echo "Downloading ${#APK_FILES_LIST[@]} F-Droid packages..."
echo " - This is in parallel, but may still take awhile."
echo " - Partially downloaded files will be resumed."
printf "%s\n" "${APK_FILES_LIST[@]}" | $XARGS_COMMAND -I{} \
   $WGET_COMMAND --output-document=${DEST_DIR}/{} https://f-droid.org/repo/{}

echo ""
echo "All packages have been downloaded!"
