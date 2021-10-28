from sys import stdin
from typing import Set, List

from functools import reduce

Clauses = List[Set[int]]

clauses = [
    {1, 2, 3},
    {1, 2, -3},
    {1, -2, 3},
    {1, -2, -3},
    {-1, 2, 3},
    {-1, 2, -3},
    {-1, -2, 3},
    {-1, -2, -3},
]


#print(clauses)


def resolve(clauses: Clauses):
    a = []


    for clause in clauses:
        if len(clause) == 0:
            return false
    

def pure_literal_elimination(clauses):
    f = reduce(lambda x, y: x | y, clauses)
    pure_literals = *filter(lambda l: -l not in f, f),
    
    return [i > 0 for i in pure_literals]



def unit_propogation():
    ...

def cut():
    ...

def complement(clause_1, clause_2):
    p, q = set(), set()

    for i in clause_1:
        if -i in clause_2:
            p |= {i}
            q |= {-i}
    
    return clause_1 - p | clause_2 - q 

#resolve(clauses)

t = {1, 2, 3}
r = {1, 2, 3}

print(complement(t, r))

