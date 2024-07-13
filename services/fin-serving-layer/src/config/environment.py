from enum import Enum, auto


class Env(Enum):
    DEV = auto()
    PROD = auto()

    @classmethod
    def from_str(cls, val: str) -> "Env":
        return cls.PROD if val == "prod" else cls.DEV
