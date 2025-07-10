# main.py
from pathlib import Path

# Import all specific phase classes
from phases.phase1.logic import Phase1
from phases.phase2.logic import Phase2
from phases.phase3.logic import Phase3
from phases.phase5.main import Phase5

# --- TEAMMATE: Import your other Phase classes here ---
# from phases.phase4.main import Phase4

# Dictionary to map choice numbers to their respective Phase classes
PHASE_CLASSES = {
    1: Phase1,
    2: Phase2,
    3: Phase3,
    5: Phase5,
    # --- TEAMMATE: Add your other Phase classes here ---
    # 4: Phase4,
}


def show_menu():
    """Displays the main menu options to the user."""
    print("\n--- Propositional Logic Solver ---")
    print("1. Phase 1: Check WFF & Generate Parse Tree")
    print("2. Phase 2: Convert Formula to CNF")
    print("3. Phase 3: Horn SAT Solver")
    print("5. Phase 5: Verify Natural Deduction")
    # --- TEAMMATE: Add menu options for your other phases here ---
    # print("4. Phase 4: Apply Natural Deduction Rule")
    print("0. Exit")


def get_input_file_path(phase_number: int) -> str:
    """
    Prompts the user for an input file path and returns it.
    Suggests a default path based on the phase number in the centralized 'data/input/' directory.
    """
    # Construct the default path in the 'data/' directory at the project root
    # __file__ is main.py, .parent takes it to the project root
    project_root = Path(__file__).parent
    default_filename = f"phase{phase_number}_input.txt"  # e.g., phase1_input.txt
    default_path = project_root / "data" / default_filename

    # user_input = input(f"Enter input file path (e.g., {default_path} or just filename): ").strip()
    #
    # # If the user provides just a filename, assume it's in the 'data/' directory
    # if user_input and not Path(user_input).is_absolute():
    #     suggested_path = project_root / "data" / user_input
    #     if suggested_path.exists():
    #         return str(suggested_path)
    #
    # # If the user provides a relative path (e.g., "my_folder/my_file.txt"),
    # # assume it's relative to the project root.
    # if user_input and not Path(user_input).is_absolute():
    #     relative_path = project_root / user_input
    #     if relative_path.exists():
    #         return str(relative_path)

    # Otherwise, use the path as provided or the default if empty
    # return user_input if user_input else str(default_path)
    return str(default_path)

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
