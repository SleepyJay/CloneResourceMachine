
import yaml
from Level import Level
from JAGpy.Structs import lookup


class Catalog (object):
    
    def __init__(self):
        self.levels = dict()
    
    def load_file(self, filename):
        f = open(filename, 'r')
        data = yaml.safe_load(f)

        for key, values in data['levels'].items():
            is_movie = lookup(values, 'movie')

            if is_movie:
                # Todo: something fancy with movies?
                continue

            self.load_data(key, values)

    def load_data(self, key, data):
        self.levels[key] = Level(key, data)

    def get_level(self, level_key):
        return self.levels[level_key]
