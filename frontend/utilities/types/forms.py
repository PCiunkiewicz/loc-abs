"""Type definitions for form fields."""

from collections.abc import Callable
from dataclasses import dataclass, field


@dataclass
class ComponentField:
    """A field in a form."""

    id: dict | str | int
    component: Callable | None = None


@dataclass
class TextField:
    """A field in a form."""

    id: dict | str | int
    label: str = ''
    type: str = 'text'
    css_class: str = 'form-input'
    tooltip: str = ''


@dataclass
class NumberField(TextField):
    """Number field in a form."""

    min: int | float | None = None
    max: int | float | None = None
    step: int | float | None = None


@dataclass
class OptionsField(TextField):
    """Field with options."""

    options: list = field(default_factory=list)


Field = ComponentField | TextField | NumberField | OptionsField
