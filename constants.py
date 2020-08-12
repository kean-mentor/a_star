import enum


WIDTH = HEIGHT = 640
SIZE = 16


class CellType(enum.Enum):
    CLOSED = 1
    OPEN = 2
    BARRIER = 3
    START = 4
    END = 5
    PATH = 6
    NULL = 7
