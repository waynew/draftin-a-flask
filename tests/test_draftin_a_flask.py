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
import shutil

try:
    from imp import reload
except ImportError:
    pass

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
            #'user': {'id': 42, 'email': 'fnord@fnord'},
            "created_at": "2013-05-23T14:11:54-05:00",
            "updated_at": "2013-05-23T14:11:58-05:00"
            }
    rv = test_client.post(draftin_a_flask.app.secret_key,
            data={'payload':json.dumps(data)})
            
    expected = [call.publish(data['name'], data['content'])]
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


def test_if_content_directory_does_not_exist_it_should_get_made():
    draftin_a_flask.subprocess = MagicMock()
    content = os.path.join(draftin_a_flask.ROOT,
                           draftin_a_flask.CONTENT)
    if os.path.exists(content):
        shutil.rmtree(content)

    draftin_a_flask.publish('whatev', 'This is some *content*')

    is_dir = os.path.isdir(content)
    assert is_dir


def test_passing_name_and_content_to_publish_should_write_it_to_content_dir():
    draftin_a_flask.subprocess = MagicMock()
    draftin_a_flask.CONTENT = 'content'
    name = "fnordy fnord"
    fname = os.path.join(draftin_a_flask.ROOT,
                         draftin_a_flask.CONTENT,
                         name.replace(' ', '-') + '.md')

    draftin_a_flask.publish(name, 'This is some *content*')

    is_file = os.path.isfile(fname)
    assert is_file


def test_publish_should_actually_write_content():
    draftin_a_flask.subprocess = MagicMock()
    draftin_a_flask.CONTENT = 'fnord'
    expected_content = "This is some sweet *content*"
    name = "fnordy fnord"
    fname = os.path.join(draftin_a_flask.ROOT,
                         draftin_a_flask.CONTENT,
                         name.replace(' ', '-') + '.md')

    draftin_a_flask.publish(name, expected_content)

    with open(fname) as f:
        actual_content = f.read()
        assert actual_content == expected_content

    shutil.rmtree(os.path.join(draftin_a_flask.ROOT, draftin_a_flask.CONTENT))


def test_passing_content_to_publish_should_call_pelican():
    draftin_a_flask.subprocess = MagicMock()
    expected = [call.check_output([draftin_a_flask.PELICAN,
                                   draftin_a_flask.CONTENT, 
                                   '-o', 
                                   draftin_a_flask.OUTPUT,
                                   '-s',
                                   draftin_a_flask.PELICANCONF]),
                ]

    draftin_a_flask.publish('a name', 'This is some content')

    assert draftin_a_flask.subprocess.mock_calls == expected


def test_if_environment_values_are_set_they_should_be_preferred():
    pelicanconf = 'repelicant'
    pelican = 'pelican or pelicant?'
    content = "Well isn't that special?"
    output = 'Buuuuuurrrrp' # get it?
    os.environ['DIF_PELICANCONF'] = pelicanconf
    os.environ['DIF_PELICAN'] = pelican
    os.environ['DIF_CONTENT'] = content
    os.environ['DIF_OUTPUT'] = output

    reload(draftin_a_flask)

    assert draftin_a_flask.PELICANCONF == pelicanconf
    assert draftin_a_flask.PELICAN == pelican
    assert draftin_a_flask.CONTENT == content
    assert draftin_a_flask.OUTPUT == output


def test_if_draftican_file_is_present_it_should_read_conf_values():
    with open('.draftican', 'w') as f:
        f.write(json.dumps(dict(OUTPUT='output',
                                CONTENT='content',
                                PELICAN='pelican',
                                PELICANCONF='pelicanconf')))

    reload(draftin_a_flask)
    os.unlink('.draftican')

    assert draftin_a_flask.PELICANCONF == 'pelicanconf'
    assert draftin_a_flask.PELICAN == 'pelican'
    assert draftin_a_flask.CONTENT == 'content'
    assert draftin_a_flask.OUTPUT == 'output'
