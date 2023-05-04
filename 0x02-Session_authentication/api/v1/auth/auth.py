#!/usr/bin/env python3
"""
  Manage API authentication
"""

from flask import request
from typing import TypeVar, List
from os import getenv


class Auth:
    """
      Create a class to manage the API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
          Require authentication before proceeding
        """
        if not path or not excluded_paths:
            return True
        path = path + '/' if path[-1] != '/' else path
        has_wildcard = any(x.endswith("*") for x in excluded_paths)
        if not has_wildcard:
            return path not in excluded_paths
        for e in excluded_paths:
            if e.endswith("*"):
                if path.startswith(e[:-1]):
                    return False
            if path == e:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization_header
        """
        if request:
            return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """
          Change if user is current login
        """
        return None

    def session_cookie(self, request=None):
        """Session Cookie"""
        if request:
            session_name = getenv('SESSION_NAME')
            return request.cookies.get(session_name, None)
