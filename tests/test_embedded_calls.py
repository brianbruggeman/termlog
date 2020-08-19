def test_simple_embedded_calls():
    """This is harder to setup as a test case, so we only have one

    Embedded calls have extra data embedded into f-strings.  So there
    may be multiple entry-points to termlog within a single format.

    This test explicitly checks to see if the multiple entry-points
    are captured and that embedded calls within f-strings will pull
    in the appropriate json-data.

    This first test only checks for the basic call to a known valid
    color within a palette.
    """
    import json

    from termlog import format, red

    message = "green"
    output = json.loads(format(f"A {red(message)} message!", json=True, color=False, add_timestamp=False))
    assert output == {"data": "A green message!", "message": "green"}
