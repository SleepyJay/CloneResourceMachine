
import yaml
from CloneResourceMachine.Level import Level


class Catalog (object):
    
    def __init__(self):
        self.levels = dict()
    
    def load_file(self, filename):
        data = self.read_yaml(filename)
        self.load_data(data['levels'])

    def load_data(self, data):
        for key, values in data.items():
            self.levels[str(key)] = Level(str(key), values)

    def get_level(self, level_key):
        return self.levels[str(level_key)]

    @staticmethod
    def read_yaml(filename):
        f = open(filename, 'r')
        data = yaml.safe_load(f)
        f.close()
        return data
