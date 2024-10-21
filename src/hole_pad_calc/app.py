# ruff: noqa: F401
from textual.app import App, ComposeResult
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Header, Footer, Button, Static, Input, Select
from rich.console import RenderableType
from rich.style import Style
from rich.text import Text
from hole_pad_calc.rect_calc import RectCalc # Import from rect_calc.py
from hole_pad_calc.measurement import Measurement
from hole_pad_calc.unit import Unit
from typing import Optional, List

UNITS = ["mm", "mil", "in"]

class ToggleButton(Button):
    def __init__(self, unit: str):
        super().__init__(label=unit, id=unit)
        self.is_selected = False
        self.update_label()

    def select(self):
        self.is_selected = True
        self.update_label()

    def unselect(self):
        self.is_selected = False
        self.update_label()

    def update_label(self):
        if self.is_selected:
            self.styles.background = "#222222"
            self.styles.color = "#ffffff"
            self.label = f"[#ffffff on #222222]{self.label}[/]"
        else:
            self.styles.background = "#aaaaaa"
            self.styles.color = "#000000"
            self.label = f"[#000000 on #aaaaaa]{self.label}[/]"

class UnitToggle(Widget):
    selected = "mm"

    def __init__(self, label: str = "mm"):
        children: List[RenderableType] = []
        for unit in UNITS:

        super().__init__(
            ToggleButton()
        )


        self.is_selected = False
        self.update_label()

    def compose(self) -> ComposeResult:
        for unit in UNITS:
            if unit =

    def select(self):
        self.is_selected = True
        self.update_label()

    def unselect(self):
        self.is_selected = False
        self.update_label()

    def update_label(self):
        if self.is_selected:
            self.styles.background = "#222222"
            self.styles.color = "#ffffff"
            self.label = f"[#ffffff on #222222]{self.unit}[/]"
        else:
            self.styles.background = "#aaaaaa"
            self.styles.color = "#000000"
            self.label = f"[#000000 on #aaaaaa]{self.unit}[/]"

    def is_selected(self):

