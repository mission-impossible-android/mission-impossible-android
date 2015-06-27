"""
This sub-module contains the commands for "mia".
"""

# Each command should expose it's main class and doc string.
available_commands = {}

# Populate the available commands with classes and help information.
from mia.commands.build import Build
from mia.commands.clean import Clean
from mia.commands.definition import Definition
from mia.commands.install import Install
