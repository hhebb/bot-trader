import pymongo

class DBManager:
    def __init__(self):
        self.conn: pymongo.MongoClient = None
        self.db = None
        self.collection = None

    def Connect(self, db='test', coll='tmp'):
        self.conn = pymongo.MongoClient('localhost', 27017)
        self.db = self.conn.get_database(db)
        self.collection = self.db.get_collection(coll)

    def GetData(self):
        # cursor 는 generator 혹은 iterator.
        query = {'timestamp' : {'$gte' : 5}}
        result = self.collection.find(query)
        print(type(result))
        for res in result:
            print(res)

    def Write(self):
        data = {
                "number": 1,
                "name": "who"
                }
        self.collection.insert_one(data)

    def Clear(self):
        self.collection.drop()


if __name__ == '__main__':
    manager = DBManager()
    manager.Connect()
    manager.GetData()
    # manager.Write()
    # manager.Clear()