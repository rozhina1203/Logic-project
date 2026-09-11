# phases/phase3/logic.py

from ..base_phase import BasePhase

class Phase3(BasePhase):
    """
    Implements Phase 3: Horn Satisfiability Solver.
    This phase takes a Horn formula and checks if it's satisfiable.
    If it is, it finds a satisfying assignment (a list of true variables).
    If not, it declares it unsatisfiable.
    """

    def process(self, input_data: str) -> str:
        """
        Processes the input Horn formula to determine its satisfiability.

        The formula must be a conjunction of implications, e.g. (⊤ → A) ∧ (A ∧ B → C) ∧ (C → ⊥),
        where each antecedent is a conjunction of variables, ⊤ or ⊥, and each consequent is
        a single variable, ⊤ or ⊥.

        Args:
            input_data (str): The Horn propositional logic formula as a string.

        Returns:
            str: "Satisfiable\n{set of true variables}" or "Unsatisfiable" or "Invalid Horn Formula".
        """
        try:
            input_data = input_data.replace(' ','')
            current = ''
            open_parens = 0
            n = len(input_data)
            clauses_list = []
            clauses = []
            i = 0
            # Split the formula into clauses at every '∧' that is outside parentheses
            while i < n:
                c = input_data[i]
                current += c

                if c == '(':
                    open_parens += 1
                elif c == ')':
                    open_parens -= 1

                if open_parens == 0 and ((i+1 < n and input_data[i+1] == '∧') or i+1 == n):
                    clauses_list.append(current.strip('()'))
                    current = ''
                    i += 1
                i += 1

            for clause in clauses_list:
                if '∧' not in clause and '→' not in clause:
                    raise ValueError

                parts = clause.split('→')

                if len(parts) != 2:
                    raise ValueError

                consequent = parts[1]
                antecedents = parts[0].split('∧')
                antecedents = [a for a in antecedents if a != '⊤']

                for a in antecedents:
                    if a != '⊥' and not a.isalpha():
                        raise ValueError

                if consequent != '⊥' and consequent != '⊤' and not consequent.isalpha():
                    raise ValueError

                clauses.append((antecedents, consequent))

            # Forward chaining: repeatedly mark a clause's consequent as true once all of its
            # antecedents are true. If ⊥ becomes true, the formula is unsatisfiable.
            is_satisfiable = True
            true_vars = set()
            changed = True

            while changed:
                changed = False
                for antecedents, consequent in clauses:
                    if consequent in true_vars:
                        continue
                    if all(a in true_vars or a == '⊤' for a in antecedents):
                        if consequent == '⊥':
                            is_satisfiable = False
                        true_vars.add(consequent)
                        changed = True

            # ⊤ can be derived as a consequent, but it is a constant, not a variable
            true_vars.discard('⊤')

            if not is_satisfiable:
                return "Unsatisfiable"
            if not true_vars:
                return "Satisfiable"  # satisfiable with every variable set to false
            # Variables are sorted so the output is the same on every run
            return "Satisfiable\n{" + ", ".join(repr(v) for v in sorted(true_vars)) + "}"

        except ValueError:
            return "Invalid Horn Formula"
        except Exception as e:
            return f"An unexpected error occurred during Horn solving: {e}"
