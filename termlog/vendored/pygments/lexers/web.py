# -*- coding: utf-8 -*-
"""
    pygments.lexers.web
    ~~~~~~~~~~~~~~~~~~~

    Just export previously exported lexers.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexers.actionscript import ActionScript3Lexer, ActionScriptLexer, MxmlLexer
from pygments.lexers.css import CssLexer, SassLexer, ScssLexer
from pygments.lexers.data import JsonLexer
from pygments.lexers.html import DtdLexer, HamlLexer, HtmlLexer, JadeLexer, ScamlLexer, XmlLexer, XsltLexer
from pygments.lexers.javascript import (
    CoffeeScriptLexer,
    DartLexer,
    JavascriptLexer,
    LassoLexer,
    LiveScriptLexer,
    ObjectiveJLexer,
    TypeScriptLexer
)
from pygments.lexers.php import PhpLexer
from pygments.lexers.webmisc import DuelLexer, QmlLexer, SlimLexer, XQueryLexer

JSONLexer = JsonLexer  # for backwards compatibility with Pygments 1.5

__all__ = []
