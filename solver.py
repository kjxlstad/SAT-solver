import argparse
from sys import stdin

from typing import List, Set

from functools import reduce
from random import choice

Clause = List[int]
Formulae = Set[Clause]
Assignments = List[int]


def user_input() -> str:
    content = ""
    while (line := stdin.readline()) != "\n":
        content += line

    return content


def file_input(path: str) -> str:
    with open(path, "r") as f:
        content = f.read()

    return content


def parse_formulae(text: str) -> Formulae:
    return [set(map(int, line.split(" "))) for line in text.split("\n")[:-1]]


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str)
    return parser.parse_args()


def boolean_constraint_propogation(formulae: Formulae, literal: int):
    # Remove any clause containing the literal
    formulae = list(filter(lambda clause: literal not in clause, formulae))


    # Remove any instances of -literal
    formulae = [clause - {-literal} if -literal in clause else clause for clause in formulae]

    if not all(formulae):
        return None

    # Filter out any empty sets
    return list(filter(lambda clause: clause != set(), formulae))


def pure_literal_elimination(formulae: Formulae):
    literals = unique_literals(formulae)
    pure_literals = list(filter(lambda l: -l not in literals, literals))

    for pure_literal in pure_literals:
        formulae = boolean_constraint_propogation(formulae, pure_literal)

    return formulae, pure_literals


def unit_propogation(formulae: Formulae) -> Assignments:
    assignments = []
    
    while (unit_clauses := list(filter(lambda c: len(c) == 1, formulae))):
        unit, *_ = unit_clauses[0]
        formulae = boolean_constraint_propogation(formulae, unit)
        assignments.append(unit)

        if not formulae or formulae is None:
            break
            
    return formulae, assignments

def unique_literals(formulae: Formulae) -> List[int]:
    if len(formulae) == 0:
        return formulae
    elif len(formulae) == 1:
        return formulae[0]

    return reduce(lambda x, y: x | y, formulae)


def dpll(formulae: Formulae, assignments: Assignments) -> bool:
    formulae, pure_assignments = pure_literal_elimination(formulae)
    formulae, unit_assignments = unit_propogation(formulae)
    assignments += pure_assignments + unit_assignments

    

    if formulae is None:
        return []

    if not formulae:
        return assignments


    cut = choice(list(unique_literals(formulae)))
    assignments.append(cut)

    return dpll(boolean_constraint_propogation(formulae, cut), assignments) or dpll(
        boolean_constraint_propogation(formulae, -cut), assignments
    )


if __name__ == "__main__":
    args = parse_arguments()

    text = user_input() if args.file is None else file_input(args.file)
    formulae = parse_formulae(text)
    
    solution = dpll(formulae, [])
    print(solution)