import sys

from phases.phase3.logic import Phase3

if __name__ == "__main__":

    # For independent execution, allow user to specify input file
    # Example usage: python phases/phase3/main.py path/to/your/input.txt
    if len(sys.argv) > 1:
        input_file_path = sys.argv[1]
    else:
        input_file_path = input("Enter input file path for Phase 3: ")

    phase = Phase3(input_file_path)
    phase.run()
    print("Phase 3 independent run completed.")
