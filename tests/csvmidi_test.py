from py_midicsv.midicsv import parse


def test_midicsv():
    parse("tests/sample.mid")
    assert True
