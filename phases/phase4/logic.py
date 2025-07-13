from phases.base_phase import BasePhase

class Phase4(BasePhase):
    """
    In this phase, the program gets a few logic formulas and a rule name.
    It checks if the rule can be used on the given lines.
    If the rule works, it prints the new formula.
    If it does not work, it prints: "Rule Cannot Be Applied".
    """

    def process(self, input_data: str) -> str:
        """
        Do the main job for this phase.
        Get the formulas and rule, and return the result or an error.

        input_data: the full input text
        return: new formula or error message
        """
        return "result"
