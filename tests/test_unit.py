import pytest
from hole_pad_calc.unit import Unit

def test_unit_initialization():
    unit = Unit('in')
    assert unit.unit == 'in'

def test_invalid_unit_initialization():
    with pytest.raises(ValueError):
        Unit('invalid')

def test_conversion_in_to_mm():
    unit = Unit('in')
    result = unit.convert(1, 'mm')
    assert pytest.approx(result, 0.01) == 25.4

def test_conversion_mm_to_in():
    unit = Unit('mm')
    result = unit.convert(25.4, 'in')
    assert pytest.approx(result, 0.01) == 1.0

def test_conversion_mm_to_mil():
    unit = Unit('mm')
    result = unit.convert(25.4, 'mil')
    assert pytest.approx(result, 0.01) == 1000.0

def test_conversion_invalid():
    unit = Unit('in')
    with pytest.raises(ValueError):
        unit.convert(1, 'invalid')
