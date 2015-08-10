"""
Install MIA custom ROM to a device (real or emulated).

Usage:
    mia install [--emulator] [--no-reboot] [--push-only] [--skip-os] <definition>
    mia install --help

Command options:
    --emulator   Use running emulator instead of a real device.
    --no-reboot  Do not reboot the device once all the files are in place.
    --push-only  Only push the OS and update zips.
    --skip-os    Do not push the OS zip file (again). Install the existing one.

Notes:
  * For a successful install a prior push is required when using `--skip-os`.


"""

import os
import sys

# Import custom helpers.
from mia.commands import available_commands
from mia.android import MiaAndroid
from mia.handler import MiaHandler


class Install(object):
    @staticmethod
    def main():
        # Push the update archive and hash file to the device.
        Install.push_update_zip()

        if not MiaHandler.args['--skip-os']:
            # Push the OS archive and hash file to the device.
            Install.push_os_zip()

        if MiaHandler.args['--push-only']:
            print('\n' + 'Finished pushing the files onto the device.')
            sys.exit(0)

        # Set the openrecoveryscript.
        MiaAndroid.set_open_recovery_script()

        if not MiaHandler.args['--no-reboot']:
            print('\n' + 'Rebooting the device into recovery...')
            MiaAndroid.reboot_device('recovery')

    @staticmethod
    def push_os_zip():
        # Get the OS file name.
        zip_name = MiaHandler.get_os_zip_filename()
        zip_path = os.path.join(MiaHandler.get_workspace_path(), 'resources', zip_name)

        if not os.path.isfile(zip_path):
            print('ERROR: OS archive is missing:\n - %s' % zip_path)
            sys.exit(1)

        os_zip_hash_path = '.'.join((zip_path, 'md5'))
        if not os.path.isfile(os_zip_hash_path):
            print('ERROR: Hash file for the OS archive is missing.')
            sys.exit(1)

        # Push the mia-os.zip to the device.
        MiaAndroid.push_file('OS archive', zip_path, '/sdcard/mia-os.zip')
        MiaAndroid.push_hash_for_file('md5', zip_path, '/sdcard/mia-os.zip')

    @staticmethod
    def push_update_zip():
        # Create the builds folder.
        zip_name = '%s.%s' % (MiaHandler.args['<definition>'], 'mia-update.zip')
        zip_path = os.path.join(MiaHandler.get_workspace_path(), 'builds', zip_name)

        if not os.path.isfile(zip_path):
            print('ERROR: Please run the build command first.')
            sys.exit(1)

        update_zip_hash_path = '.'.join((zip_path, 'md5'))
        if not os.path.isfile(update_zip_hash_path):
            print('ERROR: Hash file for the built update archive is missing.')
            sys.exit(1)

        # Push the mia-update.zip to the device.
        MiaAndroid.push_file('update archive', zip_path, '/sdcard/mia-update.zip')
        MiaAndroid.push_hash_for_file('md5', zip_path, '/sdcard/mia-update.zip')


# Add command to the list of available commands.
available_commands['install'] = {
    'class': Install,
    'help': __doc__,
}
