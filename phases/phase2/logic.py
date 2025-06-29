from ..base_phase import BasePhase


class Phase2(BasePhase):
    """
    Implements Phase 2: Conversion of a Well-Formed Formula (WFF) to Conjunctive Normal Form (CNF).
    """

    def process(self, input_data: str) -> str:
        """
        Processes the input WFF and converts it to its equivalent CNF.
        This method assumes the input is a valid WFF and performs the following steps:
        1. Eliminate implications (→) using ¬ and ∨.
        2. Move negations inwards using De Morgan's laws.
        3. Apply the distributive law to convert to CNF.
        4. Simplify the formula (optional, can be enhanced).
        Args:
            input_data (str): The propositional logic formula as a string (assumed to be WFF).
        Returns:
            str: The formula in CNF format.
        """
        # Remove whitespace
        formula = input_data.replace(" ", "")

        # Step 1: Eliminate implications
        formula = self._eliminate_implications(formula)

        # Step 2: Move negations inwards using De Morgan's laws
        formula = self._move_negations_inwards(formula)

        # Step 3: Apply distributive law to get CNF
        formula = self._apply_distributive_law(formula)

        # Step 4: Simplify the formula (optional)
        formula = self._simplify_cnf(formula)

        return formula

    def _eliminate_implications(self, formula: str) -> str:
        """Replace all implications (→) with equivalent forms using ¬ and ∨."""
        while "→" in formula:
            # Find the rightmost implication to handle nesting correctly
            # Iter1) (A → (B → ¬C)) should be retained as 5, because we process from the right.
            # Iter2) (A → (¬B ∨ ¬C)) should be retained as 2, because we process from the right.
            """Apply De Morgan's laws to push negations inwards and eliminate double negations."""
            imp_index = formula.rfind("→")

            # Find the left and right operands
            # Iter1) (A → (B → ¬C)): left: B, right: ¬C
            # Iter2) (A → (¬B ∨ ¬C)): left: A, right: ¬B ∨ ¬C
            left, right = self._find_operands(formula, imp_index)

            # Replace implication with ¬left ∨ right
            # Iter1) (A → (B → ¬C)) becomes (A → (¬B ∨ ¬C))
            # Iter2) (A → (¬B ∨ ¬C)) becomes (¬A ∨ (¬B ∨ ¬C))
            formula = formula[:imp_index - len(left)] + f"(¬{left}∨{right})" + formula[imp_index + 1 + len(right):]

        return formula

    def _move_negations_inwards(self, formula: str) -> str:
        """
        Apply De Morgan's laws to push negations inwards and eliminate double negations.
        :param formula: The propositional logic formula as a string.
        :return: The formula with negations moved inwards.
        For example:
        - ¬(A ∨ B) becomes ¬A ∧ ¬B
        - ¬(A ∧ B) becomes ¬A ∨ ¬B
        """
        i = 0
        while i < len(formula):  # Iterate through the formula until all negations are processed
            if formula[i] == "¬":
                if formula[i + 1] == "(":
                    # Find the matching closing parenthesis
                    j = i + 2
                    balance = 1
                    while j < len(formula) and balance > 0:
                        if formula[j] == "(":
                            balance += 1
                        elif formula[j] == ")":
                            balance -= 1
                        j += 1

                    sub_expr = formula[i + 2:j - 1]
                    operator = self._find_dominant_operator(sub_expr)

                    if operator == "∨":
                        # ¬(A ∨ B) becomes ¬A ∧ ¬B
                        left, right = self._split_on_operator(sub_expr, "∨")
                        new_sub = f"(¬{left}∧¬{right})"
                        formula = formula[:i] + new_sub + formula[j:]
                        i = 0  # restart after major change
                    elif operator == "∧":
                        # ¬(A ∧ B) becomes ¬A ∨ ¬B
                        left, right = self._split_on_operator(sub_expr, "∧")
                        new_sub = f"(¬{left}∨¬{right})"
                        formula = formula[:i] + new_sub + formula[j:]
                        i = 0  # restart after major change
                elif i + 1 < len(formula) and formula[i + 1] == "¬":
                    # Double negation: remove both
                    formula = formula[:i] + formula[i + 2:]
                    i = 0  # restart after major change
                else:
                    i += 1
            else:
                i += 1
        return formula

    def _apply_distributive_law(self, formula: str) -> str:
        """Apply distributive law to convert to CNF."""
        changed = True
        while changed:
            changed = False
            i = 0
            while i < len(formula):
                if formula[i] == "∨":
                    # Find the operands around this OR
                    left, right = self._find_operands(formula, i)

                    # Check if right operand is an AND
                    if right.startswith("(") and "∧" in right:
                        # A ∨ (B ∧ C) becomes (A ∨ B) ∧ (A ∨ C)
                        # and_index = right.find("∧")
                        right_left, right_right = self._split_on_operator(right, "∧")

                        new_expr = f"(({left}∨{right_left})∧({left}∨{right_right}))"
                        formula = formula[:i - len(left)] + new_expr + formula[i + 1 + len(right):]
                        changed = True
                        break

                    # Check if left operand is an AND
                    elif left.endswith(")") and "∧" in left:
                        # (A ∧ B) ∨ C becomes (A ∨ C) ∧ (B ∨ C)
                        # and_index = left.find("∧")
                        left_left, left_right = self._split_on_operator(left, "∧")

                        new_expr = f"(({left_left}∨{right})∧({left_right}∨{right}))"
                        formula = formula[:i - len(left)] + new_expr + formula[i + 1 + len(right):]
                        changed = True
                        break

                i += 1
        return formula

    @staticmethod
    def _simplify_cnf(formula: str) -> str:
        """Simplify the CNF formula by removing redundant parentheses and clauses."""
        # This is a basic simplifier - can be enhanced further
        simplified = False
        while not simplified:
            simplified = True
            # Remove unnecessary outer parentheses
            if formula.startswith("(") and formula.endswith(")"):
                # Check if the entire formula is wrapped in parentheses
                balance = 0
                has_outer = True
                for i, c in enumerate(formula):
                    if c == "(":
                        balance += 1
                    elif c == ")":
                        balance -= 1
                        if balance == 0 and i != len(formula) - 1:
                            has_outer = False
                            break
                if has_outer:
                    formula = formula[1:-1]
                    simplified = False

        return formula

    @staticmethod
    def _find_operands(formula: str, op_index: int) -> tuple[str, str]:
        """Find the left and right operands of an operator at the given index."""
        # Find left operand
        left_end = op_index - 1
        if formula[left_end] == ")":
            balance = 1
            left_start = left_end - 1
            while left_start >= 0 and balance > 0:
                if formula[left_start] == ")":
                    balance += 1
                elif formula[left_start] == "(":
                    balance -= 1
                left_start -= 1
            left_start += 1
            left = formula[left_start:left_end + 1]
        else:
            left_start = op_index - 1
            while left_start >= 0 and formula[left_start] not in "()∧∨¬→":
                left_start -= 1
            left = formula[left_start + 1:op_index]

        # Find right operand
        right_start = op_index + 1
        if formula[right_start] == "(":
            balance = 1
            right_end = right_start + 1
            while right_end < len(formula) and balance > 0:
                if formula[right_end] == "(":
                    balance += 1
                elif formula[right_end] == ")":
                    balance -= 1
                right_end += 1
            right = formula[right_start:right_end]
        else:
            right_end = right_start + 1
            while right_end < len(formula) and formula[right_end] not in "()∧∨¬→":
                right_end += 1
            right = formula[right_start:right_end]

        return left, right

    @staticmethod
    def _split_on_operator(formula: str, op: str) -> tuple[str, str]:
        """Split a formula on the given operator, handling parentheses."""
        balance = 0
        for i, c in enumerate(formula):
            if c == "(":
                balance += 1
            elif c == ")":
                balance -= 1
            elif c == op and balance == 0:
                left = formula[:i]
                right = formula[i + 1:]
                return left, right
        return formula, ""

    @staticmethod
    def _find_dominant_operator(formula: str) -> str:
        """Find the top-level operator in a formula (ignoring parentheses)."""
        balance = 0
        for c in formula:
            if c == "(":
                balance += 1
            elif c == ")":
                balance -= 1
            elif balance == 0 and c in ("∧", "∨"):
                return c
        return ""
