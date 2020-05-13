class Card:
    def __init__(self, id, sum=0):
        self.id = id
        self.sum = sum

    def put(self, sum):
        self.sum += sum

    def get(self):
        return str(self.sum)

    def withdraw(self, sum):
        self.sum -= sum


class CardStorage:
    def __init__(self):
        self.all = []

    def create_card(self, sum=0):
        id = len(self.all) + 1
        print(sum)
        self.all.append(Card(id, sum))
        return str(id)

    def put(self, id, sum):
        if id > len(self.all):
            print("Incorrect id")
        else:
            self.all[id].put(sum)

    def get_info(self, id):
        if id > len(self.all):
            return("Incorrect id")
        else:
            return "You have {} on card".format(str(self.all[id].get()))

    def withdraw(self, id, sum):
        if id > self.all.__len__():
            print("Incorrect id")
        elif sum > int(self.all[id].get()):
            print("Sorry, you don't have enough money...")
        else:
            self.all[id].withdraw(sum)
