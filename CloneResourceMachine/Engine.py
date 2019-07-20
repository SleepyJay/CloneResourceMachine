
from JAGpy.Numbers import intify

# Engine runs one level at a time
# Can run same or different programs over and over
# Ledger stores each program run for each input


class Engine(object):

    def __init__(self, level, program, ledger):
        self.level = level
        self.program = program
        self.ledger = ledger
        self.input = ledger.input.copy()

        self.cur_command = None
        self.cur_item = None
        self.next = 0
        self.output = []
        self.registers = None

        if program:
            self.labels = program.labels
            self.commands = program.commands

        self.build_registers(level.registers)

        ledger.capture_init_state(self.registers)

    def build_registers(self, registers_obj):
        if not registers_obj:
            return

        self.registers = dict()

        for key, val in registers_obj.values.items():
            self.registers[str(key)] = intify(val)

        for r in range(0, registers_obj.count):
            str_r = str(r)
            if str_r not in self.registers:
                self.registers[str_r] = ''

    def step(self):
        if self.next >= len(self.program.commands):
            return None

        command = self.program.commands[self.next]

        self.next += 1

        if command is None:
            return None

        if command.name == 'echo':
            pass

        elif command.name == 'inbox':
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
            self.cur_item = self.registers[command.val]

        elif command.name == 'copyto':
            if self.cur_item is None:
                self.error_no_current_item()
            else:
                self.registers[command.val] = self.cur_item

        elif command.name == 'jump':
            self.do_jump(command.val)

        elif command.name == 'jumpzero':
            if self.cur_item is None:
                self.error_no_current_item()
            elif not isinstance(self.cur_item, int):
                pass
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
            self.cur_item += self.registers[command.val]

        elif command.name == 'sub':
            self.cur_item -= self.registers[command.val]

        elif command.name == 'bump+':
            self.cur_item = self.registers[command.val] + 1
            self.registers[command.val] = self.cur_item

        elif command.name == 'bump-':
            self.cur_item = self.registers[command.val] - 1
            self.registers[command.val] = self.cur_item

        else:
            return None

        self.cur_command = command

        step = self.ledger.capture_state(self)

        if self.ledger.get_error():
            return None

        return step

    # These "error_" methods are "soft" errors, like a "halting warning", really.

    def error_bad_command(self, bad_command):
        self.ledger.capture_error_state(f"Error: Bad command found: {bad_command}")

    def error_no_current_item(self):
        self.ledger.capture_error_state('Error: No current item!')

    def error_bad_jump(self, val):
        self.ledger.capture_error_state(f"Error: Cannot jump to {val}!")

    def error_bad_input(self):
        self.ledger.capture_error_state('Error: Cannot use that value ({})!'.format(self.cur_item))

    def do_jump(self, val):
        # added labels in this program; not part of original game
        if str(val) in self.labels:
            self.next = self.labels[str(val)]
        else:
            try:
                val = int(val)

                if val >= len(self.program.commands):
                    self.error_bad_jump(val)
                    return

                else:
                    self.next = val - 1

            except ValueError:
                self.error_bad_jump(val)
                return

    def finish(self):
        self.ledger.capture_end_state(self.input, self.output)
        return self.ledger
