import pytest

#We can define the fixture functions in this testconfig file to make them accessible across multiple test files.

@pytest.fixture(autouse=True)
def input_pygamber_yas():
    input = 63
    return input
