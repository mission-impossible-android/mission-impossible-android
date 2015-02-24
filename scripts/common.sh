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
