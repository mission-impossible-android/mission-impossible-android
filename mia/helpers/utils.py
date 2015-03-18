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

