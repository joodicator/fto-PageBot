import dice
from fractions import Fraction
from itertools import *

def enum_defn(chan, name):
    scope = dice.global_defs[chan.lower()]
    return enum_parts(scope[name].body_ast.parts, scope, name, Fraction(1))

def enum_parts(parts, scope, name, prob):
    if parts:
        for head, head_prob in enum_part(parts[0], scope, name, prob):
            for tail, tail_prob in enum_parts(parts[1:], scope, name, head_prob):
                yield head + tail, tail_prob
    else:
        yield (), prob

def enum_part(part, scope, name, prob):
    if type(part) in (dice.Text, dice.Escape):
        return ((((part.text, name),), prob),)
    elif type(part) is dice.Expr:
        return ((((str(part.source), name),), prob),)
    elif type(part) is dice.NameApp:
        assert not part.suffixes, part
        assert not part.name.namespace, part
        return enum_parts(scope[part.name.name].body_ast.parts,
                          scope, part.name.name, prob)
    elif type(part) is dice.Branch:
        weight_sum = sum(Fraction(c.weight) for c in part.choices)
        if weight_sum == 0: weight_sum = Fraction(1)
        return chain(*(enum_parts(c.string.parts, scope, name,
            prob*Fraction(c.weight)/weight_sum) for c in part.choices))
    else:
        assert False, part
