"""
The clean command can be use to cleanup the workspace or definition files.

Usage:
    mia clean [<definition>]
    mia clean --help


"""

import os
import re
import shutil
import sys

# Import custom helpers.
from mia.commands import available_commands
from mia.handler import MiaHandler


class Clean(object):
    @classmethod
    def main(cls):
        if MiaHandler.args['<definition>']:
            cls.clean_definition()
        else:
            cls.clean_workspace()

    @staticmethod
    def clean_definition():
        if not re.search(r'^[a-z][a-z0-9-]+$', MiaHandler.args['<definition>']):
            print('ERROR: Please provide a valid definition name! See: mia help definition')
            sys.exit(1)

        # Read the definition settings.
        settings = MiaHandler.get_definition_settings()
        definition_path = MiaHandler.get_definition_path()
        print('Definition directory is:\n - %s\n' % definition_path)

        for app_type in settings['app_types']:
            relative_path = settings['app_types'][app_type]
            full_path = os.path.join(definition_path, 'archive', relative_path)
            if not os.path.isdir(full_path):
                print('No %s apps to remove.' % app_type)
                continue

            print('Removing the %s apps from:\n - %s\n' % (app_type, full_path))
            shutil.rmtree(full_path)

    @staticmethod
    def clean_workspace():
        workspace_path = MiaHandler.get_workspace_path()
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


# Add command to the list of available commands.
available_commands['clean'] = {
    'class': Clean,
    'help': __doc__,
}
