# Propositional Logic Solver

A command-line Python program for working with propositional logic. It is organised into five
phases that build on each other:

1. **Formula validation & parse trees:** check whether a formula is well-formed and print its parse tree.
2. **CNF conversion:** rewrite a formula in Conjunctive Normal Form.
3. **Horn-SAT solving:** decide whether a Horn formula is satisfiable and find a satisfying assignment.
4. **Natural deduction rule application:** apply one inference rule to given formulas.
5. **Natural deduction proof checking:** verify a complete proof, including nested sub-proofs (boxes).

Each phase reads a plain-text input file and writes its result to an output file next to it.

## Why this project exists

The project implements the standard procedures of propositional logic (parsing, normal forms,
Horn satisfiability and natural deduction) as working code with a test suite. Formulas use the usual
logical symbols (`¬ ∧ ∨ → ↔ ⊥ ⊤`) directly, and proofs use the common rule names (`∧i`, `→e`, `MT`,
`PBC`, …), so input files look like what you would write on paper.

## Features

- Well-formed formula validation using a finite-state checker with parenthesis matching
- Parse tree construction with operator precedence, printed as an indented tree
- CNF conversion: implication/biconditional elimination, De Morgan's laws, double-negation
  elimination and distribution of ∨ over ∧
- Horn-SAT solver based on forward chaining (marking algorithm)
- 8 natural deduction rules that can be applied on their own (Phase 4)
- A proof checker supporting 19 rules and markers, including box rules (`→i`, `¬i`, `PBC`, `∨e`)
  and scope checking (Phase 5)
- Interactive menu plus a standalone entry point for each phase
- A pytest test suite for every phase

## Tech Stack

| Area            | Used                                                                                  |
|-----------------|---------------------------------------------------------------------------------------|
| Language        | Python 3 (3.9 or newer)                                                               |
| Libraries       | Standard library only (`abc`, `dataclasses`, `enum`, `typing`, `copy`, `pathlib`)     |
| Testing         | [pytest](https://docs.pytest.org/)                                                    |

There is no database, web framework, external API or configuration service.

## Project Structure

```
Logic-project/
├── main.py              # Interactive menu: runs a phase on its sample file in data/
├── phases/
│   ├── base_phase.py    # BasePhase: read input file -> process() -> write output file
│   ├── phase1/          # WFF validation, parse tree (also the shared Node class and parser)
│   ├── phase2/          # CNF conversion
│   ├── phase3/          # Horn-SAT solver
│   ├── phase4/          # Applying a single natural deduction rule
│   └── phase5/          # Verifying a complete natural deduction proof
├── data/                # Sample input for each phase and the output it produces
├── tests/               # pytest tests, one file per phase
└── requirements.txt     # pytest and its dependencies
```

Every `phaseN/` package contains:

- `logic.py`: the `PhaseN` class, a subclass of `BasePhase` that implements `process(input_data) -> str`
- `main.py`: a small script to run that phase on any input file

## How It Works

All phases share the same flow, defined in `BasePhase.run()`:

```
input file ──> _read_input() ──> process(text) ──> _write_output() ──> <input name>_output.txt
```

The phases reuse each other's code:

- **Phase 1** defines the `Node` tree structure and the parser used by all later phases.
  Binary operators use both children; `¬` stores its operand in the right child.
- **Phase 2** uses the Phase 1 parser, transforms the tree, and turns it back into a string
  with minimal parentheses. Phase 4 reuses this printer.
- **Phase 3** is self-contained. It splits the formula into clauses and runs forward chaining.
- **Phase 4** defines a `LogicRule` base class with one subclass per rule, and looks rules up by name.
- **Phase 5** reuses the Phase 4 rules and adds the remaining ones (`∨i`, `∨e`, `→i`, `¬i`, `⊥e`, `PBC`, `LEM`, `Copy`).

### Phase 1: Well-formed formulas and parse trees

1. The input is tokenized character by character (spaces are ignored, so propositions are single letters).
2. A state machine (*start, negation, proposition, operator, left/right parenthesis*) checks that each
   token may follow the previous one, while a stack checks that parentheses are balanced.
3. A valid formula is parsed with an operator stack and an operand stack (shunting-yard style) into a tree.
   Precedence from tightest to loosest is `¬`, `∧`, `∨`, `→`, `↔`.
4. The tree is printed in pre-order, indenting each level by two spaces.

### Phase 2: CNF conversion

The parse tree is transformed in three recursive passes:

1. Eliminate `↔` and `→`: `A ↔ B ≡ (¬A ∨ B) ∧ (¬B ∨ A)`, `A → B ≡ ¬A ∨ B`
2. Push negations inward: `¬¬A ≡ A`, `¬(A ∧ B) ≡ ¬A ∨ ¬B`, `¬(A ∨ B) ≡ ¬A ∧ ¬B`
3. Distribute `∨` over `∧`: `A ∨ (B ∧ C) ≡ (A ∨ B) ∧ (A ∨ C)` (and the symmetric cases)

### Phase 3: Horn-SAT

The formula is split into clauses at every top-level `∧`. Each clause must have the form
`antecedents → consequent`, where the antecedents are variables, `⊤` or `⊥` joined by `∧`,
and the consequent is a single variable, `⊤` or `⊥`. Starting with every variable false, the solver
repeatedly marks a consequent as true once all of its antecedents are true. If `⊥` gets marked,
the formula is unsatisfiable. Otherwise, the marked variables (all others false) form a satisfying assignment.

### Phase 4: Applying a rule

Numbered formulas are parsed with the Phase 1 parser. The rule on the last line is looked up in a
dictionary of `LogicRule` subclasses. Each subclass checks its inputs (for example, `→e` needs an
implication and a formula structurally equal to its antecedent) and builds the resulting tree.

### Phase 5: Checking a proof

The proof is parsed into lines (line number, formula, rule, referenced lines, indentation level).
The checker walks through the lines in order:

- `Premise` and `Assumption` lines are accepted as given.
- `BeginScope` / `EndScope` push and pop a scope. A line can be referenced on its own only while its
  scope is open. After the scope closes, it can only be used as part of a box reference such as `3-5`.
- For every other line, the formulas of the referenced lines are passed to the rule, and the result
  must match the formula written on that line.

The first line that fails is reported.

## Notation

| Symbol | Meaning                          |
|--------|----------------------------------|
| `¬`    | not                              |
| `∧`    | and                              |
| `∨`    | or                               |
| `→`    | implies                          |
| `↔`    | if and only if                   |
| `⊥`    | contradiction (false)            |
| `⊤`    | true (used in Phase 3)           |

Propositions are single letters (`p`, `q`, `A`, …). Use parentheses to group sub-formulas.
Operators with the same precedence are grouped from left to right, so `a → b → c` means `(a → b) → c`.

## Installation

Requirements: Python 3.9 or newer.

```bash
git clone https://github.com/rozhina1203/Logic-project.git
cd Logic-project

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

`requirements.txt` only contains pytest and its dependencies. The program itself runs on the
standard library, so this step is only needed to run the tests.

## Configuration

There are no environment variables, API keys or configuration files.

Input files contain Unicode logic symbols, so they must be saved as **UTF-8**. All files are read and
written with UTF-8 encoding.

## Running the Project

Run all commands from the project root.

### Interactive menu

```bash
python main.py
```

```
--- Propositional Logic Solver ---
1. Phase 1: Check WFF & Generate Parse Tree
2. Phase 2: Convert Formula to CNF
3. Phase 3: Horn SAT Solver
4. Phase 4: Apply Natural Deduction Rule
5. Phase 5: Verify Natural Deduction
0. Exit
```

Choosing phase *N* reads `data/phaseN_input.txt` and writes the result to `data/phaseN_input_output.txt`.
To try your own input through the menu, edit the matching file in `data/`.

### Running a single phase on any file

```bash
python -m phases.phase2.main path/to/formula.txt
```

The result is written to `path/to/formula_output.txt`. Use the `-m` form shown above. Running
`python phases/phase2/main.py` directly fails because the `phases` package can't be imported that way.

## Testing

```bash
python -m pytest
```

The tests are in `tests/`, one file per phase. They call each phase's `process()` method directly
with an input string and check the returned output.

## Usage Examples

The examples below come from the sample files in `data/` and from the test suite.

### Phase 1: Validate a formula

Input:
```
¬((a ∨ b) ∧ (c → ¬d))
```
Output:
```
Valid Formula
¬
  ∧
    ∨
      a
      b
    →
      c
      ¬
        d
```
An ill-formed formula such as `(a ∧ ∨ b)` produces `Invalid Formula`.

### Phase 2: Convert to CNF

| Input                  | Output                                    |
|------------------------|-------------------------------------------|
| `p → q`                | `¬p ∨ q`                                  |
| `(A ∧ B) ∨ (C ∧ D)`    | `(A ∨ C) ∧ (A ∨ D) ∧ (B ∨ C) ∧ (B ∨ D)`   |
| `p → ((q → r) → s)`    | `(¬p ∨ q ∨ s) ∧ (¬p ∨ ¬r ∨ s)`            |

### Phase 3: Horn-SAT

Input:
```
(⊤ → A) ∧ (⊤ → B) ∧ (A ∧ B → C) ∧ (C ∧ D → E) ∧ (⊤ → D)
```
Output:
```
Satisfiable
{'A', 'B', 'C', 'D', 'E'}
```
`(⊤ → A) ∧ (A → B) ∧ (B → C) ∧ (C → ⊥)` produces `Unsatisfiable`, and a clause that is not a Horn
clause (e.g. `q ∨ r → p`) produces `Invalid Horn Formula`.

### Phase 4: Apply a rule

Each formula line is a line number, four spaces, and a formula. The last line names the rule and the
lines it uses.

Input:
```
1    A → B
2    A
→e, 1, 2
```
Output:
```
B
```
If the rule does not fit the formulas, the output is `Rule Cannot Be Applied`. The sample file
`data/phase4_input.txt` shows this case.

Supported rules: `∧i`, `∧e1`, `∧e2`, `→e`, `¬e`, `¬¬e`, `¬¬i`, `MT`.

### Phase 5: Check a proof

Each line has a line number, the formula and the rule, separated by at least four spaces.
Boxes are wrapped in `BeginScope` / `EndScope`, and each level is indented by two more spaces.

Input:
```
1    p → q        Premise
2    p → ¬q        Premise
      BeginScope
 3      p        Assumption
 4      q        →e, 1, 3
 5      ¬q        →e, 2, 3
 6      ⊥        ¬e, 4, 5
      EndScope
 7    ¬p        ¬i, 3-6
```
Output:
```
Valid Deduction
```

The sample file `data/phase5_input.txt` produces `Invalid Deduction at Line 5`, because line 5 uses
line 4 from a scope that has already been closed.

Rule reference formats:

| Rule(s)                                                   | References                     |
|-----------------------------------------------------------|--------------------------------|
| `Premise`, `Assumption`, `LEM`                            | none                           |
| `∧e1`, `∧e2`, `¬¬e`, `¬¬i`, `Copy`, `∨i1`, `∨i2`, `⊥e`    | one line: `∧e1, 3`             |
| `∧i`, `→e`, `¬e`, `MT`                                    | two lines: `∧i, 1, 2`          |
| `→i`, `¬i`, `PBC`                                         | one box: `→i, 3-5`             |
| `∨e`                                                      | a line and two boxes: `∨e, 1, 2-4, 5-7` |

For `MT`, the implication is referenced first and the negated consequent second.

## Known Limitations

- Propositions are single letters. Multi-character names like `p1` are not supported.
- Phase 1 does not accept `⊥` as a proposition, although the parser used by Phases 2, 4 and 5 does.
- Phases 2, 4 and 5 assume their formulas are well-formed and do not run the Phase 1 validator first.
- CNF conversion uses plain distribution, so the output can grow exponentially, and duplicate or
  tautological clauses are not simplified away.
- In Phase 5, the rules added in that phase compare formulas with `∧` and `∨` treated as commutative,
  while the rules reused from Phase 4 compare them exactly as written.
- The interactive menu always uses the sample files in `data/`. Use `python -m phases.phaseN.main <file>`
  for other inputs.

## Contributors

- [@rozhina1203](https://github.com/rozhina1203)
- [@Erfan4708](https://github.com/Erfan4708)
