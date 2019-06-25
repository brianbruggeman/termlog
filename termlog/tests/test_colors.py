from dataclasses import asdict, dataclass
from typing import Any, Optional

import pytest

from ..colors import true_color_supported

ESCAPE = '\x1b'
SUFFIX = 'm'

DIM = f'{ESCAPE}[2m'
PREFIX = f'{ESCAPE}['
RESET = f'{ESCAPE}[0m'
TRUEPREFIX = f'{ESCAPE}[38;2;'
TRUESUFFIX = f'{ESCAPE}[38;2;'


@dataclass
class ColorTestCase:
    func_name: str
    message: Any = ''
    color: Optional[bool] = None
    truecolor: Optional[bool] = true_color_supported()
    expected: str = ''

    def __str__(self):
        return ' '.join(f'{key}={value}' for key, value in asdict(self).items())


test_cases = [
    # standard uses
    ColorTestCase('black', message='hi', color=True, truecolor=False, expected=f'{PREFIX}30{SUFFIX}hi{RESET}'),
    ColorTestCase('red', message='hi', color=True, truecolor=False, expected=f'{PREFIX}31{SUFFIX}hi{RESET}'),
    ColorTestCase('green', message='hi', color=True, truecolor=False, expected=f'{PREFIX}32{SUFFIX}hi{RESET}'),
    ColorTestCase('yellow', message='hi', color=True, truecolor=False, expected=f'{PREFIX}33{SUFFIX}hi{RESET}'),
    ColorTestCase('blue', message='hi', color=True, truecolor=False, expected=f'{PREFIX}34{SUFFIX}hi{RESET}'),
    ColorTestCase('magenta', message='hi', color=True, truecolor=False, expected=f'{PREFIX}35{SUFFIX}hi{RESET}'),
    ColorTestCase('cyan', message='hi', color=True, truecolor=False, expected=f'{PREFIX}36{SUFFIX}hi{RESET}'),
    ColorTestCase('white', message='hi', color=True, truecolor=False, expected=f'{PREFIX}37{SUFFIX}hi{RESET}'),
    ColorTestCase('grey', message='hi', color=True, truecolor=False, expected=f'{PREFIX}37{SUFFIX}{DIM}hi{RESET}'),

    # truecolor uses
    ColorTestCase('black', message='hi', color=True, truecolor=True, expected=f'{TRUEPREFIX}50;50;50{SUFFIX}hi{RESET}'),
    ColorTestCase('blue', message='hi', color=True, truecolor=True, expected=f'{TRUEPREFIX}0;0;170{SUFFIX}hi{RESET}'),
    ColorTestCase('cyan', message='hi', color=True, truecolor=True, expected=f'{TRUEPREFIX}0;170;170{SUFFIX}hi{RESET}'),
    ColorTestCase('green', message='hi', color=True, truecolor=True, expected=f'{TRUEPREFIX}0;170;0{SUFFIX}hi{RESET}'),
    ColorTestCase('grey', message='hi', color=True, truecolor=True, expected=f'{TRUEPREFIX}85;85;85{SUFFIX}hi{RESET}'),
    ColorTestCase('magenta', message='hi', color=True, truecolor=True, expected=f'{TRUEPREFIX}170;0;170{SUFFIX}hi{RESET}'),
    ColorTestCase('red', message='hi', color=True, truecolor=True, expected=f'{TRUEPREFIX}170;0;0{SUFFIX}hi{RESET}'),
    ColorTestCase('yellow', message='hi', color=True, truecolor=True, expected=f'{TRUEPREFIX}170;170;0{SUFFIX}hi{RESET}'),
    ColorTestCase('white', message='hi', color=True, truecolor=True, expected=f'{TRUEPREFIX}128;128;128{SUFFIX}hi{RESET}'),

    # test uncolored uses
    ColorTestCase('black', message='hi', color=False, truecolor=False, expected='hi'),
    ColorTestCase('blue', message='hi', color=False, truecolor=False, expected='hi'),
    ColorTestCase('cyan', message='hi', color=False, truecolor=False, expected='hi'),
    ColorTestCase('green', message='hi', color=False, truecolor=False, expected='hi'),
    ColorTestCase('grey', message='hi', color=False, truecolor=False, expected='hi'),
    ColorTestCase('magenta', message='hi', color=False, truecolor=False, expected='hi'),
    ColorTestCase('red', message='hi', color=False, truecolor=False, expected='hi'),
    ColorTestCase('yellow', message='hi', color=False, truecolor=False, expected='hi'),
    ColorTestCase('white', message='hi', color=False, truecolor=False, expected='hi'),
    ]


@pytest.mark.parametrize('test_case', test_cases, ids=list(map(str, test_cases)))
def test_colors(test_case):
    from .. import colors

    func = getattr(colors, test_case.func_name)
    result = func(message=test_case.message, color=test_case.color, truecolor=test_case.truecolor)
    assert result == test_case.expected, f'TrueColor={test_case.truecolor} ({tuple(result)}) != ({tuple(test_case.expected)})'


@dataclass
class RgbColorTestCase:
    red: int = 0
    green: int = 0
    blue: int = 0
    message: Any = ''
    color: Optional[bool] = None
    truecolor: Optional[bool] = None

    def __str__(self):
        return ' '.join(f'{key}={value}' for key, value in asdict(self).items())


test_cases = [
    # black
    RgbColorTestCase(red=0, green=0, blue=0, message='hi', truecolor=True),
    # blue
    RgbColorTestCase(red=0, green=0, blue=255, message='hi', truecolor=True),
    # cyan
    RgbColorTestCase(red=0, green=255, blue=255, message='hi', truecolor=True),
    # green
    RgbColorTestCase(red=0, green=255, blue=0, message='hi', truecolor=True),
    # grey
    RgbColorTestCase(red=127, green=127, blue=127, message='hi', truecolor=True),
    # magenta
    RgbColorTestCase(red=255, green=0, blue=255, message='hi', truecolor=True),
    # red
    RgbColorTestCase(red=255, green=0, blue=0, message='hi', truecolor=True),
    # yellow
    RgbColorTestCase(red=255, green=255, blue=0, message='hi', truecolor=True),
    # white
    RgbColorTestCase(red=255, green=255, blue=255, message='hi', truecolor=True),

    # black
    RgbColorTestCase(red=0, green=0, blue=0, message='hi', truecolor=False),
    # blue
    RgbColorTestCase(red=0, green=0, blue=255, message='hi', truecolor=False),
    # cyan
    RgbColorTestCase(red=0, green=255, blue=255, message='hi', truecolor=False),
    # green
    RgbColorTestCase(red=0, green=255, blue=0, message='hi', truecolor=False),
    # grey
    RgbColorTestCase(red=127, green=127, blue=127, message='hi', truecolor=False),
    # magenta
    RgbColorTestCase(red=255, green=0, blue=255, message='hi', truecolor=False),
    # red
    RgbColorTestCase(red=255, green=0, blue=0, message='hi', truecolor=False),
    # yellow
    RgbColorTestCase(red=255, green=255, blue=0, message='hi', truecolor=False),
    # white
    RgbColorTestCase(red=255, green=255, blue=255, message='hi', truecolor=False),
    ]


@pytest.mark.parametrize('test_case', test_cases, ids=list(map(str, test_cases)))
def test_colors_rgb(test_case):
    from .. import colors

    prefix = f'\x1b[38;2;{test_case.red};{test_case.green};{test_case.blue}m'
    reset = f'\x1b[0m'
    expected = f'{prefix}{test_case.message}{reset}' if test_case.truecolor else f'{test_case.message}'

    result = colors.rgb(red=test_case.red, blue=test_case.blue, green=test_case.green, message=test_case.message, color=test_case.color, truecolor=test_case.truecolor)
    assert result == expected


def test_colors_factory():
    from .. import colors

    all_colors = {
        'BLACK': colors.black, 'RED': colors.red, 'GREEN': colors.green,
        'BLUE': colors.blue, 'CYAN': colors.cyan, 'MAGENTA': colors.magenta,
        'YELLOW': colors.yellow, 'WHITE': colors.white, 'GREY': colors.grey
        }

    new_colors = {
        'BLACK': [colors.Color(50, 50, 50), colors.Color(red=50, green=50, blue=50), colors.Color(50, 50, 50)],
        'RED': [colors.Color(red=170), colors.Color(red=170, green=0, blue=0), colors.Color(170, 0, 0)],
        'YELLOW': [colors.Color(red=170, green=170), colors.Color(red=170, green=170, blue=0)],
        'MAGENTA': [colors.Color(red=170, blue=170), colors.Color(red=170, green=0, blue=170)],
        'CYAN': [colors.Color(green=170, blue=170), colors.Color(red=0, green=170, blue=170)],
        'BLUE': [colors.Color(blue=170), colors.Color(red=0, green=0, blue=170)],
        'GREEN': [colors.Color(green=170), colors.Color(red=0, green=170, blue=0)],
        'WHITE': [colors.Color(red=128, green=128, blue=128), colors.Color(128, 128, 128)],
        'GREY': [colors.Color(red=85, green=85, blue=85), colors.Color(85, 85, 85)],
        }

    for index, color in enumerate(all_colors.values()):
        previous = list(all_colors.values())[index - 1]
        assert color != previous
        assert color.keys() == ('red', 'green', 'blue')

    for name, values in new_colors.items():
        original = all_colors[name]
        assert all([original == value for value in values]), f'{name}: {original} not equal to {values}'

    color = colors.Color()
    assert len(color) == 3
    assert list(color) == [0, 0, 0]
    assert list(color.keys()) == ['red', 'green', 'blue']
    for key in color.keys():
        assert color[key] == getattr(color, key)
    with pytest.raises(KeyError):
        assert color['not-a-key']
