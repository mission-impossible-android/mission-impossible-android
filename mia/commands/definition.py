"""
Create and configure a definition in the current workspace using the provided
template.

Usage Example:
    mia definition create
    mia definition create --template=extra --cpu=x86
    mia definition create my-xyz-phone
    mia definition configure my-xyz-phone
    mia definition configure my-mnp-tablet
"""

import os
import sys
import shutil

# Import custom helpers.
from mia.helpers.android import *
from mia.helpers.utils import *


def main():
    # Get the MIA handler singleton.
    handler = MiaHandler()

    # The definition name is optional, this is helpful for new users.
    if handler.args['<definition>'] is None:
        msg = 'Please provide a definition name'
        handler.args['<definition>'] = input_ask(msg)

    # Create the definition.
    if handler.args['create']:
        create_definition()

    # Configure the definition.
    if (handler.args['create'] and input_confirm('Configure now?', True)) \
            or handler.args['configure']:
        print()
        configure_definition()

    return None


def create_definition():
    # Get the MIA handler singleton.
    handler = MiaHandler()

    definition_path = os.path.join(handler.workspace, 'definitions',
                                   handler.args['<definition>'])
    print('Destination directory is:')
    print_nl(' - ' + definition_path)

    # Make sure the definition does not exist.
    if os.path.exists(definition_path):
        # raise Exception('Definition "%s" already exists!' % definition)
        print('ERROR: Definition "%s" already exists!' %
              handler.args['<definition>'])
        sys.exit(0)

    template = handler.args['--template']
    template_path = os.path.join(handler.root, 'templates', template)
    print('Using template:')
    print_nl(' - ' + template_path)

    # Check if the template exists.
    if not os.path.exists(template_path):
        # raise Exception('Template "%s" does not exist!' % template)
        print('ERROR: Template "%s" does not exist!' % template)
        sys.exit(0)

    # Make sure the definitions folder exists.
    os.makedirs(os.path.join(handler.workspace, 'definitions'), mode=0o755,
                exist_ok=True)

    # Create the definition using the provided template.
    shutil.copytree(template_path, definition_path)


def configure_definition():
    # Get the MIA handler singleton.
    handler = MiaHandler()

    definition = handler.args['<definition>']

    # Detect the device codename.
    cm_device_codename = get_cyanogenmod_codename()
    print_nl('Using device codename: ' + cm_device_codename)

    # Detect the CM release type.
    if input_confirm('Use recommended CyanogenMod release type?', True):
        cm_release_type = get_cyanogenmod_release_type(True)
    else:
        cm_release_type = get_cyanogenmod_release_type(False)
    print_nl('Using release type: ' + cm_release_type)

    # Detect the CM release version.
    if input_confirm('Use recommended CyanogenMod release version?', True):
        cm_release_version = get_cyanogenmod_release_version(True)
    else:
        cm_release_version = get_cyanogenmod_release_version(False)
    print_nl('Using release version: ' + cm_release_version)

    url = 'https://download.cyanogenmod.org/?device=%s&type=%s' \
          % (cm_device_codename, cm_release_type)

    file_name = '%s.%s.%s-%s.zip' % \
                (definition, cm_device_codename, cm_release_type,
                 cm_release_version)

    print("Download CyanogenMod for and save the file as\n - %s\n"
          "into the resources folder and then verify the file checksum"
          % file_name)

    print_nl(' - ' + url)
