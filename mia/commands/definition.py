"""
Create and configure a definition in the current workspace using the provided
template.

Usage:
    mia definition create [--cpu=<cpu>] [--force] [--template=<template>]
                          [<definition>]
    mia definition configure <definition>
    mia definition lock [--force-latest] <definition>
    mia definition dl-apps <definition>
    mia definition dl-os <definition>
    mia definition extract-update-binary <definition>
    mia definition update-from-template <definition>
    mia definition --help

Available sub-commands:
    create                 Creates a definition.
    configure              Configures a definition.
    lock                   Creates a lock file for the applications.
    dl-apps                Downloads the applications using data from the lock file.
    dl-os                  Show information on how to download and verify an OS zip.
    extract-update-binary  Extract the update-binary from the CyanogenMod zip file.
    update-from-template   Update definition from template

Command options:
    --template=<template>  The template to use. [default: mia-default]
    --cpu=<cpu>            The device CPU architecture. [default: armeabi]
    --force                Delete existing definition.
    --force-latest         Force using the latest versions.


Notes:
    A valid <definition> name consists of lowercase letters, digits and hyphens.
    And it must start with a letter name.


"""

import re
import os
import shutil
import sys
import zipfile
import distutils.dir_util
import xml.etree.ElementTree as ElementTree

import yaml

# Import custom helpers.
from mia.commands import available_commands
from mia.android import MiaAndroid
from mia.fdroid import MiaFDroid
from mia.handler import MiaHandler
from mia.utils import MiaUtils


class Definition(object):
    @classmethod
    def main(cls):
        # The definition name is optional, this is helpful for new users.
        if MiaHandler.args['<definition>'] is None:
            msg = 'Please provide a definition name'
            MiaHandler.args['<definition>'] = MiaUtils.input_ask(msg)

        if not re.search(r'^[a-z][a-z0-9-]+$', MiaHandler.args['<definition>']):
            print('ERROR: Please provide a valid definition name! See: mia help definition')
            sys.exit(1)

        # Create the definition.
        if MiaHandler.args['create']:
            cls.create_definition()
        elif not os.path.exists(MiaHandler.get_definition_path()):
            # Make sure the definition exists.
            print('ERROR: Definition "%s" does not exist!' % MiaHandler.args['<definition>'])
            sys.exit(1)

        # Configure the definition.
        if MiaHandler.args['configure']:
            cls.configure_definition()

        # Update definition from template.
        if MiaHandler.args['update-from-template']:
            cls.update_definition()

        # Create the apps lock file.
        if MiaHandler.args['lock']:
            cls.create_apps_lock_file()

        # Download the CyanogenMod OS.
        if MiaHandler.args['dl-os']:
            cls.download_os()

        # Download apps.
        if MiaHandler.args['dl-apps']:
            cls.download_apps()

        # Extract the update-binary from the CyanogenMod zip file.
        if MiaHandler.args['extract-update-binary']:
            cls.extract_update_binary()

        return None

    @classmethod
    def create_definition(cls):
        definition_path = MiaHandler.get_definition_path()
        print('Destination directory is:\n - %s\n' % definition_path)

        # Make sure the definition does not exist.
        if os.path.exists(definition_path):
            if MiaHandler.args['--force']:
                print('Removing the old definition folder...')
                shutil.rmtree(definition_path)
            else:
                print('ERROR: Definition "%s" already exists!' % MiaHandler.args['<definition>'])
                sys.exit(1)

        # Get the template name.
        template = MiaHandler.args['--template']
        template_path = MiaHandler.get_template_path(template)
        if template_path is None:
            print('ERROR: Template "%s" does not exist!' % template)
            sys.exit(1)

        print('Using template:\n - %s\n' % template_path)

        # Make sure the definitions folder exists.
        definitions_path = os.path.join(MiaHandler.get_workspace_path(), 'definitions')
        if not os.path.isdir(definitions_path):
            os.makedirs(definitions_path, mode=0o755)

        # Create the definition using the provided template.
        shutil.copytree(template_path, definition_path)

        # Configure the definition.
        if MiaUtils.input_confirm('Configure now?', True):
            cls.configure_definition()

    @staticmethod
    def update_definition():
        definition_path = MiaHandler.get_definition_path()
        print('Destination directory is:\n - %s\n' % definition_path)

        settings = MiaHandler.get_definition_settings()
        template = settings['general']['template']
        template_path = MiaHandler.get_template_path(template)
        print('Using template:\n - %s\n' % template_path)

        # Check if the template exists.
        if not os.path.exists(template_path):
            print('ERROR: Template "%s" does not exist!' % template)
            sys.exit(1)

        # Create the definition using the provided template.
        distutils.dir_util.copy_tree(template_path, definition_path)

    @classmethod
    def configure_definition(cls):
        # Get the android device wrapper.
        android = MiaAndroid()

        # Detect the device codename.
        cm_device_codename = android.get_cyanogenmod_codename()
        print('Using device codename: %s\n' % cm_device_codename)

        # Detect the CyanogenMod release type.
        default_release_type = android.get_cyanogenmod_release_type(True)
        message = 'Use recommended [%s] CyanogenMod release type?' % default_release_type
        if MiaUtils.input_confirm(message, True):
            cm_release_type = default_release_type
        else:
            cm_release_type = android.get_cyanogenmod_release_type(False)
        print('Using release type: %s\n' % cm_release_type)

        # Detect the CyanogenMod release version.
        default_release_version = android.get_cyanogenmod_release_version(True)
        message = 'Use recommended [%s] CyanogenMod release version?' % default_release_version
        if MiaUtils.input_confirm(message, True):
            cm_release_version = default_release_version
        else:
            cm_release_version = android.get_cyanogenmod_release_version(False)
        print('Using release version: %s\n' % cm_release_version)

        # The path to the definition settings.yaml file.
        definition_path = MiaHandler.get_definition_path()
        settings_file = os.path.join(definition_path, 'settings.yaml')
        settings_file_backup = os.path.join(definition_path, 'settings.orig.yaml')

        # Create a backup of the settings file.
        shutil.copy(settings_file, settings_file_backup)

        # Update the settings file.
        MiaUtils.update_settings(settings_file, {'general': {
            'update': {
                'cm_device_codename': cm_device_codename,
                'cm_release_type': cm_release_type,
                'cm_release_version': cm_release_version,
            },
        }})

        # Create the apps lock file.
        cls.create_apps_lock_file()

        # Download the CyanogenMod OS.
        if MiaUtils.input_confirm('Download CyanogenMod OS now?', True):
            cls.download_os()

        # Download apps.
        if MiaUtils.input_confirm('Download apps now?', True):
            cls.download_apps()

    @classmethod
    def create_apps_lock_file(cls):
        # Get the APK lock data.
        lock_data = cls.get_apps_lock_info()

        definition_path = MiaHandler.get_definition_path()
        lock_file_path = os.path.join(definition_path, 'apps_lock.yaml')
        print('Creating lock file:\n - %s\n' % lock_file_path)

        fd = open(lock_file_path, 'w')
        try:
            fd.write(yaml.dump(lock_data, default_flow_style=False))
            fd.close()
        except yaml.YAMLError:
            print('ERROR: Could not save the lock file!')
            sys.exit(1)
        finally:
            fd.close()

        # Download apps.
        if MiaHandler.args['lock'] and MiaUtils.input_confirm('Download apps now?', True):
            cls.download_apps()

    @staticmethod
    def get_apps_lock_info():
        # Read the definition settings.
        settings = MiaHandler.get_definition_settings()

        if not settings['defaults']['repository']:
            print('Missing default repository setting.')
            sys.exit(1)

        # Make sure the resources folder exists.
        resources_path = os.path.join(MiaHandler.get_workspace_path(), 'resources')
        if not os.path.isdir(resources_path):
            os.makedirs(resources_path, mode=0o755)

        # Download and read info from the index.xml file of all repositories.
        repositories_data = {}
        for repo_info in settings['repositories']:
            index_path = os.path.join(MiaHandler.get_workspace_path(), 'resources', repo_info['id'] + '.index.xml')

            if not os.path.isfile(index_path):
                index_url = '%s/%s' % (repo_info['url'], 'index.xml')
                print('Downloading the %s repository information from:\n - %s' % (repo_info['name'], index_url))
                MiaUtils.urlretrieve(index_url, index_path)

            # Parse the repository index file and return the XML root.
            xml_tree = ElementTree.parse(index_path)
            if not xml_tree:
                print('Error parsing file:\n - %s' % index_path)
            repo_info['tree'] = xml_tree.getroot()

            repositories_data[repo_info['id']] = repo_info

        apps_list = []
        warnings_found = False
        print('Looking for APKs:')
        for key, app_info in enumerate(settings['apps']):
            # Add app to list if download url was provided directly.
            if 'url' in app_info:
                lock_info = {
                    'id': app_info['id'],
                    'package_name': app_info['name'],
                    'package_url': app_info['url'],
                    'type': app_info.get('type', settings['defaults']['app_type']),
                    'hash': app_info['hash'],
                    'hash_type': app_info.get('hash_type', settings['defaults']['hash_type']),
                }

                print(' - adding `%s`' % lock_info['id'])
                apps_list.append(lock_info)
                continue

            # Lookup the app by id and versioncode in the repository index.xml.
            if 'id' in app_info:
                # Use the default repository if it has not been provided.
                if 'repo' not in app_info:
                    app_info['repo'] = settings['defaults']['repository']

                # Use the default app_type if it has not been provided.
                if 'type' not in app_info:
                    app_info['type'] = settings['defaults']['app_type']

                # Use the default hash_type if it has not been provided.
                if 'hash' in app_info and 'hash_type' not in app_info:
                    app_info['hash_type'] = settings['defaults']['hash_type']

                # Use the latest application version code.
                if MiaHandler.args['--force-latest'] or 'versioncode' not in app_info:
                    app_info['versioncode'] = 'latest'

                # Get the application info.
                lock_info = MiaFDroid.fdroid_get_app_lock_info(repositories_data, app_info)

                if lock_info is None:
                    msg = ' - app `%s` is missing'
                    print(msg % (app_info['id']))
                    warnings_found = True
                    continue

                repo_id = lock_info['repository']
                repo_name = repositories_data[repo_id]['name']

                if 'hash' in lock_info and 'hash' in app_info and lock_info['hash'] != app_info['hash']:
                    msg = ' - mismatching hash for `%s` in the %s repository.'
                    print(msg % (lock_info['id'], repo_name))
                    warnings_found = True
                    continue

                msg = ' - found `%s` in the %s repository.'
                print(msg % (lock_info['id'], repo_name))
                apps_list.append(lock_info)

        # Give the user a chance to fix any possible errors.
        if warnings_found:
            msg = 'Warnings found, some APKs will not be downloaded! Continue?'
            if not MiaUtils.input_confirm(msg):
                sys.exit(1)

        return apps_list

    @staticmethod
    def download_apps():
        # Read the definition apps lock data.
        lock_data = MiaHandler.get_definition_apps_lock_data()

        # Read the definition settings.
        settings = MiaHandler.get_definition_settings()
        definition_path = MiaHandler.get_definition_path()

        for apk_info in lock_data:
            print(' - downloading: %s' % apk_info['package_url'])
            relative_path = settings['app_types'][apk_info['type']]
            download_path = os.path.join(definition_path, 'archive', relative_path)
            if not os.path.isdir(download_path):
                os.makedirs(download_path, mode=0o755)

            apk_path = os.path.join(download_path, apk_info['package_name'])

            # Create the CPU architecture specific apps cache directory.
            architecture_cache = MiaHandler.args['--cpu'] + '-apps'
            cache_directory = os.path.join(MiaHandler.get_workspace_path(), 'resources', architecture_cache)
            if not os.path.isdir(cache_directory):
                os.makedirs(cache_directory, mode=0o755)

            path, http_message = MiaUtils.urlretrieve(apk_info['package_url'], apk_path, cache_directory)
            if http_message['status_code'] == 200:
                print('   - downloaded: %s' % MiaUtils.format_file_size(http_message['Content-Length']))
            elif http_message['status_code'] == 206:
                print('   - download continued: %s' % MiaUtils.format_file_size(http_message['Content-Length']))
            elif http_message['status_code'] == 416:
                print('   - already downloaded, using cached apk.')
            else:
                print('   - error downloading file.')
                if not MiaUtils.input_confirm('Continue?', True):
                    sys.exit('Download aborted!')

            # TODO: Verify signatures?!?
            if os.path.exists(apk_path) and 'hash' in apk_info:
                apk_hash_value = MiaUtils.get_file_hash(apk_path, apk_info['hash_type'])

                if apk_hash_value != apk_info['hash']:
                    sys.exit('WARNING: Unexpected hash for downloaded apk!')

        print('Finished downloading APKs and verifying their hash values.')

    @staticmethod
    def download_os():
        """
        Display information to the user on how to download the OS and verify it's
        checksum.
        """
        print('\nNOTE: Command not finished yet; See instructions!\n')

        # Read the definition settings.
        settings = MiaHandler.get_definition_settings()

        # Create the resources folder.
        resources_path = os.path.join(MiaHandler.get_workspace_path(), 'resources')
        if not os.path.isdir(resources_path):
            os.makedirs(resources_path, mode=0o755)

        url = 'https://download.cyanogenmod.org/?device=%s&type=%s' % (
            settings['general']['cm_device_codename'],
            settings['general']['cm_release_type']
        )

        file_name = MiaHandler.get_os_zip_filename()

        message = '\n'.join((
            'Download CyanogenMod from:\n - %s',
            'and save the file as\n - %s',
            'into the resources folder, and remember to open a new terminal and',
            'verify the that provided md5 checksum matches the the output of:',
            ' ~$ md5sum resources/%s',
        ))
        print(message % (url, file_name, file_name))

        # Make sure the OS archive exists.
        zip_file_path = os.path.join(resources_path, file_name)
        while True:
            MiaUtils.input_pause('Please follow the instructions before continuing.')

            # Only allow the user to continue if the OS image exists.
            if os.path.isfile(zip_file_path):
                break

            # Display message and try again.
            print('File not found:\n - %s' % zip_file_path)

    @staticmethod
    def extract_update_binary():
        # Get the resources folder.
        resources_path = os.path.join(MiaHandler.get_workspace_path(), 'resources')

        definition_path = MiaHandler.get_definition_path()

        # Get file path.
        zip_file_path = os.path.join(resources_path, MiaHandler.get_os_zip_filename())

        # The path to the update-binary file inside the zip.
        update_relative_path = 'META-INF/com/google/android/update-binary'

        print('Extracting the update-binary from:\n - %s' % zip_file_path)

        if os.path.isfile(zip_file_path) and zipfile.is_zipfile(zip_file_path):
            # Extract the update-binary in the definition.
            fd = zipfile.ZipFile(zip_file_path)

            # Save the file; taken from ZipFile.extract
            source = fd.open(update_relative_path)
            destination = os.path.join(definition_path, 'other', 'update-binary')
            target = open(destination, 'wb')
            with source, target:
                shutil.copyfileobj(source, target)
            os.chmod(destination, 0o755)

            print('Saved the update-binary to the definition!')
        else:
            print('File does not exist or is not a zip file.')


# Add command to the list of available commands.
available_commands['definition'] = {
    'class': Definition,
    'help': __doc__,
}
