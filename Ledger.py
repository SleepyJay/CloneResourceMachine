
from prettytable import PrettyTable
from collections import namedtuple

Step = namedtuple('step', "line command inbox holding registers outbox comment")

# TODO: I think this relationship needs a change
class Ledger(object):

    def __init__(self, level_obj, solution_obj):
        self.steps = []
        self.level = level_obj
        self.solution = solution_obj
        self.input = None





        self.level_name = ''
        self.level_key = ''
        self.solution_key = ''
        self.expected = None
        self.goal = None
        self.command_count = 0
        self.initial_state = None
        self.error_state = None
        self.iter = 0

    def yy_capture_step(self):
        step:
        line, command, inbox, holding, registers, outbox, comment

    def yy_capture_finish(self):
        actual:
            size, speed, output

    def capture_init_state(self, input, registers, name='start'):
        self.initial_state = Step('', name, str(input), '', str(registers), [], '')

        self.expected_size = self.solution.size or self.goal.size
        self.expected_speed = self.solution.speed or self.goal.speed

        self.command_count = len(engine.solution.commands)

        self.level_name = engine.level_obj.name
        self.level_key = engine.level_obj.key
        self.solution_key = engine.solution.key

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
                line =  "{} ({})".format(line, command.label)

            cmd = command.name
            if command.val:
                cmd = cmd + " " + command.val

            state_table.add_row([
                self.iter + 1,
                line + 1,
                cmd,
                step.inbox,
                step.holding,
                step.registers,
                step.outbox,
                command.comment or '',
            ])
            self.iter += 1

        ledger_str = str(state_table)
        if self.error_state:
            print(self.error_state)
            ledger_str += "\n{}\n".format(self.error_state)

        return ledger_str

    def get_goal_table(self, outbox=None):
        goal = self.goal
        exp_output = str(goal.expected)
        actual_speed = self.get_speed()
        actual_size = self.get_size()

        if exp_output == outbox:
            passing = 'FAIL'
        else:
            passing = 'PASS'

        speed_res = ''
        if actual_speed <= goal.speed:
            speed_res = 'FAST'
        elif actual_speed != self.expected_speed:
            speed_res = 'slow?'

        size_res = ''
        if actual_size <= goal.size:
            size_res = 'SMALL'
        elif actual_size != self.expected_size:
            size_res = 'long?'

        goal_table = PrettyTable([
            'type', 'goal', 'expected', 'actual', 'boxes', 'result'
        ])

        for n in ['type', 'boxes', 'result']:
            goal_table.align[n] = 'l'

        for n in ['goal', 'expected', 'actual']:
            goal_table.align[n] = 'r'

        goal_table.add_row(['input', '', '', '', self.initial_state.inbox, ''])
        goal_table.add_row([goal.formula, '', '', '', str(outbox), passing])
        goal_table.add_row(['size', goal.size, self.expected_size, actual_size, '', size_res ])
        goal_table.add_row(['speed', goal.speed, self.expected_speed, actual_speed, '', speed_res])

        return str(goal_table)

    def get_size(self):
        return self.command_count

    def get_speed(self):
        return len(self.steps)

    def __repr__(self):
        return "=== {} - {} : {}\n".format(
            self.level_name, self.level_key, self.solution_key) + self.get_result_table()







