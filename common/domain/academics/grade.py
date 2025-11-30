from dataclasses import dataclass


@dataclass(frozen=True)
class Grade:
    score: float
    letter: str
