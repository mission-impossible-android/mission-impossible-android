"""
This command can be used to generate a custom update.zip file using information
from a definition.

Usage:
    mia build <definition>
    mia build --help


"""

import zipfile

# Import custom helpers.
from mia.helpers.utils import *


def main():
    # Get the MIA handler singleton.
    handler = MiaHandler()

    # Read the definition settings.
    settings = handler.get_definition_settings()
    definition_path = handler.get_definition_path()

    # Create the builds folder.
    builds_path = os.path.join(handler.get_workspace_path(), 'builds')
    if not os.path.isdir(builds_path):
        os.makedirs(builds_path, mode=0o755)

    zip_name = '%s.%s' % (handler.args['<definition>'], 'mia-update.zip')
    zip_path = os.path.join(handler.get_workspace_path(), 'builds',
                            zip_name)
    if os.path.exists(zip_path):
        print('Deleting current build:\n - %s\n' % zip_path)
        os.remove(zip_path)

    zf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
    for entry in settings['update_content']:
        entry_base_path = os.path.join(definition_path, entry['src'])
        if os.path.isdir(entry_base_path):
            print('Adding "%s" files to the archive:' % entry['dst'])
            add_directory_to_zip(zf, entry_base_path, entry['dst'])

        elif os.path.isfile(entry_base_path):
            print('Adding "%s" file to the archive.' % entry['dst'])
            zf.write(entry_base_path, entry['dst'])

    zf.close()
    print('\n' + 'Finished creating:\n - %s' % zip_path)

    return None


def add_directory_to_zip(zf, source, destination):
    for path, folders, files in os.walk(source):
        for file_name in files:
            rel_path = os.path.relpath(path, source)
            if rel_path != '.':
                path_in_zip = os.path.join(destination, rel_path, file_name)
            else:
                path_in_zip = os.path.join(destination, file_name)

            print(' - %s' % path_in_zip)
            zf.write(os.path.join(path, file_name), path_in_zip)
