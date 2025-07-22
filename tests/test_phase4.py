import pytest
from phases.phase4.logic import Phase4, LogicLine, LogicRuleError
from phases.phase1.logic import Node

@pytest.fixture
def phase4():
    return Phase4()

def create_node(value: str, left=None, right=None) -> Node:
    """Helper to create Node objects"""
    node = Node(value)
    node.left = left
    node.right = right
    return node

def test_and_intro_success(phase4):
    """Test successful AND introduction"""
    input_data = "1    A\n2    B\n∧i,1,2"
    result = phase4.process(input_data)
    assert result == "A ∧ B"


def test_and_elim_left_success(phase4):
    """Test successful AND elimination left"""
    input_data = "1    A ∧ B\n∧e1,1"
    result = phase4.process(input_data)
    assert result == "A"


def test_and_elim_right_success(phase4):
    """Test successful AND elimination right"""
    input_data = "1    A ∧ B\n∧e2,1"
    result = phase4.process(input_data)
    assert result == "B"


def test_modus_ponens_success(phase4):
    """Test successful modus ponens (implication elimination)"""
    input_data = "1    A → B\n2    A\n→e,1,2"
    result = phase4.process(input_data)
    assert result == "B"


def test_modus_tollens_success(phase4):
    """Test successful modus tollens"""
    input_data = "1    A → B\n2    ¬B\nMT,1,2"
    result = phase4.process(input_data)
    assert result == "¬A"


def test_neg_elim_success(phase4):
    """Test successful negation elimination"""
    input_data = "1    A\n2    ¬A\n¬e,1,2"
    result = phase4.process(input_data)
    assert result == "⊥"


def test_double_neg_elim_success(phase4):
    """Test successful double negation elimination"""
    input_data = "1    ¬(¬A)\n¬¬e,1"
    result = phase4.process(input_data)
    assert result == "A"


def test_double_neg_intro_success(phase4):
    """Test successful double negation introduction"""
    input_data = "1    A\n¬¬i,1"
    result = phase4.process(input_data)
    assert result == "¬¬A"

def test_complex_formula_parsing(phase4):
    """Test with complex nested formulas"""
    input_data = "1    (A ∧ B) → (C ∨ D)\n2    A ∧ B\n→e,1,2"
    result = phase4.process(input_data)
    assert result == "C ∨ D"


def test_multiple_line_numbers_different_order(phase4):
    """Test with line numbers in different order"""
    input_data = "2    B\n1    A\n∧i,2,1"
    result = phase4.process(input_data)
    assert result == "B ∧ A"


def test_non_sequential_line_numbers(phase4):
    """Test with non-sequential line numbers"""
    input_data = "1    A\n5    B\n10    C\n∧i,1,10"
    result = phase4.process(input_data)
    assert result == "A ∧ C"


def test_negation_elimination_reversed_order(phase4):
    """Test negation elimination with ¬A, A order"""
    input_data = "1    ¬A\n2    A\n¬e,1,2"
    result = phase4.process(input_data)
    assert result == "⊥"


def test_modus_ponens_with_complex_antecedent(phase4):
    """Test modus ponens with complex antecedent"""
    input_data = "1    (A ∧ B) → C\n2    A ∧ B\n→e,1,2"
    result = phase4.process(input_data)
    assert result == "C"

def test_invalid_rule_name(phase4):
    """Test with invalid rule name"""
    input_data = "1    A\nINVALID_RULE,1"
    result = phase4.process(input_data)
    assert result == "Rule Cannot Be Applied"


def test_wrong_number_of_arguments(phase4):
    """Test AND intro with wrong number of arguments"""
    input_data = "1    A\n∧i,1"  # AND intro needs 2 arguments
    result = phase4.process(input_data)
    assert result == "Rule Cannot Be Applied"


def test_nonexistent_line_number(phase4):
    """Test referencing non-existent line number"""
    input_data = "1    A\n∧i,1,3"  # Line 3 doesn't exist
    result = phase4.process(input_data)
    assert result == "Rule Cannot Be Applied"


def test_and_elim_on_non_conjunction(phase4):
    """Test AND elimination on non-conjunction"""
    input_data = "1    A\n∧e1,1"  # A is not a conjunction
    result = phase4.process(input_data)
    assert result == "Rule Cannot Be Applied"


def test_modus_ponens_antecedent_mismatch(phase4):
    """Test modus ponens with mismatched antecedent"""
    input_data = "1    A → B\n2    C\n→e,1,2"  # C doesn't match A
    result = phase4.process(input_data)
    assert result == "Rule Cannot Be Applied"


def test_modus_tollens_consequent_mismatch(phase4):
    """Test modus tollens with mismatched consequent"""
    input_data = "1    A → B\n2    ¬C\nMT,1,2"  # ¬C doesn't match ¬B
    result = phase4.process(input_data)
    assert result == "Rule Cannot Be Applied"


def test_neg_elim_with_two_positive_nodes(phase4):
    """Test negation elimination with two positive nodes"""
    input_data = "1    A\n2    B\n¬e,1,2"  # Both positive
    result = phase4.process(input_data)
    assert result == "Rule Cannot Be Applied"


def test_neg_elim_with_two_negative_nodes(phase4):
    """Test negation elimination with two negative nodes"""
    input_data = "1    ¬A\n2    ¬B\n¬e,1,2"  # Both negative
    result = phase4.process(input_data)
    assert result == "Rule Cannot Be Applied"


def test_double_neg_elim_on_single_negation(phase4):
    """Test double negation elimination on single negation"""
    input_data = "1    ¬A\n¬¬e,1"  # Only single negation
    result = phase4.process(input_data)
    assert result == "Rule Cannot Be Applied"

def test_malformed_input_no_spaces(phase4):
    """Test with malformed input (no proper spacing)"""
    input_data = "1A\n∧i,1"  # Missing spaces
    result = phase4.process(input_data)
    assert result == "Rule Cannot Be Applied"


def test_empty_input(phase4):
    """Test with empty input"""
    input_data = ""
    result = phase4.process(input_data)
    assert result == "Rule Cannot Be Applied"


def test_input_with_only_rule(phase4):
    """Test with input containing only rule"""
    input_data = "∧i,1,2"
    result = phase4.process(input_data)
    assert result == "Rule Cannot Be Applied"


def test_invalid_line_number_format(phase4):
    """Test with invalid line number format"""
    input_data = "abc    A\n∧i,abc"
    result = phase4.process(input_data)
    assert result == "Rule Cannot Be Applied"


def test_missing_comma_in_rule(phase4):
    """Test with missing comma in rule specification"""
    input_data = "1    A\n∧i 1"  # Missing comma
    result = phase4.process(input_data)
    assert result == "Rule Cannot Be Applied"


def test_extra_whitespace_handling(phase4):
    """Test handling of extra whitespace"""
    input_data = "1    A\n2    B\n∧i , 1 , 2 "  # Extra spaces
    result = phase4.process(input_data)
    assert result == "A ∧ B"

def test_large_line_numbers(phase4):
    """Test with very large line numbers"""
    input_data = "999999    A\n1000000    B\n∧i,999999,1000000"
    result = phase4.process(input_data)
    assert result == "A ∧ B"


def test_complex_structural_equality(phase4):
    """Test complex structural equality in node comparison"""
    input_data = "1    ((A ∧ B) ∧ C) → D\n2    (A ∧ B) ∧ C\n→e,1,2"
    result = phase4.process(input_data)
    assert result == "D"


def test_empty_lines_in_input(phase4):
    """Test input with empty lines"""
    input_data = "1    A\n\n2    B\n\n∧i,1,2"
    result = phase4.process(input_data)
    assert result == "A ∧ B"


def test_unicode_in_formulas(phase4):
    """Test handling of unicode characters in formulas"""
    input_data = "1    α\n2    β\n∧i,1,2"
    result = phase4.process(input_data)
    assert result == "α ∧ β"

@pytest.mark.parametrize("rule_name,expected", [
    ("∧i", "Rule Cannot Be Applied"),
    ("∧e1", "Rule Cannot Be Applied"),
    ("∧e2", "Rule Cannot Be Applied"),
    ("→e", "Rule Cannot Be Applied"),
    ("¬e", "Rule Cannot Be Applied"),
    ("¬¬e", "Rule Cannot Be Applied"),
    ("MT", "Rule Cannot Be Applied"),
    ("¬¬i", "Rule Cannot Be Applied"),
])
def test_all_rules_with_no_arguments(phase4, rule_name, expected):
    """Test all rules with no arguments"""
    input_data = f"{rule_name},"
    result = phase4.process(input_data)
    assert result == expected

def test_conjunction_with_parentheses(phase4):
    """Test conjunction with parentheses"""
    input_data = "1    (A)\n2    (B)\n∧i,1,2"
    result = phase4.process(input_data)
    assert result == "A ∧ B"


def test_implication_with_negation(phase4):
    """Test implication with negation"""
    input_data = "1    ¬A → B\n2    ¬A\n→e,1,2"
    result = phase4.process(input_data)
    assert result == "B"


def test_nested_implications(phase4):
    """Test nested implications"""
    input_data = "1    A → (B → C)\n2    A\n→e,1,2"
    result = phase4.process(input_data)
    assert result == "B → C"


def test_multiple_conjunctions(phase4):
    """Test multiple conjunctions"""
    input_data = "1    A ∧ B\n2    C ∧ D\n∧i,1,2"
    result = phase4.process(input_data)
    assert result == "A ∧ B ∧ C ∧ D"


def test_conjunction_elimination_with_complex_formula(phase4):
    """Test conjunction elimination with complex formula"""
    input_data = "1    (A → B) ∧ (C → D)\n∧e1,1"
    result = phase4.process(input_data)
    assert result == "A → B"


def test_double_negation_with_complex_formula(phase4):
    """Test double negation with complex formula"""
    input_data = "1    ¬(¬(A ∧ B))\n¬¬e,1"
    result = phase4.process(input_data)
    assert result == "A ∧ B"


def test_modus_tollens_with_complex_formulas(phase4):
    """Test modus tollens with complex formulas"""
    input_data = "1    (A ∧ B) → (C ∨ D)\n2    ¬(C ∨ D)\nMT,1,2"
    result = phase4.process(input_data)
    assert result == "¬(A ∧ B)"


def test_negation_elimination_order_independence(phase4):
    """Test that negation elimination works regardless of order"""
    input_data = "1    A\n2    ¬A\n¬e,2,1"
    result = phase4.process(input_data)
    assert result == "⊥"

def test_line_numbers_with_leading_zeros(phase4):
    """Test line numbers with leading zeros"""
    input_data = "001    A\n002    B\n∧i,001,002"
    result = phase4.process(input_data)
    assert result == "A ∧ B"




####
def test_and_intro_simple(phase4):
    expr = "1    p ∧ q\n2    r\n∧i, 1, 2"
    expected_output = "p ∧ q ∧ r"
    assert phase4.process(expr) == expected_output

def test_and_elim1(phase4):
    expr = "1    p ∧ q\n∧e1, 1"
    expected_output = "p"
    assert phase4.process(expr) == expected_output

def test_negation_elim_to_bottom(phase4):
    expr = "1    ¬p\n2    p\n¬e, 2, 1"
    expected_output = "⊥"
    assert phase4.process(expr) == expected_output

def test_invalid_rule_application(phase4):
    expr = "1    p\n2    q\n→e, 1, 2"
    expected_output = "Rule Cannot Be Applied"
    assert phase4.process(expr) == expected_output

def test_and_intro_complex(phase4):
    expr = "1    ¬(p ∨ q)\n2    r → (p ∧ q)\n∧i, 2, 1"
    expected_output = "(r → p ∧ q) ∧ ¬(p ∨ q)"
    assert phase4.process(expr) == expected_output

def test_invalid_and_elim2_on_non_conjunction(phase4):
    expr = "1    ¬(p ∨ q)\n∧e2, 1"
    expected_output = "Rule Cannot Be Applied"
    assert phase4.process(expr) == expected_output

def test_implication_elim_nested(phase4):
    expr = "1    (p → r) → (¬(p ∨ q))\n2    p → r\n→e, 2, 1"
    expected_output = "¬(p ∨ q)"
    assert phase4.process(expr) == expected_output

def test_double_negation_elim_to_bottom(phase4):
    expr = "1    ¬(¬(p → r))\n2    ¬(¬(¬(p → r)))\n¬e, 1, 2"
    expected_output = "⊥"
    assert phase4.process(expr) == expected_output

def test_double_negation_elim(phase4):
    expr = "1    ¬(¬(¬(p → r)))\n¬¬e, 1"
    expected_output = "¬(p → r)"
    assert phase4.process(expr) == expected_output

def test_invalid_double_negation_elim_on_implication(phase4):
    expr = "1    ¬((¬(¬(p → r))) → r)\n¬¬e, 1"
    expected_output = "Rule Cannot Be Applied"
    assert phase4.process(expr) == expected_output

def test_modus_tollens_deep(phase4):
    expr = "1    (¬(¬(¬(p → r)))) → r\n2    ¬r\nMT, 1, 2"
    expected_output = "¬¬¬¬(p → r)"
    assert phase4.process(expr) == expected_output

def test_double_negation_intro(phase4):
    expr = "1    ¬(¬(¬(p → r)))\n¬¬i, 1"
    expected_output = "¬¬¬¬¬(p → r)"
    assert phase4.process(expr) == expected_output
