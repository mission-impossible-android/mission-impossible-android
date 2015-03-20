"""
Provides helper function for interfacing with devices using ADB or getting
information about the software or device.
"""
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


def get_cyanogenmod_zip_filename():
    # Get the MIA handler singleton.
    handler = MiaHandler()

    # Read the definition settings.
    settings = handler.get_definition_settings()

    return 'cm-11-%s.%s-%s.zip' % (
        settings['general']['cm_device_codename'],
        settings['general']['cm_release_type'],
        settings['general']['cm_release_version']
    )
