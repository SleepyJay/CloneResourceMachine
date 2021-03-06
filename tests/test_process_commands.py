
import unittest
from CloneResourceMachine.Level import Level, Command
from collections import namedtuple

TestItem = namedtuple("TestItem", ['input', 'expected'])


class Test_Regex(unittest.TestCase):

    def test_Level_RE(self):
        print()

        ln = 1

        tests = [
            TestItem('inbox', Command(ln, 'inbox', None, None, None)),
            TestItem('x: inbox', Command(ln, 'inbox', None, 'x', None)),
            TestItem('jump 0', Command(ln, 'jump', '0', None, None)),
            TestItem('y: jump 0', Command(ln, 'jump', '0', 'y', None)),

            # with comments:
            TestItem('inbox # blah', Command(ln, 'inbox', None, None, '# blah')),
            TestItem('x: inbox # blah', Command(ln, 'inbox', None, 'x', '# blah')),
            TestItem('jump 0 # blah', Command(ln, 'jump', '0', None, '# blah')),
            TestItem('y: jump 0 # blah', Command(ln, 'jump', '0', 'y', '# blah')),
            TestItem('echo this should show up',
                     Command(ln, 'echo', 'this should show up', None, None)),
        ]

        level = Level('test_process_commands', dict())

        for test in tests:
            actual = level.process_str_command(ln, test.input)
            # par = RE_cmd.match(test.input)
            if actual:
                print("'{}' ==> '{}'".format(test.input, actual))
                
                self.assertEqual(actual, test.expected)
            else:
                self.fail("No match for: '{}'".format(test.input))
