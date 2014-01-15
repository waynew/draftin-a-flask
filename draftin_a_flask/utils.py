# -*- coding: utf-8 -*-
import random
import string

try:
    range = xrange
except NameError:
    pass

def random_string(size):
    for _ in range(size):
        yield random.choice(string.ascii_letters+string.digits)
