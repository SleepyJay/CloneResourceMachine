
from Roboto.Game import Game
from prettytable import PrettyTable

# todo test available vs commands
# todo input builder
# todo fix regsiter setup
# todo solution confirmer
# todo edge case: protect against numerical lables that scramble command list...
# todo allow non-numeric labels for registers (easier than command list, since dict)

test_data = {
    'available': ['inbox', 'outbox', 'jump'],
    'goal': {
        'formula': 'for $a => $a',
        'size': 6,
        'speed': 6,
    },
    'input': {
        'alphabet': 'alpha-numeric',
        'count': 3,
        'sample': [3, 'E', 0]
    },
    'registers': {
        'count' : 2
    },
    'name': 'TESTING',
    'solutions': {
        'a': {
            'commands': [
                'foo: inbox',
                'outbox',
                'jump foo'
            ]
        },
        'b': {
            'commands': [
                '1: inbox',
                'jumpzero 4',
                'jump 1',
                '4: outbox',
                'jump 1'
            ]
        }
    }
}

game = Game()
game.load_level_file('levels/game.yaml')
# game.load_level_file('levels/game_16.yaml')
# game.load_level_data('test_data', test_data)

# game.start_new(2, 'fast')
game.start_new(2, 'small')

ledger = game.run()
print(ledger)

print(ledger.get_goal_table(game.get_outbox()))
