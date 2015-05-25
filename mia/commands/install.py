"""
Install MIA custom ROM to a device (real or emulated).

Usage:
    mia install [--build] [--emulator] [--no-reboot] [--push-only] [--skip-os] <definition>
    mia install --help

Command options:
    --build      Build the definition before installing it.
    --emulator   Use running emulator instead of a real device.
    --no-reboot  Do not reboot the device once all the files are in place.
    --push-only  Only push the OS and update zips.
    --skip-os    Do not push the OS zip file (again). Install the existing one.

Notes:
  * A prior push is required when using `--skip-os` for a successful install.


"""

import os
import sys

# Import custom helpers.
from mia.commands import available_commands, Build
from mia.android import MiaAndroid
from mia.handler import MiaHandler


class Install(object):
    @staticmethod
    def main():
        # TODO: Make sure build is successful before running the installer.
        if MiaHandler.args['--build']:
            build_command_handler = Build()
            build_command_handler.main()

        # Create the builds folder.
        update_zip_name = '%s.%s' % (MiaHandler.args['<definition>'], 'mia-update.zip')
        update_zip_path = os.path.join(MiaHandler.get_workspace_path(), 'builds', update_zip_name)

        if not os.path.isfile(update_zip_path):
            print('ERROR: Please run the build command first.')
            sys.exit(1)

        # Get the OS file name.
        os_zip_name = MiaHandler.get_os_zip_filename()
        os_zip_path = os.path.join(MiaHandler.get_workspace_path(), 'resources', os_zip_name)

        if not os.path.isfile(os_zip_path):
            print('ERROR: OS archive not found.')
            sys.exit(1)

        # Get the android device wrapper.
        android = MiaAndroid()

        # Push the mia-update.zip to the device.
        android.push_file_to_device('update archive', update_zip_path, '/sdcard/mia-update.zip')

        # Push the mia-os.zip to the device.
        if not MiaHandler.args['--skip-os']:
            android.push_file_to_device('OS archive', os_zip_path, '/sdcard/mia-os.zip')

        if MiaHandler.args['--push-only']:
            print('\n' + 'Finished pushing the files onto the device.')
            sys.exit(0)

        # Set the openrecoveryscript.
        android.set_open_recovery_script()

        if not MiaHandler.args['--no-reboot']:
            print('\n' + 'Rebooting the device into recovery...')
            android.reboot_device('recovery')

# Add command to the list of available commands.
available_commands['install'] = {
    'class': Install,
    'help': __doc__,
}
