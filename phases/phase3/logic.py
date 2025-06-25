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
