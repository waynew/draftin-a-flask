#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import re
import json
import subprocess
from . import utils
from flask import Flask, request

app = Flask(__name__)
OUTPUT = 'output'
CONTENT = 'content'
ROOT = os.path.dirname(os.path.abspath(__file__))
SECRET_FILE = os.path.join(ROOT, 's3kret.key')
PELICAN = '/path/to/pelican'


def setup():
    if not os.path.isfile(SECRET_FILE):
        with open(SECRET_FILE, 'w') as f:
            f.write(''.join(utils.random_string(size=42)))

setup()
with open(SECRET_FILE) as f:
    app.secret_key = f.read()


@app.route('/'+app.secret_key, methods=['POST'])
def main():
    data = json.loads(request.data)
    content = data.get('content')
    #if content is None:
    #    return 'Missing content', 500
    publish(content)


def publish(name, content):
    name = re.sub('[^a-zA-Z]', '-', name) + '.md'
    dir_ = os.path.join(ROOT, CONTENT)
    if not os.path.exists(dir_):
        os.makedirs(dir_)
    fname = os.path.join(dir_, name)
    with open(fname, 'w') as f:
        f.write(content)
    output = subprocess.check_output([PELICAN,
                                      CONTENT, 
                                      '-o', 
                                      OUTPUT])
