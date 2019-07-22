
import sys
from CloneResourceMachine.Game import Game

level_key = 1
progm_key = 'fast'

# get level_key, prog_key from ARGV
if len(sys.argv) > 2:
    level_key = sys.argv[1]
    progm_key = sys.argv[2]

game = Game('levels/game.yaml')
game.start_new(level_key, progm_key)
ledger = game.run()
avg = game.run_discrete_input()

print(ledger)
print('Results of basic run:')
print(ledger.get_goal_table())
print('Average of descrete runs:')
print(avg)


