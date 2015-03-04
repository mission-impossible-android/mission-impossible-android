#!/usr/bin/env bash

if [ -z `command -v xpath` ]; then
  echo "ERROR: xpath not found!"
  exit
fi

if [ -z `command -v wget` ]; then
  echo "ERROR: wget not found!"
  exit
fi

WGET_COMMAND="wget --no-verbose --continue"
# For debug purposes use:
# WGET_COMMAND="echo wget --no-verbose --continue"
XARGS_COMMAND="xargs --max-args=1 --max-procs=8"

echo ""
echo "Downloading the F-Droid repository information."
$WGET_COMMAND --output-document=assets/fdroid-index.xml https://f-droid.org/repo/index.xml

current_dir="$(dirname "$0")"
BASEDIR=$(readlink -e pkg)
source $current_dir/common.sh

# Read the general settings.
declare -A GENERAL_SETTINGS
get_settings_section settings.ini general GENERAL_SETTINGS


# Get a list of APKs to download.
declare -A BASE_APPS
get_settings_section settings.ini apps BASE_APPS

# Create local directory to store the APKs.
mkdir -p "${BASEDIR}${GENERAL_SETTINGS[system_app_destination]}"

# Download the APKs.
echo ""
for APP_NAME in "${!BASE_APPS[@]}"
do
  echo "Downloading ${APP_NAME} APK..."
  APK_URI="${BASE_APPS[$APP_NAME]}"
  output_document="--output-document=${BASEDIR}${GENERAL_SETTINGS[system_app_destination]}/"`basename $APK_URI`
  $WGET_COMMAND $output_document $APK_URI
  echo ""
done


# Get a list of applications to download from F-Droid.
declare -A FDROID_APPS
get_settings_section settings.ini fdroid_apps FDROID_APPS

# Create local directory to store the APKs.
mkdir -p "${BASEDIR}${GENERAL_SETTINGS[user_app_destination]}"

FDROID_XML=$(readlink -e "${BASEDIR}/../assets/fdroid-index.xml")

# Prepare a list of APKs to download.
declare -a APK_FILES_LIST
for APP_NAME in "${!FDROID_APPS[@]}"
do
  APP_VERSION="${FDROID_APPS[$APP_NAME]}"
  echo "Adding $APP_NAME [$APP_VERSION] to download queue."

  # Test if a settings section has been provided.
  APK_NAME=
  if [ "x${APP_VERSION}x" == 'xlatestx' ]; then
    echo " - Trying to determine the latest $APP_NAME version and APK file."
    APK_NAME=$(get_app_apkname $FDROID_XML $APP_NAME $APP_VERSION)

    if [ "x${APK_NAME}x" == 'xx' ]; then
      echo "ERROR: Could not determine latest version APK file for $APP_NAME"
      exit 1;
    fi
  else
    echo " - Trying to determine the $APP_NAME APK file for version $APP_VERSION."
    APK_NAME=$(get_app_apkname $FDROID_XML $APP_NAME $APP_VERSION)

    if [ "x${APK_NAME}x" == 'xx' ]; then
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
DEST_DIR="${BASEDIR}${GENERAL_SETTINGS[user_app_destination]}"

echo "Downloading ${#APK_FILES_LIST[@]} F-Droid packages..."
echo " - This is in parallel, but may still take awhile."
echo " - Partially downloaded files will be resumed."
printf "%s\n" "${APK_FILES_LIST[@]}" | $XARGS_COMMAND -I{} \
   $WGET_COMMAND --output-document=${DEST_DIR}/{} https://f-droid.org/repo/{}

echo ""
echo "All packages have been downloaded!"
