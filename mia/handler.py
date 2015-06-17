"""
Utilities for the mia script.
"""

import os
import sys
import yaml

from pkg_resources import DistributionNotFound, Requirement, resource_filename, resource_isdir


class MiaHandler:
    args = {}
    global_args = {}
    __root_path = None
    __workspace_path = None
    __definition_path = None
    __definition_settings = {}
    __definition_apps_lock_data = {}

    @classmethod
    def __init__(cls, root_path=None, workspace_path=None, global_args=None):
        if root_path:
            cls.__root_path = root_path

        if global_args:
            cls.global_args = global_args

        if workspace_path:
            cls.__workspace_path = workspace_path

    # Save and display a log message.
    @classmethod
    def log(cls, msg, log_type='info'):
        # Display the message to the user.
        if cls.global_args['--verbose']:
            print(msg)

        # Log the message.
        import logging

        if log_type == 'info':
            logging.info(msg)
        elif log_type == 'warning':
            logging.error(msg)
        elif log_type == 'debug':
            logging.debug(msg)
        else:
            logging.error(msg)

    @classmethod
    def get_root_path(cls):
        return cls.__root_path

    @classmethod
    def get_workspace_path(cls):
        return cls.__workspace_path

    @classmethod
    def get_definition_path(cls):
        if not cls.__definition_path and cls.args['<definition>']:
            cls.__definition_path = os.path.join(
                cls.__workspace_path, 'definitions',
                cls.args['<definition>']
            )

        return cls.__definition_path

    @classmethod
    def get_template_path(cls, template):
        relative_path = os.path.join('mia', 'templates', template)
        full_path = None

        try:
            # Try to use the pip distribution to determine the template path.
            resource_name = Requirement.parse('mia')

            # Check if the template directory exists in the distribution.
            if resource_isdir(resource_name, relative_path):
                full_path = resource_filename(resource_name, relative_path)

        except DistributionNotFound:
            # Otherwise, just use the script root path.
            tmp_path = os.path.join(cls.get_root_path(), relative_path)

            if os.path.exists(tmp_path):
                full_path = tmp_path

        return full_path

    @classmethod
    def get_os_zip_filename(cls):
        # Read the definition settings.
        settings = cls.get_definition_settings()

        return 'cm-11-%s.%s-%s.zip' % (
            settings['general']['cm_device_codename'],
            settings['general']['cm_release_type'],
            settings['general']['cm_release_version']
        )

    @classmethod
    def get_definition_settings(cls, force_update=False):
        if (not cls.__definition_settings and cls.args['<definition>']) or force_update:
            definition_path = cls.get_definition_path()
            settings_file = os.path.join(definition_path, 'settings.yaml')
            if not force_update:
                print('Using definition settings file:\n - %s\n' % settings_file)

            try:
                fd = open(settings_file, 'r')

                # Load the yaml and sort the top level entries.
                settings = yaml.load(fd)

                fd.close()
            except yaml.YAMLError:
                print('ERROR: Could not read configuration file!')
                sys.exit(1)

            if settings:
                cls.__definition_settings = settings

        return cls.__definition_settings

    @classmethod
    def get_definition_apps_lock_data(cls):
        if not cls.__definition_apps_lock_data and cls.args['<definition>']:
            definition_path = cls.get_definition_path()
            lock_file_path = os.path.join(definition_path, 'apps_lock.yaml')
            print('Using lock file:\n - %s\n' % lock_file_path)

            if not os.path.isfile(lock_file_path):
                print('ERROR: Apps lock file is missing! See: mia help definition')
                sys.exit(1)

            try:
                fd = open(lock_file_path, 'r')

                # Load the yaml and sort the top level entries.
                lock_data = yaml.load(fd)

                fd.close()
            except yaml.YAMLError:
                print('ERROR: Could not read configuration file!')
                sys.exit(1)

            if lock_data:
                cls.__definition_apps_lock_data = lock_data

        return cls.__definition_apps_lock_data
