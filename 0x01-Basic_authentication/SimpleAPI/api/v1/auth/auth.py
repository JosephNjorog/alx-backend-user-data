#!/usr/bin/env python3
""" Module of class Auth to manage the API authentication.
"""
from flask import request
from typing import (
    List,
    TypeVar
)


class Auth:
    """ Class to manage the API authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method to require a auth.
        """
        if path is None:
            return True
        if (excluded_paths is None) or (excluded_paths == []):
            return True

        path = path + "/" if path[-1] != "/" else path
        return not (path in excluded_paths)

    def authorization_header(self, request=None) -> str:
        """ Method to get the authorization header.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method to get the current user.
        """
        return None
