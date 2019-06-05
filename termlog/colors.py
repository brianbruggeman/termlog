import os
from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple
from .decorations import factory


__all__ = (
    'black', 'blue', 'cyan', 'green', 'grey', 'magenta', 'rgb', 'red',
    'yellow', 'white'
    )


_colors: Dict[Tuple[int, int, int], 'Color'] = {}


# This will get updated below, see: _true_color_supported
TRUE_COLOR_SUPPORTED = False


@factory(names=['red', 'green', 'blue'], repository=_colors)
@dataclass
class Color:
    red: int = 0
    green: int = 0
    blue: int = 0
    color_prefix: str = ''
    true_color_prefix: str = '\x1b[38;2;{red};{green};{blue}m'
    suffix: str = '\x1b[0m'
    true_color: bool = TRUE_COLOR_SUPPORTED

    def __post_init__(self):
        # cap red, green and blue
        self.red = max(min(int(self.red or 0), 255), 0)
        self.green = max(min(int(self.green or 0), 255), 0)
        self.blue = max(min(int(self.blue or 0), 255), 0)

    def __call__(self, message: Any, color: bool = True) -> str:
        if color:
            true_color_prefix = self.true_color_prefix.format(**asdict(self))
            prefix = true_color_prefix if self.true_color else (self.color_prefix or true_color_prefix)
            return f'{prefix}{message}{self.suffix}'
        else:
            return f'{message}'

    def __eq__(self, other):
        return id(self) == id(other)

    def __len__(self):
        return 3

    def __iter__(self):
        yield self.red
        yield self.green
        yield self.blue


# Set simple terminal colors
BLACK = Color(0, 0, 0, color_prefix='\1xb[30m')
RED = Color(255, 0, 0, color_prefix='\1xb[31m')
GREEN = Color(0, 255, 0, color_prefix='\1xb[32m')
YELLOW = Color(255, 255, 0, color_prefix='\1xb[33m')
BLUE = Color(0, 0, 255, color_prefix='\1xb[33m')
MAGENTA = Color(255, 0, 255, color_prefix='\1xb[35m')
CYAN = Color(0, 255, 255, color_prefix='\1xb[36m')
WHITE = Color(255, 255, 255, color_prefix='\1xb[37m')
GREY = Color(127, 127, 127, color_prefix='\1xb[37m\1xb[2m')


def black(message: Any, color: bool = True) -> str:
    """Add black color to *message*.

    Args:
        message: text to color
        color: enable color on output

    Returns:
        Colored text if color is enabled

    """
    return rgb(message=message, color=color)


def blue(message: Any, color: bool = True) -> str:
    """Add blue color to *message*.

    Args:
        message: text to color
        color: enable color on output

    Returns:
        Colored text if color is enabled

    """
    return rgb(message=message, color=color, blue=255)


def cyan(message: Any, color: bool = True) -> str:
    """Add cyan color to *message*.

    Args:
        message: text to color
        color: enable color on output

    Returns:
        Colored text if color is enabled

    """
    return rgb(message=message, color=color, green=255, blue=255)


def green(message: Any, color: bool = True) -> str:
    """Add green color to *message*.

    Args:
        message: text to color
        color: enable color on output

    Returns:
        Colored text if color is enabled

    """
    return rgb(message=message, color=color, green=255)


def grey(message: Any, color: bool = True) -> str:
    """Add grey color to *message*.

    Args:
        message: text to color
        color: enable color on output

    Returns:
        Colored text if color is enabled

    """
    return rgb(message=message, color=color, red=127, green=127, blue=127)


def magenta(message: Any, color: bool = True) -> str:
    """Add orange color to *message*.

    Args:
        message: text to color
        color: enable color on output

    Returns:
        Colored text if color is enabled

    """
    return rgb(message=message, color=color, red=255, blue=255)


def rgb(message: Any, red: int = 0, green: int = 0, blue: int = 0, color: bool = True) -> str:
    """Add any rgb color to *message*.

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
    _color = Color(red=red, green=green, blue=blue)
    return _color(message, color)


def red(message: Any, color: bool = True) -> str:
    """Add red color to *message*.

    Args:
        message: text to color
        color: enable color on output

    Returns:
        Colored text if color is enabled

    """
    return rgb(message=message, color=color, red=255)


def yellow(message: Any, color: bool = True) -> str:
    """Add yellow color to *message*.

    Args:
        message: text to color
        color: enable color on output

    Returns:
        Colored text if color is enabled

    """
    return rgb(message=message, color=color, red=255, green=255)


def white(message: Any, color: bool = True) -> str:
    """Add white color to *message*.

    Args:
        message: text to color
        color: enable color on output

    Returns:
        Colored text if color is enabled

    """
    return rgb(message=message, color=color, red=255, green=255, blue=255)


def _check_for_true_color():
    global TRUE_COLOR_SUPPORTED
    color_term = os.getenv('COLORTERM', '')
    TRUE_COLOR_SUPPORTED = True if any(check in color_term for check in ['truecolor', '24bit']) else False


_check_for_true_color()
