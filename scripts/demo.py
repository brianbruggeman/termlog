"""This demo requires truecolor enabled to properly render.

If your terminal does not support truecolor or cannot correctly render
the colors, then the output is not determined to correctly display.

The color wheel should be a brilliant hsl wheel extending across the
screen mapping from a saturated bright value (bright white) down to a
saturated dark value (dim black)
"""
import colorsys
import os

from termlog import (
    Color,
    black,
    blue,
    bright_black,
    bright_blue,
    bright_cyan,
    bright_green,
    bright_magenta,
    bright_red,
    bright_white,
    bright_yellow,
    cyan,
    dim_black,
    dim_blue,
    dim_cyan,
    dim_green,
    dim_magenta,
    dim_red,
    dim_white,
    dim_yellow,
    echo,
    green,
    grey,
    magenta,
    red,
    white,
    yellow
)

colors = [
    bright_black,
    black,
    dim_black,

    bright_blue,
    blue,
    dim_blue,

    bright_cyan,
    cyan,
    dim_cyan,

    bright_green,
    green,
    dim_green,

    grey,

    bright_magenta,
    magenta,
    dim_magenta,

    bright_red,
    red,
    dim_red,

    bright_white,
    white,
    dim_white,

    bright_yellow,
    yellow,
    dim_yellow,
    ]


def build_color_wheel(columns=160, rows=15, symbol='■'):
    col_step = 255 // columns if columns else 10
    row_step = 255 // rows if rows else 10
    wheel = []

    hues = list(range(0, 255, col_step + 1))
    lightnesses = list(reversed(range(0, 255, row_step + 1)))

    for lightness in lightnesses:
        for hue in hues:
            original_space = tuple(map(lambda x: x / 255, (hue, lightness, 255)))
            rgb_space = tuple(map(lambda x: int(x * 255), colorsys.hls_to_rgb(*original_space)))
            color = Color(*rgb_space, truecolor=True)
            print(color(symbol), end='')
            wheel.append(color)
        print('')
    return wheel


if __name__ == '__main__':
    try:
        cols, rows = os.get_terminal_size()
    except OSError:
        cols, rows = 160, 15
    build_color_wheel(columns=cols)
    for color in colors:
        echo(f'{color.name:>15}: {color("color")} | {color("truecolor", truecolor=True)}')
