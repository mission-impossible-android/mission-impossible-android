"""
This sub-module contains the commands for "mia".
"""

available_commands = {}

# Populate the available commands with classes and help information.
from .build import Build
from .clean import Clean
from .definition import Definition
from .install import Install
