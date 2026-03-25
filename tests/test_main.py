import pytest

@pytest.fixture
def example():
    x = 3
    return x

def test_dummy(example):
    assert example == 3