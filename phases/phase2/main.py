from phases.phase2.logic import Phase2

# This block allows running Phase 2 independently
if __name__ == "__main__":
    import sys

    # For independent execution, allow user to specify input file
    # Example usage: python phases/phase2/main.py path/to/your/input.txt
    if len(sys.argv) > 1:
        input_file_path = sys.argv[1]
    else:
        input_file_path = input("Enter input file path for Phase 2: ")

    phase = Phase2(input_file_path)
    phase.run()
    print("Phase 2 independent run completed. Check output file.")
