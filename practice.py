
from CloneResourceMachine.Game import Game

level_key = 7
progm_key = 'small'

game = Game('levels/game.yaml')
game.start_new(level_key, progm_key)
ledger = game.run()

avg = game.run_discrete_input()

print(ledger)
print('Results of basic run:')
print(ledger.get_goal_table())
print('Average of descrete runs:')
print(avg)
