"""Shared commands for the CLI.

This module provides shared CLI commands that can be used by multiple
packages in a multi-package architecture. These commands are automatically
discovered and added to the CLI by pyrig.
Example is version command that is available in all packages.
uv run my-awesome-project version will return my-awesome-project version 0.1.0
"""
