import pymongo


class DBManager:
    '''
        현재 local 에서만 작동하므로 초기엔 localhost 로 즉시 접속.
        생성될 때 connection 만 수행.
        DB, collection 은 별개로 진행.
    '''

    def __init__(self, ip='localhost', port=27017):
        # pair
        self.__conn = None
        self.__db = None
        self.__collection = None
        self.pair = None
        self.timestamp = None
        self.__Connect(ip, port)

    def __Connect(self, ip='localhost', port=27017, db='test', collection='tmp'):
        self.__conn = pymongo.MongoClient(ip, port)

        #
        # if db == 'data':
        #     self.pair, self.timestamp = self.__collection.name.split('_')

    def GetCurrentDB(self):
        return self.__db

    def GetCurrentCollection(self):
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

    def GetRow(self, timestamp):
        # find 는 cursor 반환. cursor 는 generator 혹은 iterator.
        # find_one 은 dict 반환
        query = {'timestamp': {'$eq': timestamp}}
        result = self.__collection.find_one(query)
        return result
