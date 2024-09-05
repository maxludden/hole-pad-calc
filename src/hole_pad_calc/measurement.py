from pydantic import BaseModel, Field, field_validator, ValidationError
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from hole_pad_calc.unit import Unit

class Measurement(BaseModel):
    """Measurement of a hole or pad.

    Args:
        value (float): Value of the measurement
        unit (str, optional): Unit of the measurement. Defaults to 'in'. Valid values are 'in' or 'mm' or 'mil'
    """
    value: float|int = Field(..., title="Value of the Measurement", description="Value of the measurement", init=True)
    unit: Unit = Field(Unit(), title="Unit of the Measurement", description="Unit of the measurement", init=True)

    def __init__(self, value: float|int, unit: Unit = Unit('in')) -> None:
        super().__init__(value=value, unit=unit)

    @field_validator('unit')
    def check_unit(cls, v: Unit):
        if v.unit not in ['in', 'mm', 'mil']:
            raise ValueError(f"Unit must be either 'in', 'mm', or 'mil'. Got {v.unit}")

    @field_validator('value')
    def value_is_numeric(cls, v: float|int):
        if not isinstance(v, (int, float)):
            raise ValueError(f"Value must be a number. Got {type(v)}")

    @classmethod
    def __call__(cls, value: float|int, unit: str = 'in'):
        return cls(value=value, unit=Unit(unit))

    def __str__(self) -> str:
        return f"{self.value} {self.unit}"

    def __repr__(self) -> str:
        return f"Measurement<{self.value} {self.unit}>"

    def __int__(self) -> int:
        """Converts the value to an integer if the float is an integer."""
        if isinstance(self.value, float) and not self.value.is_integer():
            raise ValueError(f"Cannot convert {self.value} to int as it is not an integer.")
        return int(self.value)

    def __float__(self) -> float:
        return float(self.value)

    def rich(self) -> Text:
        return Text.assemble(
            *[
                Text(str(self.value), style="bold #ffffff"),
                Text(" "),
                Text(str(self.unit), style="bold italic #af00ff")
            ]
        )

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

    def convert(self, to: str) -> float:
        """Converts the value to the specified unit.

        Args:
            to (str): Unit to convert to

        Returns:
            float: Converted value
        """
        return self.unit.convert(self.value, to)

    def __add__(self, other) -> 'Measurement':
        if self.unit != other.unit:
            raise ValueError(f"Cannot add measurements with different units. Got {self.unit} and {other.unit}")
        return Measurement(value=self.value + other.value, unit=self.unit)

    def __sub__(self, other) -> 'Measurement':
        if self.unit != other.unit:
            raise ValueError(f"Cannot subtract measurements with different units. Got {self.unit} and {other.unit}")
        return Measurement(value=self.value - other.value, unit=self.unit)

    def __mul__(self, other) -> 'Measurement':
        if not isinstance(other, (int, float)):
            raise ValueError(f"Cannot multiply by non-numeric type. Got {type(other)}")
        return Measurement(value=self.value * other, unit=self.unit)

    def __truediv__(self, other) -> 'Measurement':
        if not isinstance(other, (int, float)):
            raise ValueError(f"Cannot divide by non-numeric type. Got {type(other)}")
        return Measurement(value=self.value / other, unit=self.unit)

    def __floordiv__(self, other) -> 'Measurement':
        if not isinstance(other, (int, float)):
            raise ValueError(f"Cannot divide by non-numeric type. Got {type(other)}")
        return Measurement(value=self.value // other, unit=self.unit)
