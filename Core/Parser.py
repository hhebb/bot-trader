from  Core.DBManager import DBManager
import pandas as pd

class Parser:
    '''
        거래소마다 각자의 Parser 가 필요함.
    '''
    def __init__(self):
        # self.__manager = DBManager()
        pass

    def Parse(self, data: dict):
        lob, transaction, lobSnapshot, transactionSnapshot = self.Split(data)

        bid = list()
        ask = list()
        bidSnapshot = list()
        askSnapshot = list()

        for l in lob:
            if l['orderType'] == 'ask':
                ask.append(l)
            else:
                bid.append(l)

        if lobSnapshot:
            bidSnapshot = lobSnapshot[0]
            askSnapshot = lobSnapshot[1]

        return bid, ask, transaction, bidSnapshot, askSnapshot, transactionSnapshot


    def Split(self, data: dict):
        lob = list()
        transaction = list()
        lobSnapshot = None
        transactionSnapshot = list()

        if data is not None:
            if 'lob' in data:
                lob = data['lob']
            if 'transaction' in data:
                transaction = data['transaction']
            if 'snapshot_lob' in data:
                lobSnapshot = data['snapshot_lob']
            if 'snapshot_transaction' in data:
                transactionSnapshot = data['snapshot_transaction']

        else:
            # print('> empty document')
            pass

        return lob, transaction, lobSnapshot, transactionSnapshot

    def ParseLOB(self):
        pass

    def ParseTransaction(self):
        pass