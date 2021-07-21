class Transaction:
    def __init__(self):
        self.max_size = 1000
        self.History = list()

    def Parse(self):
        if len(self.History) > self.max_size:
            self.History.pop(0)

        data = MarketOrder('bid', 1000, 4)
        self.History.append(data)

    def GetHistory(self):
        return self.History


class MarketOrder:
    def __init__(self, position, price, amount):
        self.type = position # bid or ask
        self.price = price
        self.amount = amount