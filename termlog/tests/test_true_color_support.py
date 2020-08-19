from dataclasses import dataclass

import pytest


@dataclass
class TC:
    value: str = ""
    varname: str = "COLORTERM"
    expected: bool = False


test_cases = [
    TC(),
    TC("24bit", expected=True),
    TC("24BIT", expected=False),
    TC("truecolor", expected=True),
    TC("TRUECOLOR", expected=False),
]


@pytest.mark.parametrize("test_case", test_cases, ids=list(map(str, test_cases)))
def test_true_color_support(test_case):
    from ..constants import true_color_supported

    assert true_color_supported(env={test_case.varname: test_case.value}) == test_case.expected
