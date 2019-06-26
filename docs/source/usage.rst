=====
Usage
=====

A simple example can be found below.

.. code-block:: python3

    from termlog import Color, echo, set_config

    set_config(color=True, json=False, timestamp=False)

    solarized_red = Color(red=220, green=50, blue=47)
    solarized_magenta = Color(red=221, green=54, blue=130)

    msg = ...
    echo(f'{solarized_red("ERROR")}: {solarized_magenta(msg)}')


The default colors are setup by the default palette.  These are
controlled at the module level.  So if a new default palette is
desired, the following code is probably a better representation
of how to set that up.

.. code-block:: python3

    >>> import termlog
    >>> import termlog.palettes

    # Using default palette
    >>> termlog.red('hi')
    '\x1b[31mhi\x1b[0m'
    >>> termlog.red('hi', truecolor=True)
    '\x1b[38;2;170;0;0mhi\x1b[0m'
    >>> termlog.base0('hi', truecolor=True)
    AttributeError ...

    # Using a different palette
    >>> termlog.set_palette(termlog.palettes.SolarizedDark())
    >>> termlog.red('hi')
    '\x1b[31mhi\x1b[0m'
    >>> termlog.red('hi', truecolor=True)
    '\x1b[38;2;220;50;47mhi\x1b[0m'
    >>> termlog.base0('hi', truecolor=True)
    '\x1b[38;2;131;148;150mhi\x1b[0m'
