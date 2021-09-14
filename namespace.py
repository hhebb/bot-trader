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


class Fonts(Enum):
    '''
        windows font 에서 font 이름을 확인하고 작성해야함.
        bold 체가 따로 있는 font 는 QFont 의 setBold(True) 를 실행해야 함.
    '''
    SEBANG_BOLD = '세방고딕 Bold'
    SEBANG_REGULAR = '세방고딕 Regular'
    NURI = '한글누리'
    SURROUND_BOLD = '카페24 써라운드'
    ESAMANRU_BOLD = '이사만루체 Bold'
    ESAMANRU_MEDIUM = '이사만루체 Medium'


class SimulateState(Enum):
    RUNNING = 0
    STOP = 1


class SimulateSpeedLimit(Enum):
    UPPER_BOUND = 10
    LOWER_BOUND = 1


class LOBType(Enum):
    ASK = 0
    BID = 1