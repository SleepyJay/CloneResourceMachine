
from prettytable import PrettyTable
from collections import namedtuple

Step = namedtuple('step', "line command inbox holding registers outbox comment")


# TODO: I think this relationship needs a change
class Ledger(object):

    def __init__(self, level_obj, program_obj):
        self.steps = []
        self.level = level_obj
        self.program = program_obj
        self.goal = self.level.goal
        self.initial_state = None
        self.ending_state = None
        self.error_state = None
        self.outbox = []
        self.iter = 0

    def capture_init_state(self, l_input, registers, name='start'):
        self.initial_state = Step('', name, str(l_input), '', str(registers), [], '')

    def capture_error_state(self, message):
        self.error_state = message

    def capture_state(self, engine, command=None):
        command = command or engine.cur_command
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

            line = command.line
            if command.label:
                line = "{} ({})".format(line, command.label)

            cmd = command.name
            if command.val:
                cmd = cmd + " " + command.val

            self.iter += 1

            state_table.add_row([
                self.iter, line + 1, cmd, step.inbox, step.holding,
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

    def get_goal_table(self, outbox=None):
        goal = self.goal
        exp_output = goal.expected.output
        actual_speed = self.get_speed()
        actual_size = self.get_size()
        outbox = outbox or self.outbox

        print("exp({}): {}".format(type(exp_output), exp_output))
        print("act({}): {}".format(type(outbox), outbox))
        if exp_output == outbox:
            passing = 'PASS'
        else:
            passing = 'FAIL'

        speed_res = ''
        if actual_speed <= goal.speed:
            speed_res = 'FAST'
        elif actual_speed != self.goal.speed:
            speed_res = '(slow?)'

        size_res = ''
        if actual_size <= goal.size:
            size_res = 'SMALL'
        elif actual_size != self.goal.size:
            size_res = '(long?)'

        goal_table = PrettyTable([
            'type', 'goal', 'expected', 'actual', 'in/out boxes', 'result'
        ])

        for n in ['type', 'boxes', 'result']:
            goal_table.align[n] = 'l'

        for n in ['goal', 'expected', 'actual']:
            goal_table.align[n] = 'r'

        goal_table.add_row(['input', '', '', '', self.initial_state.inbox, ''])
        goal_table.add_row([goal.formula, '', '', '', str(outbox), passing])
        goal_table.add_row(['size', goal.size, goal.size, actual_size, '', size_res ])
        goal_table.add_row(['speed', goal.speed, goal.speed, actual_speed, '', speed_res])

        return str(goal_table)

    def get_size(self):
        size = 0
        for cmd in self.program.commands:
            if cmd.name == 'echo':
                continue
            size += 1

        return size

    def get_speed(self):
        speed = 0
        for step in self.steps:
            if step.command.name == 'echo':
                continue
            speed += 1

        return speed

    def capture_end_state(self, l_input, outbox):
        # line command inbox holding registers outbox comment
        self.outbox = outbox
        self.ending_state = Step('', 'end', str(l_input), '', str([]), outbox, '')

    def __repr__(self):
        return "=== {} - {} : {}\n".format(
             self.level.key, self.level.name, self.program.key) + self.get_result_table()
