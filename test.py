from sys import stdin
from typing import Set, List

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
    

def unit_propogation():
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

def prove():
    ...
