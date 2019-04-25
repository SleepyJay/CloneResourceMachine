
# Lets support these commands:
    #[] `inbox` : get item from inbox
    #[] `outbox`: put item into outbox
    #[] `copyfrom $r`: copy value from register $r
    #[] `copyto $r`: copy value to register $r
    #[] `jump $p|$l`: jump to program line number or label
    #[] `jump_zero $p|$l`
    #[] `jump_neg $p|$l`
    #[] `add`
    #[] `sub`
    #[] `echo $m`
    #[] `# $m`
    #[] `@l`

# Config
    #[] `registers $n`
    #[] `alphabet $a`
    #[] `goal_instructions $n`
    #[] `goal_runtime $n`
    #[] `instruct_set $a`
    #[] `expected $x`
    #[] `input $x`

from Ledger import Ledger
from Expected import Expected

# Engine runs one level at a time
# Can run same or different programs over and over
# Ledger stores each run for this level

class Engine(object):

    def __init__(self, level_obj, program_key, l_input=None):
        self.level_obj = level_obj
        self.program_key = program_key
        self.program = level_obj.get_program(program_key)
        self.goal = level_obj.goal

        self.input = l_input or self.create_input(level_obj.input)
        self.registers = build_registers(level_obj.registers)

        self.command_list = self.program.commands
        self.output = []
        self.expected = None

        self.labels = self.program.labels

        self.next = None
        self.cur_command = ''
        self.cur_item = None
        self.next = 0
        self.ledger = None

    # TODO: finish this
    def create_input(self, input_obj):
        return input_obj.build_new_sample()

    def step(self, command=None):
        if self.next >= len(self.program.commands):
            return None

        command = self.program.commands[self.next]

        self.next += 1

        if command is None:
            return None

        if command.name == 'inbox':
            if self.input:
                self.cur_item = self.input.pop(0)
            else:
                return None

        elif command.name == 'outbox':
            if self.cur_item is None:
                self.error_no_current_item()
            else:
                self.output.append(self.cur_item)
                self.cur_item = None

        elif command.name == 'copyfrom':
            # TODO: maybe should confirm this is a number?
            self.cur_item = self.registers[int(command.val)]

        elif command.name == 'copyto':
            if self.cur_item is None:
                self.error_no_current_item()
            else:
                self.registers[int(command.val)] = self.cur_item

        elif command.name == 'jump':
            self.do_jump(command.val)

        elif command.name == 'jumpzero':
            if self.cur_item is None:
                self.error_no_current_item()
            elif not isinstance(self.cur_item, int):
                self.error_bad_input()
            elif self.cur_item == 0:
                self.do_jump(command.val)

        elif command.name == 'jumpneg':
            if self.cur_item is None:
                self.error_no_current_item()
            elif not isinstance(self.cur_item, int):
                self.error_bad_input()
            elif self.cur_item < 0:
               self.do_jump(command.val)

        elif command.name == 'add':
            self.cur_item += self.registers[int(command.val)]

        elif command.name == 'sub':
            self.cur_item -= self.registers[int(command.val)]

        elif command.name == 'bump+':
            self.cur_item = self.registers[command.val] + 1
            self.registers[int(command.val)] = self.cur_item

        elif command.name == 'bump-':
            self.cur_item = self.registers[command.val] - 1
            self.registers[int(command.val)] = self.cur_item

        else:
            return None

        self.cur_command = command

        step = self.ledger.capture_state(self)

        if self.ledger.get_error():
            return None

        return step

    # These "error_" methods are "soft" errors, like a "halting warning", really.

    def error_no_current_item(self):
        self.ledger.capture_error_state('Error: No current item!')

    def error_bad_jump(self):
        self.ledger.capture_error_state('Error: Cannot jump there!')

    def error_bad_input(self):
        self.ledger.capture_error_state('Error: Cannot use that value ({})!'.format(self.cur_item))

    def do_jump(self, val):
        # added labels in this program; not part of original game
        if val in self.labels:
            self.next = self.labels[val]
        else:
            try:
                val = int(val)
            except:
                self.error_bad_jump()
                return

        if val >= len(self.program.commands):
            self.error_bad_jump()
            return

        else:
            self.next = val - 1

    # TODO: implement this
    def confirm_result(self, l_output=None):
        result = 'unknown'
        self.ledger.result = result

        return result

    def get_ledger(self):
        return self.ledger

    def get_goal(self):
        return self.goal

    def get_expected(self):
        if self.expected:
            return self.expected

        self.expected = Expected(self.program, self.goal)


def build_registers(registers_obj):
    registers = []

    # build a list of registers, with any starting values filled in...
    for r in range(0, registers_obj.count):
        registers.append('')

    if registers_obj.values:
        for key in registers_obj.values:
            registers[key] = registers_obj.values[key]

    return registers

