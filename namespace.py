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
    GRAY_PANEL = (50, 50, 50)