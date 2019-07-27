
from collections import namedtuple
from JAGpy.Structs import lookup
import re

Command = namedtuple('command', 'line name val label comment')

# parse something like [label:] cur_command [value] [# comment]
RE_cmd = re.compile(r'(?:(?P<lbl>\w+):)?\s*(?P<cmd>[\w+-]+)\s*(?P<val>\w+)?\s*(?P<cmt>[#]\s*.*)?')
RE_echo = re.compile(r'(echo)\s+(.*)')


class Program(object):

    def __init__(self, level_key, key, data, available_cmds=None):
        self.key = str(key)
        self.level_key = str(level_key)
        self.commands = []
        self.labels = dict()
        self.available_cmds = available_cmds or []
        self.orig_data = data

        # These are like "acceptable" values, which may differ from the goal values,
        # in which if set, override the goal values:
        self.size = 0
        self.speed = 0

        self.process_data(data)

    def process_data(self, data):
        if not data:
            return

        pre_commands = []

        # expand any repeats
        for cmd_item in data['commands']:
            if type(cmd_item) is dict:
                cmd_repeat = lookup(cmd_item, 'repeat')
                if cmd_repeat:
                    count = cmd_repeat['count']

                    for i in range(0, count):
                        pre_commands.extend(cmd_repeat['commands'])
                continue

            pre_commands.append(cmd_item)

        ln = 0

        for str_cmd in pre_commands:
            command = self.process_str_command(ln, str_cmd)

            if not command:
                continue

            assert (command.name in self.available_cmds), \
                f"Command {command.name} not available to program {self.level_key}-{self.key}!"

            if command.label is not None:
                self.labels[command.label] = ln

            self.commands.append(command)

            ln += 1

        self.size = lookup(data, 'size', 0)
        self.speed = lookup(data, 'speed', 0)

    # We don't count all commands (like `echo` in this size...
    def get_size(self):
        size = 0
        for cmd in self.commands:
            if cmd.name == 'echo':
                continue
            size += 1

        return size

    @staticmethod
    def process_str_command(ln, str_cmd):
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


