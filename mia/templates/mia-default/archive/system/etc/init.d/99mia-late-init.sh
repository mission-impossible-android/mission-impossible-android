#!/system/bin/sh
# Call mia-late-init.sh if present in /data/local.
# @see https://github.com/CyanogenMod/android_vendor_cm/blob/cm-12.1/prebuilt/common/etc/init.d/90userinit

LOG="log -p I -t MIA"
$LOG "Running MIA init script: $0"
$LOG "Environment PATH variable: ${PATH}"


INIT_SCRIPT="/data/local/mia-late-init.sh"

# Helper commands.
GREP="busybox grep"
PS="busybox ps"

# Search for active process.
ps_grep () {
  # Make sure the search down't show up.
  $PS | $GREP "$@" | $GREP -v "$(echo $GREP $@)"
}

fb_logger() {
  echo $(date): $1 >> /data/local/tmp/mia-late-init.log
}

# Install apps on first boot after system services have started.
TIMEOUT=5
if [ -e ${INIT_SCRIPT} ]; then
  fb_logger "FirstBoot script found ${INIT_SCRIPT}"

  # TODO: Find a way to prevent race conditions.
  fb_logger "Waiting for com.android.systemui..."
  while : ; do
    # Check if the system is up and running.andro
    if ps_grep com.android.systemui; then
      fb_logger "com.android.systemui is up and running!"
      busybox sleep ${TIMEOUT}

      # Run the First Boot script.

      fb_logger "Running FirstBoot init.."
      $LOG "Executing ${INIT_SCRIPT}";
      logwrapper /system/bin/sh ${INIT_SCRIPT}
      setprop cm.mia.late_init 1;
      $LOG "Finished executing ${INIT_SCRIPT}";
      fb_logger "Finished!"

      # Exit the loop.
      break
    fi

    fb_logger "Waiting, next try in ${TIMEOUT}s."
    busybox sleep ${TIMEOUT}
  done
fi
