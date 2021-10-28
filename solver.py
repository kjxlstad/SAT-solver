import argparse
from sys import stdin
from typing import List, Set, Tuple
from functools import reduce
from random import choice

Formulae = List[Set[int]]


# TODO: typing
# TODO: more commenting
# TODO: create pdf
# TODO: assignments can be set instead of list


"""
SAT solver
"""


def bc_propogation(formulae: Formulae, literal: int) -> Formulae:
    # Remove any clause containing the literal
    formulae = list(filter(lambda clause: literal not in clause, formulae))

    # Remove any instances of -literal
    formulae = [
        clause - {-literal} if -literal in clause else clause for clause in formulae
    ]

    if not all(formulae):
        return None

    # Filter out any empty sets
    return list(filter(lambda clause: clause != set(), formulae))


def pure_literal_elimination(formulae: Formulae) -> Tuple[Formulae, Set[int]]:
    literals = unique_literals(formulae)
    pure_literals = set(filter(lambda l: -l not in literals, literals))

    for pure_literal in pure_literals:
        formulae = bc_propogation(formulae, pure_literal)

    return formulae, pure_literals


def unit_propogation(formulae: Formulae) -> Tuple[Formulae, Set[int]]:
    assignments = []

    while (unit_clauses := list(filter(lambda c: len(c) == 1, formulae))) :
        unit, *_ = unit_clauses[0]
        formulae = bc_propogation(formulae, unit)
        assignments.append(unit)

        if formulae is None:
            return None, set()

        if not formulae:
            break

    return formulae, set(assignments)


def unique_literals(formulae: Formulae) -> Set[int]:
    if len(formulae) == 0:
        return formulae
    elif len(formulae) == 1:
        return formulae[0]

    return reduce(lambda x, y: x | y, formulae)


def dpll(formulae: Formulae, assignments: Set[int] = set()) -> Set[int]:
    formulae, pure_assignments = pure_literal_elimination(formulae)
    formulae, unit_assignments = unit_propogation(formulae)
    assignments |= pure_assignments | unit_assignments

    if formulae is None:
        return set()

    if not formulae:
        return assignments

    cut = choice(list(unique_literals(formulae)))

    return (
        dpll(bc_propogation(formulae, cut), assignments | {cut}) or 
        dpll(bc_propogation(formulae, -cut), assignments | {-cut})
    )


"""
Input parsing
"""


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file", type=str, help="Path to file containing clauses."
    )
    return parser.parse_args()


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


if __name__ == "__main__":
    args = parse_arguments()

    text = user_input() if args.file is None else file_input(args.file)
    formulae = parse_formulae(text)

    solution = dpll(formulae)

    if len(solution) == 0:
        print("Unsatisfiable")
    else:
        print(f"Satisfiable {solution}")
