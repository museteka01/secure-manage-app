from app.main import some_function

def test_sanity():
    assert 1 + 1 == 2

def test_some_function():
    result = some_function()
    assert result == "Hello, World!"
