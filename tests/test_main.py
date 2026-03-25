import pytest
from first_package.example import MyAnimate

@pytest.fixture
def example():
    x = 3
    return x

def test_dummy(example):
    assert example == 3

def test_distance():
    p1 = [0, 0]
    p2 = [3, 4]
    assert MyAnimate.distance(p1, p2) == 5
    assert MyAnimate.distance(p2, p1) == MyAnimate.distance(p1, p2)
    assert MyAnimate.distance(p2, p1).shape == (1,)
    assert MyAnimate.distance(p2, p2) == 0



