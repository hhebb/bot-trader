import pymongo


class DBManager:
    def __init__(self):
        self.__conn = None
        self.__db = None
        self.__collection = None
        self.Connect()

    def Connect(self, ip='localhost', port=27017, db='test', collection='tmp'):
        self.__conn = pymongo.MongoClient(ip, port)
        self.__db = self.__conn.get_database(db)
        self.__collection = self.__db.get_collection(collection)

    def GetRow(self, timestamp):
        # find 는 cursor 반환. cursor 는 generator 혹은 iterator.
        # find_one 은 dict 반환
        query = {'timestamp': {'$eq': timestamp}}
        result = self.__collection.find_one(query)
        return result
