"""
Install MIA custom ROM to a device (real or emulated).

Usage:
    mia install [--build] [--emulator] [--no-reboot] [--push-only]
                [--skip-os] <definition>
    mia install --help

Command options:
    --build      Build the definition before installing it.
    --emulator   Use running emulator instead of a real device.
    --no-reboot  Do not reboot the device once all the files are in place.
    --push-only  Only push the OS and update zips.
    --skip-os    Do not push base OS zip. \
                 NOTE: A prior push is required for a successful install.


"""

import os
import sys

# Import custom helpers.
from mia.commands import Build
from mia.helpers.android import MiaAndroid
from mia.helpers.utils import MiaHandler


class Install(object):
    def __init__(self):
        # Get the MIA handler singleton.
        self.handler = MiaHandler()

    def main(self):
        # @TODO: Make sure build is successful before running the installer.
        if self.handler.args['--build']:
            Build.main()

        # Create the builds folder.
        update_zip_name = '%s.%s' % (self.handler.args['<definition>'], 'mia-update.zip')
        update_zip_path = os.path.join(self.handler.get_workspace_path(), 'builds', update_zip_name)

        if not os.path.isfile(update_zip_path):
            print('ERROR: Please run the build command first.')
            sys.exit(1)

        # Get the OS file name.
        os_zip_name = self.handler.get_os_zip_filename()
        os_zip_path = os.path.join(self.handler.get_workspace_path(), 'resources', os_zip_name)

        if not os.path.isfile(os_zip_path):
            print('ERROR: OS archive not found.')
            sys.exit(1)

        # Get the android device wrapper.
        android = MiaAndroid()

        # Push the mia-update.zip to the device.
        android.push_file_to_device('update archive', update_zip_path, '/sdcard/mia-update.zip')

        # Push the mia-os.zip to the device.
        if not self.handler.args['--skip-os']:
            android.push_file_to_device('OS archive', os_zip_path, '/sdcard/mia-os.zip')

        if self.handler.args['--push-only']:
            print('\n' + 'Finished pushing the files onto the device.')
            sys.exit(0)

        # Set the openrecoveryscript.
        android.set_open_recovery_script()

        if not self.handler.args['--no-reboot']:
            print('\n' + 'Rebooting the device into recovery...')
            android.reboot_device('recovery')
