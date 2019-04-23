
from random import shuffle, choice, randint

ALPHABET = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
POSITIVE = range(1, 10)
NEGATIVE = range(-9, 0)
ZERO = [0]

THINGS = dict(P=POSITIVE, N=NEGATIVE, Z=[0], A=ALPHABET)


class Input(object):

    def __init__(self, alphabet='', count=0, sample=[]):
        self.alphabet = alphabet
        self.count = count
        self.sample = sample

        self.prev_samples = []

    # Todo: really build new sample
    def build_new_sample(self):
        self.prev_samples.append(self.sample)
        new_sample = []

        if self.alphabet == 'none':
            self.sample = new_sample
            return self.sample

        alphas = self.alphabet.split(' ')
        count = self.count

        mix = []
        for a in alphas:
            if len(a) > 1:
                (item, rep) = list(a)
                new_sample.extend(list(item * rep))
                count -= rep
            else:
                mix += THINGS[a]

        while count > 0:
            new_sample.append(choice(mix))
            count -= 1

        shuffle(new_sample)
        self.sample = new_sample

        return self.sample

    def __repr__(self):
        return str(dict(alphabet=self.alphabet, count=self.count, sample=self.sample))


def get_alike(val):
    pass

def get_rand_integer():
    return choice(POSITIVE + NEGATIVE)

def get_rand_positive():
    return choice(POSITIVE)

def get_rand_letter():
    return choice(ALPHABET)

def get_rand_letter_num():
    return choice(POSITIVE + ALPHABET + [0])



