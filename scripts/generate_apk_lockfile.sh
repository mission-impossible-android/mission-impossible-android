#!/usr/bin/env bash

current_dir="$(dirname "$0")"
source $current_dir/common.sh

BASEDIR=$(readlink -e pkg)

APP_LIST="$BASEDIR/misc/preinstalled.list"
APP_LIST_LOCK="$BASEDIR/misc/preinstalled.list.lock"

while read APP; do
  echo "Looking up apk filename for $APP..."
  echo $(get_download_filename $APP $BASEDIR/../assets/index.xml) >> $APP_LIST_LOCK
done < $APP_LIST
