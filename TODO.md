
## Tools:
- Use as few libraries and dependencies as possible; switch settings from YAML?
- Add `--update` option to the `definition lock` command. This will update a new
  version of the repository index file and check the locked APKs for updates.
- Implement update_orwall_init definition sub-command
    wget https://raw.githubusercontent.com/EthACKdotOrg/orWall/master/app/src/main/res/raw/userinit.sh ---output-document=91firewall


## Android:
- Try to mount system rw when changing with settings binary.
- move custom adb shell command with captured exit codes into custom script
- test if `su` command is available before attempting deploy
- Find out why `location_providers_allowed` gets set to GPS on first
  boot.
- Turn off `assisted_gps_location`?
      https://en.wikipedia.org/wiki/Assisted_GPS

- Add wizard for setting numeric pin and encrypting with long password.
- Figure out why setting device_hostname isn't working.
- why is owner information not on lock screen?
- allow fdroid access from beginning

### MyAppList
  - Create app lists for downloading certain tools. 
  - Seems to be unable to read this list...

### Orwall:
  - Set OrWall config to use Fennec for the Browser app and CSIPSimple for SIP.
  - Extract 90firewall from local orwall apk?
