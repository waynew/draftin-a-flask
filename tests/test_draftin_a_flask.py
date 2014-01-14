#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_draftin_a_flask
----------------------------------

Tests for `draftin_a_flask` module.
"""

import pytest
import os
import json

from mock import MagicMock, call

from draftin_a_flask import draftin_a_flask

@pytest.fixture
def secret_file():
    package_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    secret_file = os.path.join(package_root, 'draftin_a_flask', 's3kret.key')
    draftin_a_flask.setup()
    return secret_file


def test_if_secret_keyfile_is_missing_it_should_create_on_setup(secret_file):
    if os.path.isfile(secret_file):
        os.unlink(secret_file)
    assert not os.path.exists(secret_file)

    draftin_a_flask.setup()

    assert os.path.isfile(secret_file)


def test_after_delete_secret_file_should_contain_different_string(secret_file):
    if os.path.isfile(secret_file):
        os.unlink(secret_file)
    draftin_a_flask.setup()
    with open(secret_file) as f:
        old_secret = f.read()
    os.unlink(secret_file)

    draftin_a_flask.setup()

    with open(secret_file) as f:
        new_secret = f.read()
    assert old_secret != new_secret


def test_GET_to_secret_endpoint_should_405(secret_file):
    reload(draftin_a_flask)
    test_client = draftin_a_flask.app.test_client()
    with open(secret_file) as f:
        key = f.read()
    rv = test_client.get(key)
    assert rv.status_code == 405


def test_POST_to_secret_endpoint_should_call_publish():
    reload(draftin_a_flask)
    test_client = draftin_a_flask.app.test_client()
    draftin_a_flask.publish = MagicMock()
    data = {'id': 12345,
            'name': "Some document",
            'content': 'Some markdown',
            'content_html': 'Some html',
            'user': {'id': 42, 'email': 'fnord@fnord'},
            "created_at": "2013-05-23T14:11:54-05:00",
            "updated_at": "2013-05-23T14:11:58-05:00"
            }
    rv = test_client.post(draftin_a_flask.app.secret_key,
            data=json.dumps(data),
                          content_type='application/json')
    expected = [call.publish(data['content'])]
    assert draftin_a_flask.publish.mock_calls == expected
    

def test_POST_to_secret_endpoint_with_no_content_should_500():
    reload(draftin_a_flask)
    test_client = draftin_a_flask.app.test_client()
    data = {'id': 12345,
            'name': "Some document",
            'content_html': 'Some html',
            'user': {'id': 42, 'email': 'fnord@fnord'},
            "created_at": "2013-05-23T14:11:54-05:00",
            "updated_at": "2013-05-23T14:11:58-05:00"
            }
    rv = test_client.post(draftin_a_flask.app.secret_key,
            data=json.dumps(data),
                          content_type='application/json')
    assert rv.status_code == 500
