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
if os.path.isfile('.draftican'):
    with open('.draftican') as f:
        data = json.load(f)
        os.environ['DIF_OUTPUT'] = data.get('OUTPUT')
        os.environ['DIF_CONTENT'] = data.get('CONTENT')
        os.environ['DIF_PELICAN'] = data.get('PELICAN')
        os.environ['DIF_PELICANCONF'] = data.get('PELICANCONF')

OUTPUT = os.environ.get('DIF_OUTPUT', 'path/to/output')
CONTENT = os.environ.get('DIF_CONTENT', 'path/to/input')
PELICAN = os.environ.get('DIF_PELICAN', '/path/to/pelican')
PELICANCONF = os.environ.get('DIF_PELICANCONF', '/path/to/pelicanconf.py')
ROOT = os.path.dirname(os.path.abspath(__file__))
SECRET_FILE = os.path.join(ROOT, 's3kret.key')


def setup():
    if not os.path.isfile(SECRET_FILE):
        with open(SECRET_FILE, 'w') as f:
            f.write(''.join(utils.random_string(size=42)))

setup()
with open(SECRET_FILE) as f:
    app.secret_key = f.read()


@app.route('/'+app.secret_key, methods=['POST'])
def main():
    data = json.loads(request.data.decode())
    name = data.get('name')
    content = data.get('content')
    #if content is None:
    #    return 'Missing content', 500
    publish(name, content)
    return "OK"


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
                                      OUTPUT,
                                      '-s',
                                      PELICANCONF])


if __name__ == "__main__":
    app.run('0.0.0.0', port=5678, debug=True)
