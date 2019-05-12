
import unittest
from CloneResourceMachine.Expected import FORMULAS
from collections import namedtuple


class Test_Expected(unittest.TestCase):

    def test_functions(self):
        Test = namedtuple('test', "input expected")

        tests = {
            '() => “BUG”': Test(list('GOUNDERBED'), ['B','U','G']), # "GO UNDER BED" :)
            'for ($a, $b) => ($b - $a, $a - $b)': Test([1,2 ,3,0, 2,8], [1,-1, -3,3, 6,-6]),
            'for ($a, $b) => ($b, $a)': Test(list('ABCDEF'), list('BADCFE')),
            'for ($a, $b) => $(a|b) if $a == $b': Test(list('AABC0E'), ['A']),
            'for ($a, $b) => $a * $b': Test([1,4, 0,-3, 2,0, -1,6], [4, 0, 0, -6]),
            'for ($a, $b) => max($a, $b)': Test([1,4, 0,-3, 2,0, -1,6], [4, 0, 2, 6]),
            'for ($a, $b) => same_sign($a, $b) then 0 else 1': Test([1,4, 3,-3, -1,6], [0, 1, 1]),
            'for ($a) => $a * 3': Test([1, -2, 3, 0], [3, -6, 9, 0]),
            'for ($a) => $a * 8': Test([1, -2, 3, 0], [8, -16, 24, 0]),
            'for ($a) => $a * 40': Test([1, -2, 3, 0], [40, -80, 120, 0]),
            'for ($a) => if 0': Test([1, -2, 3, 0], [0]),
            'for ($a) => if not 0': Test([1, -2, 3, 0], [1, -2, 3]),
            'for $a => $a': Test([1, -2, 'E', 0], [1, -2, 'E', 0]),
            'for $a => abs($a)': Test([1, -2, 3, -4], [1, 2, 3, 4]),
            'for $a => each ($a to 0)': Test([1, -2, 0, 4], [1,0, -2,-1,0, 0, 4,3,2,1,0]),
            'for $a => sum(each $a until 0)': Test([1,4,0, -3,-2,0, -1,6,3,0, 0], [5, -5, 8, 0]),
        }

        for formula, test in tests.items():
            fn = FORMULAS[formula]
            actual = fn(test.input)

            print("{}: {} => {}".format(formula, test.input, actual))
            self.assertEqual(actual, test.expected)
