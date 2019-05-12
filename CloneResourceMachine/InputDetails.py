
from random import shuffle, choice
from collections import namedtuple
import string
from JAGpy.Numbers import intify
from JAGpy.Structs import lookup

ALPHABET = list(string.ascii_uppercase)
POSITIVE = list(range(1, 10))
NEGATIVE = list(range(-9, 0))

THINGS = dict(P=POSITIVE, N=NEGATIVE, Z=[0], A=ALPHABET)


class InputDetails(object):

    def __init__(self, data):
        self.alphabet = lookup(data, 'alphabet', '')
        self.count = lookup(data, 'count', 0)
        self.sample = lookup(data, 'sample', [])
        self.descrete = []

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

    def process_discrete(self, discrete):
        if discrete is None:
            return

        for dis in discrete:
            dis_list = dis.split(' ')
            self.descrete.append(dis_list)

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



