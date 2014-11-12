download_apks:
	mkdir -p pkg/data/app
	mkdir -p pkg/system/app
	./download_apks.sh

package:
	mkdir -p build
	zip -r build/mission-impossible-update.zip *
