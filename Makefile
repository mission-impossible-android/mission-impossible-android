
# Display readme for the default make target.
info:
	cat README.md

# make DEFINITION=my-phone set_openrecoveryscript
set_openrecoveryscript:
	echo "Pushing openrecoveryscript to device"

	adb push definitions/$(DEFINITION)/other/openrecoveryscript /sdcard/openrecoveryscript
	adb shell "su root cp /sdcard/openrecoveryscript /cache/recovery/"

# make DEFINITION=my-phone update_orwall_init
update_orwall_init:
	rm definitions/$(DEFINITION)/system/etc/init.d/*
	(cd definitions/$(DEFINITION)/system/etc/init.d && wget https://raw.githubusercontent.com/EthACKdotOrg/orWall/master/app/src/main/res/raw/userinit.sh ---output-document=91firewall)

# make DEFINITION=my-phone build_deploy
build_deploy: set_openrecoveryscript
	adb reboot recovery
