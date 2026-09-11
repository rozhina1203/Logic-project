from typing import List, Optional, Type, Union, Tuple
from abc import ABC, abstractmethod
from dataclasses import dataclass

from phases.base_phase import BasePhase
from phases.phase1.logic import Node, Phase1
from phases.phase4.logic import LogicRuleError, LogicSymbol, AndIntro, AndElimRight, AndElimLeft, ImpElim, NegElim, \
    DoubleNegElim, ModusTollens, DoubleNegIntro


@dataclass
class LogicLine:
    line_number: Optional[int]  # None for BeginScope/EndScope lines
    formula: Optional[Node]
    rule_name: Optional[str]
    refs: List[Union[int, Tuple[int, int]]]
    indent: int


class LogicRule(ABC):
    """
    Abstract base class for the rules added in Phase 5.
    Unlike the Phase 4 base class, node equality here treats ∧ and ∨ as commutative.
    """

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
        """Check if two nodes are structurally equal,
           accounting for commutativity of ∨ and ∧."""
        if node1.value != node2.value:
            return False

        def eq(n1, n2):
            if n1 is None and n2 is None:
                return True
            if n1 is None or n2 is None:
                return False
            return self._nodes_equal(n1, n2)

        if node1.value in {"∨", "∧"}:
            direct = eq(node1.left, node2.left) and eq(node1.right, node2.right)
            swapped = eq(node1.left, node2.right) and eq(node1.right, node2.left)
            return direct or swapped

        return eq(node1.left, node2.left) and eq(node1.right, node2.right)


class OrIntroLeft(LogicRule):
    """∨i1: From A, infer A ∨ B."""

    def _validate_input(self):
        if len(self.nodes) != 2:
            raise LogicRuleError("OrIntroLeft needs exactly two nodes (premise and target disjunction)")

    def apply(self) -> Node:
        premise, target_disjunction = self.nodes

        if target_disjunction.value != LogicSymbol.OR.value:
            raise LogicRuleError("Target must be a disjunction")

        if (target_disjunction.left is not None and
                self._nodes_equal(premise, target_disjunction.left)):
            return target_disjunction
        else:
            raise LogicRuleError("Premise must match left disjunct of target")


class OrIntroRight(LogicRule):
    """∨i2: From B, infer A ∨ B."""

    def _validate_input(self):
        if len(self.nodes) != 2:
            raise LogicRuleError("OrIntroRight needs exactly two nodes (premise and target disjunction)")

    def apply(self) -> Node:
        premise, target_disjunction = self.nodes

        if target_disjunction.value != LogicSymbol.OR.value:
            raise LogicRuleError("Target must be a disjunction")

        if (target_disjunction.right is not None and
                self._nodes_equal(premise, target_disjunction.right)):
            return target_disjunction
        else:
            raise LogicRuleError("Premise must match right disjunct of target")

class OrElim(LogicRule):
    """∨e: From A ∨ B, A ⊢ C and B ⊢ C, derive C."""

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
    """→i: if we can derive B from (A) we can conclude A → B."""

    def _validate_input(self):
        if len(self.nodes) != 2:
            raise LogicRuleError("ImpIntro needs exactly two nodes!")

    def apply(self) -> Node:
        left_node, right_node = self.nodes
        implication = Node(LogicSymbol.IMPLIES.value)
        implication.left = left_node
        implication.right = right_node
        return implication


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
        return false_assumption.right


class NegIntro(LogicRule):
    """¬i: If assuming A leads to ⊥ then infer ¬A."""

    def _validate_input(self):
        if len(self.nodes) != 2:
            raise LogicRuleError("NegIntro needs exactly two nodes!")

    def apply(self) -> Node:
        assumption, contradiction = self.nodes

        if contradiction.value != LogicSymbol.CONTRADICTION.value:
            raise LogicRuleError("Second node must be ⊥!")

        negation = Node(LogicSymbol.NOT.value)
        negation.right = assumption
        return negation


class LEM(LogicRule):
    """LEM: Infer A ∨ ¬A without premises."""

    def _validate_input(self):
        if len(self.nodes) != 1:
            raise LogicRuleError("LEM needs only one node!")

    def apply(self) -> Node:
        a = self.nodes[0]
        not_a = Node(LogicSymbol.NOT.value)
        not_a.right = a

        disjunction = Node(LogicSymbol.OR.value)
        disjunction.left = a
        disjunction.right = not_a

        return disjunction


class CopyRule(LogicRule):
    """Copy: repeat a formula from another line."""

    def _validate_input(self):
        if len(self.nodes) != 1:
            raise LogicRuleError("Copy rule requires exactly one input!")

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
    return {
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
        "¬i": NegIntro,
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
    Phase 5: Natural Deduction Proof Verification

    Reads a complete natural deduction proof and checks that every line follows
    from the rule it cites. Returns "Valid Deduction" if all lines are correct,
    or "Invalid Deduction at Line X" for the first line that is not.

    Input:
        - One proof step per line: line number, formula, and the rule with the
          lines it uses, e.g. "3    p ∧ q        ∧i, 1, 2"
        - A box (sub-proof) starts with BeginScope and ends with EndScope
        - Each scope level is indented by 2 more spaces
        - Once a scope is closed, its lines can only be referenced as a whole
          box (e.g. "→i, 3-5"), not one by one
    """

    def process(self, input_data: str) -> str:
        """
        Checks every line of the proof against the rule it cites.

        Args:
            input_data (str): The full proof text.

        Returns:
            str: "Valid Deduction", "Invalid Deduction at Line X",
                 or an error message if the input cannot be parsed.
        """
        parser = NaturalDeductionParser()
        try:
            lines = parser.parse(input_data)
        except Exception as e:
            return f"Invalid input format: {e}"

        line_map = {line.line_number: line for line in lines if line.line_number is not None}

        # Every line checked so far, including the lines of scopes that are already closed
        valid_lines = set()
        # One set of line numbers per open scope. A single line can only be referenced
        # while the scope it belongs to is still open.
        scope_stack = [set()]

        # Premises are available everywhere in the proof
        for num, line in line_map.items():
            if line.rule_name == "Premise":
                valid_lines.add(num)
                scope_stack[0].add(num)

        def is_accessible(ref) -> bool:
            return isinstance(ref, int) and any(ref in scope for scope in scope_stack)

        for line in lines:
            if line.line_number is None:
                if line.rule_name == "BeginScope":
                    scope_stack.append(set())
                elif line.rule_name == "EndScope":
                    if len(scope_stack) <= 1:
                        return "Invalid Deduction: unmatched EndScope"
                    scope_stack.pop()
                continue

            if line.rule_name == "Premise":
                continue

            if line.rule_name == "Assumption":
                scope_stack[-1].add(line.line_number)
                valid_lines.add(line.line_number)
                continue

            invalid = f"Invalid Deduction at Line {line.line_number}"

            rule_class = rule_name_to_class(line.rule_name)
            if not rule_class:
                return invalid

            try:
                # LEM - Law of Excluded Middle (uses no other lines)
                if line.rule_name == "LEM":
                    if len(line.refs) != 0:
                        return invalid

                    expected_formula = line.formula
                    if expected_formula.value != LogicSymbol.OR.value:
                        return invalid

                    # Format: A ∨ ¬A
                    if (expected_formula.right is not None and
                            expected_formula.right.value == LogicSymbol.NOT.value and
                            expected_formula.right.right is not None and
                            self.nodes_equal(expected_formula.left, expected_formula.right.right)):
                        proposition = expected_formula.left
                    # Format: ¬A ∨ A
                    elif (expected_formula.left is not None and
                          expected_formula.left.value == LogicSymbol.NOT.value and
                          expected_formula.left.right is not None and
                          self.nodes_equal(expected_formula.left.right, expected_formula.right)):
                        proposition = expected_formula.right
                    else:
                        return invalid

                    rule = rule_class(nodes=[proposition], rule_name=line.rule_name)

                # →i, ¬i, PBC - discharge a box "start-end" that begins with an assumption
                elif line.rule_name in ("→i", "¬i", "PBC"):
                    if len(line.refs) != 1 or not isinstance(line.refs[0], tuple):
                        return invalid

                    start, end = line.refs[0]
                    if start not in line_map or end not in line_map:
                        return invalid

                    if line_map[start].rule_name != "Assumption":
                        return invalid

                    if any(i not in valid_lines for i in range(start, end + 1)):
                        return invalid

                    assumption_node = line_map[start].formula
                    conclusion_node = line_map[end].formula
                    rule = rule_class(nodes=[assumption_node, conclusion_node], rule_name=line.rule_name)

                # ⊥e, ∨i1, ∨i2 - one referenced line. The formula on this line is passed in too,
                # because it cannot be built from the referenced line alone.
                elif line.rule_name in ("⊥e", "∨i1", "∨i2"):
                    if len(line.refs) != 1 or not is_accessible(line.refs[0]):
                        return invalid

                    premise_node = line_map[line.refs[0]].formula
                    rule = rule_class(nodes=[premise_node, line.formula], rule_name=line.rule_name)

                # ∨e - Or Elimination: "∨e, disjunction, box1, box2"
                elif line.rule_name == "∨e":
                    if len(line.refs) != 3:
                        return invalid

                    disjunction_ref, box1, box2 = line.refs
                    if not is_accessible(disjunction_ref):
                        return invalid

                    if not isinstance(box1, tuple) or not isinstance(box2, tuple):
                        return invalid

                    start1, end1 = box1
                    start2, end2 = box2

                    if not (start1 < end1 < start2 < end2 < line.line_number):
                        return invalid

                    if (start1 not in line_map or end1 not in line_map or
                            start2 not in line_map or end2 not in line_map):
                        return invalid

                    if (line_map[start1].rule_name != "Assumption" or
                            line_map[start2].rule_name != "Assumption"):
                        return invalid

                    disjunction_node = line_map[disjunction_ref].formula
                    if disjunction_node.value != LogicSymbol.OR.value:
                        return invalid

                    assumption1 = line_map[start1].formula
                    assumption2 = line_map[start2].formula
                    left_disjunct = disjunction_node.left
                    right_disjunct = disjunction_node.right

                    if not ((self.nodes_equal(assumption1, left_disjunct) and
                             self.nodes_equal(assumption2, right_disjunct)) or
                            (self.nodes_equal(assumption1, right_disjunct) and
                             self.nodes_equal(assumption2, left_disjunct))):
                        return invalid

                    if line_map[start2].indent > line_map[start1].indent:
                        return invalid

                    conclusion1 = line_map[end1].formula
                    conclusion2 = line_map[end2].formula
                    rule = rule_class(nodes=[disjunction_node, conclusion1, conclusion2], rule_name=line.rule_name)

                # ∧e1, ∧e2, ¬¬e, ¬¬i, Copy - one referenced line
                elif line.rule_name in ("∧e1", "∧e2", "¬¬e", "¬¬i", "Copy"):
                    if len(line.refs) != 1 or not is_accessible(line.refs[0]):
                        return invalid

                    input_node = line_map[line.refs[0]].formula
                    rule = rule_class(nodes=[input_node], rule_name=line.rule_name)

                # ∧i, →e, ¬e, MT - two referenced lines
                elif line.rule_name in ("∧i", "→e", "¬e", "MT"):
                    if len(line.refs) != 2 or not all(is_accessible(ref) for ref in line.refs):
                        return invalid

                    input_nodes = [line_map[ref].formula for ref in line.refs]
                    rule = rule_class(nodes=input_nodes, rule_name=line.rule_name)

                # Unknown rule
                else:
                    return invalid

                expected_node = rule.apply()

                if not rule._nodes_equal(expected_node, line.formula):
                    return invalid

                scope_stack[-1].add(line.line_number)
                valid_lines.add(line.line_number)

            except Exception:
                return invalid

        return "Valid Deduction"

    def nodes_equal(self, node1: Node, node2: Node) -> bool:
        if node1 is None and node2 is None:
            return True
        if node1 is None or node2 is None:
            return False
        if node1.value != node2.value:
            return False

        left_equal = self.nodes_equal(node1.left, node2.left)
        right_equal = self.nodes_equal(node1.right, node2.right)

        return left_equal and right_equal
