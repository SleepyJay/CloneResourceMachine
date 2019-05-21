
from collections import namedtuple
from JAGpy.Structs import lookup
from JAGpy.Numbers import intify
from CloneResourceMachine.InputDetails import InputDetails
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

        self.input_details = None
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

    def process_programs(self, programs_data) -> None:
        if not programs_data:
            return

        for key, program in programs_data.items():
            self.programs[key] = Program(self.key, key, program, self.available_cmds)

    def process_registers(self, register_data) -> None:
        if not register_data:
            self.registers = Registers(0, {})
            return

        self.registers = \
            Registers(lookup(register_data, 'count', 0), lookup(register_data, 'values', {}))

    def process_input(self, input_data) -> None:
        if not input_data:
            return

        self.input_details = InputDetails(input_data)

    def process_goal(self, goal_data) -> None:
        if not goal_data:
            return

        # "Expected" here is if there is ONE and ONLY ONE output for ANY GIVEN input_details
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

    def get_new_sample(self):
        return self.input_details.get_new_sample()

    def get_formula(self):
        return self.goal.formula

    def get_discrete_input(self):
        return self.input_details.discrete


