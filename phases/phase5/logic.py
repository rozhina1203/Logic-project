from typing import List, Optional, Dict, Type, Union, Tuple
from abc import ABC, abstractmethod
from dataclasses import dataclass

from phases.base_phase import BasePhase
from phases.phase1.logic import Node, Phase1
from phases.phase4.logic import LogicRuleError, LogicSymbol, AndIntro, AndElimRight, AndElimLeft, ImpElim, NegElim, DoubleNegElim, ModusTollens, DoubleNegIntro, Phase4

@dataclass
class LogicLine:
    line_number: Optional[int] #none for beginscope/endscope
    formula: Optional[Node]
    rule_name: Optional[str]
    refs: List[Union[int, Tuple[int, int]]]
    indent: int

class LogicRule(ABC):
    """Abstract base class for all logic rules"""

    def __init__(self, nodes: List[Node], rule_name: str = None):
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

class OrIntroLeft(LogicRule):
    """∨i1: Combine statements A into a disjunction (A ∨ B)."""

    def _validate_input(self):
        if len(self.nodes) != 2:
            raise LogicRuleError("OrIntro needs exactly two node!")

    def apply(self) -> Node:
        left_node, right_node = self.nodes
        disjunction = Node(LogicSymbol.OR.value)
        disjunction.left = left_node
        disjunction.right = right_node
        return disjunction
    
class OrIntroRight(LogicRule):
    """∨i2: Combine statement B into a disjunction (A ∨ B)."""

    def _validate_input(self):
        if len(self.nodes) != 2:
            raise LogicRuleError("OrIntro needs exactly two node!")
        
    def apply(self) -> Node:
        left_node, right_node = self.nodes
        disjunction = Node(LogicSymbol.OR.value)
        disjunction.left = left_node
        disjunction.right = right_node
        return disjunction
    
class OrElim(LogicRule):
    """∨e: from A ∨ B, A ⊢ C and B ⊢ c derive C."""

    def _validate_input(self):
        if len(self.nodes) != 3:
            raise LogicRuleError("OrElim needs exactly three nodes!")
        
        
        
    def apply(self) -> Node:
        or_node, c1, c2 = self.nodes
        if or_node.value != LogicSymbol.OR.value:
            raise LogicRuleError("First node must be a disjunction!")
        
        if not self._nodes_equal(c1, c2):
            raise LogicRuleError("The conclusion from both branches must be the same!")
        
        return c1
    
class ImpIntro(LogicRule):
    """→i: if we can derive B from A we can conclude A → B."""

    def _validate_input(self):
        if len(self.nodes) != 2:
            raise LogicRuleError("ImpIntro needs exactly two nodes!")
        
    def apply(self) -> Node:
        left_node, right_node = self.nodes
        Implication = Node(LogicSymbol.IMPLIES.value)
        Implication.left = left_node
        Implication.right = right_node
        return Implication
    
class FalseElim(LogicRule):
    """⊥e: From contradiction, derive any proposition."""

    def _validate_input(self):
        if len(self.nodes) != 2:
            raise LogicRuleError("FalseElim needs exactly two nodes!")
        
    def apply(self) -> Node:
        contradiction, target = self.nodes
        if contradiction.value != LogicSymbol.CONTRADICTION.value:
            raise LogicRuleError("First node must be '⊥'")
        
        return target
    
class PBC(LogicRule):
    """PBC: If assuming ¬A leads to ⊥ then infer A. """

    def _validate_input(self):
        if len(self.nodes) != 2:
            raise LogicRuleError("PBC needs exactly two nodes!")
        
    def apply(self) -> Node:
        false_assumption, contradiction = self.nodes
        
        if false_assumption.value != LogicSymbol.NOT.value:
            raise LogicRuleError("First node must be ¬A!")
        
        if contradiction.value != LogicSymbol.CONTRADICTION.value:
            raise LogicRuleError("Second node must be ⊥!")
        return Node(false_assumption.left)
        
class LEM(LogicRule):
    """LEM: Infer A ∨ ¬A without premises."""

    def _validate_input(self):
        if len(self.nodes) != 1:
            raise LogicRuleError("LEM needs only one node!")
    
    def apply(self) -> Node:
        a = self.nodes[0]
        not_a = Node(LogicSymbol.NOT.value)
        not_a.left = a

        disjunction = Node(LogicSymbol.OR.value)
        disjunction.left = a
        disjunction.right = not_a
        
        return disjunction
    
class CopyRule(LogicRule):
    """Copy: repeat a formula from another line."""
    def _validate_input(self):
        if len(self.nodes) != 1:
            raise ValueError("Copy rule requires exactly one input!")

    def apply(self) -> Node:
        return self.nodes[0]
    
class Assumption(LogicRule):
    """Assumption: A formula assumed within a scope."""
    def _validate_input(self):
        if len(self.nodes) != 0:
            raise LogicRuleError("Assumption doesn't need input nodes")
    
    def apply(self) -> Node:
        raise LogicRuleError("Assumption cannot be applied directly")

class NaturalDeductionParser:
    def __init__(self):
        self.phase1 = Phase1() 
    
    def parse(self, input_data: str) -> List[LogicLine]:
        result = []
        lines = input_data.strip().split('\n')
        
        for line in lines:
            if not line.strip():
                continue

            indent = 0
            while line.startswith('  '):
                indent += 1
                line = line[2:]

            line = line.strip()

            if line in ['BeginScope', 'EndScope']:
                result.append(LogicLine(None, None, line, [], indent))
                continue

            parts = [p.strip() for p in line.split('    ') if p.strip()]
            if len(parts) < 3:
                raise ValueError(f"Invalid line format: '{line}'")

            try:
                line_number = int(parts[0])
                formula_str = parts[1]
                rule_part = parts[2]

                node = self.phase1.parse_tree(formula_str)

                if ',' in rule_part:
                    rule_name, *refs = [x.strip() for x in rule_part.split(',')]
                    processed_refs = []
                    for ref in refs:
                        if '-' in ref:
                            start, end = map(int, ref.split('-'))
                            processed_refs.append((start, end))
                        else:
                            processed_refs.append(int(ref))
                else:
                    rule_name = rule_part
                    processed_refs = []

                result.append(LogicLine(line_number, node, rule_name, processed_refs, indent))

            except Exception as e:
                raise ValueError(f"Error parsing line '{line}': {str(e)}")

        return result
        
def rule_name_to_class(name: str) -> Optional[Type[LogicRule]]:
    return{
        "Premise": None,
        "Assumption": Assumption,
        "∧i": AndIntro,
        "∧e1": AndElimLeft,
        "∧e2": AndElimRight,
        "→e": ImpElim,
        "¬e": NegElim,
        "¬¬e": DoubleNegElim,
        "MT": ModusTollens,
        "¬¬i": DoubleNegIntro,
        "Copy": CopyRule,
        "∨i1": OrIntroLeft,
        "∨i2": OrIntroRight,
        "∨e": OrElim,
        "→i": ImpIntro,
        "⊥e": FalseElim,
        "PBC": PBC,
        "LEM": LEM
    }.get(name)
    
class Phase5(BasePhase):
    """
    In this phase, the program reads all lines of a full logic proof.
    It checks that each line follows the rules.
    If everything is oky, it prints: "Valid Deduction".
    If there is amistake, it prints: "Invalid Deduction at Line X".

    Input:
        - Many lines. Each line has:
            - Line number (except scope lines)
            - A formula
            - A rule and used lines
        - Scope starts and ends with:
            - BeginScope
            - EndScope
        - Scope is shown using 2 spaces each level

    What needs to be done:
        - Read lines and formulas
        - Keep track of scopes and assumptins
        - Check each rule and if it uses correct lines
        - Return result
    """

    def process(self, input_data: str) -> str:
        """
        Do the main job for this phase.
        Check every line and rule in the proof.

        input_data: all the proof text
        return: "Valid Deduction" or "Invalid Deduction at Line X"
        """
        parser = NaturalDeductionParser()
        try:
            lines = parser.parse(input_data)
        except Exception as e:
            return f"Invalid input format: {e}"

        line_map = {line.line_number: line for line in lines if line.line_number is not None}
        valid_lines = set()
        scope_stack = [set()] 

        # Initialize premises
        for num, line in line_map.items():
            if line.rule_name == "Premise":
                valid_lines.add(num)
                scope_stack[0].add(num)

        for line in lines:
            if line.line_number is None:
                if line.rule_name == "BeginScope":
                    scope_stack.append(set())
                elif line.rule_name == "EndScope":
                    if len(scope_stack) <= 1:
                        return "Invalid Deduction: unmatched EndScope"
                    scope_stack.pop()
                continue

            if line.rule_name in ["Premise", "Assumption"]:
                if line.rule_name == "Assumption":
                    scope_stack[-1].add(line.line_number)
                    valid_lines.add(line.line_number)
                continue

            rule_class = rule_name_to_class(line.rule_name)
            if not rule_class:
                return f"Invalid Deduction at Line {line.line_number}: Rule '{line.rule_name}' not defined"

            try:
                input_nodes = []
                for ref in line.refs:
                    if isinstance(ref, int):
                        if ref not in valid_lines:
                            return f"Invalid Deduction at Line {line.line_number}: Reference to invalid line {ref}"
                        input_nodes.append(line_map[ref].formula)
                    elif isinstance(ref, tuple):
                        start, end = ref
                        for i in range(start, end + 1):
                            if i not in valid_lines:
                                return f"Invalid Deduction at Line {line.line_number}: Reference to invalid line {i}"
                            input_nodes.append(line_map[i].formula)

                rule = rule_class(nodes=input_nodes)
                expected_node = rule.apply()

                if not rule._nodes_equal(expected_node, line.formula):
                    return f"Invalid Deduction at Line {line.line_number}: Result mismatch"

                scope_stack[-1].add(line.line_number)
                valid_lines.add(line.line_number)

            except LogicRuleError as e:
                return f"Invalid Deduction at Line {line.line_number}: {str(e)}"
            except Exception as e:
                return f"Invalid Deduction at Line {line.line_number}: Unexpected error - {str(e)}"

        return "Valid Deduction"
