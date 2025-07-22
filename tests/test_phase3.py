import re
from phases.phase3.main import Phase3
import pytest
import ast

@pytest.fixture
def phase3():
    return Phase3()

def parse_output(output: str):
    lines = output.strip().split('\n')
    status = lines[0].strip()
    variables = set()
    if len(lines) > 1:
        variables_str = re.findall(r"\{.*\}", lines[1])
        if variables_str:
            variables = set(eval(variables_str[0]))
    return status, variables


@pytest.mark.parametrize("input_data, expected_status, expected_vars", [
    ("(⊤→A)∧(A→B)∧(B→C)∧(A∧C→D)∧(D→E)", "Satisfiable", {'A', 'B', 'C', 'D', 'E'}),

    ("(⊤→A)∧(A→B)∧(B→C)∧(C→⊥)", "Unsatisfiable", set()),

    ("(⊤→X)∧(Y→Z)", "Satisfiable", {'X'}),

    ("(⊤→A)∧(A→B)∧(A→C)∧(B∧C→D)∧(D→E)∧(E∧C→F)", "Satisfiable", {'A', 'B', 'C', 'D', 'E', 'F'}),

    ("(⊤ → A) ∧ (⊤ → B) ∧ (A ∧ B → C) ∧ (C ∧ D → E) ∧ (E → ⊥) ∧ (⊤ → D)", "Unsatisfiable", set()),

    ("(⊤→A)∧(A→B)∧(X→Y)", "Satisfiable", {'A', 'B'}),

    ("(⊤→A)∧(A→B)∧(B→⊥)∧(⊤→X)", "Unsatisfiable", set()),

    ("(⊤∧⊤→X)∧(X→Y)", "Satisfiable", {'X', 'Y'}),

    ("(⊤→A)∧(A→B)∧(Z→⊤)", "Satisfiable", {'A', 'B'}),

    ("", "Satisfiable", set()),

    ("(⊤→A)∧(A→B)∧(B→C)∧(C→D)∧(D→E)∧(E→F)∧(F→G)∧(G→H)∧(H→I)∧(I→J)",
     "Satisfiable", {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'}),

    ("(⊤→A)∧(⊤→B)∧(⊤→C)∧(A∧B∧C→D)∧(D∧A→E)∧(E∧B→F)∧(F∧C→G)∧(G∧D→H)",
     "Satisfiable", {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'}),

    ("(⊤→A)∧(A→B)∧(A→C)∧(B→D)∧(C→D)∧(D→E)∧(B∧C→F)∧(E∧F→G)",
     "Satisfiable", {'A', 'B', 'C', 'D', 'E', 'F', 'G'}),

    ("(⊤→A)∧(A→B)∧(B→C)∧(C→D)∧(D→E)∧(E→F)∧(F→G)∧(G→H)∧(H→⊥)∧(⊤→X)∧(X→Y)",
     "Unsatisfiable", set()),

    ("(⊤→A)∧(A→B)∧(B→C)∧(⊤→X)∧(X→Y)∧(Y→Z)∧(Z→⊥)∧(⊤→P)∧(P→Q)",
     "Unsatisfiable", set()),

    ("(⊤→R)∧(R→A)∧(R→B)∧(R→C)∧(A∧B→X)∧(B∧C→Y)∧(A∧C→Z)∧(X∧Y∧Z→F)",
     "Satisfiable", {'R', 'A', 'B', 'C', 'X', 'Y', 'Z', 'F'}),

    ("(⊤→A)∧(A→B)∧(B→C)∧(A∧C→D)∧(D→E)∧(E∧A→F)∧(F∧B→G)",
     "Satisfiable", {'A', 'B', 'C', 'D', 'E', 'F', 'G'}),

    ("(⊤→A)∧(⊤→B)∧(⊤→C)∧(⊤→D)∧(⊤→E)∧(A∧B∧C∧D∧E→R)∧(R→F)",
     "Satisfiable", {'A', 'B', 'C', 'D', 'E', 'R', 'F'}),

    ("(⊤→A)∧(A→B)∧(A→C)∧(B→D)∧(C→E)∧(D→F)∧(E→G)∧(F→⊥)∧(G→H)",
     "Unsatisfiable", set()),

    ("(⊤→A)∧(⊤→B)∧(⊤→C)∧(A→D)∧(B→E)∧(C→F)∧(D∧E→G)∧(E∧F→H)∧(F∧D→I)∧(G∧H∧I→J)",
     "Satisfiable", {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'}),

    ("(⊤→A)∧(⊤→B)∧(⊤→C)∧(⊤→D)∧(A∧B∧C∧D→E)∧(E→F)∧(F∧A∧B∧C∧D→G)",
     "Satisfiable", {'A', 'B', 'C', 'D', 'E', 'F', 'G'}),

    ("(⊤→A)∧(A→B)∧(B→C)∧(C→D)∧(D→E)∧(E→F)∧(F→G)∧(G→H)∧(H→I)∧(I→J)∧(J∧A→K)∧(K→⊥)",
     "Unsatisfiable", set()),

    ("(⊤→R)∧(R→A)∧(R→B)∧(R→C)∧(R→D)∧(A→E)∧(B→F)∧(C→G)∧(D→H)∧(E∧F∧G∧H→M)",
     "Satisfiable", {'R', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'M'}),

    ("(⊤→A)∧(A→B)∧(A→C)∧(B∧C→D)∧(D→E)∧(E∧B→F)∧(F→G)",
     "Satisfiable", {'A', 'B', 'C', 'D', 'E', 'F', 'G'}),

    ("(⊤→A)∧(A→B)∧(A→C)∧(B∧C→D)∧(D→E)∧(E→F)∧(F∧B→G)∧(G∧C→H)∧(H∧D→I)∧(I∧E→J)∧(J→K)∧(K∧A→L)",
     "Satisfiable", {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L'}),
])
def test_horn_solver_valid(phase3, input_data, expected_status, expected_vars):
    output = phase3.process(input_data)
    status, variables = parse_output(output)
    assert status == expected_status
    if expected_status == "Satisfiable":
        assert variables == expected_vars


def test_horn_solver_invalid(phase3):
    invalid_input = "(⊤→A)∧(A⇒B)"
    output = phase3.process(invalid_input)
    assert "Invalid Horn Formula" in output


@pytest.mark.parametrize("input_data, expected_status", [
    ("(A→⊤)∧(B→⊤)∧(C→⊤)", "Satisfiable"),

    ("(A→⊥)∧(B→⊥)∧(C→⊥)", "Satisfiable"),

    ("(⊤→A)∧(A∧A→B)∧(B→C)", "Satisfiable"),

    ("(⊤→A)∧(A→B)∧(A→C)∧(B→D)∧(C→D)∧(D→E)∧(E→⊥)∧(B→F)∧(F→⊥)", "Unsatisfiable"),

    ("(⊤→A)∧(A→B)∧(A→B)∧(B→C)∧(B→C)∧(C→D)∧(D→E)∧(E→F)", "Satisfiable"),
])
def test_horn_solver_edge_cases(phase3, input_data, expected_status):
    output = phase3.process(input_data)
    status, _ = parse_output(output)
    assert status == expected_status


def test_satisfiable_no_assignment(phase3):
    expr = "(p ∧ q ∧ s → p) ∧ (q ∧ r → p) ∧ (p ∧ s → s)"
    expected_output = "Satisfiable"
    assert phase3.process(expr) == expected_output


def test_satisfiable_with_assignment(phase3):
    expr = "(p ∧ q ∧ s → ⊥) ∧ (q ∧ r → p) ∧ (⊤ → s)"
    expected_output = "Satisfiable\n{'s'}"
    assert phase3.process(expr) == expected_output


def test_unsatisfiable_top_to_bottom(phase3):
    expr = "⊤ → ⊥"
    expected_output = "Unsatisfiable"
    assert phase3.process(expr) == expected_output


def test_invalid_horn_formula_disjunction(phase3):
    expr = "q ∨ r → p"
    expected_output = "Invalid Horn Formula"
    assert phase3.process(expr) == expected_output


def test_unsatisfiable_multiple_clauses(phase3):
    expr = "(p ∧ q ∧ s → ⊥) ∧ (s → p) ∧ (s → q) ∧ (⊤ → s)"
    expected_output = "Unsatisfiable"
    assert phase3.process(expr) == expected_output

def test_satisfiable_with_multiple_assignments_subset_check(phase3):
    expr = "(s → p) ∧ (p ∧ q ∧ s → p) ∧ (⊤ → r) ∧ (s ∧ p → q) ∧ (⊤ → s)"
    output = phase3.process(expr)

    assert output.startswith("Satisfiable")

    lines = output.splitlines()
    if len(lines) == 1:
        result_set = set()
    else:
        try:
            result_set = ast.literal_eval(lines[1])
            assert isinstance(result_set, set)
        except (SyntaxError, ValueError):
            pytest.fail("Output format is not a valid set.")

    full_set = {"p", "q", "r", "s"}

    assert result_set == full_set




def test_invalid_horn_formula_with_negation(phase3):
    expr = "(¬s → p) ∧ (p ∧ q ∧ s → p) ∧ (⊤ → r) ∧ (s ∧ p → q) ∧ (⊤ → s)"
    expected_output = "Invalid Horn Formula"
    assert phase3.process(expr) == expected_output
