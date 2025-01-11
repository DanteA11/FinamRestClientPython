"""Допустимые тайм-фреймы."""

from enum import Enum


class DayTimeFrames(str, Enum):
    """Тайм-фреймы от 1 дня."""

    D1 = "D1"
    W1 = "W1"


class IntraDayTimeFrames(str, Enum):
    """Внутридневные тайм-фреймы."""

    M1 = "M1"
    M5 = "M5"
    M15 = "M15"
    H1 = "H1"
