# phases/phase1/main.py

from ..base_phase import BasePhase

class Phase1(BasePhase):
    """
    Implements Phase 1: Well-Formed Formula (WFF) validation and Parse Tree generation.
    """

    def process(self, input_data: str) -> str:
        """
        Processes the input formula to check if it's a WFF and generates its parse tree.
        Args:
            input_data (str): The propositional logic formula as a string.
        Returns:
            str: "Valid Formula\n[Parse Tree]" or "Invalid Formula".
        """
        # --- TEAMMATE: Your actual Phase 1 logic goes here ---

        is_valid = True
        result_content = "Ha Ha"
        if is_valid:
            return "Valid Formula\n" + result_content
        else:
            return "Invalid Formula"
