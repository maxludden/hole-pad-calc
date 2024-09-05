from typing import Optional, Union

from rich.console import Console
from rich.text import Text
from hole_pad_calc.unit import Unit

class Measurement:
    """Measurement of a hole or pad.

    Args:
        value (float): Value of the measurement
        unit (str or Unit, optional): Unit of the measurement. Defaults to 'in'.
    """

    def __init__(self, value: Union[float, int], unit: Optional[Union[str, Unit]] = None) -> None:
        self.unit = unit
        self.value = value

    @property
    def unit(self) -> Unit:
        return self._unit

    @unit.setter
    def unit(self, v: Optional[Union[str, Unit]]) -> None:
        if v is None:
            v = 'in'
        if isinstance(v, str):
            if v not in ['in', 'mm', 'mil']:
                raise ValueError(f"Unit must be 'in', 'mm', or 'mil'. Got {v}.")
            v = Unit(v)
        elif not isinstance(v, Unit):
            raise ValueError(f"Unit must be a string or Unit object. Got {type(v)}.")
        self._unit: Unit = v

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, v: Optional[Union[int, float]] = None) -> None:
        if isinstance(v, int):
            v = float(v)
        if not isinstance(v, float):
            raise ValueError(f"Value must be a numerical value (int or float). Got {type(v)}.")
        self._value = v

    @classmethod
    def __call__(cls, value: Union[float, int], unit: Optional[Union[str, Unit]] = 'in'):
        return cls(value=value, unit=unit)

    def __str__(self) -> str:
        return f"{self.value} {self.unit}"

    def __repr__(self) -> str:
        return f"Measurement<{self.value} {self.unit}>"

    def __int__(self) -> int:
        if isinstance(self.value, float) and not self.value.is_integer():
            raise ValueError(f"Cannot convert {self.value} to int as it is not an integer.")
        return int(self.value)

    def __float__(self) -> float:
        return float(self.value)

    def __rich__(self) -> Text:
        return self.rich()

    def __rich__repr__(self) -> Text:
        return Text.assemble(
            *[
                Text("Measurement", style="bold italic #0099ff"),
                Text("<", style="bold #cccccc"),
                self.rich(),
                Text(">", style="bold #cccccc")
            ]
        )

    def __add__(self, other: Union[int, float, "Measurement"]) -> 'Measurement':
        if isinstance(other, int):
            other = Measurement(float(other), self.unit)
            return Measurement(value=self.value + other.value, unit=self.unit)
        elif isinstance(other, float):
            other = Measurement(other, self.unit)
            return Measurement(value=self.value + other.value, unit=self.unit)
        elif isinstance(other, Measurement):
            if self.unit != other.unit:
                other.value = other.convert(str(self.unit))
                other.unit = str(self.unit)
            return Measurement(value=self.value + other.value, unit=self.unit)
        raise ValueError(f"Cannot add Measurement to {type(other)}.")

    def __sub__(self, other: 'Measurement') -> 'Measurement':
        if isinstance(other, int):
            other = Measurement(float(other), self.unit)
            return Measurement(value=self.value - other.value, unit=self.unit)
        elif isinstance(other, float):
            other = Measurement(other, self.unit)
            return Measurement(value=self.value - other.value, unit=self.unit)
        elif isinstance(other, Measurement):
            if self.unit != other.unit:
                other.value = other.convert(str(self.unit))
                other.unit = str(self.unit)
            return Measurement(value=self.value - other.value, unit=self.unit)
        raise ValueError(f"Cannot add Measurement to {type(other)}.")

    def __mul__(self, other: Union[int, float, "Measurement"]) -> 'Measurement':
        if isinstance(other, Measurement):
            if self.unit != other.unit:
                other.value = other.convert(str(self.unit))
                other.unit = str(self.unit)
            return Measurement(value=self.value * other.value, unit=self.unit)
        elif not isinstance(other, (int, float)):
            raise ValueError(f"Cannot multiply Measurement by {type(other)}.")
        return Measurement(value=self.value * other, unit=self.unit)

    def __truediv__(self, other: Union[int, float, "Measurement"]) -> 'Measurement':
        if isinstance(other, Measurement):
            if self.unit != other.unit:
                other.value = other.convert(str(self.unit))
                other.unit = str(self.unit)
            return Measurement(value=self.value / other.value, unit=self.unit)
        elif not isinstance(other, (int, float)):
            raise ValueError(f"Cannot multiply Measurement by {type(other)}.")
        return Measurement(value=self.value / other, unit=self.unit)

    def __floordiv__(self, other: Union[int, float]) -> 'Measurement':
        if isinstance(other, Measurement):
            if self.unit != other.unit:
                other.value = other.convert(str(self.unit))
                other.unit = str(self.unit)
            return Measurement(value=self.value // other.value, unit=self.unit)
        elif not isinstance(other, (int, float)):
            raise ValueError(f"Cannot multiply Measurement by {type(other)}.")
        return Measurement(value=self.value // other, unit=self.unit)

    def convert(self, to: str) -> float:
        """Converts the value to the specified unit.

        Args:
            to (str): Unit to convert to

        Returns:
            float: Converted value
        """
        return self.unit.convert(self.value, to)

    def rich(self) -> Text:
        return Text.assemble(
            *[
                Text(str(self.value), style="bold #ffffff"),
                Text(" "),
                Text(str(self.unit), style="bold italic #af00ff")
            ]
        )
