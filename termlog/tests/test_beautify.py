from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import pytest


@dataclass
class BeautifyData:
    message: Any
    output: str = ''
    indent: int = 0
    lexer: Any = None


@pytest.mark.parametrize('test_data', [
    BeautifyData('a', output='\x1b[38;5;247ma\x1b[39m'),
    BeautifyData('ls', lexer='bash', output='\x1b[38;5;245mls\x1b[39m'),
    BeautifyData('SELECT * FROM some_table;', output='\x1b[38;5;100mSELECT\x1b[39m\x1b[38;5;245m \x1b[39m\x1b[38;5;245m*\x1b[39m\x1b[38;5;245m \x1b[39m\x1b[38;5;100mFROM\x1b[39m\x1b[38;5;245m \x1b[39m\x1b[38;5;247msome_table\x1b[39m\x1b[38;5;245m;\x1b[39m'),
    BeautifyData('SELECT * FROM some_table;', lexer='postgres', output='\x1b[38;5;100mSELECT\x1b[39m\x1b[38;5;245m \x1b[39m\x1b[38;5;245m*\x1b[39m\x1b[38;5;245m \x1b[39m\x1b[38;5;100mFROM\x1b[39m\x1b[38;5;245m \x1b[39m\x1b[38;5;247msome_table\x1b[39m\x1b[38;5;245m;\x1b[39m'),
    BeautifyData(
        '''\
          File "<stdin>", line 1, in <module>
        ''',
        lexer='py3tb',
        output='\x1b[38;5;166m \x1b[39m\x1b[38;5;166m \x1b[39m\x1b[38;5;166m \x1b[39m\x1b[38;5;166m \x1b[39m\x1b[38;5;166m \x1b[39m\x1b[38;5;166m \x1b[39m\x1b[38;5;166m \x1b[39m\x1b[38;5;166m \x1b[39m\x1b[38;5;166m \x1b[39m\x1b[38;5;166m \x1b[39m\x1b[38;5;166mF\x1b[39m\x1b[38;5;166mi\x1b[39m\x1b[38;5;166ml\x1b[39m\x1b[38;5;166me\x1b[39m\x1b[38;5;166m \x1b[39m\x1b[38;5;166m"\x1b[39m\x1b[38;5;166m<\x1b[39m\x1b[38;5;166ms\x1b[39m\x1b[38;5;166mt\x1b[39m\x1b[38;5;166md\x1b[39m\x1b[38;5;166mi\x1b[39m\x1b[38;5;166mn\x1b[39m\x1b[38;5;166m>\x1b[39m\x1b[38;5;166m"\x1b[39m\x1b[38;5;166m,\x1b[39m\x1b[38;5;166m \x1b[39m\x1b[38;5;166ml\x1b[39m\x1b[38;5;166mi\x1b[39m\x1b[38;5;166mn\x1b[39m\x1b[38;5;166me\x1b[39m\x1b[38;5;166m \x1b[39m\x1b[38;5;166m1\x1b[39m\x1b[38;5;166m,\x1b[39m\x1b[38;5;166m \x1b[39m\x1b[38;5;166mi\x1b[39m\x1b[38;5;166mn\x1b[39m\x1b[38;5;166m \x1b[39m\x1b[38;5;166m<\x1b[39m\x1b[38;5;166mm\x1b[39m\x1b[38;5;166mo\x1b[39m\x1b[38;5;166md\x1b[39m\x1b[38;5;166mu\x1b[39m\x1b[38;5;166ml\x1b[39m\x1b[38;5;166me\x1b[39m\x1b[38;5;166m>\x1b[39m\n\x1b[38;5;166m \x1b[39m\x1b[38;5;166m \x1b[39m\x1b[38;5;166m \x1b[39m\x1b[38;5;166m \x1b[39m\x1b[38;5;166m \x1b[39m\x1b[38;5;166m \x1b[39m\x1b[38;5;166m \x1b[39m\x1b[38;5;166m \x1b[39m',
        ),
    BeautifyData(Path('.'), output='\x1b[38;5;245m.\x1b[39m'),

    ])
def test_beautify(test_data):
    from ..formatting import beautify

    input_params = asdict(test_data)
    output = input_params.pop('output')
    result = beautify(**input_params)
    assert result == output, f'{result} did not match {output}, {(result,)}'
