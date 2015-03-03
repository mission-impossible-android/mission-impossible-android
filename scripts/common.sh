#!/usr/bin/env bash

# Check device type via `ro.product.device`
# Examples: mako, flo, etc.

function connect_adb()
{
  adb start-server
}

function get_device_name()
{
  connect_adb
  # Note: Whitespace character \r was causing odd formatting.
  local device_name=`adb shell getprop ro.product.device | tr -d "\r"`
  [[ -z "$device_name" ]] && device_name='DEVICE_CODENAME'
  echo "$device_name"
}

function get_download_filename()
# Usage get_download_filename <com.org.app> [ <path/to/index.xml> ]
{
  APP=$1
  INDEX_FILE=${2:-index.xml}
  echo $(xpath -q -e "//application[@id='$APP']/package[1]/apkname/text()" $INDEX_FILE)
}


# Populates an asociative array with the values read from an INI file.
#
# To read settings from a particular file and section you first need to declare
# a global associative array in wich to store the values:
#
# Usage:
# > source $current_dir/common.sh
# > declare -A SETTINGS_GENERAL
# > get_settings_section settings.ini apps SETTINGS_GENERAL
function get_settings_section()
{
  # Test if a settings file has been provided.
  if [ "x${1}x" == 'xx' ]
  then
    echo "ERROR: Please provide a settings file!"
    return
  fi

  # Test if a settings file exists.
  local settings_file=$(readlink --canonicalize-existing --zero $1)
  if [ "x${settings_file}x" == 'xx' ] || [ ! -r $settings_file ]
  then
    echo "ERROR: Configuration file not found or could not be read!"
    return
  fi

  # Test if a settings section has been provided.
  if [ "x${2}x" == 'xx' ]
  then
    echo "ERROR: Please provide a settings file section!"
    return
  fi

  # Get the settings section.
  local section_name=$2

  # Test if a settings section has been provided.
  if [ "x${3}x" == 'xx' ]
  then
    echo "ERROR: Please provide a variable to store the settings!"
    return
  fi

  # Read section entry strings into an array.
  local section_entries=($(
    # Read the file contents.
    cat $settings_file |
    # Strip out the comments
    sed -e "s/;.*$//" |
    # Get only content from the requested section.
    sed --quiet -e "/^\[$section_name\]/,/^\s*\[/{/^[^;].*\=.*/p;}" |
    # Remove spaces around the equal sign.
    sed -e 's/[[:space:]]*\=[[:space:]]*/=/g' |
    # Remove preceding spaces.
    sed -e 's/^[[:space:]]*//' |
    # Remove trailing spaces.
    sed -e 's/[[:space:]]*$//'
  ))

  # Get the number of entries in the section.
  local entries_count=${#section_entries[@]}

  for (( i=0; i<${entries_count}; i++ ));
  do
    local entry=${section_entries[$i]}

    # Get the key and value.
    local entry_key=${entry%%=*}
    local entry_value=${entry#*=}

    # Populate the provided global variable.
    eval $3[$entry_key]=$entry_value
  done
}


# Returns the apk name for a specific version of an application.
#
# Usage:
# > source $current_dir/common.sh
# > declare -A SETTINGS_GENERAL
# > get_app_latest_apkname ./fdroid-index.xml com.fsck.k9 22002
get_app_apkname()
{
  INDEX_FILE=$1
  APP_NAME=$2
  APP_VERSION=$3

  # openSUSE has a different version of xpath.
  OSNAME=`grep -i opensuse /etc/issue | sed 's/.*\(opensuse\).*/\1/i'`

  case $OSNAME in
    'openSUSE')
      if [ $APP_VERSION == 'latest' ]; then
        echo $(xpath $INDEX_FILE "//application[@id='$APP_NAME']/package[1]/apkname/text()" 2>/dev/null)
      else
        # @see http://stackoverflow.com/questions/912194/matching-a-node-based-on-a-siblings-value-with-xpath
        echo $(xpath $INDEX_FILE "//application[@id='$APP_NAME']/package/apkname/text()[../../versioncode/text() = $APP_VERSION]" 2>/dev/null)
      fi
      ;;
    *)
      if [ $APP_VERSION == 'latest' ]; then
        echo $(xpath -q -e "//application[@id='$APP_NAME']/package[1]/apkname/text()" $INDEX_FILE)
      else
        # @see http://stackoverflow.com/questions/912194/matching-a-node-based-on-a-siblings-value-with-xpath
        echo $(xpath -q -e "//application[@id='$APP_NAME']/package/apkname/text()[../../versioncode/text() = $APP_VERSION]" $INDEX_FILE)
      fi
      ;;
  esac
}
