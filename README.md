# DPLL Boolean Satisfiability Solver

SAT-solver implemented in Python 3.10 using the DPLL algorithm with most frequent literal branching heuristic.

## Usage
Input is taken as raw input by running the script and entering directly into the terminal, terminating the input with a blank line, or alternatively file by passing the `-f` flag followed by filename
```sh
python solver.py -f problem.in
```

### Input and Output
Input is taken in clausal form and is interpreted in the following manner. Each line in the input represents a clause, and each clause is built form space-delimited integers. The integers $1, \, 2, \, 3, \ldots \, n$ represents the propositional variables $p_1, \, p_2, \, p_3, \, \ldots \, p_n$, and the negative integers $-1, \, -2, \, -3, \, \ldots \, -n$ represents the negated propositional variables $\neg p_1, \, \neg p_2, \, \neg p_3 \, \ldots \, \neg p_n$

For example, the set of clauses:
$$\left\{\left\{p_1\right\}, \, \left\{\neg p_1, \, p_3\right\}, \, \left\{\neg p_1, \, p_2, \, \neg p_3\right\}\right\}$$ 
is given as input to the program as:
```
1
-1 3
-1 2 -3
```


Given legal input the program will return either `Unsatisfiable` or `Satisfiable` and yield the assignments that makes a satisfying interpretation. With the above input it will yield:
```
Satisfiable with: {1: True, 2: True, 3: True}
```