import os
import re
import shutil
import subprocess
import sys

from mia.handler import MiaHandler

# Replace the input() function in Python 2 with raw_input.
try:
    if sys.version_info[0] == 2:
        import __builtin__
        input = getattr(__builtin__, 'raw_input', input)
except ImportError or NameError:
    pass


class DocParserError(Exception):
    pass


class MiaUtils(object):
    @staticmethod
    def input_pause(display_text='Paused.'):
        input("%s\nPress enter to continue.\n" % display_text)

    @staticmethod
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

    @staticmethod
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

    # TODO: Find a way to keep comments in the setting files.
    @staticmethod
    def update_settings(settings_file, changes):
        import yaml

        # Make sure the settings file exists.
        if not os.path.isfile(settings_file):
            print('Settings file "%s" not found' % settings_file)
            return None

        try:
            fd = open(settings_file, 'r')

            # Load the YAML file and sort the top level entries.
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
        print("Updating settings file:\n - %s\n" % settings_file)

        try:
            # Define a custom order of the sections
            order = ['general', 'apps']
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

        # Load the settings in the main handler file.
        MiaHandler.get_definition_settings(True)

    @staticmethod
    def format_file_size(file_size, precision=2):
        import math
        file_size = int(file_size)

        if file_size is 0:
            return '0 bytes'

        log = math.floor(math.log(file_size, 1024))

        return "%.*f %s" % (
            precision,
            file_size / math.pow(1024, log),
            ['bytes', 'Kb', 'Mb'][int(log)]
        )

    @staticmethod
    def urlretrieve(url, install_filepath, cache_path=None):
        """
        Use wget to download files to specific location.
        (Caching not yet implemented.)
        """

        # Create the arguments list for wget.
        wget_arguments = ['--no-verbose', '--server-response']

        if cache_path is None:
            cache_enabled = False
            download_filepath = install_filepath
        else:
            cache_enabled = True
            wget_arguments.append('--continue')
            filename = install_filepath.split('/')[-1]
            download_filepath = os.path.join(cache_path, filename)

        wget_arguments.append('--output-document=%s' % download_filepath)
        wget_arguments.append('%s' % url)

        proc = subprocess.Popen(['wget'] + wget_arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            stdout, stderr = proc.communicate()
        except subprocess.TimeoutExpired:
            # TODO: Fix, subprocess.TimeoutExpired does not exist in PY2.
            proc.kill()
            print('ERROR: wget has timed out...')
            sys.exit(1)

        # Line ranges below hold true for `--no-verbose` mode output
        raw_response_data = stderr.splitlines()[0]
        raw_headers = stderr.splitlines()[1:-1]

        matches = re.match(r'^ *HTTP/[\d\.]+ (?P<code>\d{3}) (?P<msg>[\w ]*)$', raw_response_data.decode())

        response_data = {
            'status_code': int(matches.group('code')),
            'status_message': matches.group('msg'),
        }

        headers = {}
        for raw_header in iter(raw_headers):
            matches = re.match(r'^ *(?P<name>[\dA-Za-z\-]+): (?P<value>.+)$', raw_header.decode())
            if matches:
                headers[matches.group('name')] = matches.group('value')

        if proc.returncode != 0:
            raise IOError(stderr)

        if cache_enabled:
            shutil.copyfile(download_filepath, install_filepath)

        path = install_filepath

        http_message = {}
        http_message.update(response_data)
        http_message.update(headers)

        return path, http_message

    @staticmethod
    def version_compare(version1, version2, func='eq'):
        """
        Compare two Semantic Versions.
        @see http://semver.org/spec/v2.0.0.html
        """
        # @see https://docs.python.org/3.4/library/operator.html
        import operator

        from distutils.version import StrictVersion
        return getattr(operator, func)(
            StrictVersion(version1),
            StrictVersion(version2)
        )
