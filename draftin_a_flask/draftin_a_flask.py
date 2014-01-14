#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

def setup():
    root = os.path.dirname(os.path.abspath(__file__))
    secret_file = os.path.join(root, 's3kret.key')
    if not os.path.isfile(secret_file):
        with open(secret_file, 'w') as f:
            f.write('')
