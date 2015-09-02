"""
Provides helper function for interfacing with devices using ADB or getting
information about the software or device.
"""

import re
import os
import sys
import subprocess
from tempfile import mkstemp

# Import custom helpers.
from mia.handler import MiaHandler
from mia.utils import MiaUtils


class MiaAndroid(object):
    @staticmethod
    def adb_get_version():
        # The `adb version` command returns a string in the following format:
        # Android Debug Bridge version 1.0.31
        std_output = str(subprocess.check_output(['adb', 'version']))

        # Get the version string.
        match_instance = re.search('(\d+\.\d+\.\d+)', std_output)
        if match_instance is not None and match_instance.group() is not None:
            return match_instance.group()

        return None

    @staticmethod
    def adb_check_device():
        # TODO: Check if `adb` sees the device.
        return None

    @classmethod
    def get_cyanogenmod_codename(cls):
        """
        Try to determine the device name.
        """
        # TODO: First check the settings.ini file inside the definition, if any.
        codename = None

        # Try to determine the device name using `adb`.
        if cls.adb_check_device():
            # TODO: Try to get the device name using ADB.
            return None

        # If nothing worked, prompt the user for the device name.
        if codename is None:
            print('Lookup your device codename on the CyanogenMod wiki page:')
            print(' - http://wiki.cyanogenmod.org/w/Devices')
            codename = MiaUtils.input_ask('Please provide the device name')

        return codename

    @staticmethod
    def get_cyanogenmod_version(recommended=True):
        """
        Try to determine what kind of CyanogenMod release version to use.
        """
        # TODO: First check the settings.ini file inside the definition.
        if not recommended:
            return MiaUtils.input_ask('Please provide a CM version', None, True)

        return '11'

    @staticmethod
    def reboot_device(mode):
        if mode == 'bootloader' or mode == 'recovery':
            if MiaHandler.args['--emulator']:
                # Restart the emulator.
                adb_exit_code = subprocess.call(['adb', '-e', 'reboot', mode])
            else:
                # Restart the device.
                adb_exit_code = subprocess.call(['adb', 'reboot', mode])

            if adb_exit_code != 0:
                raise RuntimeError('Could not reboot the device!')

    # TODO: Check the md5sum of the files on the device, make sure they are OK.
    @classmethod
    def set_open_recovery_script(cls):
        # Push the open recovery script to the device.
        script_path = os.path.join(MiaHandler.get_definition_path(), 'other', 'openrecoveryscript')
        cls.push_file('file', script_path, '/sdcard/openrecoveryscript')

        # TODO: See whether `su` is really required, works fine in recovery mode?!?
        command = 'su root cp /sdcard/openrecoveryscript /cache/recovery/openrecoveryscript'
        if MiaHandler.args['--emulator']:
            # Run the command on the emulator.
            adb_exit_code = subprocess.call(['adb', '-e', 'shell', command])
        else:
            # Run the command on the device.
            adb_exit_code = subprocess.call(['adb', 'shell', command])

        if adb_exit_code != 0:
            raise RuntimeError('Could not set the open recovery script!')

    @classmethod
    def push_file(cls, source_type, source, destination):
        # Get the file size.
        file_size = os.path.getsize(source)

        print('Pushing %s (%s) onto the device:\n - %s' %
              (source_type, MiaUtils.format_file_size(file_size), source))

        # Create the arguments list for ADB.
        adb_arguments = [source, destination]

        # Display progress bar on newer versions of ADB.
        if MiaUtils.version_compare(cls.adb_get_version(), '1.0.32', 'ge'):
            adb_arguments.insert(0, '-p')
        else:
            print('Please wait...')

        # Add the `push` command before the `push` specific arguments and options.
        adb_arguments.insert(0, 'push')

        # Check if an emulator should be used instead of a device.
        if MiaHandler.args['--emulator']:
            adb_arguments.insert(0, '-e')

        # Push file to the device.
        adb_exit_code = subprocess.call(['adb'] + adb_arguments)
        if adb_exit_code != 0:
            raise RuntimeError('Could not push to the device!')

    @classmethod
    def push_hash_for_file(cls, hash_type, source, destination):
        source_path = '.'.join((source, hash_type))
        destination_path = '.'.join((destination, hash_type))

        try:
            with open(source_path, 'r') as source_file:
                """:type sourcefile: FileIO"""
                """:type temp_file: FileIO"""

                # Read the file content.
                source_content = source_file.read()

                # Update the content.
                destination_content = source_content.replace(
                    os.path.basename(source),
                    os.path.basename(destination)
                )

                # Create a temporary file.
                tfd, temp_file_path = mkstemp(suffix='.mia_hash_file', text=True)

                # Save the content to the temporary file
                with open(temp_file_path, 'w') as temp_file:
                    temp_file.write(destination_content)
        except IOError:
            print('ERROR: Could not open file:\n - %s' % source)
            sys.exit(1)

        # Push the file onto the devices.
        cls.push_file('hash file', temp_file_path, destination_path)

        # Delete the temporary file.
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
