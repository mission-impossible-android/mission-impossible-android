"""
Detailed information about the 'clean' command goes here!

Usage:
    mia clean <definition>
    mia clean --help

Command options:
    -h, --help  Show this screen.


"""

import re
import shutil

# Import custom helpers.
from mia.helpers.utils import *


def main():
    # Get the MIA handler singleton.
    handler = MiaHandler()

    if handler.args['<definition>']:
        clean_definition()
    else:
        clean_workspace()


def clean_definition():
    # Get the MIA handler singleton.
    handler = MiaHandler()

    if not re.search(r'^[a-z][a-z0-9-]+$', handler.args['<definition>']):
        # raise Exception('Definition "%s" already exists!' % definition)
        print('ERROR: Please provide a valid definition name! '
              'See: mia help definition')
        sys.exit(1)

    definition_path = handler.get_definition_path()
    print('Destination directory is:\n - %s\n' % definition_path)

    user_apps_path = os.path.join(definition_path, 'user-apps')
    if os.path.isdir(user_apps_path):
        print('Removing the user-apps:\n - %s\n' % user_apps_path)
        shutil.rmtree(user_apps_path)
    else:
        print('No user-apps.')

    system_apps_path = os.path.join(definition_path, 'system-apps')
    if os.path.isdir(system_apps_path):
        print('Removing the system-apps:\n - %s\n' % system_apps_path)
        shutil.rmtree(system_apps_path)
    else:
        print('No system-apps.')


def clean_workspace():
    # Get the MIA handler singleton.
    handler = MiaHandler()

    workspace_path = handler.get_workspace_path()
    print('Workspace directory is:\n - %s\n' % workspace_path)

    # Clean the workspace builds folder.
    builds_path = os.path.join(workspace_path, 'builds')
    if os.path.isdir(builds_path):
        print('Removing items from builds:\n - %s' % builds_path)
        dir_items = [f for f in os.listdir(builds_path)]
        for item in dir_items:
            item_path = os.path.join(builds_path, item)
            if os.path.isdir(item_path):
                print(' - removing directory: %s' % item)
                shutil.rmtree(item_path)
            else:
                print(' - removing file: %s' % item)
                os.remove(item_path)

    # Clean the workspace resources folder.
    resources_path = os.path.join(workspace_path, 'resources')
    if os.path.isdir(resources_path):
        print('Removing items from resources:\n - %s' % resources_path)
        dir_items = [f for f in os.listdir(resources_path)]
        for item in dir_items:
            item_path = os.path.join(resources_path, item)
            if os.path.isdir(item_path):
                print('   - removing directory: %s' % item)
                shutil.rmtree(item_path)
            else:
                print('   - removing file: %s' % item)
                os.remove(item_path)
