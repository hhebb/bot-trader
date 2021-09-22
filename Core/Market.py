import datetime
import pandas as pd
import namespace
from Core.OrderBook import OrderBook
from Core.Transaction import Transaction
from Core.Ticker import Ticker
from Core.DBManager import DBManager
from Core.Parser import Parser

class Market:
    def __init__(self):
        self.dbManager = DBManager()
        self.__pairSymbol = 0
        self.__startTime = 0
        self.__LOB_ask = OrderBook(namespace.LOBType.ASK)
        self.__LOB_bid = OrderBook(namespace.LOBType.BID)
        self.__transaction = Transaction()
        self.__ticker = Ticker()
        self.__parser = Parser()
        self.__dataIndex = 0

    def SetSnapShots(self):
        # for fill initial data. for adjust
        self.__LOB_ask.SetSnapshot()
        self.__LOB_bid.SetSnapshot()

    def Step(self, timestamp: datetime.datetime):
        '''
            Get Data from loaded data.
            Parse data for use
            save lob, transaction, ticker datas.
            Ready to send these datas.

            snapshot 있으면 주고 없으면 걍 넘어감.
            snapshot 있으면 통째로 갈아치우고 아니면 추가하여 갱신함.
        '''
        data = self.dbManager.GetPopRow()
        bid, ask, transaction, bidSnapshot, askSnapshot, transactionSnapshot = \
            self.__parser.Parse(data)

        # lob. snapshot 이 있으면 바로 적용.
        if bidSnapshot or askSnapshot:
            self.__LOB_bid.SetSnapshot(bidSnapshot)
            self.__LOB_ask.SetSnapshot(askSnapshot)
            # print('> lob snapshot parse')
            pass
        else:
            self.__LOB_bid.Update(bid) # lob
            self.__LOB_ask.Update(ask) # lob
            # self.__ticker.Update()
            # print('> lob realtime parse')

        # transaction. snapshot 이 있으면 바로 적용.
        if transactionSnapshot:
            self.__transaction.SetSnapshot(transactionSnapshot)
            self.__transaction.Update(transaction)  # trans
            # print('> transaction snapshot parse')
            pass
        else:
            self.__transaction.Update(transaction)  # trans
            self.__transaction.UnSet()

        # candle chart 를 위한 체결 데이터 수신.
        self.__ticker.Update(timestamp, self.GetTransaction().GetHistoryDiff())

        self.__dataIndex += 1
        # print('> step\n')

    def GetASK(self):
        return self.__LOB_ask

    def GetBID(self):
        return self.__LOB_bid

    def GetTransaction(self):
        return self.__transaction

    def GetTicker(self):
        return self.__ticker

    def GetDBManager(self):
        return self.dbManager