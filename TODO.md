
## Tools:
*   Add `--update` option to the `definition lock` command. This will update a new
    version of the repository index file and check the locked APKs for updates.
*   Implement update_orwall_init definition sub-command

    ```
    # Download from the EthACKdotOrg/orWall repo
    wget https://raw.githubusercontent.com/EthACKdotOrg/orWall/master/app/src/main/res/raw/userinit.sh ---output-document=91firewall
    # or extract 91firewall from local orwall apk?
    ```


## Android:
*   Try to mount system rw when changing with settings binary.
*   Find out why `location_providers_allowed` gets set to GPS on first
    boot.
*   Turn off `assisted_gps_location`? https://en.wikipedia.org/wiki/Assisted_GPS
*   Figure out why setting device_hostname isn't working.
*   why is owner information not on lock screen?
