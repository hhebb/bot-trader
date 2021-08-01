from Core.OrderBook import OrderBook
from Core.Transaction import Transaction
from Core.Ticker import Ticker
from Core.DBManager import DBManager
from Core.Parser import Parser

class Market:
    def __init__(self):
        self.__LOB_ask = OrderBook('ask')
        self.__LOB_bid = OrderBook('bid')
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
        bid, ask, transaction, bidSnapshot, askSnapshot, transactionSnapshot = self.__parser.Parse(data)

        # lob. snapshot 이 있으면 바로 적용.
        if bidSnapshot:
            self.__LOB_bid.SetSnapshot(bidSnapshot)
            self.__LOB_ask.SetSnapshot(askSnapshot)
            print('> lob snapshot parse')
        else:
            self.__LOB_bid.Update(bid) # lob
            self.__LOB_ask.Update(ask) # lob
            # self.__ticker.Update()
            print('> lob realtime parse')

        # transaction. snapshot 이 있으면 바로 적용.
        if transactionSnapshot:
            self.__transaction.SetSnapshot(transactionSnapshot)
            print('> transaction snapshot parse')
        else:
            self.__transaction.Update(transaction) # trans
            print('> transaction realtime parse')

        print('> step\n')

    def GetASK(self):
        return self.__LOB_ask

    def GetBID(self):
        return self.__LOB_bid

    def GetTransaction(self):
        return self.__transaction

    def GetTicker(self):
        return self.__ticker