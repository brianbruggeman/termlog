# -*- coding: utf-8 -*-
"""
    pygments.lexers.x10
    ~~~~~~~~~~~~~~~~~~~

    Lexers for the X10 programming language.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re

from pygments.lexer import RegexLexer
from pygments.token import Comment, Error, Keyword, Name, Number, Operator, Punctuation, String, Text

__all__ = ['X10Lexer']

class X10Lexer(RegexLexer):
    """
    For the X10 language.

    .. versionadded:: 0.1
    """

    name = 'X10'
    aliases = ['x10', 'xten']
    filenames = ['*.x10']
    mimetypes = ['text/x-x10']

    keywords = (
        'as', 'assert', 'async', 'at', 'athome', 'ateach', 'atomic',
        'break', 'case', 'catch', 'class', 'clocked', 'continue',
        'def', 'default', 'do', 'else', 'final', 'finally', 'finish',
        'for', 'goto', 'haszero', 'here', 'if', 'import', 'in',
        'instanceof', 'interface', 'isref', 'new', 'offer',
        'operator', 'package', 'return', 'struct', 'switch', 'throw',
        'try', 'type', 'val', 'var', 'when', 'while'
    )

    types = (
        'void'
    )

    values = (
        'false', 'null', 'self', 'super', 'this', 'true'
    )

    modifiers = (
        'abstract', 'extends', 'implements', 'native', 'offers',
        'private', 'property', 'protected', 'public', 'static',
        'throws', 'transient'
    )

    tokens = {
        'root': [
            (r'[^\S\n]+', Text),
            (r'//.*?\n', Comment.Single),
            (r'/\*(.|\n)*?\*/', Comment.Multiline),
            (r'\b(%s)\b' % '|'.join(keywords), Keyword),
            (r'\b(%s)\b' % '|'.join(types), Keyword.Type),
            (r'\b(%s)\b' % '|'.join(values), Keyword.Constant),
            (r'\b(%s)\b' % '|'.join(modifiers), Keyword.Declaration),
            (r'"(\\\\|\\"|[^"])*"', String),
            (r"'\\.'|'[^\\]'|'\\u[0-9a-fA-F]{4}'", String.Char),
            (r'.', Text)
        ],
    }
