from phases.base_phase import BasePhase

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
        return "Coming soon... powered by Rozhina :)"
