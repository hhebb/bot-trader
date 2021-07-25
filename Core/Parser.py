from  Core.DBManager import DBManager

class Parser:
    def __init__(self):
        self.__manager = DBManager()
        self.__manager.Connect()

    def Parse(self, data):
        lob, transaction, lobSnapshot, transactionSnapshot = self.Splitter(data)

        ask = list()
        bid = list()

        for l in lob:
            if l['orderType'] == 'ask':
                ask.append(l)
            else:
                bid.append(l)

        return ask, bid, transaction, lobSnapshot, transactionSnapshot


    def Splitter(self, data):
        lob = None
        transaction = None
        lobSnapshot = None
        transactionSnapshot = None

        if data is not None:
            if 'lob' in data:
                lob = data['lob']
            if 'transaction' in data:
                transaction = data['transaction']
            if 'snapshot_lob' in data:
                lobSnapshot = data['snapshot_lob']
            if 'transaction' in data:
                transactionSnapshot = data['snapshot_transaction']

        else:
            print('> empty document')

        return lob, transaction, lobSnapshot, transactionSnapshot

    def ParseLOB(self):
        pass

    def ParseTransaction(self):
        pass