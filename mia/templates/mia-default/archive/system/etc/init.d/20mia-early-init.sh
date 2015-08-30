#!/system/bin/sh
# Call mia-early-init.sh if present in /data/local.
# @see https://github.com/CyanogenMod/android_vendor_cm/blob/cm-12.1/prebuilt/common/etc/init.d/90userinit

LOG="log -p I -t MIA"
$LOG "Running MIA init script: $0"
$LOG "Environment PATH variable: ${PATH}"


INIT_SCRIPT="/data/local/mia-early-init.sh"
if [ -e ${INIT_SCRIPT} ];
then
  $LOG "Executing ${INIT_SCRIPT}";
  logwrapper /system/bin/sh ${INIT_SCRIPT};
  setprop cm.mia.early_init 1;
  $LOG "Finished executing ${INIT_SCRIPT}";
fi;
