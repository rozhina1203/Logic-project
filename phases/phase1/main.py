
from phases.phase1.logic import Phase1

# This block allows running Phase 1 independently for testing or specific execution
if __name__ == "__main__":
    import sys

    # For independent execution, allow user to specify input file
    # Example usage: python phases/phase1/main.py path/to/your/input.txt
    if len(sys.argv) > 1:
        input_file_path = sys.argv[1]
    else:
        # Prompt for input if no argument is provided
        input_file_path = input("Enter input file path for Phase 1: ")

    phase = Phase1(input_file_path)
    phase.run()
    print("Phase 1 independent run completed. Check output file.")
