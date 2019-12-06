def test_multilayer_calls():
    """This is harder to setup as a test case, so we only have one"""
    import json
    from termlog import format, red

    message = 'green'
    output = json.loads(format(f'A {red(message)} message!', json=True, color=False, add_timestamp=False))
    assert output == {'data': 'A green message!', 'message': 'green'}
