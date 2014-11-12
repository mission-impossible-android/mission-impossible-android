download_apks:
	mkdir -p pkg/data/app
	mkdir -p pkg/system/app
	./download_apks.sh

package: download_apks
	mkdir -p build
	(cd pkg; zip -r ../build/mission-impossible-update.zip *)

push_emulator:
	adb -e push build/mission-impossible-update.zip /sdcard/
