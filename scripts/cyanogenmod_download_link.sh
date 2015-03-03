#!/usr/bin/env bash

current_dir="$(dirname "$0")"
BASEDIR=$(readlink -e pkg)
source $current_dir/common.sh

# Read the general settings.
declare -A GENERAL_SETTINGS
get_settings_section settings.ini general GENERAL_SETTINGS

# Prepare variables.
snapshot_version="${GENERAL_SETTINGS[snapshot_version]}"
device_name=`get_device_name`

# if (isNexus)
echo "--- Please download the snapshot (${snapshot_version} recommended) from this page:"
echo "    https://download.cyanogenmod.org/?device=${device_name}&type=snapshot"
echo
echo "--- Remember to verify the file's provided MD5 checksum against the ouput of this local command:"
echo "     ~$ md5sum path/to/cm-11-<TIMESTAMP>-SNAPSHOT-${snapshot_version}-${device_name}.zip"
echo
echo "When you are done:"
echo "     ~$ mv path/to/cm-11-<TIMESTAMP>-SNAPSHOT-${snapshot_version}-${device_name}.zip assets/cm-11.zip"
