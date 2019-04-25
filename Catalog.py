
import yaml
from Level import Level


class Catalog (object):
    
    def __init__(self):
        self.levels = dict()
    
    def load_multi_file(self, filename):
        data = read_yaml(filename)
        self.load_data(data['levels'])

    def load_single_file(self, filename):
        data = read_yaml(filename)
        self.load_data(data)

    def load_data(self, data):
        for key, values in data.items():
            self.levels[key] = Level(key, values)

    def get_level(self, level_key):
        return self.levels[level_key]


def read_yaml(filename):
    f = open(filename, 'r')
    return yaml.safe_load(f)
