"""
MIA - Mission Impossible: Hardening Android for Security and Privacy

This project is a attempting to streamline the process of following Mike Perry's
Android hardening tutorial on the Tor blog:
    https://blog.torproject.org/blog/mission-impossible-hardening-android-security-and-privacy

Please keep in mind that this is experimental, and may not be functional at any
given moment. Also, it will likely wipe your Android device, and this is by
design!

Usage:
    mia [options] <command> [<command_args_and_opts>...]
    mia [ --commands | --options ] [<command>]
    mia --help

Global options:
    --commands  Displays a list of available commands or sub-commands.
    --options   Displays a list of global or command specific options.
    --quiet     Restrict output to warnings and errors.
    --verbose   Spew out even more information than normal.
    --help      Show this screen.
    --version   Show version.

Available commands:
    build       Build an update.zip file.
    clean       Cleanup the current workspace.
    definition  Create and configure a definition for a new update.zip file \
                based on existing templates.
    install     Install the OS and the built update.zip file onto the device.


Notes:
  You can use 'mia <command> --help' for more information on a specific command.

"""

import re
import os
import sys

# Import docopt - the command-line interface description language.
# @see https://github.com/docopt/docopt/releases
from docopt import docopt

# Import custom helpers.
from mia import (__version__)
from mia.handler import MiaHandler
from mia.commands import Build, Clean, Definition, Install

# Get the current directory.
WORKSPACE = os.getcwd()

# Add the script root the the PYTHONPATH environment variable.
ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(ROOT)


def delegate_command(command_name, command_args):
    """
    Main command handler.
    """
    # Get the MIA handler singleton.
    handler = MiaHandler()

    if not command_name:
        # Display a list of commands and exit.
        if handler.global_args['--commands']:
            print(get_doc_section(__doc__, 'commands'))
            sys.exit(0)

        # Display a list of global options and exit.
        if handler.global_args['--options']:
            print(get_doc_section(__doc__, 'global-options'))
            sys.exit(0)

    # Prepare the the argv parameter for the command specific docopt.
    command_argv = [command_name] + command_args

    # Get the command handler.
    command_handler = None
    if command_name == 'build':
        command_handler = Build()
    elif command_name == 'clean':
        command_handler = Clean()
    elif command_name == 'definition':
        command_handler = Definition()
    elif command_name == 'install':
        command_handler = Install()

    if command_handler is None:
        msg = 'Command "%s" does not exist or has not been implemented yet!'
        print(msg % command_name)
        sys.exit(1)

    # Note that docopt deals with the help option.
    handler.args = docopt(command_handler.__doc__, argv=command_argv)

    # Display a list of commands and exit.
    if handler.global_args['--commands']:
        print(get_doc_section(command_handler.__doc__, 'sub-commands'))
        sys.exit(0)

    # Display a list of global options and exit.
    if handler.global_args['--options']:
        print(get_doc_section(command_handler.__doc__, 'command-options'))
        sys.exit(0)

    # Remove command from the command arguments list.
    del handler.args[command_name]

    # Execute the command and return the exit code.
    return command_handler.main()


def get_doc_section(doc, section):
    """
    :return: A string with the available commands or options from the section.
    """

    if section == 'global-options':
        section_name = 'Global options'
        usage_split = re.split(r'(Global options:)', doc, flags=re.IGNORECASE)
    elif section == 'command-options':
        section_name = 'Command options'
        usage_split = re.split(r'(Command options:)', doc, flags=re.IGNORECASE)
    elif section == 'sub-commands':
        section_name = 'Available sub-commands'
        usage_split = re.split(r'(Available sub-commands:)', doc, flags=re.IGNORECASE)
    else:
        section_name = 'Available commands'
        usage_split = re.split(r'(Available commands:)', doc, flags=re.IGNORECASE)

    if len(usage_split) < 3:
        # No section was found.
        return ''
    elif len(usage_split) > 3:
        msg = 'More than one "%s:" (case-insensitive).' % section_name
        raise DocParserError(msg)

    return re.split(r'\n\s*\n', ''.join(usage_split[1:]))[0].strip()


def main():
    # Read the CLI arguments.
    # Use options_first to force reading the global options only.
    global_args = docopt(__doc__, version=__version__, options_first=True)

    # Create the MiaHandler instance. It can be used in other modules in order
    # to retrieve arguments, configuration, a logger...
    MiaHandler(ROOT, WORKSPACE, global_args)

    try:
        # Execute the command and exit the program.
        return delegate_command(
            global_args['<command>'],
            global_args['<command_args_and_opts>']
        )
    except KeyboardInterrupt:
        print('\n' + 'Exiting...')

    # The program did not finish successfully.
    return 1


if __name__ == "__main__":
    sys.exit(main())
