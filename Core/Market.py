from Core.OrderBook import OrderBook
from Core.Transaction import Transaction
from Core.Ticker import Ticker
from Core.DBManager import DBManager
from Core.Parser import Parser

class Market:
    def __init__(self):
        self.__LOB_ask = OrderBook(1)
        self.__LOB_bid = OrderBook(1)
        self.__transaction = Transaction()
        self.__ticker = Ticker()
        self.__dbManager = DBManager()
        self.__parser = Parser()

    def SetSnapShots(self):
        # for fill initial data. for adjust
        self.__LOB_ask.SetSnapshot()
        self.__LOB_bid.SetSnapshot()

    def Step(self, timestamp):
        data = self.__dbManager.GetRow(timestamp)
        ask, bid, transaction, lobSnapshot, transactionSnapshot = self.__parser.Parse(data)

        self.__LOB_bid.Update() # lob
        self.__LOB_ask.Update() # trans
        self.__transaction.Update()
        self.__ticker.Update()
        print('> step')

    def GetASK(self):
        return self.__LOB_ask

    def GetBID(self):
        return self.__LOB_bid

    def GetTransaction(self):
        return self.__transaction

    def GetTicker(self):
        return self.__ticker