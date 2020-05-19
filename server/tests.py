import unittest
import lib


class TestCaseCard(unittest.TestCase):
    def test_create_one(self):
        card_storage = lib.CardStorage()
        card_id = card_storage.create_card()
        self.assertEqual(int(card_id) - 1, 0)

    def test_create(self):
        card_storage = lib.CardStorage()
        card_id_f = card_storage.create_card(1200)
        card_id_s = card_storage.create_card(1300)
        self.assertEqual(int(card_id_s) - int(card_id_f), 1)

    def test_put(self):
        card_storage = lib.CardStorage()
        card_id = card_storage.create_card(1200)
        print(card_id)
        card_storage.put(int(card_id) - 1, 1000)
        print(int(card_storage.all[int(card_id) - 1].get()))
        self.assertEqual(int(card_storage.all[int(card_id) - 1].get()), int(2200))

    def test_withdraw(self):
        card_storage = lib.CardStorage()
        card_id = int(card_storage.create_card(1200)) - 1
        card_storage.withdraw(card_id, 1000)
        self.assertEqual(int(card_storage.all[card_id].get()), int(200))

    def test_get_info(self):
        card_storage = lib.CardStorage()
        card_id = card_storage.create_card(1200)
        info = card_storage.get_info(int(card_id) - 1)
        self.assertEqual(info, "You have 1200 on card")


if __name__ == '__main__':
    unittest.main()

