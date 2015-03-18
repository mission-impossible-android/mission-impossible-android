"""
Utilities for the mia script.
"""

import os


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            super_class = super(Singleton, cls)
            cls._instances[cls] = super_class.__call__(*args, **kwargs)
        return cls._instances[cls]


class MiaHandler(metaclass=Singleton):
    args = []
    config_parser = []

    def __init__(self, script_root=None, workspace_dir=None, cli_args=None):
        if script_root:
            self.root = script_root

        if cli_args:
            self.args = cli_args

        if workspace_dir:
            self.workspace = workspace_dir

    # Save and display a log message.
    def log(self, msg, log_type='info'):
        # Display the message to the user.
        if self.args['--verbose']:
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


def input_confirm(display_text='Confirm', default_value=False):
    """
    Ask the user to confirm an action.
    :param display_text:
    :param default_value:
    :return: boolean
    """

    # Update the text depending on the default return value.
    if default_value:
        display_text = '%s [%s/%s]: ' % (display_text, 'Y', 'n')
    else:
        display_text = '%s [%s/%s]: ' % (display_text, 'y', 'N')

    while True:
        value = input(display_text)
        value = value.lower()

        # Return the default value.
        if not value:
            return default_value

        if value not in ['y', 'yes', 'n', 'no']:
            print('This is a yes and no question!')
            continue

        if value == 'y' or value == 'yes':
            return True
        if value == 'n' or value == 'no':
            return False


def input_ask(display_text, default_value=None, free_text=False):
    """
    Ask the user to provide a string.
    :param display_text:
    :param default_value:
    :return: string
    """

    # Update the text depending on the default return value.
    if default_value:
        display_text = '%s [%s]: ' % (display_text, default_value)
    else:
        display_text = '%s: ' % display_text

    while True:
        value = input(display_text)

        # Return the default value, if any.
        if not value and default_value is not None:
            return default_value
        elif not value:
            continue

        # Limit the allowed characters.
        if not free_text:
            import re
            if not re.search(r'^[a-z][a-z0-9-]+$', value):
                print('A sting containing letters, numbers, hyphens.')
                print('The string must start with a letter.')
                continue

        return value


def print_nl(string=''):
    print(string + "\n")


# TODO: Find a way to keep comments in the setting files.
def update_settings(settings_file, changes):
    import yaml

    # Make sure the settings file exists.
    if not os.path.isfile(settings_file):
        print('Settings file "%s" not found' % settings_file)
        return None

    try:
        fd = open(settings_file, 'r')

        # Load the yaml and sort the top level entries.
        settings = yaml.load(fd)

        fd.close()
    except yaml.YAMLError:
        print('ERROR: Could not read configuration file!')
        return None

    for section in changes:
        # Update entries.
        if hasattr(changes[section], 'update'):
            for key in changes[section]['update']:
                settings[section][key] = changes[section]['update'][key]

        # Remove entries.
        if hasattr(changes[section], 'remove'):
            for key in changes[section]['remove']:
                del settings[section][key]

    # Save the changes.
    print("Updating settings file: \n - %s" % settings_file)

    try:
        # Define a custom order of the sections
        order = ['general', 'other_apps', 'fdroid_apps']
        for section in settings.keys():
            if section not in order:
                order.append(section)

        # Open the file.
        fd = open(settings_file, 'w')

        # Save all the settings in oder.
        for section in order:
            if section in settings.keys():
                data = {section: settings[section]}
                fd.write(yaml.dump(data, default_flow_style=False))

        fd.close()
    except yaml.YAMLError:
        fd.close()
        print('ERROR: Could not save configuration file!')
        return None
