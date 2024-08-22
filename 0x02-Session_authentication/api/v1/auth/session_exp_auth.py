#!/usr/bin/env python3
""" Module of class SessionExpAuth to manage session expiration
"""
from api.v1.auth.session_auth import SessionAuth
from os import environ
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ Class to manage session expiration
    """
    def __init__(self) -> None:
        super().__init__()
        try:
            self.session_duration = int(environ.get("SESSION_DURATION", 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ creates Session ID for a user_id with expiration
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ retusn a User ID based on Session ID
        """
        session_dict = super().user_id_for_session_id(session_id)
        if not session_dict:
            return None
        if self.session_duration <= 0:
            try:
                return session_dict["user_id"]
            except KeyError:
                return None
        try:
            exp = timedelta(seconds=self.session_duration)
            duration = session_dict["created_at"] + exp
            if duration < datetime.now():
                return None
            return session_dict["user_id"]
        except KeyError:
            return None
