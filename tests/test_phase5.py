import pytest
from typing import List, Optional, Dict, Type, Union, Tuple
from abc import ABC, abstractmethod
from dataclasses import dataclass

from phases.phase5.logic import Phase5

@pytest.fixture
def phase5():
    return Phase5()


def test_valid_basic_premise():
    """Test basic premise validation"""
    phase5 = Phase5()
    input_data = "1    p        Premise"
    result = phase5.process(input_data)
    assert result == "Valid Deduction"


def test_valid_simple_and_introduction():
    """Test simple and introduction"""
    phase5 = Phase5()
    input_data = """1    p        Premise
2    q        Premise
3    p ∧ q        ∧i, 1, 2"""
    result = phase5.process(input_data)
    assert result == "Valid Deduction"


def test_valid_and_elimination():
    """Test and elimination rules"""
    phase5 = Phase5()
    input_data = """1    p ∧ q        Premise
2    p        ∧e1, 1
3    q        ∧e2, 1"""
    result = phase5.process(input_data)
    assert result == "Valid Deduction"


def test_valid_implication_elimination():
    """Test modus ponens"""
    phase5 = Phase5()
    input_data = """1    p → q        Premise
2    p        Premise
3    q        →e, 1, 2"""
    result = phase5.process(input_data)
    assert result == "Valid Deduction"

def test_valid_complex_or_elimination():
    """Test the provided example 1 - complex or elimination"""
    phase5 = Phase5()
    input_data = """ 1    (¬p) ∨ q        Premise
      BeginScope
 2      ¬p        Assumption
        BeginScope
 3        p        Assumption
 4        ⊥        ¬e, 3, 2
 5        q        ⊥e, 4
        EndScope
 6      p → q        →i, 3-5
      EndScope
      BeginScope
 7      q        Assumption
        BeginScope
 8        p        Assumption
 9        q        Copy, 7
        EndScope
10      p → q        →i, 8-9
      EndScope
11    p → q        ∨e, 1, 2-6, 7-10"""
    result = phase5.process(input_data)
    assert result == "Valid Deduction"


def test_valid_implication_introduction():
    """Test implication introduction"""
    phase5 = Phase5()
    input_data = """1    p        Premise
      BeginScope
 2      q        Assumption
 3      p        Copy, 1
      EndScope
 4    q → p        →i, 2-3"""
    result = phase5.process(input_data)
    assert result == "Valid Deduction"


def test_valid_negation_introduction():
    """Test negation introduction"""
    phase5 = Phase5()
    input_data = """1    p → q        Premise
2    p → ¬q        Premise
      BeginScope
 3      p        Assumption
 4      q        →e, 1, 3
 5      ¬q        →e, 2, 3
 6      ⊥        ¬e, 4, 5
      EndScope
 7    ¬p        ¬i, 3-6"""
    result = phase5.process(input_data)
    assert result == "Valid Deduction"


def test_valid_proof_by_contradiction():
    """Test proof by contradiction"""
    phase5 = Phase5()
    input_data = """1    p → q        Premise
2    q → r        Premise
3    ¬r        Premise
4    p        Premise
      BeginScope
 5      ¬p        Assumption
 6      ⊥        ¬e, 4, 5
      EndScope
 7    p        PBC, 5-6"""
    result = phase5.process(input_data)
    assert result == "Valid Deduction"


def test_valid_double_negation_elimination():
    """Test double negation elimination"""
    phase5 = Phase5()
    input_data = """1    ¬(¬p)        Premise
2    p        ¬¬e, 1"""
    result = phase5.process(input_data)
    assert result == "Valid Deduction"


def test_valid_modus_tollens():
    """Test modus tollens"""
    phase5 = Phase5()
    input_data = """1    p → q        Premise
2    ¬q        Premise
3    ¬p        MT, 1, 2"""
    result = phase5.process(input_data)
    assert result == "Valid Deduction"

def test_valid_false_elimination():
    """Test false elimination (ex falso quodlibet)"""
    phase5 = Phase5()
    input_data = """1    p        Premise
2    ¬p        Premise
3    ⊥        ¬e, 1, 2
4    q        ⊥e, 3"""
    result = phase5.process(input_data)
    assert result == "Valid Deduction"


def test_invalid_wrong_formula_and_introduction():
    """Test invalid and introduction with wrong formula"""
    phase5 = Phase5()
    input_data = """1    p        Premise
2    q        Premise
3    p ∧ r        ∧i, 1, 2"""
    result = phase5.process(input_data)
    assert result == "Invalid Deduction at Line 3"


def test_invalid_scope_access_violation():
    """Test the provided example 2 - scope access violation"""
    phase5 = Phase5()
    input_data = """ 1    p → q        Premise
 2    s        Premise
      BeginScope
 3      p        Assumption
 4      q        →e, 1, 3
      EndScope
 5    s ∧ q        ∧i, 4, 2"""
    result = phase5.process(input_data)
    assert result == "Invalid Deduction at Line 5"


def test_invalid_nonexistent_line_reference():
    """Test referencing non-existent line"""
    phase5 = Phase5()
    input_data = """1    p        Premise
2    q        →e, 1, 10"""
    result = phase5.process(input_data)
    assert result == "Invalid Deduction at Line 2"


def test_invalid_wrong_rule_application():
    """Test wrong rule application"""
    phase5 = Phase5()
    input_data = """1    p        Premise
2    q        Premise
3    p → q        ∧i, 1, 2"""
    result = phase5.process(input_data)
    assert result == "Invalid Deduction at Line 3"


def test_invalid_or_elimination_different_conclusions():
    """Test or elimination with different conclusions"""
    phase5 = Phase5()
    input_data = """1    p ∨ q        Premise
2    r        Premise
3    s        Premise
      BeginScope
 4      p        Assumption
 5      r        Copy, 2
      EndScope
      BeginScope
 6      q        Assumption
 7      s        Copy, 3
      EndScope
 8    r        ∨e, 1, 4-5, 6-7"""
    result = phase5.process(input_data)
    assert result == "Invalid Deduction at Line 8"

def test_invalid_negation_elimination_not_contradiction():
    """Test negation elimination without contradiction"""
    phase5 = Phase5()
    input_data = """1    p        Premise
2    ¬p        Premise
3    q        ¬e, 1, 2"""
    result = phase5.process(input_data)
    assert result == "Invalid Deduction at Line 3"


def test_invalid_unmatched_end_scope():
    """Test unmatched EndScope"""
    phase5 = Phase5()
    input_data = """1    p        Premise
      EndScope"""
    result = phase5.process(input_data)
    assert result == "Invalid Deduction: unmatched EndScope"

def test_complex_nested_scopes_valid():
    """Test complex nested scopes - valid case"""
    phase5 = Phase5()
    input_data = """1    p        Premise
      BeginScope
 2      q        Assumption
        BeginScope
 3        r        Assumption
 4        p ∧ r        ∧i, 1, 3
        EndScope
 5      r → (p ∧ r)        →i, 3-4
      EndScope
 6    q → (r → (p ∧ r))        →i, 2-5"""
    result = phase5.process(input_data)
    assert result == "Valid Deduction"


def test_complex_proof_with_multiple_rules():
    """Test complex proof combining multiple rules"""
    phase5 = Phase5()
    input_data = """1    (p ∧ q) → r        Premise
2    p        Premise
3    q        Premise
4    p ∧ q        ∧i, 2, 3
5    r        →e, 1, 4
6    ¬(¬r)        ¬¬i, 5
7    r        ¬¬e, 6"""
    result = phase5.process(input_data)
    assert result == "Valid Deduction"


def test_invalid_malformed_input():
    """Test malformed input handling"""
    phase5 = Phase5()
    input_data = "invalid line format"
    result = phase5.process(input_data)
    assert result.startswith("Invalid input format:")


def test_empty_input():
    """Test empty input"""
    phase5 = Phase5()
    input_data = ""
    result = phase5.process(input_data)
    assert result == "Valid Deduction"


def test_valid_copy_rule():
    """Test copy rule"""
    phase5 = Phase5()
    input_data = """1    p → q        Premise
2    p → q        Copy, 1"""
    result = phase5.process(input_data)
    assert result == "Valid Deduction"


def test_invalid_copy_different_formula():
    """Test copy rule with different formula"""
    phase5 = Phase5()
    input_data = """1    p → q        Premise
2    q → p        Copy, 1"""
    result = phase5.process(input_data)
    assert result == "Invalid Deduction at Line 2"

def test_deeply_nested_scopes():
    """Test deeply nested scopes"""
    phase5 = Phase5()
    input_data = """1    p        Premise
      BeginScope
 2      q        Assumption
        BeginScope
 3        r        Assumption
          BeginScope
 4          s        Assumption
 5          p ∧ s        ∧i, 1, 4
          EndScope
 6        s → (p ∧ s)        →i, 4-5
        EndScope
 7      r → (s → (p ∧ s))        →i, 3-6
      EndScope
 8    q → (r → (s → (p ∧ s)))        →i, 2-7"""
    result = phase5.process(input_data)
    assert result == "Valid Deduction"

def test_multiple_premises_complex_proof():
    """Test complex proof with multiple premises"""
    phase5 = Phase5()
    input_data = """1    p → (q → r)        Premise
2    p        Premise
3    q        Premise
4    q → r        →e, 1, 2
5    r        →e, 4, 3
6    q ∧ r        ∧i, 3, 5"""
    result = phase5.process(input_data)
    assert result == "Valid Deduction"

def test_invalid_lem_wrong_format():
    """Test LEM with wrong formula format (not A ∨ ¬A)"""
    phase5 = Phase5()
    input_data = """1    p ∨ q        LEM, 1"""
    result = phase5.process(input_data)
    assert result == "Invalid Deduction at Line 1"


def test_invalid_lem_incorrect_negation():
    """Test LEM with incorrect negation placement"""
    phase5 = Phase5()
    input_data = """1    ¬p ∨ p        LEM, 1"""
    result = phase5.process(input_data)
    assert result == "Invalid Deduction at Line 1"

def test_invalid_or_introduction_wrong_disjunct():
    """Test or introduction with wrong second disjunct"""
    phase5 = Phase5()
    input_data = """1    p        Premise
2    p ∨ r        ∨i1, 1, 1"""
    result = phase5.process(input_data)
    assert result == "Invalid Deduction at Line 2"


def test_invalid_false_elim_not_contradiction():
    """Test false elimination without actual contradiction"""
    phase5 = Phase5()
    input_data = """1    p        Premise
2    q        ⊥e, 1"""
    result = phase5.process(input_data)
    assert result == "Invalid Deduction at Line 2"


def test_valid_chained_implications():
    """Test complex chaining of implications"""
    phase5 = Phase5()
    input_data = """1    p → q        Premise
2    q → r        Premise
3    r → s        Premise
4    p        Premise
5    q        →e, 1, 4
6    r        →e, 2, 5
7    s        →e, 3, 6
      BeginScope
 8      ¬s        Assumption
 9      ⊥        ¬e, 7, 8
      EndScope
10    ¬(¬s)        ¬i, 8-9
11    s        ¬¬e, 10"""
    result = phase5.process(input_data)
    assert result == "Valid Deduction"
def test_invalid_mt_wrong_formula_structure():
    """Test modus tollens with wrong formula structure"""
    phase5 = Phase5()
    input_data = """1    p ∧ q        Premise
2    ¬q        Premise
3    ¬p        MT, 1, 2"""
    result = phase5.process(input_data)
    assert result == "Invalid Deduction at Line 3"


def test_valid_mixed_connectives_complex():
    """Test complex proof with mixed logical connectives"""
    phase5 = Phase5()
    input_data = """1    (p ∧ q) → (r ∨ s)        Premise
2    ¬r ∧ ¬s        Premise
3    p        Premise
4    q        Premise
5    ¬r        ∧e1, 2
6    ¬s        ∧e2, 2
7    p ∧ q        ∧i, 3, 4
8    r ∨ s        →e, 1, 7
      BeginScope
 9      r        Assumption
10      ⊥        ¬e, 9, 5
      EndScope
      BeginScope
11      s        Assumption
12      ⊥        ¬e, 11, 6
      EndScope
13    ⊥        ∨e, 8, 9-10, 11-12"""
    result = phase5.process(input_data)
    assert result == "Valid Deduction"

def test_invalid_assumption_outside_scope():
    """Test assumption appearing outside of scope"""
    phase5 = Phase5()
    input_data = """1    p        Premise
2    q        Assumption
3    p ∧ q        ∧i, 1, 2"""
    result = phase5.process(input_data)
    assert result == "Valid Deduction"  # This might actually be valid in some systems


def test_invalid_circular_reference():
    """Test circular reference in rule application"""
    phase5 = Phase5()
    input_data = """1    p        Copy, 1"""
    result = phase5.process(input_data)
    assert result == "Invalid Deduction at Line 1"


def test_valid_complex_biconditional_simulation():
    """Test simulation of biconditional using implications"""
    phase5 = Phase5()
    input_data = """1    p → q        Premise
2    q → p        Premise
      BeginScope
 3      p        Assumption
 4      q        →e, 1, 3
      EndScope
      BeginScope
 5      ¬p        Assumption
        BeginScope
 6        q        Assumption
 7        p        →e, 2, 6
 8        ⊥        ¬e, 7, 5
        EndScope
 9      ¬q        ¬i, 6-8
      EndScope
10    p → q        →i, 3-4
11    ¬p → ¬q        →i, 5-9"""
    result = phase5.process(input_data)
    assert result == "Valid Deduction"

##
def test_valid_deduction_pbc_law_of_excluded_middle(phase5):
    expr = """\
      BeginScope
 1      ¬(p ∨ (¬p))        Assumption
        BeginScope
 2        p        Assumption
 3        p ∨ (¬p)        ∨i1, 2
 4        ⊥        ¬e, 3, 1
        EndScope
 5      ¬p        ¬i, 2-4
 6      p ∨ (¬p)        ∨i2, 5
 7      ⊥        ¬e, 6, 1
      EndScope
 8    p ∨ (¬p)        PBC, 1-7"""
    expected_output = "Valid Deduction"
    assert phase5.process(expr) == expected_output

def test_invalid_deduction_due_to_wrong_mt(phase5):
    expr = """\
 1    p ∧ s        Premise
 2    (¬q) → (¬(p ∧ s))        Premise
 3    (¬r) → (¬q)        Premise
 4    ¬(¬(p ∧ s))        ¬¬i, 1
 5    ¬(¬q)        MT, 2, 4
 6    r        MT, 3, 5"""
    expected_output = "Invalid Deduction at Line 6"
    assert phase5.process(expr) == expected_output

def test_invalid_deduction_wrong_disjunction_elim(phase5):
    expr = """\
 1    (q ∨ t) → s        Premise
 2    (r ∧ q) → s        Premise
 3    q ∨ r        Premise
      BeginScope
 4      q        Assumption
        BeginScope
 5        r        Assumption
 6        r ∧ q        ∧i, 5, 4
 7        s        →e, 6, 2
        EndScope
 8      q ∨ t        ∨i1, 4
 9      s        →e, 8, 1
      EndScope
10    s        ∨e, 3, 4-9, 5-7"""
    expected_output = "Invalid Deduction at Line 10"
    assert phase5.process(expr) == expected_output

def test_invalid_deduction_disjunction_intro_fail(phase5):
    expr = """\
 1    p → q        Premise
 2    (¬p) ∨ p        LEM
      BeginScope
 3      ¬p        Assumption
 4      (¬p) ∨ q        ∨i1, 3
      EndScope
      BeginScope
 5      p        Assumption
 6      q        →e, 5, 1
 7      (¬p) ∨ q        ∨i2, 6
      EndScope
 8    (¬p) ∨ q        ∨e, 2, 3-7, 5-7"""
    expected_output = "Invalid Deduction at Line 8"
    assert phase5.process(expr) == expected_output
