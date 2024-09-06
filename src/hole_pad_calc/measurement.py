from typing import Optional, Union
from rich.text import Text
from hole_pad_calc.unit import Unit

from hole_pad_calc import console


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
        if isinstance(other, (int, float)):
            return Measurement(value=self.value + float(other), unit=self.unit)
        elif isinstance(other, Measurement):
            if self.unit != other.unit:
                other = other.convert(str(self.unit))
            return Measurement(value=self.value + other.value, unit=self.unit)
        raise ValueError(f"Cannot add Measurement to {type(other)}.")

    def __sub__(self, other: Union[int, float, "Measurement"]) -> 'Measurement':
        if isinstance(other, (int, float)):
            return Measurement(value=self.value - float(other), unit=self.unit)
        elif isinstance(other, Measurement):
            if self.unit != other.unit:
                other = other.convert(str(self.unit))
            return Measurement(value=self.value - other.value, unit=self.unit)
        raise ValueError(f"Cannot subtract Measurement from {type(other)}.")

    def __mul__(self, other: Union[int, float, "Measurement"]) -> 'Measurement':
        if isinstance(other, (int, float)):
            return Measurement(value=self.value * float(other), unit=self.unit)
        elif isinstance(other, Measurement):
            if self.unit != other.unit:
                other = other.convert(str(self.unit))
            return Measurement(value=self.value * other.value, unit=self.unit)
        raise ValueError(f"Cannot multiply Measurement by {type(other)}.")

    def __truediv__(self, other: Union[int, float, "Measurement"]) -> 'Measurement':
        if isinstance(other, (int, float)):
            return Measurement(value=self.value / float(other), unit=self.unit)
        elif isinstance(other, Measurement):
            if self.unit != other.unit:
                other = other.convert(str(self.unit))
            return Measurement(value=self.value / other.value, unit=self.unit)
        raise ValueError(f"Cannot divide Measurement by {type(other)}.")

    def __floordiv__(self, other: Union[int, float, "Measurement"]) -> 'Measurement':
        if isinstance(other, (int, float)):
            return Measurement(value=self.value // float(other), unit=self.unit)
        elif isinstance(other, Measurement):
            if self.unit != other.unit:
                other = other.convert(str(self.unit))
            return Measurement(value=self.value // other.value, unit=self.unit)
        raise ValueError(f"Cannot floor divide Measurement by {type(other)}.")

    def convert(self, to: str) -> "Measurement":
        """Converts the value to the specified unit.

        Args:
            to (str): Unit to convert to

        Returns:
            Measurement: Converted measurement with the new unit
        """
        CONVERSIONS = {
            "in": {"mm": 25.4, "mil": 1000},
            "mm": {"in": 0.0393701, "mil": 39.3701},
            "mil": {"in": 0.001, "mm": 0.0254},
        }
        PLACES = {"in": 5, "mm": 4, "mil": 3}
        if to == str(self.unit):
            return self
        if to not in CONVERSIONS:
            raise ValueError(f"Invalid unit: {to}. Must be 'in', 'mm', or 'mil'.")
        conversion_value = self.value * CONVERSIONS[str(self.unit)][to]
        return Measurement(value=round(conversion_value, PLACES[to]), unit=to)

    def rich(self) -> Text:
        PLACES = {"in": 5, "mm": 4, "mil": 3}
        return Text.assemble(
            *[
                Text(str(round(self.value, PLACES[str(self.unit)])), style="bold"),
                Text(" "),
                Text(str(self.unit), style="bold")
            ]
        )


if __name__ == '__main__':
    from typing import List
    from rich.prompt import FloatPrompt, Prompt
    from rich.box import ROUNDED
    from rich.table import Table
    from rich_gradient import Gradient

    value = FloatPrompt.ask(
        "Enter a value",
        console=console,
        default=25.4
    )
    unit = Prompt.ask(
        "Enter a unit",
        choices=['in', 'mm', 'mil'],
        default="mm",
        console=console
    )
    measurement = Measurement(value, unit)
    convert_to = Prompt.ask(
        "Convert to",
        choices=['in', 'mm', 'mil'],
        default="in",
        console=console
    )
    converted = measurement.convert(convert_to)
    colors: List[str] = ["#ff00ff", "#af00ff", "#5f00ff"]
    table = Table(
        title=Gradient(
            "Example of Measurement Class",
            colors=colors,
            justify="center",
            style="bold"),
        box=ROUNDED
    )
    table.add_column("Input", justify="center", style="bold")
    table.add_column("Convert To", justify="center", style="bold")
    table.add_column("Answer", justify="center", style="bold")
    table.add_row(
        Text.assemble(
            *[
                Text(str(measurement.value), style="bold #ff00ff"),
                Text(" "),
                Text(str(measurement.unit), style="i #ff00ff")
            ]
        ),
        Text(convert_to, style="bold #af00ff"),
        Text.assemble(
            *[
                Text(str(converted.value), style="bold #5f00ff"),
                Text(" "),
                Text(str(converted.unit), style="i #5f00ff")
            ]
        )
    )
    console.print(
        table,
        justify="center"
    )
