from enum import Enum, auto
from math import sqrt
from pathlib import Path
from typing import Literal, Optional, Tuple, TypeAlias

from rich.box import ROUNDED
from rich.console import Console
from rich.prompt import FloatPrompt, Confirm, Prompt
from rich.table import Table
from rich.text import Text
from rich_gradient import Gradient

# Importing the Measurement class from measurement.py
from hole_pad_calc.measurement import Measurement


class RectCalc:
    length: Measurement
    width: Measurement
    hypo: Measurement
    hole_size: Measurement
    pad_size: Measurement
    PLACES = {'in': 5, 'mm': 4, 'mil': 3}

    def __init__(
        self, length: Optional[Measurement] = None, width: Optional[Measurement] = None
    ) -> None:
        if not length and not width:
            raise ValueError("Length and/or width must be provided")
        if length and width:
            self.length = length.convert("in")
            self.width = width.convert("in")
            self.hypo = self.calc_hypo()
            self.hole_size = self.calc_hole()
            self.pad_size = self.calc_pad()
        elif length and not width:
            self.length = length
            _square: bool = Confirm.ask("Is the rectangle a square?")
            if _square:
                self.width = self.length
            else:
                width_value = FloatPrompt.ask("Enter the width of the rectangle")
                width_unit = Prompt.ask(
                    "Enter the unit of the width",
                    choices=['in', 'mm', 'mil'],
                    default="in",
                )
                self.width = Measurement(width_value, unit=width_unit)
            self.hypo = self.calc_hypo()
            self.hole_size = self.calc_hole()
            self.pad_size = self.calc_pad()
        else:
            length_value = FloatPrompt.ask("Enter the length of the rectangle")
            length_unit = Prompt.ask(
                "Enter the unit of the length",
                choices=['in', 'mm', 'mil'],
                default="in",
            )
            self.length = Measurement(length_value, unit=length_unit)
            if self.length.unit != "in":
                self.length = self.length.convert("in")
            width_value = FloatPrompt.ask("Enter the width of the rectangle")
            width_unit = Prompt.ask(
                "Enter the unit of the width",
                choices=['in', 'mm', 'mil'],
                default="in",
            )
            self.width = Measurement(width_value, width_unit)
            if self.width.unit != "in":
                self.width = self.width.convert("in")
            self.hypo = self.calc_hypo()
            self.hole_size = self.calc_hole()
            self.pad_size = self.calc_pad()

    def __rich__(self) -> Table:
        places: int = self.PLACES[str(self.length.unit)]
        table = Table(
            title=Gradient(
                "Rectangular Hole Calculator", rainbow=True, justify="center"
            ),
            box=ROUNDED,
            row_styles=['on #000000', 'on #222222'],
        )
        table.add_column(
            Text("Length", style="b #000000 on #00aaff", justify="center"),
            style="b #00aaff",
            justify="center",
            min_width=12,
        )
        table.add_column(
            Text("Width", style="b #000000 on #ffaa00", justify="center"),
            style="b #ffaa00",
            justify="center",
            min_width=12,
        )
        table.add_column(
            Text("Hypotenuse", style="b #000000 on #00ff00", justify="center"),
            style="b #00ff00",
            justify="center",
            min_width=12,
        )
        table.add_column(
            Text("Hole Size", style="b #000000 on #ffff00", justify="center"),
            style="b #ffff00",
            justify="center",
            min_width=12,
        )
        table.add_column(
            Text("Pad Size", style="b #000000 on #ff9900", justify="center"),
            style="b #ff9900",
            justify="center",
            min_width=12,
        )
        table.add_row(
            str(self.length),
            str(self.width),
            Text.assemble(
                *[
                    str(round(self.hypo.value, places)),
                    " ",
                    Text(str(self.hypo.unit)),
                ]
            ),
            Text.assemble(
                *[
                    str(round(self.hole_size.value, places)),
                    " ",
                    Text(str(self.hole_size.unit)),
                ]
            ),
            Text.assemble(
                *[
                    str(round(self.pad_size.value, places)),
                    " ",
                    Text(str(self.pad_size.unit)),
                ]
            ),
        )
        table.add_row(
            self.length.convert("mm"),
            self.width.convert("mm"),
            self.hypo.convert("mm"),
            self.hole_size.convert("mm"),
            self.pad_size.convert("mm")
        )
        table.add_row(
            self.length.convert("mil"),
            self.width.convert("mil"),
            self.hypo.convert("mil"),
            self.hole_size.convert("mil"),
            self.pad_size.convert("mil"),
        )
        return table


    def calc_hypo(
        self,
        length: Optional[Measurement] = None,
        width: Optional[Measurement] = None,
        verbose: bool = False) -> Measurement:
        # Validate input
        if length or self.length:
            length = length or self.length
            if length.unit != "in":
                length = length.convert("in")
        if width or self.width:
            width = width or self.width
            if width.unit != "in":
                width = width.convert("in")
        assert length and width, "Length and/or width must be provided"

        # Calculate the hypotenuse
        a_sq = float(length.value) ** 2
        if verbose:
            console.log(f"Length: {length}")
            console.log(f"Length Squared: {a_sq}")
        b_sq = float(width.value) ** 2
        if verbose:
            console.log(f"Width: {width}")
            console.log(f"Width Squared: {b_sq}")
        a_sq_plus_b_sq = a_sq + b_sq
        if verbose:
            console.log(f"Length Squared + Width Squared: {a_sq_plus_b_sq}")
        hypo_value = sqrt(a_sq_plus_b_sq)
        if verbose:
            console.log(f"Hypotenuse: {hypo_value}")
        return Measurement(hypo_value, "in")

    def calc_hole(
        self, length: Optional[Measurement] = None, width: Optional[Measurement] = None
    ) -> Measurement:
        self.hypo = self.calc_hypo(length, width).convert("in")
        hole_value = (float(self.hypo.value) + 0.0029) + 0.003
        hole_size = Measurement(hole_value, "in")
        _hole_size_mil:int = int(round(hole_size.convert("mil").value, 0))
        return Measurement(_hole_size_mil, "mil").convert("in")

    def calc_pad(
        self, length: Optional[Measurement] = None, width: Optional[Measurement] = None
    ) -> Measurement:
        self.hole_size = self.calc_hole(length, width)
        hole_size_tol = float(self.hole_size)
        annular_ring = 0.004
        level_a = 0.016
        pad_value = hole_size_tol + annular_ring + level_a
        self.pad_size = Measurement(pad_value, self.hole_size.unit)
        return self.pad_size


if __name__ == "__main__":
    console = Console()

    # Clear the console
    console.clear()
    console.line(2)

    # Prompt for the length and width of the rectangle
    try:
        length = FloatPrompt.ask(
            "[#00ff00]Enter the length of the rectangle[/]",
            console=console,
            default=1.0
        )
        length_unit = Prompt.ask(
            "[#00ff00]Enter the unit of the length[/]",
            choices=['in', 'mm', 'mil'],
            default="mm",
            console=console
        )
        width = FloatPrompt.ask(
            "[#00ff00]Enter the width of the rectangle[/]",
            console=console,
            default=1.0
        )
        width_unit = Prompt.ask(
            "[#00ff00]Enter the unit of the width[/]",
            choices=['in', 'mm', 'mil'],
            default="mm",
            console=console
        )
    except ValueError:
        console.print("[#ff0000]Invalid input. Please enter numeric values.[/]")
        exit(1)

    # Calculate the rectangle
    rect_calc = RectCalc(Measurement(length, length_unit), Measurement(width, width_unit))

    console.line(3)
    console.print(rect_calc, justify="center")
    console.line(2)
