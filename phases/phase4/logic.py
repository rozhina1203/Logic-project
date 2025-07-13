from typing import List

from phases.base_phase import BasePhase
from phases.phase1.logic import Node
from abc import ABC, abstractmethod


class Phase4(BasePhase):
    """
    In this phase, the program gets a few logic formulas and a rule name.
    It checks if the rule can be used on the given lines.
    If the rule works, it prints the new formula.
    If it does not work, it prints: "Rule Cannot Be Applied".

    # ∧i  → and_intro()
    # Combine two statements into a conjunction (A ∧ B)

    # ∧e1 → and_elim_left()
    # Extract the left part (A) from a conjunction (A ∧ B)

    # ∧e2 → and_elim_right()
    # Extract the right part (B) from a conjunction (A ∧ B)

    # →e  → imp_elim()
    # Apply implication: from A and A → B, infer B (Modus Ponens)

    # ¬e  → neg_elim()
    # Eliminate contradiction: from A and ¬A, infer contradiction (⊥)

    # ¬¬e → double_neg_elim()
    # Remove double negation: from ¬¬A, infer A

    # MT   → modus_tollens()
    # From A → B and ¬B, infer ¬A

    # ¬¬i → double_neg_intro()
    # Introduce double negation: from A, infer ¬¬A

    """
    def __init__(self):
        super().__init__()
        self.logic_rule_map = {
            "∧i": AndIntro,
            "∧e1": AndElimLeft,
            "∧e2": AndElimRight,
            "→e": ImpElim,
            "¬e": NegElim,
            "¬¬e": DoubleNegElim,
            "MT": ModusTollens,
            "¬¬i": DoubleNegIntro,
        }

    def process(self, input_data: str) -> str:
        """
        Do the main job for this phase.
        Get the formulas and rule, and return the result or an error.

        input_data: the full input text
        return: new formula or error message
        """
        # lines = parse text to LogicLine instances

        return "result"
class LogicRule(ABC):
    def __init__(self, rule_name: str, nodes: List[Node]):
        self.rule_name = rule_name
        self.nodes = nodes

    @abstractmethod
    def do(self) -> Node:
        pass


class AndIntro(LogicRule):
    """
    ∧i
    Combine two statements into a conjunction (A ∧ B)
    """
    def __init__(self, nodes: List[Node], rule_name="∧i"):
        super().__init__(rule_name, nodes)

    def do(self) -> Node:
        if len(self.nodes) != 2:
            raise ValueError("AndIntro requires exactly two nodes.")

        left_node = self.nodes[0]
        right_node = self.nodes[1]

        new_node = Node("∧")
        new_node.left = left_node
        new_node.right = right_node
        return new_node


class AndElimLeft(LogicRule):
    """
    ∧e1
    Extract the left part (A) from a conjunction (A ∧ B)
    """
    def __init__(self, nodes: List[Node], rule_name="∧e1"):
        super().__init__(rule_name, nodes)

    def do(self) -> Node:
        if len(self.nodes) != 1:
            raise ValueError("AndElimLeft requires exactly one node (A ∧ B).")

        conj_node = self.nodes[0]

        if conj_node.value != "∧" or conj_node.left is None:
            raise ValueError("Input node must be a conjunction (∧) with a left child.")

        return conj_node.left


class AndElimRight(LogicRule):
    """
    ∧e2
    Extract the right part (B) from a conjunction (A ∧ B)
    """
    def __init__(self, nodes: List[Node], rule_name="∧e2"):
        super().__init__(rule_name, nodes)

    def do(self) -> Node:
        if len(self.nodes) != 1:
            raise ValueError("AndElimRight requires exactly one node (A ∧ B).")

        conj_node = self.nodes[0]

        if conj_node.value != "∧" or conj_node.right is None:
            raise ValueError("Input node must be a conjunction (∧) with a right child.")

        return conj_node.right


class ImpElim(LogicRule):
    """
    →e (Modus Ponens)
    From A → B and A, infer B
    """
    def __init__(self, nodes: List[Node], rule_name="→e"):
        super().__init__(rule_name, nodes)

    def do(self) -> Node:
        if len(self.nodes) != 2:
            raise ValueError("ImpElim requires exactly two nodes (A→B and A).")

        imp_node, a_node = self.nodes

        if imp_node.value != "→" or imp_node.left is None or imp_node.right is None:
            raise ValueError("First node must be an implication (→) with left and right children.")

        if imp_node.left.value != a_node.value:
            raise ValueError("Second node must match the antecedent (left side) of the implication.")

        return imp_node.right


class NegElim(LogicRule):
    """
    ¬e
    From A and ¬A, infer contradiction (⊥)
    """
    def __init__(self, nodes: List[Node], rule_name="¬e"):
        super().__init__(rule_name, nodes)

    def do(self) -> Node:
        if len(self.nodes) != 2:
            raise ValueError("NegElim requires exactly two nodes (A and ¬A).")

        a_node, not_a_node = self.nodes

        if not_a_node.value != "¬" or not_a_node.left is None:
            raise ValueError("Second node must be a negation node (¬A).")

        if not_a_node.left.value != a_node.value:
            raise ValueError("Second node must be negation of the first node.")

        return Node("⊥")


class DoubleNegElim(LogicRule):
    """
    ¬¬e
    From ¬¬A, infer A
    """
    def __init__(self, nodes: List[Node], rule_name="¬¬e"):
        super().__init__(rule_name, nodes)

    def do(self) -> Node:
        if len(self.nodes) != 1:
            raise ValueError("DoubleNegElim requires exactly one node (¬¬A).")

        double_neg_node = self.nodes[0]

        if double_neg_node.value != "¬" or double_neg_node.left is None:
            raise ValueError("Input node must be a negation (¬) node.")

        inner_node = double_neg_node.left

        if inner_node.value != "¬" or inner_node.left is None:
            raise ValueError("Input node must be a double negation (¬¬A).")

        return inner_node.left


class ModusTollens(LogicRule):
    """
    MT
    From A → B and ¬B, infer ¬A
    """
    def __init__(self, nodes: List[Node], rule_name="MT"):
        super().__init__(rule_name, nodes)

    def do(self) -> Node:
        if len(self.nodes) != 2:
            raise ValueError("ModusTollens requires exactly two nodes (A→B and ¬B).")

        imp_node, not_b_node = self.nodes

        if imp_node.value != "→" or imp_node.left is None or imp_node.right is None:
            raise ValueError("First node must be an implication (→) with left and right children.")

        if not_b_node.value != "¬" or not_b_node.left is None:
            raise ValueError("Second node must be a negation node (¬B).")

        if not_b_node.left.value != imp_node.right.value:
            raise ValueError("Negation must be of the consequent (right side) of implication.")

        not_a_node = Node("¬")

        not_a_node.left = imp_node.left

        return not_a_node


class DoubleNegIntro(LogicRule):
    """
    ¬¬i
    From A, infer ¬¬A
    """
    def __init__(self, nodes: List[Node], rule_name="¬¬i"):
        super().__init__(rule_name, nodes)

    def do(self) -> Node:
        if len(self.nodes) != 1:
            raise ValueError("DoubleNegIntro requires exactly one node (A).")
        a_node = self.nodes[0]
        neg_a = Node("¬")
        neg_a.left = a_node
        double_neg = Node("¬")
        double_neg.left = neg_a
        return double_neg

class LogicLine:
    def __init__(self, line_number: int, formula_node: Node = None, rule: LogicRule = None, is_formula: bool = True):
        self.line_number = line_number
        self.formula = formula_node
        self.rule = rule
        self.is_formula = is_formula  # True if it’s a logic formula line, False if it's a rule line

    def __repr__(self):
        type_str = "Formula" if self.is_formula else "Rule"
        return f"<{type_str} Line {self.line_number}: {self.formula.value}>"
