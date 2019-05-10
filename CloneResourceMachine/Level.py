
from collections import namedtuple
from JAGpy.Structs import lookup
from JAGpy.Numbers import intify
from CloneResourceMachine.Input import Input
from CloneResourceMachine.Program import Program

Registers = namedtuple('registers', 'count values')
Goal = namedtuple('goal', 'formula size speed expected')
ALWAYS_AVAILABLE = ['echo']


class Level(object):

    def __init__(self, key, data) -> None:
        self.original_data = data
        self.key = str(key)
        self.name = lookup(data, 'name')
        self.is_movie = lookup(data, 'movie')
        self.programs = dict()
        self.available_cmds = []

        self.input = None
        self.goal = None
        self.registers = None

        self.process_data(data)

    def process_data(self, data):
        if self.is_movie:
            return

        self.available_cmds = lookup(data, 'available', [])
        self.available_cmds.extend(ALWAYS_AVAILABLE)

        self.process_input(lookup(data, 'input'))
        self.process_goal(lookup(data, 'goal'))
        self.process_registers(lookup(data, 'registers'))
        self.process_programs(lookup(data, 'programs'))

    def process_programs(self, programs_data):
        if not programs_data:
            return

        for key, program in programs_data.items():
            self.programs[key] = \
                Program(self.key, key, program, self.available_cmds)

    def process_registers(self, register_data):
        if not register_data:
            return Registers(0, [])

        values = lookup(register_data, 'values', [])

        new_vals = dict()

        # string-ify all keys
        for key in values:
            new_vals[str(key)] = values[key]

        return Registers(lookup(register_data, 'count', 0), new_vals)

    def process_input(self, input_data):
        if not input_data:
            return

        self.input = Input(input_data)

    def process_goal(self, goal_data):
        if not goal_data:
            return

        # "Expected" here is if there is ONE and ONLY ONE output for ANY GIVEN input
        # (e.g. Level 3 in the main game has this property)
        self.goal = Goal(
            lookup(goal_data, 'formula'), lookup(goal_data, 'size'),
            lookup(goal_data, 'speed'), lookup(goal_data, 'expected'))

    def get_program(self, key):
        if self.is_movie:
            return None

        sol = lookup(self.programs, key)

        if not sol and (key == 'fast' or key == 'small'):
            sol = lookup(self.programs, 'optimal')

        return sol


