#!/usr/bin/python

import unittest
from Game import Game


class Test_ConfirmTests(unittest.TestCase):
    game = Game()
    game.load_multi_level_file('../levels/game.yaml')

    for key, values in game.catalog.levels.items():
        if int(key) > 1:
            break

        for goal_type in ['fast', 'small']:
            game.start_new(key, goal_type)
            ledger = game.run()

        continue

