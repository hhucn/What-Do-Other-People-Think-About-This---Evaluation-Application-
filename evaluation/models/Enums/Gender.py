from enum import Enum


class Gender(Enum):
    MALE = 1
    FEMALE = 2
    DIVERS = 3
    NO_SELECTION = 4

    def __str__(self):
        return self.name
