import pymongo

class DBManager:
    def __init__(self):
        self.__conn = None
        self.__db = None
        self.__collection = None

    def Connect(self, ip='localhost', port=27017, db='test', collection='tmp'):
        self.__conn = pymongo.MongoClient(ip, port)
        self.__db = self.__conn.get_database(db)
        self.__collection = self.__db.get_collection(collection)

    def GetNextRow(self, timestamp):
        query = {'timestamp':timestamp}
        cursor = self.__collection.find(query)
        return 1