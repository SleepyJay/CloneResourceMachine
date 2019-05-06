#!/usr/bin/python

import unittest
from CloneResourceMachine.Game import Game


class Test_ConfirmTests(unittest.TestCase):

    def test_confirm_levels(self):
        game = Game()
        game.load_multi_level_file('../levels/game.yaml')

        for key, values in game.catalog.levels.items():
            if int(key) > 6:
                break

            for goal_type in ('fast', 'small'):
                print(f"Testing {key}-{goal_type}")

                game.start_new(key, goal_type)
                ledger = game.run()
                level_key = game.current_level.key
                
                if game.current_level.is_movie:
                    print(f"skipping movie: {level_key}")
                    continue

                actual_output = game.get_outbox()
                expect_output = ledger.goal.expected.output
                self.assertEqual(actual_output, expect_output,
                                 f"Output for ({level_key}-{goal_type}): OK")

                if goal_type == 'fast':
                    actual_speed = ledger.get_speed()
                    expect_speed = ledger.goal.speed
                    self.assertLessEqual(actual_speed, expect_speed,
                        f"Speed for ({level_key}-{goal_type}): OK")

                if goal_type == 'small':
                    actual_size = ledger.get_size()
                    expect_size = ledger.goal.size
                    self.assertLessEqual(actual_size, expect_size,
                        f"Size for ({level_key}-{goal_type}): OK")


