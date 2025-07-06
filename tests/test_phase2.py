import pytest

from phases.phase1.logic import Phase1
from phases.phase2.logic import Phase2

@pytest.fixture
def phase2():
    return Phase2()

def test_eliminates_implication_correctly(phase2):
    expr = "p → q"
    expected_output = phase2.tree_to_string(Phase1().parse_tree("¬p ∨ q"))
    actual_output = phase2.eliminate_implications(Phase1().parse_tree(expr))
    actual_output_str = phase2.tree_to_string(actual_output)
    assert actual_output_str == expected_output

def test_eliminates_biconditional_correctly(phase2):
    expr = "p ↔ q"
    expected_output = phase2.tree_to_string(Phase1().parse_tree("(¬p ∨ q) ∧ (¬q ∨ p)"))
    actual_output = phase2.eliminate_implications(Phase1().parse_tree(expr))
    actual_output_str = phase2.tree_to_string(actual_output)
    assert actual_output_str == expected_output

def test_handles_nested_implications_and_biconditionals(phase2):
    expr = "(p → q) ↔ (r → s)"
    expected_output = phase2.tree_to_string(Phase1().parse_tree("(¬(¬p ∨ q) ∨ ¬r ∨ s) ∧ (¬(¬r ∨ s) ∨ ¬p ∨ q)"))
    actual_output = phase2.eliminate_implications(Phase1().parse_tree(expr))
    actual_output_str = phase2.tree_to_string(actual_output)
    assert actual_output_str == expected_output

def test_handles_single_variable(phase2):
    expr = "a"
    expected_output = phase2.tree_to_string(Phase1().parse_tree("a"))
    actual_output = phase2.eliminate_implications(Phase1().parse_tree(expr))
    actual_output_str = phase2.tree_to_string(actual_output)
    assert actual_output_str == expected_output

def test_handles_empty_node(phase2):
    assert phase2.eliminate_implications(None) is None

def test_eliminates_double_negation(phase2):
    expr = "¬(¬a)"
    expected_output = "a"
    actual_output = phase2.move_negations_inward(Phase1().parse_tree(expr))
    actual_output_str = phase2.tree_to_string(actual_output)
    assert actual_output_str == expected_output

def test_applies_de_morgan_to_or(phase2):
    expr = "¬(a ∨ b)"
    expected_output = "¬a ∧ ¬b"
    actual_output = phase2.move_negations_inward(Phase1().parse_tree(expr))
    actual_output_str = phase2.tree_to_string(actual_output)
    assert actual_output_str == expected_output

def test_applies_de_morgan_to_and(phase2):
    expr = "¬(a ∧ b)"
    expected_output = "¬a ∨ ¬b"
    actual_output = phase2.move_negations_inward(Phase1().parse_tree(expr))
    actual_output_str = phase2.tree_to_string(actual_output)
    assert actual_output_str == expected_output

def test_handles_single_negation(phase2):
    expr = "¬a"
    expected_output = "¬a"
    actual_output = phase2.move_negations_inward(Phase1().parse_tree(expr))
    actual_output_str = phase2.tree_to_string(actual_output)
    assert actual_output_str == expected_output

def test_handles_empty_node_for_negation(phase2):
    assert phase2.move_negations_inward(None) is None

def test_distributes_or_over_and_with_nested_and_or(phase2):
    expr = "(a ∧ b) ∨ (c ∧ d)"
    expected_output = "(a ∨ c) ∧ (a ∨ d) ∧ (b ∨ c) ∧ (b ∨ d)"
    actual_output = phase2.distribute_or_over_and(Phase1().parse_tree(expr))
    actual_output_str = phase2.tree_to_string(actual_output)
    assert actual_output_str == expected_output

def test_distributes_or_over_and_with_left_and(phase2):
    expr = "(a ∧ b) ∨ c"
    expected_output = "(a ∨ c) ∧ (b ∨ c)"
    actual_output = phase2.distribute_or_over_and(Phase1().parse_tree(expr))
    actual_output_str = phase2.tree_to_string(actual_output)
    assert actual_output_str == expected_output

def test_distributes_or_over_and_with_right_and(phase2):
    expr = "a ∨ (b ∧ c)"
    expected_output = "(a ∨ b) ∧ (a ∨ c)"
    actual_output = phase2.distribute_or_over_and(Phase1().parse_tree(expr))
    actual_output_str = phase2.tree_to_string(actual_output)
    assert actual_output_str == expected_output

def test_handles_single_variable_or(phase2):
    expr = "a ∨ b"
    expected_output = "a ∨ b"
    actual_output = phase2.distribute_or_over_and(Phase1().parse_tree(expr))
    actual_output_str = phase2.tree_to_string(actual_output)
    assert actual_output_str == expected_output

def test_handles_empty_node_for_or_and_distribution(phase2):
    assert phase2.distribute_or_over_and(None) is None


@pytest.mark.parametrize("expr, expected", [
    ("¬(p ∧ q)", "¬p ∨ ¬q"),

    ("p ∨ (q ∧ r)", "(p ∨ q) ∧ (p ∨ r)"),

    ("¬p → q", "p ∨ q"),

    ("((p → q) ∧ (r ∨ s))", "(¬p ∨ q) ∧ (r ∨ s)"),

    ("(p ↔ q)", "(¬p ∨ q) ∧ (¬q ∨ p)"),

    ("(p ∨ q) ∨ (r ∧ s)", "(p ∨ q ∨ r) ∧ (p ∨ q ∨ s)"),

    ("A → B", "¬A ∨ B"),

    ("A ↔ B", "(¬A ∨ B) ∧ (¬B ∨ A)"),

    ("¬(A ∧ B)", "¬A ∨ ¬B"),

    ("¬(A ∨ B)", "¬A ∧ ¬B"),

    ("A → (B → C)", "¬A ∨ ¬B ∨ C"),

    ("(A ∧ B) → C", "¬A ∨ ¬B ∨ C"),

    ("A ∨ (B ∧ C)", "(A ∨ B) ∧ (A ∨ C)"),

    ("(A ∧ B) ∨ (C ∧ D)", "(A ∨ C) ∧ (A ∨ D) ∧ (B ∨ C) ∧ (B ∨ D)"),

    ("¬(¬A)", "A"),

    ("¬(A → (B ∨ C))", "A ∧ ¬B ∧ ¬C"),

    ("A → (B → (C → (D → E)))", "¬A ∨ ¬B ∨ ¬C ∨ ¬D ∨ E"),

    ("¬(¬(A ∧ B) ∨ ¬(C ∧ D))", "A ∧ B ∧ C ∧ D"),

    ("A ∨ (B ∧ C ∧ D)", "(A ∨ B) ∧ (A ∨ C) ∧ (A ∨ D)"),

    ("(A ∨ B) ∧ (C ∨ D) ∧ (E ∨ F)", "(A ∨ B) ∧ (C ∨ D) ∧ (E ∨ F)"),

    ("A ∨ (B ∧ C ∧ (D ∨ E))", "(A ∨ B) ∧ (A ∨ C) ∧ (A ∨ D ∨ E)"),

    ("(A → B) ∨ (C ∧ D)", "(¬A ∨ B ∨ C) ∧ (¬A ∨ B ∨ D)"),

    ("(A ∧ B ∧ C) ∨ D", "(A ∨ D) ∧ (B ∨ D) ∧ (C ∨ D)"),

    ("(A → B) ∧ (C → D) ∧ (E → F)", "(¬A ∨ B) ∧ (¬C ∨ D) ∧ (¬E ∨ F)"),

    ("(A ∨ B) ∧ (C ∨ (D ∧ E))", "(A ∨ B) ∧ (C ∨ D) ∧ (C ∨ E)"),

    ("¬(¬A ∧ ¬B ∧ ¬C)", "A ∨ B ∨ C"),

    ("A", "A"),

    ("¬A", "¬A"),

    ("A ∧ B", "A ∧ B"),

    ("A ∨ B", "A ∨ B"),

    ("A → (B → (C → (D → (E → F))))", "¬A ∨ ¬B ∨ ¬C ∨ ¬D ∨ ¬E ∨ F"),
])
def test_cnf_conversion(expr, expected):
    phase2 = Phase2()
    result = phase2.process(expr)

    # Normalize space to avoid false negatives due to formatting
    def normalize(expr1):
        return expr1.replace(" ", "")

    assert normalize(result) == normalize(expected), f"Expected: {expected}, Got: {result}"


# Additional test cases for edge cases and error handling
@pytest.mark.parametrize("expr, description", [
    # Test formulas that should be valid CNF inputs
    ("(A ∨ B) ∧ (C ∨ D)", "Already in CNF"),
    ("A ∧ B ∧ C", "Simple conjunction"),
    ("A ∨ B ∨ C", "Simple disjunction"),
    ("¬A ∨ ¬B ∨ C", "Mixed literals"),
])
def test_cnf_already_in_cnf(expr, description):
    """Test cases where input is already in CNF or close to it"""
    phase2 = Phase2()
    result = phase2.process(expr)
    # Should not throw errors and should produce valid output
    assert result is not None
    assert len(result) > 0


@pytest.mark.parametrize("expr", [
    "A → (B → (C → (D → (E → (F → G)))))",

    "(A ↔ B) ↔ (C ↔ (D ↔ E))",

    "¬(((A → B) ∧ (C ↔ D)) ∨ ¬((E → F) ∧ (G ↔ H)))",

    "(A ∨ B) ∧ (C ∨ D) ∧ (E ∨ F) ∧ (G ∨ H) ∧ (I ∨ J)",

    "(A ∨ B ∨ C) ∧ (D ∨ (E ∧ F ∧ G))",
])
def test_cnf_complex_structures(expr):
    phase2 = Phase2()
    result = phase2.process(expr)
    # Should not throw errors and should produce valid output
    assert result is not None
    assert len(result) > 0
    # Result should not contain → or ↔ symbols (fully converted)
    assert "→" not in result
    assert "↔" not in result
