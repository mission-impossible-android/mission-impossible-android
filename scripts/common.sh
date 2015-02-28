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
  # The 'ro.product.device' property isn't very reliable.
  # Note: Whitespace character \r was causing odd formatting.
  local device_name=`adb shell getprop ro.cm.device | tr -d "\r"`
  [[ -z "$device_name" ]] && device_name=`adb shell getprop ro.product.device | tr -d "\r"`
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
