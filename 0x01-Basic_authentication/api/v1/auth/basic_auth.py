#!/usr/bin/env python3
""" Module of class Auth to manage the API authentication.
"""
import base64
from typing import TypeVar

from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """ Class to manage the app authentication.
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str
                                            ) -> str:
        """ Method to extract the base64 authorization header.
        """
        AUTH_SCHEME = "Basic "

        if authorization_header is None:
            return None
        try:
            assert type(authorization_header) == str
        except AssertionError:
            return None
        if not authorization_header.startswith(AUTH_SCHEME):
            return None

        return authorization_header[len(AUTH_SCHEME):]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ Method to decode the base64 authorization header.
        """
        if base64_authorization_header is None:
            return None
        try:
            assert type(base64_authorization_header) == str
        except AssertionError:
            return None

        try:
            byte_auth = bytes(base64_authorization_header, "utf-8")
            data = base64.b64decode(byte_auth)
            return data.decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """ Method to extract the user credentials.
        """
        try:
            assert decoded_base64_authorization_header is not None
            assert type(decoded_base64_authorization_header) == str
            assert ":" in decoded_base64_authorization_header
        except AssertionError:
            return None, None

        email = password = ""
        for i in range(len(decoded_base64_authorization_header)):
            if decoded_base64_authorization_header[i] == ":":
                email = decoded_base64_authorization_header[:i]
                if (i + 1) < len(decoded_base64_authorization_header):
                    password = decoded_base64_authorization_header[i + 1:]
                break
        return email, password

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str
                                     ) -> TypeVar('User'):
        """ Method to get the user object from the credentials.
        """
        try:
            assert type(user_email) == str and user_email is not None
            assert type(user_pwd) == str and user_pwd is not None
        except AssertionError:
            return None

        try:
            users = User.search({"email": user_email})
        except KeyError:
            return None
        if (type(users) != list) or (len(users) != 1):
            return None
        user = users[0]
        if user.is_valid_password(user_pwd):
            return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method to get the current user.
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        base64_auth = self.extract_base64_authorization_header(auth_header)
        if base64_auth is None:
            return None
        decoded_auth = self.decode_base64_authorization_header(base64_auth)
        if decoded_auth is None:
            return None
        user_email, user_pwd = self.extract_user_credentials(decoded_auth)
        if (user_email is None) or (user_pwd is None):
            return None
        return self.user_object_from_credentials(user_email, user_pwd)
