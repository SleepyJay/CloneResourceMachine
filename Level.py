
from collections import namedtuple
from JAGpy.Structs import lookup
from Input import Input
from Goal import Goal
import re

Solution = namedtuple('solution', 'key commands size speed labels')
Command = namedtuple('command', 'line name val label comment')
Registers = namedtuple('registers', 'count values')

# parse something like [label:] cur_command [value] [# comment]
RE_cmd = re.compile(r'(?:(?P<lbl>\w+):)?\s*(?P<cmd>\w+)\s*(?P<val>\w+)?\s*(?P<cmt>[#]\s*.*)?')


class Level(object):

    def __init__(self, key, data):
        self.original_data = data
        self.key = str(key)
        self.name = lookup(data, 'name')
        self.available = lookup(data, 'available', [])

        self.goal = self.process_goal(lookup(data, 'goal'))
        self.input = self.process_input(lookup(data, 'input'))
        self.registers = self.process_registers(lookup(data, 'registers'))
        self.solutions = self.process_solutions(lookup(data, 'solutions'))

        # list of input tried
        self.inboxes = []

    def get_solution(self, key):
        sol = lookup(self.solutions, key)

        if not sol and (key == 'fast' or key == 'small'):
            sol = lookup(self.solutions, 'optimal')

        return sol

    def process_solutions(self, solutions_data):
        solutions = dict()

        for key, solution in solutions_data.items():
            pre_commands = []

            # expand any repeats
            for cmd_item in solution['commands']:
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
                # just stripping any comments (for now?)
                if str_cmd.startswith('#'):
                    continue

                m = RE_cmd.match(str_cmd)
                (cmd, val, lbl, cmt) = m.group('cmd', 'val', 'lbl', 'cmt')

                command = Command(ln, cmd, val, lbl, cmt)

                if not command:
                    continue

                if command.label is not None:
                    labels[command.label] = ln

                commands.append(command)

                ln += 1

            size = lookup(solution, 'size', self.goal.size)
            speed = lookup(solution, 'speed', self.goal.speed)

            solutions[key] = Solution(key, commands, size, speed, labels)

        return solutions

    def process_registers(self, register_data):
        if not register_data:
            return Registers(0, [])

        return Registers(lookup(register_data, 'count', 0), lookup(register_data, 'registers', []))

    def process_input(self, input_data):
        input = Input(
            lookup(input_data, 'alphabet'), lookup(input_data, 'count'), lookup(input_data, 'sample'))

        return input

    def process_goal(self, goal_data):
        # print("fomula: {}".format(lookup(goal_data, 'formula')))
        return Goal(
            lookup(goal_data, 'formula'), lookup(goal_data, 'size'),
            lookup(goal_data, 'speed'), lookup(goal_data, 'expected'))

