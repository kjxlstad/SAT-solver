# DPLL Boolean Satisfiability Solver

SAT-solver implemented in Python 3.10 using the DPLL algorithm with most frequent literal branching heuristic.

## Usage
Input is taken in clausal form and is interpreted in the following manner. Each line in the input represents a clause, and each clause is built form space-delimited integers, where the integers $1, \, 2, \, 3, \ldots \, n$ represents the propositional variables $p_1, \, p_2, \, p_3, \, \ldots \, p_n$, and the negative integers $-1, \, -2, \, -3, \, \ldots \, -n$ represents the negated propositional variables $\neg p_1, \, \neg p_2, \, \neg p_3 \, \ldots \, \neg p_n$
