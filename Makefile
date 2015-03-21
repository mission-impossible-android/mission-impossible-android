
# Display readme for the default make target.
info:
	cat README.md

# make DEFINITION=my-phone push_emulator
push_emulator:
	echo "Pushing MIA update to device"
	adb -e push build/mia-$(DEFINITION)-update.zip /sdcard/

# make DEFINITION=my-phone push_update_zip
push_update_zip:
	echo "Pushing update zip to device"
	scripts/push_zip_files.sh $(DEFINITION) update

# make DEFINITION=my-phone push_cm_zip
push_cm_zip:
	echo "Pushing CM to device"
	scripts/push_zip_files.sh $(DEFINITION) cm

# make DEFINITION=my-phone set_openrecoveryscript
set_openrecoveryscript:
	echo "Pushing openrecoveryscript to device"
	definitions/$(DEFINITION)/scripts/OpenRecovery

	adb push definitions/$(DEFINITION)/scripts/OpenRecovery /sdcard/openrecoveryscript
	adb shell "su root cp /sdcard/openrecoveryscript /cache/recovery/"

# make DEFINITION=my-phone update_orwall_init
update_orwall_init:
	rm definitions/$(DEFINITION)/system/etc/init.d/*
	(cd definitions/$(DEFINITION)/system/etc/init.d && wget https://raw.githubusercontent.com/EthACKdotOrg/orWall/master/app/src/main/res/raw/userinit.sh ---output-document=91firewall)

# make DEFINITION=my-phone build_deploy
build_deploy: push_cm_zip push_update_zip set_openrecoveryscript
	adb reboot recovery
