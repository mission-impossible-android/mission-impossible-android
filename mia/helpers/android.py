"""
Provides helper function for interfacing with devices using ADB or getting
information about the software or device.
"""

import subprocess

# Import custom helpers.
from mia.helpers.utils import *


def check_adb():
    return True


def get_cyanogenmod_codename():
    """
    Try to determine the device name.
    """
    # TODO: First check the settings.ini file inside the definition, if any.
    codename = None

    # TODO: Try to get the device name using ADB.
    if check_adb:
        print('NOTE: ADB integration not implemented yet!')

    if codename is None:
        print('Look up your device codename on the CyanogenMod wiki page:')
        print(' - http://wiki.cyanogenmod.org/w/Devices')
        codename = input_ask('Please provide the device name')

    return codename


def get_cyanogenmod_release_type(recommended=True):
    """
    Try to determine what kind of CyanogenMod release type to use.
    """
    # TODO: First check the settings.ini file inside the definition.
    if not recommended:
        return input_ask('Please provide a CM release type')

    return 'snapshot'


def get_cyanogenmod_release_version(recommended=True):
    """
    Try to determine what kind of CyanogenMod release version to use.
    """
    # TODO: First check the settings.ini file inside the definition.
    if not recommended:
        return input_ask('Please provide a CM release version', None, True)

    return 'M12'


def reboot_device(mode):
    # Get the MIA handler singleton.
    handler = MiaHandler()

    if mode == 'bootloader' or mode == 'recovery':
        if handler.args['--emulator']:
            # Restart the emulator.
            subprocess.call(['adb', '-e', 'reboot', mode])
        else:
            # Restart the device.
            subprocess.call(['adb', 'reboot', mode])


def set_open_recovery_script():
    # Get the MIA handler singleton.
    handler = MiaHandler()
    # TODO: Check the md5sum of the files on the device, make sure they are OK.

    # Push the open recovery script to the device.
    script_path = os.path.join(handler.get_definition_path(),
                               'other', 'openrecoveryscript')
    push_file_to_device('file', script_path, '/sdcard/openrecoveryscript')

    command = 'su root cp /sdcard/openrecoveryscript /cache/recovery/'
    if handler.args['--emulator']:
        # Run the command on the emulator.
        subprocess.call(['adb', '-e', 'shell', command])
    else:
        # Run the command on the device.
        subprocess.call(['adb', 'shell', command])


def push_file_to_device(source_type, source, destination):
    # Get the MIA handler singleton.
    handler = MiaHandler()

    # Get the file size.
    file_size = os.path.getsize(source)

    print('Pushing %s (%s) onto the device:\n - %s' %
          (source_type, format_file_size(file_size), source))
    print('Please wait...')

    # TODO: Add progress bar.
    # http://stackoverflow.com/questions/6595374/adb-push-pull-with-progress-bar
    print('NOTE: Progress bar has not been implemented yet!')

    if handler.args['--emulator']:
        # Push file to the emulator.
        subprocess.call(['adb', '-e', 'push', source, destination])
    else:
        # Push file to the device.
        subprocess.call(['adb', 'push', source, destination])
