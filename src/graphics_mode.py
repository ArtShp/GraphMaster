from enum import Enum


class GraphicsMode(Enum):
    """Enum for app working mode."""
    NONE = 0
    CURSOR = 1
    ADD_NODE = 2
    ADD_EDGE = 3
    DELETE_ITEM = 4
