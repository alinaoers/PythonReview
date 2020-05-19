class Card:
    def __init__(self, card_id, card_sum=0):
        self.card_id = card_id
        self.card_sum = card_sum

    def put(self, card_sum):
        self.card_sum += card_sum

    def get(self):
        return str(self.card_sum)

    def withdraw(self, card_sum):
        self.card_sum -= card_sum


class CardStorage:
    def __init__(self):
        self.all = []

    def create_card(self, card_sum=0):
        card_id = len(self.all) + 1
        self.all.append(Card(card_id, card_sum))
        return str(card_id)

    def put(self, card_id, card_sum):
        if card_id > len(self.all):
            print("Incorrect id")
        else:
            self.all[card_id].put(card_sum)

    def get_info(self, card_id):
        if card_id > len(self.all):
            return("Incorrect id")
        else:
            return "You have {} on card".format(str(self.all[card_id].get()))

    def withdraw(self, card_id, card_sum):
        if card_id > len(self.all):
            print("Incorrect id")
        elif card_sum > int(self.all[card_id].get()):
            print("Sorry, you don't have enough money...")
        else:
            self.all[card_id].withdraw(card_sum)

