from typing import Union

from rich.text import Text
from rich_gradient import Color, Gradient

from hole_pad_calc import console


class Unit:
    VALID_UNITS = ['in', 'mm', 'mil']
    CONVERSIONS = {
            'in': {'mm': 25.4, 'mil': 1000},
            'mm': {'in': 1 / 25.4, 'mil': 1000 / 25.4},
            'mil': {'in': 1 / 1000, 'mm': 25.4 / 1000}
        }
    PLACES = { 'in': 5, 'mm': 4, 'mil': 3}
    COLORS = {
        'in': '#ff5fff',
        'mm': '#00ff00',
        'mil': '#5f00ff'
    }

    def __init__(self, unit: Union[str, 'Unit'] = 'in') -> None:
        self._unit: str = ''
        self.unit = unit  # This uses the property setter for validation

    def __str__(self) -> str:
        return self.unit


    def __eq__(self, other: Union[str, "Unit"]) -> bool:
        if not isinstance(other, (str, Unit)):
            raise NotImplementedError("Cannot compare Unit with non-string or non-Unit type.")
        if isinstance(other, Unit):
            return self.unit == other.unit
        return str(self.unit) == other

    def __ne__(self, other: Union[str, "Unit"]) -> bool:
        if not isinstance(other, (str, Unit)):
            raise NotImplementedError("Cannot compare Unit with non-string or non-Unit type.")
        if isinstance(other, Unit):
            return self.unit != other.unit
        return str(self.unit) != other

    def __hash__(self) -> int:
        return hash(self.unit)

    def __rich__(self) -> Text:
        color = self.COLORS[self.unit]
        return Text(self.unit, style=f"i {color}")

    @property
    def unit(self) -> str:
        return self._unit

    @unit.setter
    def unit(self, value: Union[str, 'Unit']) -> None:
        if isinstance(value, Unit):
            value = value.unit
        if value not in self.VALID_UNITS:
            raise ValueError(f"Invalid unit: {value}. Must be 'in', 'mm', or 'mil'.")
        self._unit = value


    def convert(self, value: float|int, to_unit: str) -> float:
        if to_unit not in self.VALID_UNITS:
            raise ValueError(f"Units must be one of {self.VALID_UNITS}")
        self_unit = self.unit

        # Convert int to float
        if isinstance(value, int):
            value = float(value)

        # Determine the number of decimal places to round to
        places = self.PLACES[to_unit]

        # If the units are the same, return the rounded value
        if self_unit == to_unit:
            return round(value, places)

        # Convert the value to the new unit
        conversion = self.CONVERSIONS[self_unit][to_unit]
        return round((value * conversion), places)

    def __repr__(self) -> str:
        return f"Unit(unit='{self.unit}')"

    @classmethod
    def example(cls) -> None:
        from rich.box import ROUNDED
        from rich.table import Table
        from rich.prompt import FloatPrompt, Prompt

        # Prompt
        console.clear()
        console.line(2)
        value = FloatPrompt.ask("Enter the value to convert", console=console)
        unit = Prompt.ask("Enter the unit to convert from", choices=['in', 'mm', 'mil'], default="in")
        convert_to = Prompt.ask("Enter the unit to convert to", choices=['in', 'mm', 'mil'], default="mm")

        # Logic
        u = cls(unit)
        converted_value = u.convert(value, convert_to)

        # Output
        table = Table(title=Gradient("Example of Unit class", justify="center", style="bold"), box=ROUNDED)
        table.add_column("Input", justify="center", style="bold")
        table.add_column("Convert To", justify="center", style="bold")
        table.add_column("Answer", justify="center", style="bold")
        from_color = u.COLORS[unit]
        to_color = u.COLORS[convert_to]
        table.add_row(
            Text.assemble(
                *[
                    Text(str(value), style = f"bold {from_color}"),
                    Text(" "),
                    Text(str(u), style=f"i {from_color}")
                ]
            ),
            Unit(convert_to),
            Text.assemble(
                *[
                    Text(str(converted_value), style = f"bold {to_color}"),
                    Text(" "),
                    Text(str(Unit(convert_to)), style=f"i {to_color}")
                ]
            ),
        )

        console.line(2)
        console.print(table, justify="center")



if __name__ == '__main__':
    Unit.example()
