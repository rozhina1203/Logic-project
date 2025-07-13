import pytest
from phases.phase4.logic import Phase4, LogicLine, LogicRuleError
from phases.phase1.logic import Node


def create_node(value: str, left=None, right=None) -> Node:
    """Helper to create Node objects"""
    node = Node(value)
    node.left = left
    node.right = right
    return node

def test_and_intro_success():
    """Test successful AND introduction"""
    phase4 = Phase4()
    input_data = "1    A\n2    B\n∧i,1,2"
    result = phase4.process(input_data)
    assert result == "A ∧ B"


def test_and_elim_left_success():
    """Test successful AND elimination left"""
    phase4 = Phase4()
    input_data = "1    A ∧ B\n∧e1,1"
    result = phase4.process(input_data)
    assert result == "A"


def test_and_elim_right_success():
    """Test successful AND elimination right"""
    phase4 = Phase4()
    input_data = "1    A ∧ B\n∧e2,1"
    result = phase4.process(input_data)
    assert result == "B"


def test_modus_ponens_success():
    """Test successful modus ponens (implication elimination)"""
    phase4 = Phase4()
    input_data = "1    A → B\n2    A\n→e,1,2"
    result = phase4.process(input_data)
    assert result == "B"


def test_modus_tollens_success():
    """Test successful modus tollens"""
    phase4 = Phase4()
    input_data = "1    A → B\n2    ¬B\nMT,1,2"
    result = phase4.process(input_data)
    assert result == "¬A"


def test_neg_elim_success():
    """Test successful negation elimination"""
    phase4 = Phase4()
    input_data = "1    A\n2    ¬A\n¬e,1,2"
    result = phase4.process(input_data)
    assert result == "⊥"


def test_double_neg_elim_success():
    """Test successful double negation elimination"""
    phase4 = Phase4()
    input_data = "1    ¬(¬A)\n¬¬e,1"
    result = phase4.process(input_data)
    assert result == "A"


def test_double_neg_intro_success():
    """Test successful double negation introduction"""
    phase4 = Phase4()
    input_data = "1    A\n¬¬i,1"
    result = phase4.process(input_data)
    assert result == "¬¬A"

def test_complex_formula_parsing():
    """Test with complex nested formulas"""
    phase4 = Phase4()
    input_data = "1    (A ∧ B) → (C ∨ D)\n2    A ∧ B\n→e,1,2"
    result = phase4.process(input_data)
    assert result == "C ∨ D"


def test_multiple_line_numbers_different_order():
    """Test with line numbers in different order"""
    phase4 = Phase4()
    input_data = "2    B\n1    A\n∧i,2,1"
    result = phase4.process(input_data)
    assert result == "B ∧ A"


def test_non_sequential_line_numbers():
    """Test with non-sequential line numbers"""
    phase4 = Phase4()
    input_data = "1    A\n5    B\n10    C\n∧i,1,10"
    result = phase4.process(input_data)
    assert result == "A ∧ C"


def test_negation_elimination_reversed_order():
    """Test negation elimination with ¬A, A order"""
    phase4 = Phase4()
    input_data = "1    ¬A\n2    A\n¬e,1,2"
    result = phase4.process(input_data)
    assert result == "⊥"


def test_modus_ponens_with_complex_antecedent():
    """Test modus ponens with complex antecedent"""
    phase4 = Phase4()
    input_data = "1    (A ∧ B) → C\n2    A ∧ B\n→e,1,2"
    result = phase4.process(input_data)
    assert result == "C"

def test_invalid_rule_name():
    """Test with invalid rule name"""
    phase4 = Phase4()
    input_data = "1    A\nINVALID_RULE,1"
    result = phase4.process(input_data)
    assert result == "Rule Cannot Be Applied"


def test_wrong_number_of_arguments():
    """Test AND intro with wrong number of arguments"""
    phase4 = Phase4()
    input_data = "1    A\n∧i,1"  # AND intro needs 2 arguments
    result = phase4.process(input_data)
    assert result == "Rule Cannot Be Applied"


def test_nonexistent_line_number():
    """Test referencing non-existent line number"""
    phase4 = Phase4()
    input_data = "1    A\n∧i,1,3"  # Line 3 doesn't exist
    result = phase4.process(input_data)
    assert result == "Rule Cannot Be Applied"


def test_and_elim_on_non_conjunction():
    """Test AND elimination on non-conjunction"""
    phase4 = Phase4()
    input_data = "1    A\n∧e1,1"  # A is not a conjunction
    result = phase4.process(input_data)
    assert result == "Rule Cannot Be Applied"


def test_modus_ponens_antecedent_mismatch():
    """Test modus ponens with mismatched antecedent"""
    phase4 = Phase4()
    input_data = "1    A → B\n2    C\n→e,1,2"  # C doesn't match A
    result = phase4.process(input_data)
    assert result == "Rule Cannot Be Applied"


def test_modus_tollens_consequent_mismatch():
    """Test modus tollens with mismatched consequent"""
    phase4 = Phase4()
    input_data = "1    A → B\n2    ¬C\nMT,1,2"  # ¬C doesn't match ¬B
    result = phase4.process(input_data)
    assert result == "Rule Cannot Be Applied"


def test_neg_elim_with_two_positive_nodes():
    """Test negation elimination with two positive nodes"""
    phase4 = Phase4()
    input_data = "1    A\n2    B\n¬e,1,2"  # Both positive
    result = phase4.process(input_data)
    assert result == "Rule Cannot Be Applied"


def test_neg_elim_with_two_negative_nodes():
    """Test negation elimination with two negative nodes"""
    phase4 = Phase4()
    input_data = "1    ¬A\n2    ¬B\n¬e,1,2"  # Both negative
    result = phase4.process(input_data)
    assert result == "Rule Cannot Be Applied"


def test_double_neg_elim_on_single_negation():
    """Test double negation elimination on single negation"""
    phase4 = Phase4()
    input_data = "1    ¬A\n¬¬e,1"  # Only single negation
    result = phase4.process(input_data)
    assert result == "Rule Cannot Be Applied"

def test_malformed_input_no_spaces():
    """Test with malformed input (no proper spacing)"""
    phase4 = Phase4()
    input_data = "1A\n∧i,1"  # Missing spaces
    result = phase4.process(input_data)
    assert result == "Rule Cannot Be Applied"


def test_empty_input():
    """Test with empty input"""
    phase4 = Phase4()
    input_data = ""
    result = phase4.process(input_data)
    assert result == "Rule Cannot Be Applied"


def test_input_with_only_rule():
    """Test with input containing only rule"""
    phase4 = Phase4()
    input_data = "∧i,1,2"
    result = phase4.process(input_data)
    assert result == "Rule Cannot Be Applied"


def test_invalid_line_number_format():
    """Test with invalid line number format"""
    phase4 = Phase4()
    input_data = "abc    A\n∧i,abc"
    result = phase4.process(input_data)
    assert result == "Rule Cannot Be Applied"


def test_missing_comma_in_rule():
    """Test with missing comma in rule specification"""
    phase4 = Phase4()
    input_data = "1    A\n∧i 1"  # Missing comma
    result = phase4.process(input_data)
    assert result == "Rule Cannot Be Applied"


def test_extra_whitespace_handling():
    """Test handling of extra whitespace"""
    phase4 = Phase4()
    input_data = "1    A\n2    B\n∧i , 1 , 2 "  # Extra spaces
    result = phase4.process(input_data)
    assert result == "A ∧ B"

def test_large_line_numbers():
    """Test with very large line numbers"""
    phase4 = Phase4()
    input_data = "999999    A\n1000000    B\n∧i,999999,1000000"
    result = phase4.process(input_data)
    assert result == "A ∧ B"


def test_complex_structural_equality():
    """Test complex structural equality in node comparison"""
    phase4 = Phase4()
    input_data = "1    ((A ∧ B) ∧ C) → D\n2    (A ∧ B) ∧ C\n→e,1,2"
    result = phase4.process(input_data)
    assert result == "D"


def test_empty_lines_in_input():
    """Test input with empty lines"""
    phase4 = Phase4()
    input_data = "1    A\n\n2    B\n\n∧i,1,2"
    result = phase4.process(input_data)
    assert result == "A ∧ B"


def test_unicode_in_formulas():
    """Test handling of unicode characters in formulas"""
    phase4 = Phase4()
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
def test_all_rules_with_no_arguments(rule_name, expected):
    """Test all rules with no arguments"""
    phase4 = Phase4()
    input_data = f"{rule_name},"
    result = phase4.process(input_data)
    assert result == expected

def test_conjunction_with_parentheses():
    """Test conjunction with parentheses"""
    phase4 = Phase4()
    input_data = "1    (A)\n2    (B)\n∧i,1,2"
    result = phase4.process(input_data)
    assert result == "A ∧ B"


def test_implication_with_negation():
    """Test implication with negation"""
    phase4 = Phase4()
    input_data = "1    ¬A → B\n2    ¬A\n→e,1,2"
    result = phase4.process(input_data)
    assert result == "B"


def test_nested_implications():
    """Test nested implications"""
    phase4 = Phase4()
    input_data = "1    A → (B → C)\n2    A\n→e,1,2"
    result = phase4.process(input_data)
    assert result == "B → C"


def test_multiple_conjunctions():
    """Test multiple conjunctions"""
    phase4 = Phase4()
    input_data = "1    A ∧ B\n2    C ∧ D\n∧i,1,2"
    result = phase4.process(input_data)
    assert result == "A ∧ B ∧ C ∧ D"


def test_conjunction_elimination_with_complex_formula():
    """Test conjunction elimination with complex formula"""
    phase4 = Phase4()
    input_data = "1    (A → B) ∧ (C → D)\n∧e1,1"
    result = phase4.process(input_data)
    assert result == "A → B"


def test_double_negation_with_complex_formula():
    """Test double negation with complex formula"""
    phase4 = Phase4()
    input_data = "1    ¬(¬(A ∧ B))\n¬¬e,1"
    result = phase4.process(input_data)
    assert result == "A ∧ B"


def test_modus_tollens_with_complex_formulas():
    """Test modus tollens with complex formulas"""
    phase4 = Phase4()
    input_data = "1    (A ∧ B) → (C ∨ D)\n2    ¬(C ∨ D)\nMT,1,2"
    result = phase4.process(input_data)
    assert result == "¬(A ∧ B)"


def test_negation_elimination_order_independence():
    """Test that negation elimination works regardless of order"""
    phase4 = Phase4()
    input_data = "1    A\n2    ¬A\n¬e,2,1"
    result = phase4.process(input_data)
    assert result == "⊥"

def test_line_numbers_with_leading_zeros():
    """Test line numbers with leading zeros"""
    phase4 = Phase4()
    input_data = "001    A\n002    B\n∧i,001,002"
    result = phase4.process(input_data)
    assert result == "A ∧ B"
