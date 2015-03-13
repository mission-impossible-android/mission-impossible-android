
TODO: Add description of how things work.

## Folders list

`init.d`:
  This folder will be copied to `/system/etc/init.d` in the generated update.zip
  and it will end up in the phone at the same location.

`META-INF`:
  This folder will be copied to the root of the generated update.zip.

`misc`:
  This folder will be copied to `/sdcard`

`system-lib`:
  The contents of this folder will be copied to `/system/lib` in the generated
  update.zip and it will end up in the phone at the same location.

`user-data`:
  The contents of this folder will be copied to `/data/data` in the generated
  update.zip and it will end up in the phone at the same location.

## Files list

`scripts/OpenRecovery`:
  The [OpenRecoveryScript](http://www.teamw.in/OpenRecoveryScript) used to install CM and the Mission Impossible
  update.zip and it will be copied into the phone at `/cache/recovery/openrecoveryscript`

`scripts/updater`:
  This script will be copied to `META-INF/com/google/android/updater-script` in
  the generated update.zip.
