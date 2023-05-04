#!/usr/bin/env python3

"""
  Session DB authentication module
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from os import getenv
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
      Session DB Auth class.
    """

    def create_session(self, user_id=None):
        """create_session.
        """
        if user_id:
            session_id = super().create_session(user_id)
            if not session_id:
                return
            new_user = UserSession(user_id=user_id, session_id=session_id)
            new_user.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """user_id_for_session_id.
        """
        if not session_id:
            return
        try:
            user_list = UserSession.search({session_id: session_id})
            for user in user_list:
                created_at = user.get('created_at', None)
                if not created_at:
                    return
                if (datetime.now() > created_at +
                        timedelta(seconds=self.session_duration)):
                    return
                return user.get('user_id', None)
        except Exception:
            return

    def destroy_session(self, request=None) -> bool:
        """
        destroy_session.
        """
        if request:
            session_id = self.session_cookie(request)
            if session_id:
                if super().destroy_session(request):
                    try:
                        user_list = UserSession.search(
                            {session_id: session_id})
                        for user in user_list:
                            user.remove()
                            return True
                    except Exception:
                        return False
        return False
