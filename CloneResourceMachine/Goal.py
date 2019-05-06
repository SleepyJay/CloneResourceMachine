
from CloneResourceMachine.Expected import Expected


class Goal(object):

    def __init__(self, formula, size, speed, expected=None):
        self.formula = formula
        self.size = size
        self.speed = speed
        self.expected = None

    def prepare_expected(self, program):
        self.expected = Expected(program, self)

    def get_expected(self):
        return self.expected

