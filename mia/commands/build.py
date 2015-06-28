"""
This command can be used to generate a custom update.zip file using information
from a definition.

Usage:
    mia build [--no-hash] <definition>
    mia build --help

Command options:
    --no-hash  Build faster, skip hash computation.


WARNING:
  Skipping the hash computation will allow you to install incomplete or broken
  builds onto your device.


"""

import glob
import os
import sys
import zipfile

# Import custom helpers.
from mia.commands import available_commands
from mia.handler import MiaHandler
from mia.utils import MiaUtils


class Build(object):
    @classmethod
    def main(cls):
        definition_path = MiaHandler.get_definition_path()

        # Create the builds directory.
        builds_path = os.path.join(MiaHandler.get_workspace_path(), 'builds')
        if not os.path.isdir(builds_path):
            os.makedirs(builds_path, mode=0o755)

        zip_name = '.'.join((
            MiaHandler.args['<definition>'],
            'mia-update.zip',
        ))
        zip_path = os.path.join(MiaHandler.get_workspace_path(), 'builds', zip_name)
        if os.path.exists(zip_path):
            print('Deleting current build: {}'.format(zip_path))
            os.remove(zip_path)

        # Open a ZIP file.
        zf = zipfile.ZipFile(zip_path, mode='w', compression=zipfile.ZIP_DEFLATED)

        # TODO: Verify available hashes for files added to the generated update.zip.
        archive_root_directory_path = os.path.join(definition_path, 'archive')
        for entry in glob.glob(archive_root_directory_path + '/*'):
            # Allow only directories at the root of the generated update.zip
            if not os.path.isdir(entry):
                continue

            destination = os.path.basename(entry)
            print('Adding "{}" directory to the archive:'.format(destination))
            cls.add_directory_to_zip(zf, entry, destination)

        # Make sure the created file is valid.
        print('Verifying built mia-update.zip file...')
        bad_file = zf.testzip()
        zf.close()
        if bad_file:
            sys.exit('Created zip file is corrupted: {!r}'.format(bad_file))

        # Only generate hash upon successful build. Keeping the old hash
        # will help prevent installing broken update.zip files.
        if not MiaHandler.args['--no-hash']:
            # TODO: Verify hash during the install process.
            MiaUtils.create_hash_file(zip_path)
        else:
            # Remove hash from previous build.
            hash_file_path = '.'.join((zip_path, 'SHA256SUM'))
            if os.path.exists(hash_file_path):
                os.remove(hash_file_path)

        print('Build finished successfully:\n - {}'.format(zip_path))

        return None

    @staticmethod
    def add_directory_to_zip(zf, source, destination):
        for path, directories, files in os.walk(source):
            for file_name in files:
                rel_path = os.path.relpath(path, source)
                if rel_path != '.':
                    path_in_zip = os.path.join(destination, rel_path, file_name)
                else:
                    path_in_zip = os.path.join(destination, file_name)

                print(' - {}'.format(path_in_zip))
                zf.write(os.path.join(path, file_name), path_in_zip)


# Add command to the list of available commands.
available_commands['build'] = {
    'class': Build,
    'help': __doc__,
}
