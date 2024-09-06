import pytest
from hole_pad_calc.measurement import Measurement
from hole_pad_calc.unit import Unit
from rich.text import Text

def test_measurement_initialization_with_float():
    m = Measurement(10.5, 'in')
    assert m.value == 10.5
    assert str(m.unit) == 'in'

def test_measurement_initialization_with_int():
    m = Measurement(10, 'mm')
    assert m.value == 10.0  # Value should be converted to float
    assert str(m.unit) == 'mm'

def test_measurement_initialization_with_unit_object():
    m = Measurement(10.5, Unit('mil'))
    assert m.value == 10.5
    assert str(m.unit) == 'mil'

def test_measurement_invalid_unit():
    with pytest.raises(ValueError):
        Measurement(10.5, 'invalid')

def test_addition_same_units():
    m1 = Measurement(10, 'in')
    m2 = Measurement(5, 'in')
    result = m1 + m2
    assert result.value == 15
    assert str(result.unit) == 'in'

def test_addition_different_units():
    m1 = Measurement(1, 'in')
    m2 = Measurement(25.4, 'mm')
    result = m1 + m2
    assert pytest.approx(result.value, 0.01) == 2
    assert str(result.unit) == 'in'

def test_subtraction_same_units():
    m1 = Measurement(10, 'mm')
    m2 = Measurement(5, 'mm')
    result = m1 - m2
    assert result.value == 5
    assert str(result.unit) == 'mm'

def test_multiplication_with_number():
    m = Measurement(10, 'in')
    result = m * 2
    assert result.value == 20
    assert str(result.unit) == 'in'

def test_multiplication_with_measurement():
    m1 = Measurement(10, 'in')
    m2 = Measurement(2, 'in')
    result = m1 * m2
    assert result.value == 20
    assert str(result.unit) == 'in'

def test_division_with_number():
    m = Measurement(10, 'mm')
    result = m / 2
    assert result.value == 5
    assert str(result.unit) == 'mm'

def test_division_with_measurement():
    m1 = Measurement(10, 'in')
    m2 = Measurement(2, 'in')
    result = m1 / m2
    assert result.value == 5
    assert str(result.unit) == 'in'

def test_floordiv_with_number():
    m = Measurement(10, 'mm')
    result = m // 3
    assert result.value == 3
    assert str(result.unit) == 'mm'

def test_conversion():
    m = Measurement(1, 'in')
    result = m.convert('mm')
    assert pytest.approx(result.value, 0.01) == 25.4

def test_rich_text():
    m = Measurement(10.5, 'in')
    result = m.rich()
    assert isinstance(result, Text)
