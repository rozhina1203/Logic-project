from typing import List, Optional, Dict, Type
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from phases.base_phase import BasePhase
from phases.phase1.logic import Node, Phase1
from phases.phase2.logic import Phase2


class LogicSymbol(Enum):
    AND = "∧"
    IMPLIES = "→"
    NOT = "¬"
    CONTRADICTION = "⊥"


@dataclass
class LogicLine:
    line_number: int
    formula: Optional[Node] = None
    rule:Optional['LogicRule'] = None
    is_formula: bool = True

class LogicRuleError(Exception):
    """Custom exception for logic rule errors"""
    pass


class LogicRule(ABC):
    """Abstract base class for all logic rules"""

    def __init__(self, nodes: List[Node], rule_name: str):
        self.rule_name = rule_name
        self.nodes = nodes
        self._validate_input()

    @abstractmethod
    def _validate_input(self) -> None:
        """Validate the input nodes for this rule"""
        pass

    @abstractmethod
    def apply(self) -> Node:
        """Apply the logic rule and return the result"""
        pass

    def _nodes_equal(self, node1: Node, node2: Node) -> bool:
        """Check if two nodes are structurally equal"""
        if node1.value != node2.value:
            return False

        if node1.left is None and node2.left is None:
            left_equal = True
        elif node1.left is not None and node2.left is not None:
            left_equal = self._nodes_equal(node1.left, node2.left)
        else:
            left_equal = False

        if node1.right is None and node2.right is None:
            right_equal = True
        elif node1.right is not None and node2.right is not None:
            right_equal = self._nodes_equal(node1.right, node2.right)
        else:
            right_equal = False

        return left_equal and right_equal


class AndIntro(LogicRule):
    """∧i: Combine two statements into a conjunction (A ∧ B)"""

    def _validate_input(self) -> None:
        if len(self.nodes) != 2:
            raise LogicRuleError("AndIntro requires exactly two nodes")

    def apply(self) -> Node:
        left_node, right_node = self.nodes
        conjunction = Node(LogicSymbol.AND.value)
        conjunction.left = left_node
        conjunction.right = right_node
        return conjunction


class AndElimLeft(LogicRule):
    """∧e1: Extract the left part (A) from a conjunction (A ∧ B)"""

    def _validate_input(self) -> None:
        if len(self.nodes) != 1:
            raise LogicRuleError("AndElimLeft requires exactly one node")

    def apply(self) -> Node:
        conjunction = self.nodes[0]

        if conjunction.value != LogicSymbol.AND.value or conjunction.left is None:
            raise LogicRuleError("Input must be a conjunction (∧) with a left child")

        return conjunction.left


class AndElimRight(LogicRule):
    """∧e2: Extract the right part (B) from a conjunction (A ∧ B)"""

    def _validate_input(self) -> None:
        if len(self.nodes) != 1:
            raise LogicRuleError("AndElimRight requires exactly one node")

    def apply(self) -> Node:
        conjunction = self.nodes[0]

        if conjunction.value != LogicSymbol.AND.value or conjunction.right is None:
            raise LogicRuleError("Input must be a conjunction (∧) with a right child")

        return conjunction.right


class ImpElim(LogicRule):
    """→e: From A → B and A, infer B"""

    def _validate_input(self) -> None:
        if len(self.nodes) != 2:
            raise LogicRuleError("ImpElim requires exactly two nodes (A→B and A)")

    def apply(self) -> Node:
        implication,antecedent = self.nodes

        if implication.value != LogicSymbol.IMPLIES.value or implication.left is None or implication.right is None:
            raise LogicRuleError("First node must be an implication (→) with left and right children")

        if not self._nodes_equal(implication.left, antecedent):
            raise LogicRuleError("Second node must match the antecedent of the implication")

        return implication.right


class NegElim(LogicRule):
    """¬e: From A and ¬A, infer contradiction (⊥)"""

    def _validate_input(self) -> None:
        if len(self.nodes) != 2:
            raise LogicRuleError("NegElim requires exactly two nodes (A and ¬A)")

    def apply(self) -> Node:
        node1, node2 = self.nodes

        # Check if we have A and ¬A in either order
        if node1.value != LogicSymbol.NOT.value and node2.value == LogicSymbol.NOT.value:
            positive_node, negative_node = node1, node2
        elif node1.value == LogicSymbol.NOT.value and node2.value != LogicSymbol.NOT.value:
            negative_node, positive_node = node1, node2
        else:
            raise LogicRuleError("NegElim requires one positive and one negative node")

        if negative_node.left is None or not self._nodes_equal(positive_node, negative_node.left):
            raise LogicRuleError("Nodes must be A and ¬A")

        return Node(LogicSymbol.CONTRADICTION.value)


class DoubleNegElim(LogicRule):
    """¬¬e: From ¬¬A, infer A"""

    def _validate_input(self) -> None:
        if len(self.nodes) != 1:
            raise LogicRuleError("DoubleNegElim requires exactly one node (¬¬A)")

    def apply(self) -> Node:
        double_neg_node = self.nodes[0]

        if double_neg_node.value != LogicSymbol.NOT.value or double_neg_node.left is None:
            raise LogicRuleError("Input must be a negation (¬) node")

        inner_node = double_neg_node.left

        if inner_node.value != LogicSymbol.NOT.value or inner_node.left is None:
            raise LogicRuleError("Input must be a double negation (¬¬A)")

        return inner_node.left


class ModusTollens(LogicRule):
    """MT: From A → B and ¬B, infer ¬A"""

    def _validate_input(self) -> None:
        if len(self.nodes) != 2:
            raise LogicRuleError("ModusTollens requires exactly two nodes (A→B and ¬B)")

    def apply(self) -> Node:
        implication, negated_consequent = self.nodes

        if implication.value != LogicSymbol.IMPLIES.value or implication.left is None or implication.right is None:
            raise LogicRuleError("First node must be an implication (→) with left and right children")

        if negated_consequent.value != LogicSymbol.NOT.value or negated_consequent.left is None:
            raise LogicRuleError("Second node must be a negation (¬B)")

        if not self._nodes_equal(negated_consequent.left, implication.right):
            raise LogicRuleError("Negation must be of the consequent of the implication")

        negated_antecedent = Node(LogicSymbol.NOT.value)
        negated_antecedent.left = implication.left
        return negated_antecedent


class DoubleNegIntro(LogicRule):
    """¬¬i: From A, infer ¬¬A"""

    def _validate_input(self) -> None:
        if len(self.nodes) != 1:
            raise LogicRuleError("DoubleNegIntro requires exactly one node (A)")

    def apply(self) -> Node:
        original_node = self.nodes[0]

        inner_negation = Node(LogicSymbol.NOT.value)
        inner_negation.left = original_node

        outer_negation = Node(LogicSymbol.NOT.value)
        outer_negation.left = inner_negation

        return outer_negation


class InputParser:
    """Handles parsing of input data"""

    def __init__(self):
        self.phase1 = Phase1()

    def parse_input(self, input_data: str) -> tuple[List[LogicLine], str, List[int]]:
        """Parse input data into logic lines, rule name, and line numbers"""
        lines = input_data.strip().split('\n')

        if not lines:
            raise ValueError("Empty input")

        # Parse logic lines (all but the last line)
        logic_lines = []
        for line in lines[:-1]:
            if not line.strip():
                continue

            parts = line.split('    ')  # 4 spaces
            if len(parts) != 2:
                raise ValueError(f"Invalid line format: {line}")

            try:
                line_number = int(parts[0])
                formula_str = parts[1]
                formula_node = self.phase1.parse_tree(formula_str)
                logic_lines.append(LogicLine(line_number, formula_node))
            except ValueError as e:
                raise ValueError(f"Error parsing line {line}: {e}")

        # Parse rule line (last line)
        rule_parts = lines[-1].split(',')
        if not rule_parts:
            raise ValueError("Missing rule specification")

        rule_name = rule_parts[0].strip()

        try:
            line_numbers = [int(num.strip()) for num in rule_parts[1:]]
        except ValueError:
            raise ValueError("Invalid line numbers in rule specification")

        return logic_lines, rule_name, line_numbers

class Phase4(BasePhase):
    """
    Phase 4: Logic Rule Application

    This phase takes logic formulas and a rule name, checks if the rule
    can be applied to the given lines, and either returns the new formula
    or indicates that the rule cannot be applied.
    """

    RULE_CANNOT_BE_APPLIED = "Rule Cannot Be Applied"

    def __init__(self, input_filepath: Optional[str] = None):
        super().__init__(input_filepath)
        self.logic_rule_map: Dict[str, Type[LogicRule]] = {
            "∧i": AndIntro,
            "∧e1": AndElimLeft,
            "∧e2": AndElimRight,
            "→e": ImpElim,
            "¬e": NegElim,
            "¬¬e": DoubleNegElim,
            "MT": ModusTollens,
            "¬¬i": DoubleNegIntro,
        }
        self.parser = InputParser()
        self.phase2 = Phase2()

    def process(self, input_data: str) -> str:
        """
        Process the input data and apply the specified logic rule

        Args:
            input_data: The input text containing formulas and rule specification

        Returns:
            The resulting formula as a string, or error message
        """
        try:
            logic_lines, rule_name, line_numbers = self.parser.parse_input(input_data)

            # Get the rule class
            rule_class = self.logic_rule_map.get(rule_name)
            if rule_class is None:
                return self.RULE_CANNOT_BE_APPLIED

            # Get the formulas for the specified line numbers
            formulas = self._get_formulas_for_lines(logic_lines, line_numbers)

            # Apply the rle
            rule = rule_class(formulas, rule_name)
            result = rule.apply()

            # Convert resultback to string
            return self.phase2.tree_to_string(result)

        except (ValueError, LogicRuleError, Exception):
            return self.RULE_CANNOT_BE_APPLIED

    @staticmethod
    def _get_formulas_for_lines(logic_lines: List[LogicLine], line_numbers: List[int]) -> List[Node]:
        """Extract formulas for the specifed line numbers"""
        line_map = {line.line_number: line.formula for line in logic_lines}

        formulas = []
        for line_num in line_numbers:
            if line_num not in line_map:
                raise ValueError(f"Line number {line_num} not found")
            formula = line_map[line_num]
            if formula is None:
                raise ValueError(f"No formula found for line {line_num}")
            formulas.append(formula)

        return formulas
