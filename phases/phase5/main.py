import sys

from phases.phase5.logic import Phase5

if __name__ == "__main__":

    # For independent execution, allow user to specify input file
    # Example usage: python phases/phase5/main.py path/to/your/input.txt
    if len(sys.argv) > 1:
        input_file_path = sys.argv[1]
    else:
        input_file_path = input("Enter input file path for Phase 5: ")

    phase = Phase5(input_file_path)
    phase.run()
    print("Phase 5 independent run completed.")
