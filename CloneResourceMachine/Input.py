
from random import shuffle, choice
import string
from JAGpy.Numbers import intify

ALPHABET = list(string.ascii_uppercase)
POSITIVE = list(range(1, 10))
NEGATIVE = list(range(-9, 0))

THINGS = dict(P=POSITIVE, N=NEGATIVE, Z=[0], A=ALPHABET)


class Input(object):

    def __init__(self, alphabet='', count=0, sample=None):
        self.alphabet = alphabet
        self.count = count
        self.sample = sample or []

        self.prev_samples = []

    def build_new_sample(self):
        if self.sample:
            self.prev_samples.append(self.sample)
        new_sample = []

        if self.alphabet == 'none':
            self.sample = []
            return self.sample

        alphas = self.alphabet.split(' ')
        count = self.count

        mix = []
        for a in alphas:
            if len(a) > 1:
                (item, rep) = list(a)
                rep = int(rep)
                for i in range(0, rep):
                    new_sample.extend(THINGS[item])
                count -= rep
            else:
                mix += THINGS[a]

        while count > 0:
            new_sample.append(str(choice(mix)))
            count -= 1

        shuffle(new_sample)
        self.sample = [intify(x) for x in new_sample]

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



