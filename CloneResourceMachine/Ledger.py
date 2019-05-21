
from prettytable import PrettyTable
from collections import namedtuple
from CloneResourceMachine.Expected import Expected

Step = namedtuple('step', "line command inbox holding registers outbox comment")
Result = namedtuple('result', 'passed, speed, size, fast, small')


class Ledger(object):

    def __init__(self, level_obj, program_obj, list_input=None):
        self.steps = []
        self.level = level_obj
        self.program = program_obj

        self.initial_state = None
        self.ending_state = None
        self.error_state = None

        self.input = None
        self.expected = None
        self.iter = 0
        self.outbox = None

        self._build_input(list_input)

    def _build_input(self, list_input=None):
        if not list_input:
            list_input = self.level.get_new_sample()

        self.input = list_input
        self.expected = Expected(self.level.get_formula(), self.input)

    def capture_init_state(self, registers, name='start'):
        self.initial_state = Step('', name, str(self.input), '', str(registers), [], '')

    def capture_error_state(self, message):
        self.error_state = message

    def capture_state(self, engine):
        command = engine.cur_command
        line = engine.next

        if line is None:
            line = ''

        step = Step(
            line, command, str(engine.input), engine.cur_item, str(engine.registers),
            str(engine.output), command.comment or ''
        )

        self.steps.append(step)

        return step

    def get_error(self):
        return self.error_state

    def get_result_table(self):
        state_table = PrettyTable(
            ["i", "line", "command", "inbox", "holding", "registers", "outbox", "comment"])

        for n in state_table.field_names:
            state_table.align[n] = 'l'

        init = self.initial_state
        state_table.add_row([
            '', init.line, init.command, init.inbox, init.holding, init.registers, init.outbox, ''
        ])

        for step in self.steps:
            command = step.command

            line = command.line + 1
            if command.label:
                line = "{} ({})".format(line, command.label)

            cmd = command.name
            if command.val:
                cmd = cmd + " " + command.val

            self.iter += 1

            state_table.add_row([
                self.iter, line, cmd, step.inbox, step.holding,
                step.registers, step.outbox, command.comment or ''
            ])

        final = self.ending_state
        state_table.add_row([
            '', final.line, final.command, final.inbox,
            final.holding, final.registers, final.outbox, ''
        ])

        ledger_str = str(state_table)
        if self.error_state:
            print(self.error_state)
            ledger_str += "\n{}\n".format(self.error_state)

        return ledger_str

    def get_goal_table(self):
        goal = self.level.goal
        actual_speed = self.get_speed()
        actual_size = self.program.get_size()
        outbox = self.outbox
        expect_speed = self.program.speed or goal.speed

        result = self.get_result()
        if result.passed:
            passing = 'PASS'
        else:
            passing = 'FAIL'

        speed_res = ''
        if result.fast:
            speed_res = 'FAST'
        #elif
        elif actual_speed <= expect_speed:
            speed_res = '(expected)'

        size_res = ''
        if result.small:
            size_res = 'SMALL'

        goal_table = PrettyTable([
            'type', 'formula', 'size', 'speed', 'values'
        ])

        for n in ['type', 'formula', 'values']:
            goal_table.align[n] = 'l'

        for n in ['size', 'speed']:
            goal_table.align[n] = 'r'

        expect_size = self.program.size or goal.size
        expect_speed = self.program.speed or goal.speed
        goal_table.add_row(['input', goal.formula, goal.size, goal.speed, self.initial_state.inbox])
        goal_table.add_row(['expected', '', expect_size, expect_speed, self.expected.output])
        goal_table.add_row(['actual', '', actual_size, actual_speed, str(outbox)])
        goal_table.add_row(['result', '', size_res, speed_res, passing])

        return str(goal_table)

    def get_speed(self):
        speed = 0
        for step in self.steps:
            if step.command.name == 'echo':
                continue
            speed += 1

        return speed

    def capture_end_state(self, l_input, outbox):
        # line command inbox holding registers outbox comment
        self.outbox = outbox.copy()
        self.ending_state = Step('', 'end', str(l_input), '', '', self.outbox, '')

    def get_result(self):
        actual_speed = self.get_speed()
        actual_size = self.program.get_size()
        goal = self.level.goal

        fast = False
        small = False
        passed = False
        speed = actual_speed
        size = actual_size

        if self.expected.output == self.outbox:
            passed = True

        if actual_speed <= goal.speed:
            fast = True

        if actual_size <= goal.size:
            small = True

        return Result(passed, speed, size, fast, small)

    def __repr__(self):
        return "=== {} - {} : {}\n".format(
             self.level.key, self.level.name, self.program.key) + self.get_result_table()
