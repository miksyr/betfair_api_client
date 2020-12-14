

class RunnerPrice:

    def __init__(self, betType, price, size):
        super().__init__()
        self.betType = betType
        self.price = price
        self.size = size

    def __str__(self):
        return f'betType: {self.betType}, price: {self.price}, size: {self.size}'

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash((self.betType, self.price, self.size))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
