#!/usr/bin/env python3
"""
Authentification
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Manage API auth
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines paths in need of auth
        """
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        elif path in excluded_paths:
            return False
        else:
            for i in excluded_paths:
                if i.startswith(path):
                    return False
                if path.startswith(i):
                    return False
                if i[-1] == "*":
                    if path.startswith(i[:-1]):
                        return False
        
        return True


    def authorized_header(self, request=None) -> str:
        """
        Returns athorized_header
        """
        if request is None:
            return None
        
        header = request.headers.get('Authorized')
        if header is None:
            return None
        
        return header


    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returrns a User
        """
        return None
        