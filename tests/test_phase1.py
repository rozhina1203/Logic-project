import pytest
from phases.phase1.logic import Phase1

@pytest.fixture
def phase1():
    return Phase1()

def test_valid_formula_simple(phase1):
    expr = "a"
    expected_output = "Valid Formula\n" \
                      "a\n"
    assert phase1.process(expr) == expected_output

def test_valid_multiple_negations(phase1):
    # TODO: Fix this test to match the expected output format.
    # You can run `pytest -k test_valid_multiple_negations` to see the error.
    expr = "¬¬a"
    expected_output = (
        "Valid Formula\n"
        "¬\n"
        "  ¬\n"
        "    a\n"
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
        "      r\n"
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
                      "a\n"
    assert phase1.process(expr) == expected_output
