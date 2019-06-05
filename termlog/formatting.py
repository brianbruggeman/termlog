import textwrap
from pathlib import Path
from typing import Any, Optional, Union

from .message import Message
from .styles import SolarizedStyle
from .vendored import pygments
from .vendored.pygments.formatters import get_formatter_by_name
from .vendored.pygments.lexer import Lexer
from .vendored.pygments.lexers import get_lexer_by_name, guess_lexer

__all__ = ('beautify', 'format')


def beautify(message: Any, indent: int = 0, lexer: Optional[Union[pygments.lexer.Lexer, str]] = None):
    """Beautify *message*.

    Args:
        message: message to beautify
        indent: number of spaces to indent
        lexer: message lexical analyzer

    Returns:
        str: beautified message

    """
    formatter = get_formatter_by_name('256', style=SolarizedStyle)

    indent = max(int(indent or 0), 0)
    if isinstance(message, Path):
        message = str(message)
    elif isinstance(message, bytes):
        message = message.decode('utf-8')

    single = False
    if isinstance(message, str):
        single = len(message) - len(message.rstrip('\n')) == 0

    if isinstance(message, Exception):
        lexer = lexer or 'py3tb'

    if isinstance(lexer, str):
        lexer = get_lexer_by_name(lexer)

    if not lexer and isinstance(message, str):
        lexer = guess_lexer(message, stripall=True) if lexer is None else lexer

    if lexer and isinstance(message, str):
        messages = message.split('\n')
        for index, message in enumerate(messages):
            message = pygments.highlight(message, lexer, formatter)
            messages[index] = message.strip()
        message = '\n'.join(messages)
    if indent > 0:
        message = textwrap.indent(message, ' ' * indent)
    return message.rstrip('\n') if single and isinstance(message, str) else message


def format(*messages: Any,
           lexer: Optional[Union[Lexer, str]] = None,
           color: bool = None,
           json: bool = None,
           time_format: Optional[str] = None,
           string_format: Optional[str] = None,
           add_timestamp: bool = False,
           ) -> str:
    """Echo *message*.

    lexers can be passed in, and if they are, the resulting output
    will attempt to be setup

    Args:
        messages: messages to echo
        color: colorize output
        lexer: message lexical analyzer
        json: Dump out a structured text
        time_format: control time format
        string_format: control string format
        add_timestamp: add a timestamp to the output

    Returns:
        Tuple[str]: beautified messages

    """
    # Allows echo to be used in settings and prevents circular dependencies
    string = ''
    for index, message in enumerate(messages):
        message = Message(data=message, lexer=str(lexer) if lexer else '', json=json, color=color, time_format=time_format, string_format=string_format)
        if index == 0:
            if not json and add_timestamp:
                # ts = message.timestamp.strftime(message.time_format)
                msg = f'{message.timestamp} '
                string = msg
        elif index > 0:
            if not json:
                msg = ' '
                string += msg
        string += message
    string = str(string)
    return string
