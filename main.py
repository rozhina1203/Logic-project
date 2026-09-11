# main.py
from pathlib import Path

from phases.phase1.logic import Phase1
from phases.phase2.logic import Phase2
from phases.phase3.logic import Phase3
from phases.phase4.logic import Phase4
from phases.phase5.logic import Phase5

# Dictionary to map choice numbers to their respective Phase classes
PHASE_CLASSES = {
    1: Phase1,
    2: Phase2,
    3: Phase3,
    4: Phase4,
    5: Phase5,
}


def show_menu():
    """Displays the main menu options to the user."""
    print("\n--- Propositional Logic Solver ---")
    print("1. Phase 1: Check WFF & Generate Parse Tree")
    print("2. Phase 2: Convert Formula to CNF")
    print("3. Phase 3: Horn SAT Solver")
    print("4. Phase 4: Apply Natural Deduction Rule")
    print("5. Phase 5: Verify Natural Deduction")
    print("0. Exit")


def get_input_file_path(phase_number: int) -> str:
    """
    Returns the default input file for a phase: 'data/phase<N>_input.txt' at the project root.
    To run a phase on a different file, use its standalone entry point instead,
    e.g. `python -m phases.phase1.main path/to/input.txt`.
    """
    project_root = Path(__file__).parent
    default_filename = f"phase{phase_number}_input.txt"  # e.g., phase1_input.txt
    return str(project_root / "data" / default_filename)


def main():
    """Main function to run the propositional logic solver with a menu."""
    while True:
        show_menu()
        choice = input("Enter your choice (number or '0' to exit): ").strip()

        if choice == '0':
            print("Exiting application. Goodbye!")
            break

        try:
            choice_int = int(choice)
            if choice_int not in PHASE_CLASSES:
                print("Invalid choice. Please enter a number from the menu.")
                continue

            input_file = get_input_file_path(choice_int)
            phase_instance = PHASE_CLASSES[choice_int](input_file)
            phase_instance.run()

            print("Operation completed for the selected phase.")

        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
