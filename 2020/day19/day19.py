import itertools
import functools


def expand(ruleset, v):
    if '"' in v:
        return [[v.strip('"')]]
    else:
        if '|' in v:
            interim = [expand(ruleset, x.strip()) for x in v.split('|')]
            return [[''.join(list(x)) for x in itertools.product(*y)] for y in interim]
        else:
            interim = [[expand(ruleset, ruleset[int(x)]) for x in v.split()]]
            interim = [[list(itertools.chain(*z)) for z in y] for y in interim]
            return [[''.join(list(x)) for x in itertools.product(*y)] for y in interim]


def expand_wrapper(ruleset, v):
    return functools.reduce(lambda x, y: x+y, expand(ruleset, v), [])


with open("input.txt") as ifp:
    messages = list()
    rules = dict()
    for line in [x.strip() for x in ifp.readlines()]:
        if len(line):
            s = line.split(':')
            if len(s) > 1:
                rules[int(s[0])] = s[1].strip()
            else:
                messages.append(s[0])


    ## Part A
    valid_a_messages = set(messages).intersection(set(expand_wrapper(rules, rules[0])))
    print("result_a:{}".format(len(valid_a_messages)))


    ## Part B
    ## 0: 8 11
    ## 8: 42 -> 42 | 42 8
    ## 11: 42 31 -> 42 31 | 42 11 31

    ## 42 .. 42 .. .. 31
    ## n(42) > 0
    ## n(31) > 0
    ## n(42) > n(31)
    ## begins with 31
    ## ends with 31

    rules_42 = set(expand_wrapper(rules, rules[42]))
    rules_42_length = set([len(x) for x in rules_42])

    rules_31 = set(expand_wrapper(rules, rules[31]))
    rules_31_length = set([len(x) for x in rules_31])

    m_chunksize = 0
    if len(rules_31_length) == 1 and len(rules_42_length) == 1:
        m_chunksize = list(rules_42_length)[0]

    valid_a_messages = set()
    for m in messages:

        m_words = [m[x:x+m_chunksize] for x in range(0, len(m), m_chunksize)]

        count42 = 0
        count31 = 0

        for w in reversed(range(len(m_words))):
            if m_words[w] in rules_31:
                count31 += 1
            else:
                break

        for w in range(len(m_words)-count31):
            if m_words[w] in rules_42:
                count42 += 1
            else:
                break
        
        if len(m_words) == count31 + count42 and count42 > count31 and count31 > 0:
            valid_a_messages.add(m)
    
    print("result_b:{}".format(len(valid_a_messages)))
