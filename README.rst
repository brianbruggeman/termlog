======
Readme
======

Termlog
=======

.. image:: http://img.shields.io/badge/license-MIT-brightgreen.svg
    :target: http://opensource.org/licenses/MIT

.. image:: https://badge.fury.io/py/termlog.svg
    :target: https://pypi.python.org/pypi/termlog

.. image:: https://travis-ci.org/brianbruggeman/termlog.svg
    :target: https://travis-ci.org/brianbruggeman/termlog

.. image:: https://codecov.io/gh/brianbruggeman/termlog/branch/develop/graph/badge.svg?token=y6xPnPtcdc
  :target: https://codecov.io/gh/brianbruggeman/termlog


Termlog: A terminal logging library for logging data both as lexed text or json


Motivation
==========

I love f-strings and I wanted a method of displaying
beautiful f-strings in command-line interfaces.
However, I needed a way of simultaneously creating a
developer friendly text log and producing structured
text that could be interpreted by a log-shipper in a
clustered environment.

Termlog will...

* wrap print statements with a new method, `echo`
* `echo` is fully compatible with print and is meant
  to be a drop-in replacement
* `echo` can immediately control: color, json,
  timestamp, time-format outputs on each invocation
* Alternatively, a `set_config` command can set the
  library to use a specific configuration for each subsequent call to `echo`


Usage
=====

.. code-block:: python

     from termlog import blue, echo, red, rgb, set_config

     key = 'abc'
     value = 123

     set_config(color=True, json=False)

     echo(f'{red(key)}: {blue(value)}')
     echo(f'{rgb(message=key, red=71, green=61, blue=139)}: {blue(value)}')
     echo(f'{key}: {blue(value)}', color=True)



Installation
============

To install termlog, simply run the following.

.. code-block:: bash

    $ pip install termlog


.. include::./CONTRIBUTING.rst

