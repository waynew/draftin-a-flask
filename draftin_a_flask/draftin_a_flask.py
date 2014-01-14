#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
from . import utils
import json
from flask import Flask, request

app = Flask(__name__)
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
    data = json.loads(request.data)
    content = data.get('content')
    #if content is None:
    #    return 'Missing content', 500
    publish(content)


def publish(arg):
    pass
