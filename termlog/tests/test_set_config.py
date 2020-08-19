from dataclasses import asdict, dataclass
from typing import Optional

import pytest


@dataclass
class TC:
    color: bool = True
    json: bool = False
    time_format: str = "%Y%m%d%H%M%S"
    timestamp: Optional[bool] = None

    def __getitem__(self, item):
        data = asdict(self)
        return data[item]

    def keys(self):
        data = asdict(self)
        return data.keys()


test_cases = [
    TC(),
    TC(color=False),
    TC(color=True),
    TC(json=True),
    TC(json=False),
    TC(time_format="%Y/%m/%d %H:%M:%S"),
    TC(timestamp=False),
    TC(timestamp=True),
]


@pytest.mark.parametrize("test_case", test_cases, ids=list(map(str, test_cases)))
def test_true_color_support(test_case):
    from .. import config

    default = config.TerminalConfig()
    config.set_config(**default)

    expected = config.TerminalConfig(**test_case)
    assert expected == config.set_config(**test_case)
    assert config._terminal_config == expected
