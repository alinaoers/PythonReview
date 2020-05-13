import unittest
import lib


class TestCaseCard(unittest.TestCase):
    def test_create_one(self):
        card_storage = lib.CardStorage()
        id = card_storage.create_card()
        self.assertEqual(int(id) - 1, int(0))

    def test_create(self):
        card_storage = lib.CardStorage()
        id_f = card_storage.create_card(1200)
        id_s = card_storage.create_card(1300)
        self.assertEqual(int(id_s) - int(id_f), 1)

    def test_put(self):
        card_storage = lib.CardStorage()
        id = card_storage.create_card(1200)
        print(id)
        card_storage.put(int(id) - 1, 1000)
        print(int(card_storage.all[int(id) - 1].get()))
        self.assertEqual(int(card_storage.all[int(id) - 1].get()), int(2200))

    def test_withdraw(self):
        card_storage = lib.CardStorage()
        id = int(card_storage.create_card(1200)) - 1
        card_storage.withdraw(id, 1000)
        self.assertEqual(int(card_storage.all[id].get()), int(200))

    def test_get_info(self):
        card_storage = lib.CardStorage()
        id = card_storage.create_card(1200)
        info = card_storage.get_info(int(id) - 1)
        self.assertEqual(info, "You have 1200 on card")



if __name__ == '__main__':
    unittest.main()
