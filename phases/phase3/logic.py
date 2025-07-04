# phases/phase3/main.py

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

        Args:
            input_data (str): The Horn propositional logic formula as a string.

        Returns:
            str: "Satisfiable\n[list of true variables]" or "Unsatisfiable" or "Invalid Horn Formula".
        """
        print("Initiating Horn SAT Protocol...")

        # --- TEAMMATE: Your actual Phase 3 logic goes here ---
        try:
            is_satisfiable, assignment_or_message = True, "[list of true variables]"

            input_data = input_data.replace(' ','')
            current = ''
            open_parens = 0
            n = len(input_data)
            clauses_list = []
            clauses = []
            variables = set()
            i = 0
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
                    
                    if a not in ['⊤', '⊥']:
                        variables.add(a)
                
                if consequent != '⊥' and consequent != '⊤' and not consequent.isalpha():
                    raise ValueError
                if consequent not in ['⊤', '⊥']:
                    variables.add(consequent)
                
                clauses.append((antecedents, consequent))

            #forward chaining algorithm
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
                        if consequent not in true_vars:
                            true_vars.add(consequent)
                            changed = True

            assignment_or_message = true_vars
            
            if is_satisfiable:
                if assignment_or_message:
                    # If satisfiable and there's an assignment, print it nicely.
                    # Otherwise, just "Satisfiable" if no variables became true.
                    return f"Satisfiable\n{assignment_or_message}"
                else:
                    return "Satisfiable"  # Horn formula satisfiable with no true variables
            else:
                return "Unsatisfiable"  # The formula decided it just wasn't feeling it today.

        except ValueError as e:
            return f"Invalid Horn Formula: {e}"
        except Exception as e:
            return f"An unexpected error occurred during Horn solving: {e}"
