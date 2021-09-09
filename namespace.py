from enum import Enum

FIAT_PRICE = -1

class EOrderStatus(Enum):
    WAIT = 0
    COMPLETE = 1

class EPostion(Enum):
    SELL = 0
    BUY = 1
    HOLD = 2


class ColorCode(Enum):
    DARK_BACKGROUND = (10, 10, 10)
    DARK_PANEL = (30, 30, 30)
    DARK_MIDDLE = (50, 50, 50)

    GRAY_BACKGROUND = (50, 50, 61)
    GRAY_PANEL = (38, 38, 50)
    NAVY_BACKGROUND = (17, 20, 45)
    NAVY_PANEL = (32, 39, 79)


class SimulateState(Enum):
    RUNNING = 0
    STOP = 1


class SimulateSpeedLimit(Enum):
    UPPER_BOUND = 10
    LOWER_BOUND = 1