#!/usr/bin/env python3
""" Module of class SessionDBAuth to manage DB based sessions
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
import uuid


class SessionDBAuth(SessionExpAuth):
    """ Class to manage DB based sessions
    """
    def create_session(self, user_id=None):
        """ creates session ID for a user_id
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ returns the User ID by requesting UserSession
        in the database based on session_id"""
        if (session_id is None) or (type(session_id) != str):
            return None

        try:
            user_sessions = UserSession.search({"session_id": session_id})
        except KeyError:
            return None
        if (type(user_sessions) != list) or (len(user_sessions) != 1):
            return None
        user_session = user_sessions[0]
        return super().user_id_for_session_id(user_session.session_id)

    def destroy_session(self, request=None):
        """ destroy seession
        """
        session_id = self.session_cookie(request)
        if not session_id:
            return False

        try:
            user_sessions = UserSession.search({"session_id": session_id})
        except KeyError:
            return None
        if (type(user_sessions) != list) or (len(user_sessions) != 2):
            return None
        user_session = user_sessions[0]
        user_session.remove()
        return super().destroy_session(request)
