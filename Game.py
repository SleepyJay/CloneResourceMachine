
from Roboto.Engine import Engine
from Roboto.Catalog import Catalog

MAX_ITERS = 1000


class Game(object):

    def __init__(self):
        self.engine = None
        self.catalog = None
        self.current_level = None

    def load_level_file(self, filename):
        if not self.catalog:
            self.catalog = Catalog()

        self.catalog.load_file(filename)

    def load_level_data(self, key, data):
        if not self.catalog:
            self.catalog = Catalog()

        self.catalog.load_data(key, data)

    def start_new(self, level_key, solution_key, l_input=None):
        level = self.catalog.get_level(level_key)
        self.current_level = level

        self.engine = Engine(level, solution_key, l_input)

    def restart(self, l_input=None):
        level = self.engine.level_obj
        solution_key = self.engine.solution_key

        self.engine = Engine(level, solution_key, l_input)

    def run(self):
        i = 0
        while self.engine.step() and i < MAX_ITERS:
            i += 1

        self.engine.confirm_result()
        return self.engine.get_ledger()

    def step(self, to_line=None):
        i = 0
        if to_line and i < MAX_ITERS:
            while self.engine.cur_line != to_line and self.engine.step():
                i += 1
        else:
            return self.engine.step()

    # TODO: implement this
    def step_back(self, to_line=None):
        print("not yet implemented")

    def confirm(self, l_output=None):
        return self.engine.confirm_result(l_output)

    def get_ledger(self):
        return self.engine.get_ledger()

    def get_goal(self):
        return self.current_level.goal

    def get_outbox(self):
        return self.engine.output