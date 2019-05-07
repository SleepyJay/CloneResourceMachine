
from collections import namedtuple
from JAGpy.Structs import lookup
from JAGpy.Numbers import intify
from CloneResourceMachine.Input import Input
from CloneResourceMachine.Goal import Goal
import re

Program = namedtuple('program', 'key commands size speed labels')
Command = namedtuple('command', 'line name val label comment')
Registers = namedtuple('registers', 'count values')

# parse something like [label:] cur_command [value] [# comment]
RE_cmd = re.compile(r'(?:(?P<lbl>\w+):)?\s*(?P<cmd>\w+)\s*(?P<val>\w+)?\s*(?P<cmt>[#]\s*.*)?')
RE_echo = re.compile(r'(echo)\s+(.*)')
ALWAYS_AVAILABLE = ['echo']


class Level(object):

    def __init__(self, key, data):
        self.original_data = data
        self.key = str(key)
        self.name = lookup(data, 'name')
        self.is_movie = lookup(data, 'movie')

        self.available = []
        self.goal = None
        self.input = None
        self.registers = None
        self.programs = None
        self.inboxes = []        # list of input tried

        self.process_data(data)

    def process_data(self, data):
        if self.is_movie:
            return

        self.available = lookup(data, 'available', [])
        self.available.extend(ALWAYS_AVAILABLE)

        self.goal = self.process_goal(lookup(data, 'goal'))
        self.input = self.process_input(lookup(data, 'input'))
        self.registers = self.process_registers(lookup(data, 'registers'))
        self.programs = self.process_programs(lookup(data, 'programs', dict()))

    def get_program(self, key):
        if self.is_movie:
            return None

        sol = lookup(self.programs, key)

        if not sol and (key == 'fast' or key == 'small'):
            sol = lookup(self.programs, 'optimal')

        return sol

    def process_programs(self, programs_data):
        if self.is_movie:
            return

        programs = dict()

        for key, program in programs_data.items():
            pre_commands = []

            # expand any repeats
            for cmd_item in program['commands']:
                if type(cmd_item) is dict:
                    cmd_repeat = cmd_item['repeat']
                    count = cmd_repeat['count']

                    for i in range(0, count):
                        pre_commands.extend(cmd_repeat['commands'])
                else:
                    pre_commands.append(cmd_item)

            ln = 0
            labels = dict()
            commands = []

            for str_cmd in pre_commands:
                command = self.process_str_command(ln, str_cmd)

                if not command:
                    continue

                if command.label is not None:
                    labels[command.label] = ln

                commands.append(command)

                ln += 1

            size = lookup(program, 'size', self.goal.size)
            speed = lookup(program, 'speed', self.goal.speed)

            programs[key] = Program(key, commands, size, speed, labels)

        return programs

    def process_str_command(self, ln, str_cmd):
        # just stripping any comments (for now?)
        if str_cmd.startswith('#'):
            return

        m = RE_cmd.match(str_cmd)
        (cmd, val, lbl, cmt) = m.group('cmd', 'val', 'lbl', 'cmt')

        if cmd == 'echo':
            m = RE_echo.match(str_cmd)
            (cmd, val) = m.groups()

        command = Command(ln, cmd, val, lbl, cmt)

        return command

    def process_registers(self, register_data):
        if self.is_movie:
            return

        if not register_data:
            return Registers(0, [])

        values = lookup(register_data, 'values', [])

        for key in values:
            values[key] = intify(values[key])

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


