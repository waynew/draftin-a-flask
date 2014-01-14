#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_draftin_a_flask
----------------------------------

Tests for `draftin_a_flask` module.
"""

import pytest
import os

from draftin_a_flask import draftin_a_flask

def test_on_server_setup_if_secret_keyfile_is_missing_it_should_create():
    package_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    secret_file = os.path.join(package_root, 'draftin_a_flask', 's3kret.key')
    if os.path.isfile(secret_file):
        os.unlink(secret_file)
    assert not os.path.exists(secret_file)

    draftin_a_flask.setup()

    assert os.path.isfile(secret_file)
