# -*- coding: utf-8 -*-
"""
    pygments.lexers.text
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for non-source code file types.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexers.configs import (
    ApacheConfLexer,
    IniLexer,
    LighttpdConfLexer,
    NginxConfLexer,
    PropertiesLexer,
    RegeditLexer,
    SquidConfLexer
)
from pygments.lexers.console import PyPyLogLexer
from pygments.lexers.data import YamlLexer
from pygments.lexers.diff import DarcsPatchLexer, DiffLexer
from pygments.lexers.haxe import HxmlLexer
from pygments.lexers.installers import DebianControlLexer, SourcesListLexer
from pygments.lexers.make import BaseMakefileLexer, CMakeLexer, MakefileLexer
from pygments.lexers.markup import BBCodeLexer, GroffLexer, MoinWikiLexer, RstLexer, TexLexer
from pygments.lexers.sgf import SmartGameFormatLexer
from pygments.lexers.textedit import VimLexer
from pygments.lexers.textfmts import GettextLexer, HttpLexer, IrcLogsLexer

__all__ = []
