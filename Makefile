cm_dl_link:
	scripts/cyanogenmod_download_link.sh

download_apks:
	mkdir -p pkg/data/app
	mkdir -p pkg/system/priv-app
	scripts/download_apks.sh

clean:
	rm -f pkg/*/*app/*

extract_update_binary:
	unzip -o assets/cm-11.zip META-INF/com/google/android/update-binary -d pkg

package: extract_update_binary
	mkdir -p build
	rm -f build/mission-impossible-update.zip
	(cd pkg; zip -r ../build/mission-impossible-update.zip *)

push_emulator:
	adb -e push build/mission-impossible-update.zip /sdcard/

push_update_zip: package
	adb push -p build/mission-impossible-update.zip /sdcard/

push_cm_zip:
	adb push -p assets/cm-11.zip /sdcard/cm-11.zip

set_openrecoveryscript:
	adb push -p assets/openrecoveryscript /sdcard/
	adb shell "su root cp /sdcard/openrecoveryscript /cache/recovery/"

get_app_index:
	cd assets && curl --remote-name --progress https://f-droid.org/repo/index.xml

generate_applist_lockfile:
	rm -f pkg/misc/preinstalled.list.lock
	scripts/generate_apk_lockfile.sh

update_orwall_init:
	rm pkg/system/etc/init.d/*
	(cd pkg/system/etc/init.d && wget https://raw.githubusercontent.com/EthACKdotOrg/orWall/master/app/src/main/res/raw/userinit.sh ---output-document=91firewall)

build_deploy: download_apks push_update_zip set_openrecoveryscript
	adb reboot recovery
