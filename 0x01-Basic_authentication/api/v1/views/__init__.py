#!/usr/bin/env python3
""" Document import
"""
from views.users import *
from views.index import *
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")


User.load_from_file()
