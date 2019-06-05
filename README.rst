Motivation
----------

A library that can create either json-enabled output or colored, syntax-highlighted
output for production and development built on f-strings for use in a container
on a cluster where logging is shipped.


LICENSE
-------
MIT


Examples
--------

.. code-block:: python

    >>> import termlog
    >>> name = 'world'
    >>> termlog.echo(f'Hello, {name}', json=True, color=False)
    {message: 'Hello, world', name='world', timestamp='YYYY-MM-DD HH:MM:SS.msec'}

    >>> termlog.echo(f'Hello, {name}', json=False, color=True, add_timestamp=False)
    'Hello, world'

    >>> termlog.echo(f'Hello, {terminal.red(name)}')
    '2019-06-05 00:34:44.184216 Hello, \1xb[31mworld\1xb[0m'

    >>> command = 'ls -lashtr .'
    >>> terminal.echo(f'{command}', lexer='bash', add_timestamp=False)
    '\x1b[38;5;245mls\x1b[39m\x1b[38;5;245m \x1b[39m\x1b[38;5;245m-lashtr\x1b[39m\x1b[38;5;245m \x1b[39m\x1b[38;5;245m.\x1b[39m'

    >>> terminal.echo(f'{command}', lexer='bash', color=False, add_timestamp=False)
    'ls -lashtr .'


Installation
------------

.. code-block:: bash

    pip install termlog


Testing
-------

.. code-block:: bash

    pip install termlog[test]
    pytest

