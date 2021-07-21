import OrderBook
import Transaction
import Ticker

class Market:
    def __init__(self):
        self.LOB_ask = OrderBook()
        self.LOB_bid = OrderBook()
        self.transaction = Transaction()
        self.ticker = Ticker()

    def Step(self):
        pass