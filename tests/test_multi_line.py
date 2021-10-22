import json


def test_multiline_call():
    """This is harder to setup as a test case, so we only have one

    This test checks to validate that multiple lines are extracted.

    Black might span multiple rows within the code; the initial design
    did not handle multi-line calls.

    """
    from termlog import format

    output = json.loads(
        format(
            f"A super, duper, really, fantastically, long, colorful message so that black won't refactor this into one line!",
            json=True,
            color=False,
            add_timestamp=False,
        )
    )
    assert output == {
        "data": f"A super, duper, really, fantastically, long, colorful message so that black won't refactor this into one line!",
        "output": None,
    }
