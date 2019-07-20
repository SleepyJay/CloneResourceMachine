
from collections import namedtuple
from CloneResourceMachine.Engine import Engine
from CloneResourceMachine.Catalog import Catalog
from CloneResourceMachine.Ledger import Ledger

AvgResult = namedtuple('avg_result', 'all_passed, best_speed, worst_speed, avg_speed, passed, failed')

MAX_ITERS = 1000


class Game(object):

    def __init__(self):
        # This object is really only to abstract the YAML parsing into Levels,
        # no need to expose it anywhere.
        self.__catalog = None
        self.engine = None

        self.current_level = None
        self.program = None
        self.ledgers = []
        self.ledger = None

    @property
    def levels(self):
        return self.__catalog.levels

    def load_single_level_file(self, filename):
        if not self.__catalog:
            self.__catalog = Catalog()

        self.__catalog.load_single_file(filename)

    def load_multi_level_file(self, filename):
        if not self.__catalog:
            self.__catalog = Catalog()

        self.__catalog.load_multi_file(filename)

    def load_level_data(self, data):
        if not self.__catalog:
            self.__catalog = Catalog()

        self.__catalog.load_data(data)

    def start_new(self, level_key, program_key, list_input=None):
        self.current_level = self.__catalog.get_level(level_key)

        if self.current_level.is_movie:
            return

        if program_key is not None:
            self.program = self.current_level.get_program(program_key)

        return self._build_new_engine(list_input)

    def restart(self, list_input=None):
        assert self.current_level, "Cannot restart, no previous level set!"

        if self.current_level.is_movie:
            return

        return self._build_new_engine(list_input)

    def _build_new_engine(self, list_input=None):
        if self.ledger:
            # Remember the previous one
            self.ledgers.append(self.ledger)

        self.ledger = Ledger(self.current_level, self.program, list_input)
        self.engine = Engine(self.current_level, self.program, self.ledger)

        return self.engine

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

    def run_discrete_input(self):
        discrete_list = self.current_level.get_discrete_input()

        if not discrete_list:
            return

        all_passed = True
        passed = 0
        failed = 0
        total_runs = 0
        best_speed = None
        worst_speed = None
        total_speed = 0

        for discrete_input in discrete_list:
            self.restart(discrete_input)
            ledger = self.run()
            res = ledger.get_result()
            total_runs += 1

            if res.passed:
                if best_speed is None or res.speed < best_speed:
                    best_speed = res.speed

                if worst_speed is None or res.speed > worst_speed:
                    worst_speed = res.speed

                total_speed += res.speed

                passed += 1
            else:
                all_passed = False
                failed += 1

        avg_speed = int(total_speed/total_runs)
        return AvgResult(all_passed, best_speed, worst_speed, avg_speed, passed, failed)

    @staticmethod
    def play_movie(level):
        print("Level Movie: '{} - {}'".format(level.key, level.name))

    def get_ledger(self):
        return self.engine.get_ledger()

    def get_goal(self):
        return self.current_level.goal

    def get_outbox(self):
        return self.engine.output

    # sugar so you don't have to worry so much about strings
    def get_level(self, level_key=None):
        if level_key is None:
            return self.current_level
        else:
            return self.levels[str(level_key)]



