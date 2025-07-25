"""
Pages package for the PACTA application.
"""
from .login import login
from .dashboard import dashboard

__all__ = [
    "login",
    "dashboard",
]