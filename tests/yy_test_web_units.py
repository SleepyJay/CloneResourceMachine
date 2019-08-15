import unittest
import json
import web.game.views as controller
import web.web.settings as settings
from CloneResourceMachine.Game import Game

# TODO: this wont test as unit, because settings needs to be defined for views file to run


class Test_ConfirmTests(unittest.TestCase):

    def test_level_to_data(self):
        tests = [
            {'level': 1},
            {'level': 5},
        ]

        for test in tests:
            game = Game(controller.LEVEL_PATH)
            game.start_new(test['level'], None)

            # expect = {"name": "Mail Room", "key": "1", "is_movie": None, "formula": "for $a => $a", "input": [], "register_count": 0, "register_values": {}}
            expect = game.to_data()
            # This will be different each time, punt for now...
            expect['input'] = []

            my_json = controller.load_level()
            actual = json.loads(my_json)

            self.assertDictEqual(expect, actual, f"Level {test['level']} data OK")



