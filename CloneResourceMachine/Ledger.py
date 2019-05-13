
from prettytable import PrettyTable
from collections import namedtuple
from CloneResourceMachine.Expected import Expected

Step = namedtuple('step', "line command inbox holding registers outbox comment")
Result = namedtuple('result', 'passed, speed, size, fast, small, fast_enough')


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

        result = self.get_result()
        if result.passed:
            passing = 'PASS'
        else:
            passing = 'FAIL'

        speed_res = ''
        if result.fast:
            speed_res = 'FAST'
        elif result.fast_enough:
            speed_res = '(expected)'

        size_res = ''
        if result.small:
            size_res = 'SMALL'

        goal = self.level.goal
        actual_speed = self.get_speed()
        actual_size = self.program.get_size()
        outbox = self.outbox

        goal_table = PrettyTable([
            'type', 'goal', 'expected', 'actual', 'result'
        ])

        for n in ['type', 'result']:
            goal_table.align[n] = 'l'

        # I think I like left align for these now?
        for n in ['goal', 'expected', 'actual']:
            goal_table.align[n] = 'l'

        expect_size = self.program.size or goal.size
        expect_speed = self.program.speed or goal.speed
        goal_table.add_row(['input', '', '', self.initial_state.inbox, ''])
        goal_table.add_row([goal.formula, '', self.expected.output, str(outbox), passing])
        goal_table.add_row(['size', goal.size, expect_size, actual_size, size_res ])
        goal_table.add_row(['speed', goal.speed, expect_speed, actual_speed, speed_res])

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
        expect_speed = self.program.speed or goal.speed

        fast = False
        small = False
        passed = False
        fast_enough = False
        speed = actual_speed
        size = actual_size

        if self.expected.output == self.outbox:
            passed = True

        if actual_speed <= goal.speed:
            fast = True
            fast_enough = True
        elif actual_speed <= expect_speed:
            fast_enough = True

        if actual_size <= goal.size:
            small = True

        return Result(passed, speed, size, fast, small, fast_enough)

    def __repr__(self):
        return "=== {} - {} : {}\n".format(
             self.level.key, self.level.name, self.program.key) + self.get_result_table()
