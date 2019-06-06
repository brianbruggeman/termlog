=====
Usage
=====

.. code-block:: python3

    from termlog import Color, echo, set_config

    set_config(color=True, json=False, timestamp=False)

    solarized_red = Color(red=220, green=50, blue=47)
    solarized_magenta = Color(red=221, green=54, blue=130)

    msg = ...
    echo(f'{solarized_red("ERROR")}: {solarized_magenta(msg)}')
