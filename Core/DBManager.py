import pymongo
import pandas as pd

class DBManager:
    '''
        현재 local 에서만 작동하므로 초기엔 localhost 로 즉시 접속.
        생성될 때 connection 만 수행.
        DB, collection 연결은 별개로 진행.

        ----------------------------------

        * data pipeline
            1. DBManager
            2. Parser
            3. Market
            4. Runner
            5. Widget

    '''

    def __init__(self, ip='localhost', port=27017):
        # pair
        self.__conn = None
        self.__db = None
        self.__collection = None
        self.pair = None
        self.timestamp = None
        self.__Connect(ip, port)
        self.__rows = None

    def __Connect(self, ip='localhost', port=27017, db='test', collection='tmp'):
        self.__conn = pymongo.MongoClient(ip, port)

    def GetCurrentDB(self) -> pymongo.database.Database:
        return self.__db

    def GetCurrentCollection(self) -> pymongo.collection.Collection:
        return self.__collection

    def SetCurrentDB(self, dbName: str='test'):
        self.__collection = None
        self.__db = self.__conn.get_database(dbName)

    def SetCurrentCollection(self, collectionName: str):
        self.__collection = self.__db.get_collection(collectionName)

    def GetDBNames(self):
        return self.__conn.list_database_names()

    def GetCollectionNames(self, dbName: str='test'):
        db = self.__conn.get_database(dbName)
        return db.list_collection_names()

    def GetDataCount(self, collectionName: str) -> int:
        return self.__db.get_collection(collectionName).count()

    def GetPopRow(self) -> dict:
        '''
            성능 향상을 위해 list pop.
            시뮬레이션에서 사용.
        '''
        # find 는 cursor 반환. cursor 는 generator 혹은 iterator.
        # find_one 은 dict 반환

        try:
            result = self.__rows.pop(0)
        except:
            print('> No datas. Call "QueryAllRows" first.')
            return None
        return result

    def QueryRow(self, timestamp):
        # find 는 cursor 반환. cursor 는 generator 혹은 iterator.
        # find_one 은 dict 반환
        query = {'timestamp': {'$eq': timestamp}}
        result = self.__collection.find_one(query)
        return result

    def QueryAllRows(self):
        # current collection 의 모든 rows 를 cursor 객체로 가져옴.
        result = list(self.__collection.find())
        self.__rows = result


    def WriteLOB(self, stamp, lob):
        self.__collection.update_one({'timestamp': stamp}, {'$set': {'lob': lob}}, upsert=True)

    def PushLOB(self, stamp, lob):
        self.__collection.update_one({'timestamp': stamp}, {'$push': {'lob': lob}}, upsert=True)

    def WriteTransaction(self, stamp, transaction):
        self.__collection.update_one({'timestamp': stamp}, {'$set': {'transaction': transaction}}, upsert=True)

    def PushTransaction(self, stamp, transaction):
        self.__collection.update_one({'timestamp': stamp}, {'$push': {'transaction': transaction}}, upsert=True)

    def WriteLOBSnapshot(self, stamp, snapshot):
        self.__collection.update_one({'timestamp': stamp}, {'$set': {'snapshot_lob': snapshot}}, upsert=True)

    def WriteTransactionSnapshot(self, stamp, snapshot):
        self.__collection.update_one({'timestamp': stamp}, {'$set': {'snapshot_transaction': snapshot}}, upsert=True)

    def DropCollection(self):
        self.__collection.drop()