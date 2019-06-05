from dataclasses import dataclass

from .vendored.pygments.style import Style
from .vendored.pygments.token import (
    Comment,
    Error,
    Generic,
    Keyword,
    Literal,
    Name,
    Number,
    Operator,
    Other,
    Punctuation,
    String,
    Text,
    Whitespace
)


@dataclass
class SolarizedStyle(Style):
    """
    Solarized Dark style, inspired by Schoonover.

    from: http://ethanschoonover.com/solarized
    """

    default_style: str = ''

    # 'dark' background tones
    base03: str = '#002b36'  # 15
    base02: str = '#073642'  # 20

    # content tones
    base01: str = '#586e75'  # 45
    base00: str = '#657b83'  # 50
    base0: str = '#839496'  # 60
    base1: str = '#93a1a1'  # 65

    # 'light' background tones
    base2: str = '#eee8d5'  # 92
    base3: str = '#fdf6e3'  # 97

    # accent colors
    yellow: str = '#b58900'  # split comp
    orange: str = '#cb4b16'  # compliment
    red: str = '#dc322f'  # triad
    magenta: str = '#d33682'  # tetrad
    violet: str = '#6c71c4'  # analogous
    blue: str = '#268bd2'  # monotone
    cyan: str = '#2aa198'  # analogous
    green: str = '#859900'  # tetrad

    background_color: str = base03

    # So it turns out that pygments doesn't handle dataclasses very well
    #  and assumes that the Class value (SolarizedStyle.styles) is accessible
    #  without actually instantiating the class.  Dataclasses require
    #  the usage of `field` for mutable values and doesn't make it accessible
    #  until the dataclass is instantiated.  As a consequence, pygments is
    #  not directly compatible with dataclasses.  The fix is to
    #  make styles unavailable to the 'dataclass' portion and simply to
    #  use a standard class level attribute assignment.
    styles = {
        Text: base0,
        Whitespace: base03,
        Error: red,
        Other: base0,
        Comment: f'italic {base01}',
        Comment.Multiline: f'italic {base01}',
        Comment.Preproc: f'italic {base01}',
        Comment.Single: f'italic {base01}',
        Comment.Special: f'italic {base01}',
        Keyword: green,
        Keyword.Constant: green,
        Keyword.Declaration: green,
        Keyword.Namespace: orange,
        Keyword.Pseudo: orange,
        Keyword.Reserved: green,
        Keyword.Type: green,
        Operator: base0,
        Operator.Word: green,
        Name: base1,
        Name.Attribute: base0,
        Name.Builtin: blue,
        Name.Builtin.Pseudo: f'bold {blue}',
        Name.Class: blue,
        Name.Constant: yellow,
        Name.Decorator: orange,
        Name.Entity: orange,
        Name.Exception: orange,
        Name.Function: blue,
        Name.Property: blue,
        Name.Label: base0,
        Name.Namespace: yellow,
        Name.Other: base0,
        Name.Tag: green,
        Name.Variable: orange,
        Name.Variable.Class: blue,
        Name.Variable.Global: blue,
        Name.Variable.Instance: blue,
        Number: cyan,
        Number.Float: cyan,
        Number.Hex: cyan,
        Number.Integer: cyan,
        Number.Integer.Long: cyan,
        Number.Oct: cyan,
        Literal: base0,
        Literal.Date: base0,
        Punctuation: base0,
        String: cyan,
        String.Backtick: cyan,
        String.Char: cyan,
        String.Doc: cyan,
        String.Double: cyan,
        String.Escape: orange,
        String.Heredoc: cyan,
        String.Interpol: orange,
        String.Other: cyan,
        String.Regex: cyan,
        String.Single: cyan,
        String.Symbol: cyan,
        Generic: base0,
        Generic.Deleted: base0,
        Generic.Emph: base0,
        Generic.Error: base0,
        Generic.Heading: base0,
        Generic.Inserted: base0,
        Generic.Output: base0,
        Generic.Prompt: base0,
        Generic.Strong: base0,
        Generic.Subheading: base0,
        Generic.Traceback: base0,
        }
