
from CloneResourceMachine.Engine import Engine
from CloneResourceMachine.Catalog import Catalog
from CloneResourceMachine.Ledger import Ledger

MAX_ITERS = 1000


class Game(object):

    def __init__(self):
        self.engine = None
        self.catalog = None
        self.current_level = None
        self.ledgers = []
        self.ledger = None

    def load_single_level_file(self, filename):
        if not self.catalog:
            self.catalog = Catalog()

        self.catalog.load_single_file(filename)

    def load_multi_level_file(self, filename):
        if not self.catalog:
            self.catalog = Catalog()

        self.catalog.load_multi_file(filename)

    def load_level_data(self, data):
        if not self.catalog:
            self.catalog = Catalog()

        self.catalog.load_data(data)

    def start_new(self, level_key, program_key, l_input=None):
        self.current_level = self.catalog.get_level(level_key)

        if self.current_level.is_movie:
            return

        self._build_new_engine(program_key, l_input)

    def restart(self, l_input=None):
        if self.current_level.is_movie:
            return

        program_key = self.engine.program_key

        self._build_new_engine(program_key, l_input)

    def _build_new_engine(self, program_key, l_input):
        self.engine = Engine(self.current_level, program_key, l_input)

        if self.ledger:
            self.ledgers.append(self.ledger)

        self.ledger = Ledger(self.current_level, self.engine.program)
        self.ledger.capture_init_state(self.engine.input, self.engine.registers)
        self.engine.ledger = self.ledger

        self.confirm_available()

    def confirm_available(self):
        program = self.engine.program
        for cmd in program.commands:
            if cmd.name not in self.current_level.available:
                self.engine.error_bad_command(cmd.name)

    def run(self):
        if self.current_level.is_movie:
            self.play_movie(self.current_level)
            return

        i = 0
        while self.engine.step() and i < MAX_ITERS:
            i += 1

        return self.engine.finish()

    def step(self, to_line=None):
        if self.current_level.is_movie:
            self.play_movie(self.current_level)
            return

        i = 0
        if to_line and i < MAX_ITERS:
            while self.engine.cur_line != to_line and self.engine.step():
                i += 1
        else:
            return self.engine.step()

    def confirm_result(self, l_output=None):
        if self.current_level.is_movie:
            return

        return self.engine.confirm_result(l_output)

    def get_ledger(self):
        return self.engine.get_ledger()

    def get_goal(self):
        return self.current_level.goal

    def get_outbox(self):
        return self.engine.output

    def play_movie(self, level):
        print("Level Movie: '{} - {}'".format(level.key, level.name))