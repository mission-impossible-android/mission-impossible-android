"""
Utilities for the mia script.
"""


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

    def __init__(self, script_root=None, cli_args=None):
        if script_root:
            self.root = script_root

        if cli_args:
            self.args = cli_args

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

    print("free_text: %s" % free_text)
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
