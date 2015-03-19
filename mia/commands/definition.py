"""
Create and configure a definition in the current workspace using the provided
template.

Usage patterns:
    mia definition create [--template=<template>] [--cpu=<cpu>] [<definition>]
    mia definition configure <definition>
    mia definition lock [--force-latest] <definition>

Usage Example:
    mia definition create
    mia definition create my-xyz-phone
    mia definition configure my-xyz-phone
    mia definition lock my-xyz-phone
    mia definition create --template=extra --cpu=x86 my-mnp-tablet
    mia definition configure my-mnp-tablet
    mia definition lock --force-latest my-mnp-tablet

Notes:
    A valid <definition> name consists of lowercase letters, digits and hyphens.
    And it must start with a letter name.

"""

import re
import sys
import shutil
from urllib.request import urlretrieve

# Import non-standard libraries.
from lxml import html as lxml_html

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

    if not re.search(r'^[a-z][a-z0-9-]+$', handler.args['<definition>']):
        # raise Exception('Definition "%s" already exists!' % definition)
        print('ERROR: Please provide a valid definition name! '
              'See: mia help definition')
        sys.exit(0)

    # Create the definition.
    if handler.args['create']:
        create_definition()

    # Configure the definition.
    if (handler.args['create'] and input_confirm('Configure now?', True)) \
            or handler.args['configure']:
        print()
        configure_definition()

    # Create the definition.
    if handler.args['lock']:
        generate_apk_lock_file()

    return None


def create_definition():
    # Get the MIA handler singleton.
    handler = MiaHandler()

    definition_path = os.path.join(handler.workspace, 'definitions',
                                   handler.args['<definition>'])
    print('Destination directory is:\n - %s\n' % definition_path)

    # Make sure the definition does not exist.
    if os.path.exists(definition_path):
        # raise Exception('Definition "%s" already exists!' % definition)
        print('ERROR: Definition "%s" already exists!' %
              handler.args['<definition>'])
        sys.exit(0)

    template = handler.args['--template']
    template_path = os.path.join(handler.root, 'templates', template)
    print('Using template:\n - %s\n' % definition_path)

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

    definition_path = os.path.join(handler.workspace, 'definitions',
                                   handler.args['<definition>'])

    # Detect the device codename.
    cm_device_codename = get_cyanogenmod_codename()
    print('Using device codename: %s\n' % cm_device_codename)

    # Detect the CM release type.
    if input_confirm('Use recommended CyanogenMod release type?', True):
        cm_release_type = get_cyanogenmod_release_type(True)
    else:
        cm_release_type = get_cyanogenmod_release_type(False)
    print('Using release type: %s\n' % cm_release_type)

    # Detect the CM release version.
    if input_confirm('Use recommended CyanogenMod release version?', True):
        cm_release_version = get_cyanogenmod_release_version(True)
    else:
        cm_release_version = get_cyanogenmod_release_version(False)
    print('Using release version: %s\n' % cm_release_version)

    url = 'https://download.cyanogenmod.org/?device=%s&type=%s' \
          % (cm_device_codename, cm_release_type)

    file_name = '%s.%s.%s-%s.zip' % \
                (handler.args['<definition>'], cm_device_codename,
                 cm_release_type, cm_release_version)

    print("Download CyanogenMod for and save the file as\n - %s\n"
          "into the resources folder and then verify the file checksum.\n - %s"
          % (file_name, url))

    # The path to the definition settings.yaml file.
    settings_file = os.path.join(definition_path, 'settings.yaml')
    settings_file_backup = os.path.join(definition_path, 'settings.orig.yaml')

    # Create a backup of the settings file.
    shutil.copy(settings_file, settings_file_backup)

    # Update the settings file.
    update_settings(settings_file, {'general': {
        'update': {
            'cm_device_codename': cm_device_codename,
            'cm_release_type': cm_release_type,
            'cm_release_version': cm_release_version,
        },
    }})


# TODO: Implement the APK lock functionality.
def generate_apk_lock_file():
    # Get the MIA handler singleton.
    handler = MiaHandler()

    import yaml

    definition_path = os.path.join(handler.workspace, 'definitions',
                                   handler.args['<definition>'])

    settings_file = os.path.join(definition_path, 'settings.yaml')
    print('Using settings file:\n - %s\n' % settings_file)

    try:
        fd = open(settings_file, 'r')

        # Load the yaml and sort the top level entries.
        settings = yaml.load(fd)

        fd.close()
    except yaml.YAMLError:
        print('ERROR: Could not read configuration file!')
        return None

    # Generate APK lock files for all repositories.
    lock_file_data = {}
    for repo_info in settings['repositories']:
        apps_keys = repo_info['apps_key']
        lock_file_data[apps_keys] = repo_lock_info(repo_info, settings[apps_keys])

    lock_file_path = os.path.join(definition_path, 'apps_lock.yaml')

    print("Creating lock file: \n - %s" % lock_file_path)
    try:
        fd = open(lock_file_path, 'w')
        fd.write(yaml.dump(lock_file_data, default_flow_style=False))
        fd.close()
    except yaml.YAMLError:
        fd.close()
        print('ERROR: Could not save the lock file!')
        return None


def repo_lock_info(repo_info, repo_apps):
    # Get the MIA handler singleton.
    handler = MiaHandler()

    index_path = os.path.join(handler.root, 'resources',
                              repo_info['apps_key'] + '.index.xml')

    # Download the repository index.xml file.
    if not os.path.isfile(index_path):
        index_url = '%s/%s' % (repo_info['base_url'], 'index.xml')
        print('Downloading the %s repository information from:\n - %s' %
              (repo_info['name'], index_url))
        urlretrieve(index_url, index_path)

    # Read the whole file index in memory?!?
    try:
        with open(index_path, 'r') as index_fd:
            index_data = index_fd.read()

        xml_document = lxml_html.fromstring(index_data)
        index_fd.close()
    except FileNotFoundError:
        print('File not found:\n - %s' % index_path)

    print('Looking for APKs for repo %s' % repo_info['name'])
    for key, app_info in enumerate(repo_apps):
        if handler.args['--force-latest'] or app_info['app_code'] == 'latest':
            # Get information about the latest version of the application.
            latest_name_xpath = "//application[@id='%s']/package[0]/apkname/text()" % \
                                (app_info['app_name'])
            app_package_names = xml_document.xpath(latest_name_xpath)

            code_xpath = "//application[@id='%s']/marketvercode/text()" % \
                         app_info['app_name']
            app_version_codes = xml_document.xpath(code_xpath)
        else:
            # Get information about an exact version of the application.
            name_xpath = "//application[@id='%s']/package/apkname/text()[../../versioncode/text() = %s]" % \
                         (app_info['app_name'], app_info['app_code'])
            app_package_names = xml_document.xpath(name_xpath)
            app_version_codes = None

        if len(app_package_names):
            print(' - found: %s:%s' % (app_info['app_name'],
                                       app_info['app_code']))
        else:
            print(' - not found: %s' % app_info['app_name'])
            del repo_apps[key]
            continue

        app_info['package_name'] = "%s" % app_package_names[0]
        app_info['package_url'] = "%s/%s" % (repo_info['base_url'],
                                             app_package_names[0])
        if app_version_codes is not None and len(app_version_codes):
            app_info['code'] = app_version_codes[0]

    return repo_apps
