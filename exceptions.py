"""
Exceptions module.

This module contains all custom exceptions to raise.
"""


class LoginException(Exception):
    """Exception raised when the user hasn't saved his login information (username and password)"""


class PageStructureException(Exception):
    """Exception raised when the page structure doesn't match with the searched element"""


class FileNotExpectedError(Exception):
    """Raised when the file is not the expected one"""
