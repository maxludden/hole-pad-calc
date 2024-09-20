from math import sqrt
from typing import Optional, Tuple

from rich.box import ROUNDED
from rich.console import Console
from rich.prompt import Confirm, FloatPrompt, Prompt
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
    PLACES = {"in": 5, "mm": 4, "mil": 3}
    TOLERANCE = 0.001

    def __init__(
        self,
        length: Optional[Measurement] = None,
        width: Optional[Measurement] = None,
        *,
        hole: Optional[Measurement] = None,
        verbose: bool = False) -> None:
        """Calculate the pin, hole, and pad sizes for a rectangular pin."""
        self.verbose: bool = verbose
        # Validate input
        if not length and not width:
            # If no length or width is provided but hole size is:
            if hole:
                # calculate the pin size from the hole size
                self.hole_size = hole.convert("in")
                self.hypo = self.hole_size - Measurement(0.0059, "in")
                length = self.hypo / sqrt(2)
                width = length
            else:
                raise ValueError("Length and/or width or hole must be provided.")

        if length or width:
            # if length or width is provided, calculate the pin size
            if length and width:
                self.length = length.convert("in")
                self.width = width.convert("in")
                if hole:
                    self.hole_size = hole.convert("in")
                    self.hypo = self.calc_hypo(self.length, self.width)
                    calculated_hole = self.calc_hole(self.length, self.width)
                    # Check if the provided hole size is close to the calculated hole size
                    if abs(calculated_hole.value - self.hole_size.value) > self.TOLERANCE:
                        raise ValueError(
                            f"Provided hole size {self.hole_size} is not consistent with "
                            f"calculated hole size {calculated_hole}."
                        )
            elif length and not width:
                self.length = length.convert("in")
                self.width = self.length
                if hole:
                    self.hole_size = hole.convert("in")
            elif width and not length:
                self.width = width.convert("in")
                self.length = self.width
                if hole:
                    self.hole_size = hole.convert("in")
            else:
                raise ValueError("Length and/or width must be provided")

        self.hypo = self.calc_hypo()
        self.hole_size = self.calc_hole()
        if hole:
            if self.verbose:
                console.print(
                    f"Calculated Hole Size: {self.hole_size}",
                )
                console.print(
                    f"Entered Hole Size: {self.hole_size}",
                )
        self.pad_size = self.calc_pad()


    @classmethod
    def prompt(cls) -> "RectCalc":
        mode = Prompt.ask("Generate from pin or hole size?", choices=["pin", "hole"], default="pin", show_choices=True)
        if mode == "pin":
            length_value = FloatPrompt.ask("Enter the length of the rectangle")
            length_unit = Prompt.ask(
                "Enter the unit of the length",
                choices=["in", "mm", "mil"],
                default="in",
            )
            length = Measurement(length_value, unit=length_unit)
            if length.unit != "in":
                length = length.convert("in")
            width_value = FloatPrompt.ask("Enter the width of the rectangle")
            width_unit = Prompt.ask(
                "Enter the unit of the width",
                choices=["in", "mm", "mil"],
                default="in",
            )
            width = Measurement(width_value, unit=width_unit)
            if width.unit != "in":
                width = width.convert("in")
            return cls(length, width)
        else:
            hole_size = FloatPrompt.ask("Enter the size of the hole")
            hole_unit = Prompt.ask(
                "Enter the unit of the hole",
                choices=["in", "mm", "mil"],
                default="in",
            )
            hole_size = Measurement(hole_size, unit=hole_unit)
            return cls(hole=hole_size)

    def __rich__(self) -> Table:
        places: int = self.PLACES[str(self.length.unit)]
        table = Table(
            title=Gradient(
                "Rectangular Hole Calculator", rainbow=True, justify="center"
            ),
            box=ROUNDED,
            row_styles=["on #000000", "on #222222"],
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
            Text.assemble(
                *[
                    str(round(self.length.value, places)),
                    " ",
                    Text(str(self.length.unit)),
                ]
            ),
            Text.assemble(
                *[
                    str(round(self.width.value, places)),
                    " ",
                    Text(str(self.width.unit)),
                ]
            ),
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
            self.pad_size.convert("mm"),
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
    ) -> Measurement:
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
        if self.verbose:
            console.log(f"Length: {length}")
            console.log(f"Length Squared: {a_sq}")
        b_sq = float(width.value) ** 2
        if self.verbose:
            console.log(f"Width: {width}")
            console.log(f"Width Squared: {b_sq}")
        c_sq = a_sq + b_sq
        if self.verbose:
            console.log(f"Length Squared + Width Squared: {c_sq}")
        hypo_value = sqrt(c_sq)
        if self.verbose:
            console.log(f"Hypotenuse: {hypo_value}")
        return Measurement(hypo_value, "in")


    def calc_hole(
        self,
        length: Optional[Measurement] = None,
        width: Optional[Measurement] = None
    ) -> Measurement:
        if not self.hypo:
            self.hypo = self.calc_hypo(length, width).convert("in")
        hole_value = (float(self.hypo.value) + 0.0059)
        hole_size = Measurement(hole_value, "in")
        _hole_size_mil: int = int(round(hole_size.convert("mil").value, 0))
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
    console.line(9)
    console.clear()
    console.line(2)

    # Prompt for the length and width of the rectangle
    try:
        rect_calc = RectCalc.prompt()

    except KeyboardInterrupt:
        console.print("Operation cancelled by user.")
        console.line(2)
        raise SystemExit
    except Exception as e:
        console.print(f"An error occurred: {e}")
        console.line(2)
        raise SystemExit

    console.line(3)
    console.print(rect_calc, justify="center")
    console.line(2)
