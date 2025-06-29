# phases/base_phase.py
from pathlib import Path
from abc import ABC, abstractmethod


class BasePhase(ABC):
    """
    Base class for all project phases.
    Defines the common interface for reading input, writing output,
    and a 'process' method that must be implemented by concrete phases.
    """

    def __init__(self, input_filepath=None):
        """
        Initializes the BasePhase with the path to the input file.
        Args:
            input_filepath (str): Path to the input text file.
        """
        if input_filepath is None:
            return
        self.input_file = Path(input_filepath)

        # The output file will be named like 'input_file_name_output.txt' in the same directory.
        self.output_file = self.input_file.parent / f"{self.input_file.stem}_output.txt"

    def _read_input(self) -> str:
        """
        Reads content from the specified input file.
        Raises:
            FileNotFoundError: If the input file does not exist.
        Returns:
            str: The content of the input file as a string.
        """
        if not self.input_file.exists():
            raise FileNotFoundError(f"Input file not found: {self.input_file}")
        with open(self.input_file, 'r', encoding='utf-8') as f:
            return f.read().strip()

    def _write_output(self, output_content: str):
        """
        Writes the processed output content to the determined output file.
        Args:
            output_content (str): The content to write to the output file.
        """
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(output_content)

    def run(self):
        """
        Executes the main flow for a phase: reads input, processes it, and writes output.
        This method should not be overridden by subclasses unless the overall flow changes.
        """
        print(f"--- Running {self.__class__.__name__} ---")
        try:
            input_data = self._read_input()
            result = self.process(input_data)
            self._write_output(result)
            print(f"Output for {self.__class__.__name__} written to: {self.output_file}")
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except NotImplementedError as e:
            print(f"Error: {self.__class__.__name__} has not implemented its 'process' method. {e}")
        except Exception as e:
            print(f"An unexpected error occurred during {self.__class__.__name__}: {e}")

    @abstractmethod
    def process(self, input_data: str) -> str:
        """
        Abstract method that must be implemented by each concrete phase.
        This method contains the core logic specific to each phase.
        Args:
            input_data (str): The content read from the input file.
        Returns:
            str: The formatted output string for the phase.
        """
        pass
