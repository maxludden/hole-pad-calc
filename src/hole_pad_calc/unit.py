from typing import Optional
from pydantic import BaseModel, Field, field_validator, validationError

class Unit(BaseModel):
    """Unit of measurement. Defaults to `in`.

    Args:
        unit (str, optional): Unit of the measurement. Defaults to 'in'. Valid values are 'in' or 'mm' or 'mil'"""
    unit: str = Field('in', title="Unit of the Measurement", description="Unit of the measurement", init=True)

    def __init__(self, unit: Optional[str] = None) -> None:
        if unit is not None:
            unit = 'in'
        if unit not in ['in', 'mm', 'mil']:
            raise ValueError(f"Unit must be either 'in', 'mm', or 'mil'. Got {unit}")
        super().__init__(unit=unit)

    def __call__(self, unit: str = 'in'):
        return self(unit=unit)

    @field_validator(unit)
    def check_unit(cls, v: str):
        if v not in ['in', 'mm', 'mil']:
            raise ValueError(f"Unit must be either 'in', 'mm', or 'mil'. Got {v}")

    def __str__(self) -> str:
        return self.unit


    def convert(self, value: float, to: str) -> float:
        """Converts the value to the specified unit.

        Args:
            value (float): Value to convert
            to (str): Unit to convert to

        Returns:
            float: Converted value
        """
        if self.unit == to:
            return value
        if self.unit == 'in' and to == 'mm':
            return value * 25.4
        if self.unit == 'in' and to == 'mil':
            return value * 1000
        if self.unit == 'mm' and to == 'in':
            return value / 25.4
        if self.unit == 'mm' and to == 'mil':
            return value * 39.3701
        if self.unit == 'mil' and to == 'in':
            return value / 1000
        if self.unit == 'mil' and to == 'mm':
            return value / 39.3701
        return value
