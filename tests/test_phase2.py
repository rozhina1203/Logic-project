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
    # Test 1: Demorgan
    ("¬(p ∧ q)", "¬p ∨ ¬q"),

    # Test 2: Distribution
    ("p ∨ (q ∧ r)", "(p ∨ q) ∧ (p ∨ r)"),

    # Test 3: Implication
    ("¬p → q", "p ∨ q"),

    # Test 4: Implication with conjunction and disjunction
    ("((p → q) ∧ (r ∨ s))", "(¬p ∨ q) ∧ (r ∨ s)"),

    # Test 5: Bi-conditional
    ("(p ↔ q)", "(¬p ∨ q) ∧ (¬q ∨ p)"),

    # Test 6: Nested implications
    ("(p ∨ q) ∨ (r ∧ s)", "(p ∨ q ∨ r) ∧ (p ∨ q ∨ s)"),

    # Basic implication
    ("A → B", "¬A ∨ B"),

    # Bi-conditional
    ("A ↔ B", "(¬A ∨ B) ∧ (¬B ∨ A)"),

    # De Morgan's Law
    ("¬(A ∧ B)", "¬A ∨ ¬B"),
    ("¬(A ∨ B)", "¬A ∧ ¬B"),

    # Nested implications
    ("A → (B → C)", "¬A ∨ (¬B ∨ C)"),

    # Complex: implication with conjunction
    ("(A ∧ B) → C", "¬A ∨ ¬B ∨ C"),

    # CNF distribution
    ("A ∨ (B ∧ C)", "(A ∨ B) ∧ (A ∨ C)"),

    ("(A ∧ B) ∨ (C ∧ D)", "((A ∨ C) ∧ (A ∨ D)) ∧ ((B ∨ C) ∧ (B ∨ D))"),

    # Double negation
    ("¬(¬A)", "A"),

    # Mixed example
    ("¬(A → (B ∨ C))", "A ∧ ¬B ∧ ¬C"),
])
def test_cnf_conversion(phase2, expr, expected):
    # result = phase2.process(expr)
    # assert result == expected

    phase2 = Phase2()
    result = phase2.process(expr)

    # Normalize space to avoid false negatives due to formatting
    def normalize(expr1):
        return expr1.replace("(", "").replace(")", "").replace(" ", "")

    assert normalize(result) == normalize(expected), f"Expected: {expected}, Got: {result}"
