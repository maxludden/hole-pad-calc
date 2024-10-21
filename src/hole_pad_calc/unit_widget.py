from typing import List, Optional, Any
from textual.app import App
from textual.widgets import Button
from textual.containers import Horizontal
from textual.widget import Widget


class ToggleButton(Button):
    def __init__(self, label: str, id: str):
        super().__init__(label=label, id=id)
        self.is_selected = False
        self.update_label()

    def select(self):
        self.is_selected = True
        self.update_label()

    def unselect(self):
        self.is_selected = False
        self.update_label()

    def update_label(self):
        # Update the button label to indicate if it's selected or not
        if self.is_selected:
            self.styles.background = "#222222"
            self.styles.color = "#ffffff"
            self.label = f"[#ffffff on #222222]{self.label}[/]"
        else:
            self.styles.background = "#aaaaaa"
            self.styles.color = "#000000"
            self.label = f"[#000000 on #aaaaaa]{self.label}[/]"


class ToggleWidget(Widget):
    def __init__(self):
        super().__init__()
        # Keep track of the selected button
        self.selected_button = "mm"

    def compose(self0) -> ComposeResult:
        # Compose the widget
        units: List[str] = ["mm", "mil", "in"]
        selected: str = "mm"
        for unit in units:
            yield ToggleButton(unit)

    async def on_mount(self):
        # Add three toggle buttons representing measurement units
        self.buttons = [
            ToggleButton("mm", "mm"),
            ToggleButton("mil", "mil"),
            ToggleButton("in", "in")
        ]
        # Add the buttons horizontally in the layout
        await self.mount(Horizontal(*self.buttons))

    async def on_button_pressed(self, event: Button.Pressed):
        # Handle button presses
        pressed_button = event.button
        if self.selected_button is not pressed_button:
            if self.selected_button:
                if isinstance(self.selected_button, ToggleButton):
                    self.selected_button.unselect()
            if isinstance(pressed_button, ToggleButton):
                pressed_button.select()
            self.selected_button = pressed_button
        print(f"Selected unit: {pressed_button.id}")


class ToggleApp(App):
    async def on_mount(self):
        # Mount the toggle widget to the app
        await self.mount(ToggleWidget())

    def compose(self) -> ComposeResult:




if __name__ == "__main__":
    ToggleApp().run()
