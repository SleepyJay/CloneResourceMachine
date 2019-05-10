
from collections import namedtuple
from JAGpy.Structs import lookup
from JAGpy.Numbers import intify
from CloneResourceMachine.Input import Input
from CloneResourceMachine.Goal import Goal
from CloneResourceMachine.Program import Program

Registers = namedtuple('registers', 'count values')
ALWAYS_AVAILABLE = ['echo']


class Level(object):

    def __init__(self, key, data):
        self.original_data = data
        self.key = str(key)
        self.name = lookup(data, 'name')
        self.is_movie = lookup(data, 'movie')
        self.programs = dict()
        self.available_cmds = []

        self.goal = None
        self.input = None
        self.registers = None
        self.inboxes = []        # list of input tried

        self.process_data(data)

    def process_data(self, data):
        if self.is_movie:
            return

        self.available_cmds = lookup(data, 'available', [])
        self.available_cmds.extend(ALWAYS_AVAILABLE)

        self.goal = self.process_goal(lookup(data, 'goal'))
        self.input = self.process_input(lookup(data, 'input'))
        self.registers = self.process_registers(lookup(data, 'registers'))

        self.process_programs(lookup(data, 'programs', dict()))

    def process_programs(self, programs_data):
        for key, program in programs_data.items():
            self.programs[key] = \
                Program(self.key, key, program, self.available_cmds)

    def get_program(self, key):
        if self.is_movie:
            return None

        sol = lookup(self.programs, key)

        if not sol and (key == 'fast' or key == 'small'):
            sol = lookup(self.programs, 'optimal')

        return sol

    def process_registers(self, register_data):
        if self.is_movie:
            return

        if not register_data:
            return Registers(0, [])

        values = lookup(register_data, 'values', [])

        new_vals = dict()

        for key in values:
            new_vals[str(key)] = values[key]

        return Registers(lookup(register_data, 'count', 0), values)

    def process_input(self, input_data):
        if self.is_movie:
            return

        if not input_data:
            return

        input_obj = Input(
            lookup(input_data, 'alphabet'), lookup(input_data, 'count'), lookup(input_data, 'sample'))

        return input_obj

    def process_goal(self, goal_data):
        if self.is_movie:
            return

        if not goal_data:
            return

        return Goal(
            lookup(goal_data, 'formula'), lookup(goal_data, 'size'),
            lookup(goal_data, 'speed'), lookup(goal_data, 'expected'))


