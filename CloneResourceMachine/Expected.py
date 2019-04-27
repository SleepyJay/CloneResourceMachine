
from functools import partial
from JAGpy.Numbers import has_sign, is_int
from JAGpy.Structs import lookup


class Expected(object):

    def __init__(self, program, goal):
        self.program = program
        self.goal = goal

        self.size = 0
        self.speed = 0
        self.output = []

        if program.size is None:
            self.size = self.goal.size
        else:
            self.size = program.size

        if program.speed is None:
            self.speed = self.goal.speed
        else:
            self.speed = program.speed

    def predict_output(self, formula, input):
        fn = FORMULAS[formula]
        return fn(input)


def fn_identity(items):
    return items


def fn_just_respond(response, items):
    return response


def fn_subtact_both(items):
    result = []
    for a, b in zip(items[0::2], items[1::2]):
        result.extend([b - a, a - b])

    return result


def fn_None():
    return None


def fn_reverse_two(items):
    result = []
    for a, b in zip(items[0::2], items[1::2]):
        result.extend([b, a])

    return result


def fn_equal_pairs(items):
    result = []
    for a, b in zip(items[0::2], items[1::2]):
        if a == b:
            result.append(a)

    return result


def fn_max_of_pairs(items):
    result = []
    for a, b in zip(items[0::2], items[1::2]):
        if a > b:
            result.append(a)
        else:
            result.append(b)

    return result


def fn_multiply_pairs(items):
    result = []
    for a, b in zip(items[0::2], items[1::2]):
        result.append(a * b)

    return result


def fn_sign_of_pairs(items):
    result = []
    for a, b in zip(items[0::2], items[1::2]):
        sign_a = has_sign(a)
        sign_b = has_sign(b)

        if sign_a == sign_b:
            result.append(0)
        else:
            result.append(1)

    return result


def fn_multiply_by(by, items):
    result = []
    for a in items:
        result.append(a * by)

    return result


def fn_keep_when_zero(items):
    result = []
    for a in items:
        if a == 0:
            result.append(a)
    return result


def fn_keep_when_not_zero(items):
    result = []
    for a in items:
        if a != 0:
            result.append(a)

    return result


def fn_abs(items):
    result = []
    for a in items:
        result.append(abs(a))

    return result


def fn_count_to_zero(items):
    result = []
    for a in items:
        if a == 0:
            result.append(0)
        elif a > 0:
            vals = list(range(0, a + 1))
            vals.reverse()
            result.extend(vals)
        else:
            vals = list(range(a, 1))
            result.extend(vals)
    return result


def fn_sum_until_zero(items):
    result = []
    cur_sum = 0
    for a in items:
        cur_sum += a
        if a == 0:
            result.append(cur_sum)
            cur_sum = 0

    return result


FORMULAS = {
    '() => “BUG”': partial(fn_just_respond, ['B','U','G']),
    'for ($a, $b) => ($b - $a, $a - $b)': fn_subtact_both,
    'for ($a, $b) => ($b, $a)': fn_reverse_two,
    'for ($a, $b) => $(a|b) if $a == $b': fn_equal_pairs,
    'for ($a, $b) => $a * $b': fn_multiply_pairs,
    'for ($a, $b) => max($a, $b)': fn_max_of_pairs,
    'for ($a, $b) => same_sign($a, $b) then 0 else 1': fn_sign_of_pairs,
    'for ($a) => $a * 3': partial(fn_multiply_by, 3),
    'for ($a) => $a * 8': partial(fn_multiply_by, 8),
    'for ($a) => $a * 40': partial(fn_multiply_by, 40),
    'for ($a) => if 0': fn_keep_when_zero,
    'for ($a) => if not 0': fn_keep_when_not_zero,
    'for $a => $a': fn_identity,
    'for $a => abs($a)': fn_abs,
    'for $a => each ($a to 0)': fn_count_to_zero,
    'for $a => sum(each $a until 0)': fn_sum_until_zero,
}
