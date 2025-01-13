from enum import Enum


class Education(Enum):
    BACHELOR = 1
    MASTER = 2
    PHD = 3

    def __str__(self):
        return self.name
