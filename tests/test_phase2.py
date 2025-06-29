import pytest
from phases.phase2.logic import Phase2


@pytest.fixture
def phase2():
    return Phase2()

def is_cnf(formula: str) -> bool:
    """Helper function to validate CNF structure."""
    if "→" in formula:
        return False  # Implications not allowed in CNF
    if "¬(" in formula:
        return False  # Negations should only apply to literals
    return True


# Implication Elimination Tests
def test_eliminate_implications_basic(phase2):
    assert phase2._eliminate_implications("P→Q") == "(¬P∨Q)"


def test_eliminate_implications_nested(phase2):
    assert phase2._eliminate_implications("(A→B)→C") == "(¬(¬A∨B)∨C)"


# De Morgan's Law Tests
def test_demorgan_simple(phase2):
    assert phase2._move_negations_inwards("¬(A∧B)") == "(¬A∨¬B)"


def test_demorgan_nested(phase2):
    assert phase2._move_negations_inwards("¬(A∨(B∧C))") == "(¬A∧(¬B∨¬C))"


def test_double_negation(phase2):
    assert phase2._move_negations_inwards("¬¬P") == "P"


# Distributive Law Tests
# def test_distribute_simple(phase2):
#     assert phase2._apply_distributive_law("(A∧B)∨C") == "((A∨C)∧(B∨C))"


def test_distribute_multiple(phase2):
    assert phase2._apply_distributive_law("(A∨B)∧(C∨D)") == "(A∨B)∧(C∨D)"  # Already in CNF


# Full CNF Conversion Tests
def test_full_conversion_simple(phase2):
    result = phase2.process("P→Q")
    assert result == "(¬P∨Q)"
    assert is_cnf(result)


def test_full_conversion_complex(phase2):
    input_u = "¬(A ∧ (B → C)) → D"
    result = phase2.process(input_u)
    expected = "((A ∨ D) ∧ (¬B ∨ C ∨ D))"
    assert result == expected
    assert is_cnf(result)


# Edge Cases
def test_tautology(phase2):
    result = phase2.process("A ∨ ¬A")
    assert result == "A ∨ ¬A"
    assert is_cnf(result)


def test_contradiction(phase2):
    result = phase2.process("A ∧ ¬A")
    assert result == "A ∧ ¬A"
    assert is_cnf(result)


def test_already_cnf(phase2):
    result = phase2.process("(A∨B)∧C")
    assert result == "(A∨B)∧C"
    assert is_cnf(result)


# Parametrized Tests
# @pytest.mark.parametrize("input_e,expected", [
#     ("A→B", "(¬A∨B)"),
#     ("¬(A∧B)", "(¬A∨¬B)"),
#     ("(A∧B)∨C", "((A∨C)∧(B∨C))"),
#     ("¬¬P", "P"),
#     ("(P∨Q)∧R", "(P∨Q)∧R"),  # Already in CNF
#     ("¬(P∨Q)", "(¬P∧¬Q)"),
# ])
# def test_parametrized_conversion(phase2, input_e, expected):
#     result = phase2.process(input_e)
#     assert result == expected
#     if "→" not in input_e:  # Skip CNF check for inputs with implications
#         assert is_cnf(result)


# Negative/Validation Tests
def test_invalid_input(phase2):
    with pytest.raises(Exception):
        phase2.process("A ∧→ B")  # Invalid syntax


def test_empty_input(phase2):
    with pytest.raises(Exception):
        phase2.process("")


# Stress Test
def test_complex_nested_expression(phase2):
    input_u = "¬((A → B) ∧ (C ∨ ¬(D ∧ E))) → F"
    result = phase2.process(input_u)
    # Expected result after full conversion:
    expected = "(((¬A ∨ B) ∧ (C ∨ ¬D ∨ ¬E)) ∨ F)"
    assert is_cnf(result)
