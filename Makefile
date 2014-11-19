cm_dl_link:
	scripts/cyanogenmod_download_link.sh

download_apks:
	mkdir -p pkg/data/app
	mkdir -p pkg/system/app
	scripts/download_apks.sh

package:
	mkdir -p build
	(cd pkg; zip -r ../build/mission-impossible-update.zip *)

push_emulator:
	adb -e push build/mission-impossible-update.zip /sdcard/
