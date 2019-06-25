"""Color module

Contains resources to build 256 (standard) and 16m (true-color) text
output.

"""
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

from .decorations import factory

__all__ = (
    'bright_black',
    'dim_black',
    'black',
    'bright_blue',
    'dim_blue',
    'blue',
    'bright_cyan',
    'dim_cyan',
    'cyan',
    'bright_green',
    'dim_green',
    'green',
    'grey',
    'bright_magenta',
    'dim_magenta',
    'magenta',
    'rgb',
    'bright_red',
    'dim_red',
    'red',
    'bright_yellow',
    'dim_yellow',
    'yellow',
    'bright_white',
    'dim_white',
    'white',
    'Color'
    )


_colors: Dict[Tuple[int, int, int], 'Color'] = {}


# This will get updated below, see: _true_color_supported
def true_color_supported() -> bool:
    """Check if truecolor is supported by the current tty.

    Note: this currently only checks to see if COLORTERM contains
          one of the following enumerated case-sensitive values:
             - truecolor
             - 24bit

    """
    color_term = os.getenv('COLORTERM', '')
    return True if any(check in color_term for check in ['truecolor', '24bit']) else False


TRUE_COLOR_SUPPORTED = true_color_supported()
ESCAPE: str = '\x1b'

# style codes
#  Not all of these are supported within all terminals
BRIGHT: str = f'{ESCAPE}[1m'
DIM: str = f'{ESCAPE}[2m'
ITALIC: str = f'{ESCAPE}[3m'
UNDERLINED: str = f'{ESCAPE}[4m'
BLINK: str = f'{ESCAPE}[5m'
STROBE: str = f'{ESCAPE}[6m'
INVERTED: str = f'{ESCAPE}[7m'
HIDDEN: str = f'{ESCAPE}[8m'
STRIKE_THROUGH: str = f'{ESCAPE}[9m'
DOUBLE_UNDERLINE: str = f'{ESCAPE}[21m'


@factory(names=['red', 'green', 'blue'], repository=_colors)  # look up color by rgb value
# @factory(names=['name'], repository=_colors)  # look up color by name
@dataclass
class Color:
    """A data structure for packaging up Color display information

    Example:
        >>> from termlog import Color, echo
        >>> solarized_red = Color(red=220, green=50, blue=47)
        >>> solarized_magenta = Color(red=221, green=54, blue=130)
        >>> msg = ...
        >>> echo(f'{solarized_red("ERROR")}: {solarized_magenta(msg)}')

    Attributes:
        red: the value for the red aspect of the color [0-255]
        green: the value for the green aspect of the color [0-255]
        blue: the value for the blue aspect of the color [0-255]
        color_prefix: the string prefix when true-color is not enabled
        true_color_prefix: the string prefix for when true-color is enabled
        suffix: the reset suffix
        truecolor: enables true color when True
        bright: a bold/bright version of the color
        dim: a dim version of the color
        italic: an italic version of the color
        underlined: an underlined version of the message

    """
    red: int = 0
    green: int = 0
    blue: int = 0
    color_prefix: str = ''
    true_color_prefix: str = f'{ESCAPE}[38;2;{{red}};{{green}};{{blue}}m'
    suffix: str = f'{ESCAPE}[0m'
    truecolor: bool = TRUE_COLOR_SUPPORTED
    name: str = ''

    # style attributes
    dim: bool = False
    bright: bool = False
    italic: bool = False
    underline: bool = False
    blink: bool = False
    inverted: bool = False
    hidden: bool = False
    strobe: bool = False

    def __post_init__(self):
        # Cap red, green and blue to integer values
        self.red = max(min(int(self.red or 0), 255), 0)
        self.green = max(min(int(self.green or 0), 255), 0)
        self.blue = max(min(int(self.blue or 0), 255), 0)

        self.true_color_prefix = self.true_color_prefix.format(red=self.red, green=self.green, blue=self.blue)
        if not self.color_prefix:
            self.color_prefix = self.true_color_prefix

    def __hash__(self):
        return hash((self.red, self.green, self.blue))

    def __call__(self, message: Any, color: bool = True, truecolor: Optional[bool] = None) -> str:
        """Colors a message

        Args:
            color: flag to disable color entirely
            truecolor: flag to explicitly enable truecolor

        Returns:
            message with escape sequences for terminal colors

        """
        truecolor = self.truecolor if truecolor is None else truecolor
        colored_message = message
        prefix = ''
        if truecolor:
            prefix = self.true_color_prefix
        elif color:
            prefix = self.color_prefix
        if prefix:
            if self.hidden:
                prefix += HIDDEN
            else:
                if self.dim and not truecolor:
                    prefix += DIM
                elif self.bright and not truecolor:
                    prefix += BRIGHT
                if self.italic:
                    prefix += ITALIC
                if self.underline:
                    prefix += UNDERLINED
                if self.blink:
                    prefix += BLINK
                if self.strobe:
                    prefix += STROBE
            colored_message = f'{prefix}{message}{self.suffix}'
        return colored_message

    def __eq__(self, other):
        return id(self) == id(other)

    def __getitem__(self, item):
        if item in ('red', 'green', 'blue'):
            return getattr(self, item)
        else:
            raise KeyError(f'Could not find {item} in {self}')

    @staticmethod
    def keys():
        return ('red', 'green', 'blue')

    @staticmethod
    def __len__():
        return 3

    def __iter__(self):
        for name in ('red', 'green', 'blue'):
            yield getattr(self, name)


# Set simple terminal colors
#  Default colors here do not follow a standard.
#  TODO: Create a palette and initialize colors with a palette
black = Color(50, 50, 50, color_prefix=f'{ESCAPE}[30m', name='black', truecolor=False)
red = Color(170, 0, 0, color_prefix=f'{ESCAPE}[31m', name='red', truecolor=False)
green = Color(0, 170, 0, color_prefix=f'{ESCAPE}[32m', name='green', truecolor=False)
yellow = Color(170, 170, 0, color_prefix=f'{ESCAPE}[33m', name='yellow', truecolor=False)
blue = Color(0, 0, 170, color_prefix=f'{ESCAPE}[34m', name='blue', truecolor=False)
magenta = Color(170, 0, 170, color_prefix=f'{ESCAPE}[35m', name='magenta', truecolor=False)
cyan = Color(0, 170, 170, color_prefix=f'{ESCAPE}[36m', name='cyan', truecolor=False)
white = Color(128, 128, 128, color_prefix=f'{ESCAPE}[37m', name='white', truecolor=False)

dim_black = Color(0, 0, 0, color_prefix=f'{ESCAPE}[30m', name='dim black', dim=True, truecolor=False)
dim_red = Color(85, 0, 0, color_prefix=f'{ESCAPE}[31m', name='dim red', dim=True, truecolor=False)
dim_green = Color(0, 85, 0, color_prefix=f'{ESCAPE}[32m', name='dim green', dim=True, truecolor=False)
dim_yellow = Color(85, 85, 0, color_prefix=f'{ESCAPE}[33m', name='dim yellow', dim=True, truecolor=False)
dim_blue = Color(0, 0, 85, color_prefix=f'{ESCAPE}[34m', name='dim blue', dim=True, truecolor=False)
dim_magenta = Color(85, 0, 85, color_prefix=f'{ESCAPE}[35m', name='dim magenta', dim=True, truecolor=False)
dim_cyan = Color(0, 85, 85, color_prefix=f'{ESCAPE}[36m', name='dim cyan', dim=True, truecolor=False)
dim_white = Color(85, 85, 85, color_prefix=f'{ESCAPE}[37m', name='dim white', dim=True, truecolor=False)
grey = dim_white

bright_black = Color(60, 60, 60, color_prefix=f'{ESCAPE}[90m', name='bright black', truecolor=False)
bright_red = Color(255, 85, 85, color_prefix=f'{ESCAPE}[91m', name='bright red', truecolor=False)
bright_green = Color(85, 255, 85, color_prefix=f'{ESCAPE}[92m', name='bright green', truecolor=False)
bright_yellow = Color(255, 255, 85, color_prefix=f'{ESCAPE}[93m', name='bright yellow', truecolor=False)
bright_blue = Color(85, 85, 255, color_prefix=f'{ESCAPE}[94m', name='bright blue', truecolor=False)
bright_magenta = Color(255, 85, 255, color_prefix=f'{ESCAPE}[95m', name='bright magenta', truecolor=False)
bright_cyan = Color(85, 255, 255, color_prefix=f'{ESCAPE}[96m', name='bright cyan', truecolor=False)
bright_white = Color(255, 255, 255, color_prefix=f'{ESCAPE}[97m', name='bright white', truecolor=False)


def rgb(message: Any, red: int = 0, green: int = 0, blue: int = 0, color: bool = True, truecolor: Optional[bool] = None) -> str:
    """Add any true color to *message*.

    Example:
        >>> from termlog import echo, rgb, Color
        >>> c = Color(red=223, green=81, blue=127)
        >>> print(f'{c!r}')
        Color(red=223, green=81, blue=127, color_prefix='', true_color_prefix='{ESCAPE}[38;2;{red};{green};{blue}m', suffix='{ESCAPE}[0m', truecolor=False)
        >>> f'A {rgb("colored", **c)} message'
        'A {ESCAPE}[38;2;223;81;127mcolored{ESCAPE}[0m message'

    Note: this only works if the terminal supports true color and there
          is no way to definitively determine if truecolor is supported
          by the terminal.

    Args:
        message: text to color
        red: red portion of color [0 to 255]
        green: green portion of color [0 to 255]
        blue: blue portion of color [0 to 255]
        color: enable color on output

    Returns:
        Colored text if color is enabled

    """
    truecolor = TRUE_COLOR_SUPPORTED if truecolor is None else truecolor
    _color = Color(red=red, green=green, blue=blue, truecolor=truecolor)
    return _color(message, color)
