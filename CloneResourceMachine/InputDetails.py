
from random import shuffle, choice
import string
from JAGpy.Numbers import intify
from JAGpy.Structs import lookup

ALPHABET = list(string.ascii_uppercase)
POSITIVE = list(range(1, 10))
NEGATIVE = list(range(-9, 0))
MANY = list(range(1,21))

THINGS = dict(P=POSITIVE, N=NEGATIVE, Z=[0], A=ALPHABET, M=MANY)


class InputDetails(object):

    def __init__(self, data):
        self.alphabet = lookup(data, 'alphabet', '')
        self.count = lookup(data, 'count', 0)
        self.sample = lookup(data, 'sample', [])
        self.discrete = []

        self.process_discrete(lookup(data, 'discrete'))

    def get_new_sample(self):
        new_sample = []

        if self.alphabet == 'none':
            self.sample = []
            return self.sample

        alphas = self.alphabet.split(' ')
        count = self.count

        mix = []
        for a in alphas:
            if len(a) == 2:
                (item, rep) = list(a)
                rep = int(rep)
                for i in range(0, rep):
                    new_sample.extend(THINGS[item])
                count -= rep
            # elif len(a) == 3:
            #     (item, op, num) = list(a)
            #     if item == 'M' and op == '<':
            #         new_sample.extend(range(1,))
            else:
                mix += THINGS[a]

        while count > 0:
            new_sample.append(str(choice(mix)))
            count -= 1

        shuffle(new_sample)
        self.sample = [intify(x) for x in new_sample]

        return self.sample

    def process_discrete(self, discrete):
        if discrete is None:
            return

        self.discrete.extend(discrete)

    def __repr__(self):
        return str(dict(alphabet=self.alphabet, count=self.count, sample=self.sample))


def get_rand_integer():
    return choice(POSITIVE + NEGATIVE)


def get_rand_positive():
    return choice(POSITIVE)


def get_rand_letter():
    return choice(ALPHABET)


def get_rand_letter_num():
    return choice(POSITIVE + ALPHABET + [0])



