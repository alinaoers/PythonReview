class Card:
    def __init__(self, card_id, sum=0):
        self.id = card_id
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
        card_id = len(self.all) + 1
        print(sum)
        self.all.append(Card(card_id, sum))
        return str(card_id)

    def put(self, card_id, sum):
        if card_id > len(self.all):
            print("Incorrect id")
        else:
            self.all[card_id].put(sum)

    def get_info(self, card_id):
        if card_id > len(self.all):
            return("Incorrect id")
        else:
            return "You have {} on card".format(str(self.all[card_id].get()))

    def withdraw(self, card_id, sum):
        if card_id > len(self.all):
            print("Incorrect id")
        elif sum > int(self.all[card_id].get()):
            print("Sorry, you don't have enough money...")
        else:
            self.all[card_id].withdraw(sum)
