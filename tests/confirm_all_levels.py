#!/usr/bin/python

import unittest
from CloneResourceMachine.Game import Game


class Test_ConfirmTests(unittest.TestCase):

    def test_confirm_levels(self):
        game = Game()
        game.load_multi_level_file('../levels/game.yaml')

        for key, values in game.catalog.levels.items():
            if int(key) > 20:
                break

            for goal_type in ('fast', 'small'):
                game.start_new(key, goal_type)

                if game.current_level.is_movie:
                    goal_formula = 'MOVIE'
                else:
                    goal_formula = game.current_level.goal.formula

                print(f"Testing {key}-{goal_type}: {goal_formula}")

                ledger = game.run()
                level_key = game.current_level.key

                self.assertFalse(game.ledger.error_state, 'Game runs without error')
                
                if game.current_level.is_movie:
                    print(f"skipping movie: {level_key}")
                    break

                # print("{} => {}".format(game.engine.initial_input, game.engine.output))

                actual_output = game.get_outbox()
                expect_output = ledger.goal.expected.output
                self.assertEqual(actual_output, expect_output,
                                 f"Output for ({level_key}-{goal_type}): OK")

                if goal_type == 'fast':
                    actual_speed = ledger.get_speed()
                    goal_speed = ledger.goal.speed
                    expect_speed = ledger.program.speed or goal_speed

                    self.assertLessEqual(actual_speed, expect_speed,
                        f"Speed for ({level_key}-{goal_type}): OK")

                    if actual_speed > goal_speed:
                        print("Warning: speed too slow for Goal: {} vs {}".format(actual_speed, goal_speed))

                if goal_type == 'small':
                    actual_size = ledger.get_size()
                    goal_size = ledger.goal.size
                    expect_size = ledger.program.size or goal_size

                    self.assertLessEqual(actual_size, expect_size,
                        f"Size for ({level_key}-{goal_type}): OK")

                    if actual_size > goal_size:
                        print("Warning: size too large for Goal: {} vs {}".format(actual_size, goal_size))


            print()
