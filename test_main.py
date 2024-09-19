import pytest
from main import Calculator

def test_add():
    calc = Calculator()
    assert calc.add(10, 5) == 15

def test_subtract():
    calc = Calculator()
    assert calc.subtract(10, 5) == 5

def test_multiply():
    calc = Calculator()
    assert calc.multiply(10, 5) == 50

def test_divide():
    calc = Calculator()
    assert calc.divide(10, 5) == 2

def test_divide_by_zero():
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.divide(10, 0)
