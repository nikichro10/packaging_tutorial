import pytest
import numpy as np  
from  first_package.example import MyAnimate

@pytest.fixture
def example():
    x = 3
    return x

def test_dummy(example):
    assert example == 3

def test_distance():
    p1 = np.array([0, 0])
    p2 = np.array([3, 4])
    assert MyAnimate.distance(p1, p2) == 5
    assert MyAnimate.distance(p2, p1) == MyAnimate.distance(p1, p2)
    #assert MyAnimate.distance(p2, p1).shape == (1,)
    assert MyAnimate.distance(p2, p2) == 0

def test_update_model_bounds():
    model = MyAnimate(n=5)
    model.update_model()

    # positions must stay within [0, 1]
    assert np.all(model.r >= 0)
    assert np.all(model.r <= 1)

def test_model():
    model = MyAnimate(n=10)
    model.update_model()
    assert model.n == 10
    assert model.counter == 10




