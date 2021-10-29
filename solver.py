import argparse
from sys import stdin
from typing import List, Set, Tuple
from functools import reduce
from random import choice


# TODO: implement most common cutting
# TODO: write readme-like pdf
# TODO: "Where the literals 1, 2, 3 ... n represents the propositional variables p_1, p_2, p_3 ... p_n"


# Shorthand type for formulae
Formulae = List[Set[int]]


"""
SAT solver
"""


def bc_propogation(formulae: Formulae, literal: int) -> Formulae:
    # Remove any clause containing the given literal
    formulae = filter(lambda clause: literal not in clause, formulae)

    # Remove any instances of the negated literal
    formulae = [clause - {-literal} for clause in formulae]

    # If the above yields an empty clause, we know the formulae to be unsatisfiable
    if not all(formulae):
        return None

    return formulae


def unit_propogation(formulae: Formulae) -> Tuple[Formulae, Set[int]]:
    assignments = set()

    # Find all unit clauses
    while (unit_clauses := list(filter(lambda c: len(c) == 1, formulae))):
        # Extract the literal from the first unit clause
        unit, *_ = unit_clauses[0]

        formulae = bc_propogation(formulae, unit)
        assignments |= {unit}

        # If formulae is None, it is unsatisfiable
        if formulae is None:
            return None, set()

    return formulae, assignments


def pure_literal_elimination(formulae: Formulae) -> Tuple[Formulae, Set[int]]:
    # Fetch all literals in formulae
    literals = reduce(lambda x, y: x | y, formulae)

    # Filter out the literals without a complement
    pure_literals = set(filter(lambda l: -l not in literals, literals))

    for pure_literal in pure_literals:
        formulae = bc_propogation(formulae, pure_literal)

    return formulae, pure_literals


def dpll(formulae: Formulae, assignments: Set[int] = set()) -> Set[int]:
    formulae, pure_assignments = pure_literal_elimination(formulae)
    formulae, unit_assignments = unit_propogation(formulae)
    assignments |= pure_assignments | unit_assignments

    # If formulae has been set to None, it is unsatisfiable.
    if formulae is None:
        return set()

    # If the formulae is empty, it is satisfied, return interpretation.
    if not formulae:
        return assignments

    # Pick variable for cutting and branch
    cut = choice(list(reduce(lambda x, y: x | y, formulae)))

    return (
        dpll(bc_propogation(formulae, cut), assignments | {cut}) or 
        dpll(bc_propogation(formulae, -cut), assignments | {-cut})
    )


"""
Input parsing and entry point
"""


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str)
    parser.add_argument("-v", "--verbose", action="store_true")
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

    text_input = user_input() if args.file is None else file_input(args.file)
    formulae = parse_formulae(text_input)

    solution = dpll(formulae)

    interpretation = ", ".join(sorted([f"{abs(i)} := {i > 0}" for i in solution]))
    print((solution and f"Satisfiable with: {interpretation}") or "Unsatisfiable")