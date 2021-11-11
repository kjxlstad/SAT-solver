import argparse
from sys import stdin
from typing import List, Set, Tuple
from functools import reduce


# Shorthand type for formulae
Formulae = List[Set[int]]


"""
SAT solver
"""


def unique_literals(formulae: Formulae) -> List[int]:
    # If formulae contains literals, return unique_literals, else reuturn empty
    return (formulae and list(reduce(lambda a, b: a | b, formulae))) or []


def most_frequent_literal(formulae: Formulae) -> int:
    # Collect the unique literals
    literals = unique_literals(formulae)

    # Count occurences of each unique literal
    count = [
        sum([literal in clause for clause in formulae])
        for literal in literals
    ]

    # Return the first literal with the highest frequency
    return literals[count.index(max(count))]


def bc_propogation(formulae: Formulae, literal: int) -> Formulae:
    # Remove clauses containing the given literal
    # Remove instances of the negated literal in the remaining clauses
    formulae = [
        clause - {-literal} for clause in formulae if literal not in clause
    ]

    # If the above yields an empty clause, it is unsatisfiable
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
    literals = unique_literals(formulae)

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
    cut = most_frequent_literal(formulae)

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
    # Splits text on newline into list of clauses
    # Splits lines on space into set of literals
    return [set(map(int, line.split(" "))) for line in text.split("\n")[:-1]]


if __name__ == "__main__":
    args = parse_arguments()

    text_input = user_input() if args.file is None else file_input(args.file)
    formulae = parse_formulae(text_input)

    solution = dpll(formulae)

    # Pretty print satisfiability and satisfying interpretation
    interpretation = dict(sorted({abs(i) : i > 0 for i in solution}.items()))
    print((solution and f"Satisfiable with: {interpretation}") or "Unsatisfiable")