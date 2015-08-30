
## The `archive` directory
This directory will be the root of the generated `mia-update.zip`.

* `/data/local/mia-firstboot.sh`:
  This simple bash script will be executed on the first boot by 
  `/system/etc/init.d/Y02firstboot`
  TODO: Rename, we don't really want hidden dot files in the archive.


## Other Files

* `other/openrecoveryscript`:
  The [OpenRecoveryScript](http://www.teamw.in/OpenRecoveryScript) is used to
  install CM and the mia-update.zip and it will be directly copied into the 
  phone at `/cache/recovery/openrecoveryscript`

* `settings.yaml`:
  This file contains a list of settings for the current definition.
