===============================
Draft in a Flask
===============================

.. image:: https://badge.fury.io/py/draftin_a_flask.png
    :target: http://badge.fury.io/py/draftin_a_flask
    
.. image:: https://travis-ci.org/waynew/draftin-a-flask.png?branch=master
        :target: https://travis-ci.org/waynew/draftin-a-flask

.. image:: https://pypip.in/d/draftin_a_flask/badge.png
        :target: https://crate.io/packages/draftin_a_flask?version=latest


A simple Flask server that allows you to publish Pelican blags from 
http://draftin.com using `WebHooks`_

.. _WebHooks: https://draftin.com/documents/69898?token=5fjKKlZ0-AeBzqj_RAftAGdzRzl9VBfBHj5wpSWm_gU)

* Free software: BSD license
* Documentation: http://draftin_a_flask.rtfd.org.

Usage
-----

::

    $ pip install draftin_a_flask
    $ env DIF_CONTENT=/path/to/content \
    DIF_OUTPUT=/path/to/output \
    DIF_PELICAN=/path/to/pelican_binary draftican
    Listening at endpoint QRFky1tR0KqHGM3cJoitwEi8tTpknaNnMpNHHiTIm8
    * Running on http://0.0.0.0:5678/
    * Restarting with reloader
    Listening at endpoint QRFky1tR0KqHGM3cJoitwEi8tTpknaNnMpNHHiTIm8
    
(Yes, it displays the print twice :-\\ I'm sure there's a way to get around it. If
it bothers you too much, I accept pull requests!

Setup your WebHook from within Draft, and now you can write your blog posts in
Draft and easily publish.


Future Features
---------------

* Automatic uploads using rsync/ssh/file copy
* Settings provided in a file
* Improved error handling (e.g. missing title, etc.)


Known Bugs
----------

* If you're missing important fields (like title and date) it probably will
  skip publishing that doc.
