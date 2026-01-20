import pytest
import calculator

def test_add():
    assert calculator.add(1, 2) == 3
    assert calculator.add(-1, 1) == 0
    assert calculator.add(0.5, 0.5) == 1.0

def test_subtract():
    assert calculator.subtract(5, 3) == 2
    assert calculator.subtract(1, 1) == 0
    assert calculator.subtract(0.5, 0.3) == 0.2

def test_multiply():
    assert calculator.multiply(2, 3) == 6
    assert calculator.multiply(-2, 3) == -6
    assert calculator.multiply(0.5, 2) == 1.0

def test_divide():
    assert calculator.divide(6, 2) == 3.0
    assert calculator.divide(5, 2) == 2.5
    assert calculator.divide(-6, 2) == -3.0

def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calculator.divide(5, 0)