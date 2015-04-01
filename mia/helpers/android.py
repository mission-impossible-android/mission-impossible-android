"""
Provides helper function for interfacing with devices using ADB or getting
information about the software or device.
"""

import subprocess

# Import custom helpers.
from mia.helpers.utils import *


def adb_get_version():
    # The `adb version` command returns a string in the following format:
    # Android Debug Bridge version 1.0.31
    std_output = str(subprocess.check_output(['adb', 'version']))

    # Get the version string.
    import re
    match_instance = re.search('(\d+\.\d+\.\d+)', std_output)
    if match_instance is not None and match_instance.group() is not None:
        return match_instance.group()

    return None


def adb_check_device():
    # TODO: Check if `adb` sees the device.
    return None


def get_cyanogenmod_codename():
    """
    Try to determine the device name.
    """
    # TODO: First check the settings.ini file inside the definition, if any.
    codename = None

    # Try to determine the device name using `adb`.
    if adb_check_device():
        # TODO: Try to get the device name using ADB.
        return None

    # If nothing worked, prompt the user for the device name.
    if codename is None:
        print('Lookup your device codename on the CyanogenMod wiki page:')
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

    # TODO: Cleanup!
    command = 'cp /sdcard/openrecoveryscript /cache/recovery/openrecoveryscript'
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

    # Create the arguments list for ADB.
    adb_arguments = [source, destination]

    # Display progress bar on newer versions of ADB.
    if version_compare(adb_get_version(), '1.0.32', 'ge'):
        adb_arguments.insert(0, '-p')
    else:
        print('Please wait...')

    # Add the `push` command before the `push` specific arguments and options.
    adb_arguments.insert(0, 'push')

    # Check if an emulator should be used instead of a device.
    if handler.args['--emulator']:
        adb_arguments.insert(0, '-e')

    # Push file to the device.
    subprocess.call(['adb'] + adb_arguments)
