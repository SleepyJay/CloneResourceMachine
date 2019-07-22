import unittest
from CloneResourceMachine.Game import Game


# This is sort of dumb...at some point I'm going to add a level count and this is going to need
# to be increased, but I don't know of another way ATM to get the count...
LEVEL_COUNT = 22
LEVEL_PATH = '../levels/game.yaml'

class Test_ConfirmTests(unittest.TestCase):

    def test_levels(self):
        print("\n>> Testing levels...")
        game = Game(LEVEL_PATH)

        levels = game.levels

        self.assertTrue(levels, "Levels exist")
        self.assertEqual(len(levels), LEVEL_COUNT, f"There are {LEVEL_COUNT} levels")

        # I know some specfics about levels...

        level_1 = game.get_level(1)
        self.assertTrue(level_1, "Level 1 exists")
        self.assertTrue(level_1.registers, 'Level 1 has registers')
        self.assertEqual(level_1.registers.count, 0, 'Level 1 registers count 0')

        level_3 = game.get_level(3)
        self.assertTrue(level_3, "Level 3 exists")

        level_5 = game.get_level(5)
        self.assertTrue(level_5, "Level 5 exists")
        self.assertTrue(level_5.is_movie, "Level 5 is a movie")

    def test_empty_program(self):
        print("\n>> Testing level with empty program...")
        game = Game(LEVEL_PATH)

        engine = game.start_new(1, None)
        self.assertTrue(engine)

    def test_level_to_data(self):
        game = Game(LEVEL_PATH)

        game.start_new(1, None)
        actual_1 = game.to_data()
        actual_1['input'] = []
        expect_1 = {"name": "Mail Room", "key": "1", "is_movie": None, "formula": "for $a => $a", "input": [], "register_count": 0, "register_values": {}}
        self.assertDictEqual(expect_1, actual_1, "Level 1 data OK")

        game.start_new(5, None)
        actual_5 = game.to_data()
        expect_5 = {"name": "Coffee Time", "key": "5", "is_movie": True, "formula": None, "input": None, "register_count": None, "register_values": None}
        self.assertDictEqual(expect_5, actual_5, "Level 5 data OK")




















# game.load_level_file('levels/game_16.yaml')
# game.load_level_data('test_data', test_data)

# game.start_new(21, 'fast')
# # game.start_new(20, 'small')
# ledger = game.run()

# for i in range(0,1):
#     game.start_new(7, 'fast', ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])
#     ledger = game.run()
#     speed = ledger.get_speed()
#     print(f"{ledger.initial_state.inbox} ==> {speed}")
#     if game.ledger.error_state:
#         print(game.ledger.error_state)
