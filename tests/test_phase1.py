import pytest
from phases.phase1.logic import Phase1

@pytest.fixture
def phase1():
    return Phase1()

def test_valid_formula_simple(phase1):
    expr = "a"
    expected_output = "Valid Formula\n" \
                      "a"
    assert phase1.process(expr) == expected_output

def test_valid_multiple_negations(phase1):
    expr = "¬(¬a)"
    expected_output = (
        "Valid Formula\n"
        "¬\n"
        "  ¬\n"
        "    a"
    )
    assert phase1.process(expr) == expected_output

def test_valid_nested_formula(phase1):
    expr = "((¬q → r) ∧ (p ∧ ¬r))"
    expected_output = (
        "Valid Formula\n"
        "∧\n"
        "  →\n"
        "    ¬\n"
        "      q\n"
        "    r\n"
        "  ∧\n"
        "    p\n"
        "    ¬\n"
        "      r"
    )
    assert phase1.process(expr) == expected_output
def test_invalid_unmatched_parenthesis(phase1):
    expr = "(p ∧ q"
    assert phase1.process(expr) == "Invalid Formula"


def test_invalid_double_operator(phase1):
    expr = "(a ∧ ∨ b)"
    assert phase1.process(expr) == "Invalid Formula"


def test_invalid_missing_operator(phase1):
    expr = "(a b)"
    assert phase1.process(expr) == "Invalid Formula"


def test_invalid_empty_negation(phase1):
    expr = "(¬)"
    assert phase1.process(expr) == "Invalid Formula"


def test_invalid_extra_closing_parenthesis(phase1):
    expr = "a ∨ b)"
    assert phase1.process(expr) == "Invalid Formula"


def test_invalid_start_with_binary_operator(phase1):
    expr = "∧ (a ∨ b)"
    assert phase1.process(expr) == "Invalid Formula"

def test_many_parentheses_around_single_var(phase1):
    expr = "((((((((a))))))))"
    expected_output = "Valid Formula\n" \
                      "a"
    assert phase1.process(expr) == expected_output


def test_valid_formula_complex_1(phase1):
    expr = "((¬q) → r) ∧ (p ∧ (¬r))"
    expected_output = "Valid Formula\n" \
                      "∧\n" \
                      "  →\n" \
                      "    ¬\n" \
                      "      q\n" \
                      "    r\n" \
                      "  ∧\n" \
                      "    p\n" \
                      "    ¬\n" \
                      "      r"
    assert phase1.process(expr) == expected_output

def test_invalid_formula_missing_paren(phase1):
    expr = "(p ∧ q"
    expected_output = "Invalid Formula"
    assert phase1.process(expr) == expected_output

def test_valid_formula_single_var(phase1):
    expr = "p"
    expected_output = "Valid Formula\n" \
                      "p"
    assert phase1.process(expr) == expected_output

def test_valid_formula_nested(phase1):
    expr = "(p → (¬((¬r) ∧ q))) ∨ s"
    expected_output = "Valid Formula\n" \
                      "∨\n" \
                      "  →\n" \
                      "    p\n" \
                      "    ¬\n" \
                      "      ∧\n" \
                      "        ¬\n" \
                      "          r\n" \
                      "        q\n" \
                      "  s"
    assert phase1.process(expr) == expected_output

def test_invalid_formula_operator_at_end(phase1):
    expr = "(p → r) ¬"
    expected_output = "Invalid Formula"
    assert phase1.process(expr) == expected_output

def test_invalid_formula_misplaced_parens(phase1):
    expr = "¬q)( → (¬r)"
    expected_output = "Invalid Formula"
    assert phase1.process(expr) == expected_output

def test_invalid_formula_unexpected_operator(phase1):
    expr = "¬ ∧ q"
    expected_output = "Invalid Formula"
    assert phase1.process(expr) == expected_output
