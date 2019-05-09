
from CloneResourceMachine.Game import Game

# todo test available vs commands
# todo input builder
# todo fix regsiter setup
# todo program confirmer
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
    'programs': {
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
game.load_multi_level_file('levels/game.yaml')
# game.load_level_file('levels/game_16.yaml')
# game.load_level_data('test_data', test_data)

game.start_new(21, 'fast')
# game.start_new(20, 'small')
ledger = game.run()

# for i in range(0,1):
#     game.start_new(7, 'fast', ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])
#     ledger = game.run()
#     speed = ledger.get_speed()
#     print(f"{ledger.initial_state.inbox} ==> {speed}")
#     if game.ledger.error_state:
#         print(game.ledger.error_state)


print(ledger)
print(ledger.get_goal_table())
