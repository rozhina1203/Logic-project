import copy
from ..base_phase import BasePhase
from ..phase1.logic import Phase1, Node


class Phase2(BasePhase):
    """
    Implements Phase 2: Conversion of a Well-Formed Formula (WFF) to Conjunctive Normal Form (CNF).
    """

    def process(self, input_data: str) -> str:
        """
        Processes the input Well-Formed Formula (WFF) and converts it to its equivalent Conjunctive Normal Form (CNF).

        This method performs the following steps:
        1. Parses the input string into a parse tree representation using Phase1.
        2. Converts the parse tree to CNF format by applying logical transformations.
        3. Converts the CNF parse tree back into a string representation.

        Args:
            input_data (str): The propositional logic formula as a string (assumed to be a valid WFF).

        Returns:
            str: The formula converted into CNF format as a string.
        """
        # Parse the input to create a tree representation of the formula
        tree = Phase1().parse_tree(input_data)

        # Convert the parse tree to CNF format through multiple logical transformation steps
        cnf_tree = self.convert_to_cnf(tree)

        # Convert the CNF parse tree back to string format for output
        return self.tree_to_string(cnf_tree)

    def convert_to_cnf(self, root):
        """
        Converts a parse tree representation of a Well-Formed Formula (WFF) into Conjunctive Normal Form (CNF).

        This method applies a series of logical transformations to the input tree:
        1. Eliminates implications and biconditionals.
        2. Moves negations inward using De Morgan's laws and other simplifications.
        3. Distributes OR over AND to achieve CNF structure.

        Args:
            root (Node): The root node of the parse tree representing the WFF.

        Returns:
            Node: The root node of the transformed parse tree in CNF format.
        """
        if root is None:
            return None

        # Step 1: Eliminate implications and biconditionals
        root = self.eliminate_implications(root)

        # Step 2: Move negations inward
        root = self.move_negations_inward(root)

        # Step 3: Distribute OR over AND
        root = self.distribute_or_over_and(root)

        return root

    def eliminate_implications(self, node):
        """
        Eliminates implications and biconditionals in a parse tree using logical equivalences.

        This method transforms nodes in the parse tree to remove implications (→) and biconditionals (↔)
        by applying the following rules:
        - A → B ≡ ¬A ∨ B
        - A ↔ B ≡ (A → B) ∧ (B → A) ≡ (¬A ∨ B) ∧ (¬B ∨ A)

        The method processes the tree recursively, ensuring that all implications and biconditionals
        are eliminated from the entire tree.

        Args:
            node (Node): The current node in the parse tree.

        Returns:
            Node: The transformed node with implications and biconditionals eliminated.
        """
        if node is None:
            return None

        # Recursively process children first
        if node.left:
            node.left = self.eliminate_implications(node.left)
        if node.right:
            node.right = self.eliminate_implications(node.right)

        # If this is a biconditional, convert it
        if node.value == '↔':
            # A ↔ B becomes (A → B) ∧ (B → A)
            # Which becomes (¬A ∨ B) ∧ (¬B ∨ A)

            # Left side: ¬A ∨ B
            not_left = Node('¬')
            not_left.right = copy.deepcopy(node.left)

            or_left = Node('∨')
            or_left.left = not_left
            or_left.right = copy.deepcopy(node.right)

            # Right side: ¬B ∨ A
            not_right = Node('¬')
            not_right.right = copy.deepcopy(node.right)

            or_right = Node('∨')
            or_right.left = not_right
            or_right.right = copy.deepcopy(node.left)

            # Combine with AND
            and_node = Node('∧')
            and_node.left = or_left
            and_node.right = or_right

            return and_node

        # If this is an implication, convert it
        elif node.value == '→':
            # A → B becomes ¬A ∨ B
            not_left = Node('¬')
            not_left.right = node.left

            or_node = Node('∨')
            or_node.left = not_left
            or_node.right = node.right

            return or_node

        return node

    def move_negations_inward(self, node):
        """
        Moves negations inward in a parse tree using De Morgan's laws and simplifies double negations.

        This method applies the following transformations:
        - Double negation elimination: ¬¬A ≡ A
        - De Morgan's laws:
            ¬(A ∨ B) ≡ ¬A ∧ ¬B
            ¬(A ∧ B) ≡ ¬A ∨ ¬B
        - Retains negation for propositions.

        The method processes the tree recursively to ensure all negations are moved inward.

        Args:
            node (Node): The current node in the parse tree.

        Returns:
            Node: The transformed node with negations moved inward.
        """
        if node is None:
            return None

        # If this is a negation
        if node.value == '¬':
            child = node.right

            # Double negation elimination: ¬¬A ≡ A
            if child.value == '¬':
                return self.move_negations_inward(child.right)

            # De Morgan's law: ¬(A ∨ B) ≡ ¬A ∧ ¬B
            elif child.value == '∨':
                and_node = Node('∧')

                not_left = Node('¬')
                not_left.right = child.left

                not_right = Node('¬')
                not_right.right = child.right

                and_node.left = self.move_negations_inward(not_left)
                and_node.right = self.move_negations_inward(not_right)

                return and_node

            # De Morgan's law: ¬(A ∧ B) ≡ ¬A ∨ ¬B
            elif child.value == '∧':
                or_node = Node('∨')

                not_left = Node('¬')
                not_left.right = child.left

                not_right = Node('¬')
                not_right.right = child.right

                or_node.left = self.move_negations_inward(not_left)
                or_node.right = self.move_negations_inward(not_right)

                return or_node

            # If it's a proposition, keep the negation
            else:
                return node

        # Recursively process children
        if node.left:
            node.left = self.move_negations_inward(node.left)
        if node.right:
            node.right = self.move_negations_inward(node.right)

        return node

    def distribute_or_over_and(self, node):
        """
        Distributes OR over AND in a parse tree to achieve Conjunctive Normal Form (CNF).

        This method applies the following logical equivalences:
        - A ∨ (B ∧ C) ≡ (A ∨ B) ∧ (A ∨ C)
        - (A ∧ B) ∨ C ≡ (A ∨ C) ∧ (B ∨ C)
        - (A ∧ B) ∨ (C ∧ D) ≡ (A ∨ C) ∧ (A ∨ D) ∧ (B ∨ C) ∧ (B ∨ D)

        The method processes the tree recursively to ensure all OR operations are distributed over AND.

        Args:
            node (Node): The current node in the parse tree.

        Returns:
            Node: The transformed node with OR distributed over AND.
        """
        if node is None:
            return None

        # Recursively process children first
        if node.left:
            node.left = self.distribute_or_over_and(node.left)
        if node.right:
            node.right = self.distribute_or_over_and(node.right)

        # If this is an OR operation
        if node.value == '∨':
            left = node.left
            right = node.right

            # Case 1: (A ∧ B) ∨ (C ∧ D) ≡ (A ∨ C) ∧ (A ∨ D) ∧ (B ∨ C) ∧ (B ∨ D)
            if left.value == '∧' and right.value == '∧':
                and1 = Node('∧')
                and2 = Node('∧')
                and3 = Node('∧')

                # (A ∨ C)
                or1 = Node('∨')
                or1.left = copy.deepcopy(left.left)
                or1.right = copy.deepcopy(right.left)

                # (A ∨ D)
                or2 = Node('∨')
                or2.left = copy.deepcopy(left.left)
                or2.right = copy.deepcopy(right.right)

                # (B ∨ C)
                or3 = Node('∨')
                or3.left = copy.deepcopy(left.right)
                or3.right = copy.deepcopy(right.left)

                # (B ∨ D)
                or4 = Node('∨')
                or4.left = copy.deepcopy(left.right)
                or4.right = copy.deepcopy(right.right)

                # Build the tree: ((A ∨ C) ∧ (A ∨ D)) ∧ ((B ∨ C) ∧ (B ∨ D))
                and1.left = self.distribute_or_over_and(or1)
                and1.right = self.distribute_or_over_and(or2)

                and2.left = self.distribute_or_over_and(or3)
                and2.right = self.distribute_or_over_and(or4)

                and3.left = and1
                and3.right = and2

                return and3

            # Case 2: A ∨ (B ∧ C) ≡ (A ∨ B) ∧ (A ∨ C)
            elif right.value == '∧':
                and_node = Node('∧')

                or_left = Node('∨')
                or_left.left = copy.deepcopy(left)
                or_left.right = copy.deepcopy(right.left)

                or_right = Node('∨')
                or_right.left = copy.deepcopy(left)
                or_right.right = copy.deepcopy(right.right)

                and_node.left = self.distribute_or_over_and(or_left)
                and_node.right = self.distribute_or_over_and(or_right)

                return and_node

            # Case 3: (A ∧ B) ∨ C ≡ (A ∨ C) ∧ (B ∨ C)
            elif left.value == '∧':
                and_node = Node('∧')

                or_left = Node('∨')
                or_left.left = copy.deepcopy(left.left)
                or_left.right = copy.deepcopy(right)

                or_right = Node('∨')
                or_right.left = copy.deepcopy(left.right)
                or_right.right = copy.deepcopy(right)

                and_node.left = self.distribute_or_over_and(or_left)
                and_node.right = self.distribute_or_over_and(or_right)

                return and_node

        return node

    def tree_to_string(self, node):
        """
        Converts a parse tree back to string format.

        This method traverses the parse tree and generates a string representation of the formula.
        It handles propositions, unary operators (e.g., negation), and binary operators (e.g., AND, OR).
        Parentheses are added for clarity based on operator precedence and associativity.

        Args:
            node (Node): The current node in the parse tree.

        Returns:
            str: The string representation of the formula.
        """
        if node is None:
            return ""

        # If it's a proposition (leaf node)
        if node.value.isalpha():
            return node.value

        # If it's a unary operator (negation)
        if node.value == '¬':
            right_str = self.tree_to_string(node.right)
            if not right_str:  # Handle empty strings
                return ""
            # Add parentheses if the right operand is complex
            if node.right and node.right.value in ['∧', '∨', '→', '↔']:
                return f"¬({right_str})"
            else:
                return f"¬{right_str}"

        # If it's a binary operator
        left_str = self.tree_to_string(node.left)
        right_str = self.tree_to_string(node.right)

        # Handle empty strings (from simplification)
        if not left_str and not right_str:
            return ""
        if not left_str:
            return right_str
        if not right_str:
            return left_str

        # Add parentheses for clarity
        if node.left and self.needs_parentheses(node.left, node, True):
            left_str = f"({left_str})"

        if node.right and self.needs_parentheses(node.right, node, False):
            right_str = f"({right_str})"

        return f"{left_str} {node.value} {right_str}"

    def needs_parentheses(self, child, parent, is_left):
        """
        Determines if parentheses are needed based on operator precedence.

        This method evaluates whether parentheses are required around a child node
        in a parse tree based on the precedence and associativity of the operators
        in the parent and child nodes.

        Rules applied:
        - Parentheses are not needed for propositions or unary operators (e.g., negation).
        - Parentheses are required if the child's operator has lower precedence than the parent's operator.
        - Parentheses may be required for operators with the same precedence, depending on associativity:
            - Right-associative operators (e.g., →, ↔) require parentheses for the right operand.

        Args:
            child (Node): The child node in the parse tree.
            parent (Node): The parent node in the parse tree.
            is_left (bool): Indicates whether the child is the left operand of the parent.

        Returns:
            bool: True if parentheses are needed, False otherwise.
        """
        if child.value.isalpha() or child.value == '¬':
            return False

        child_prec = self.precedence(child.value)
        parent_prec = self.precedence(parent.value)

        # Lower precedence needs parentheses
        if child_prec > parent_prec:
            return True

        # Same precedence might need parentheses based on associativity
        if child_prec == parent_prec:
            # For right-associative operators or right operand
            if not is_left and parent.value in ['→', '↔']:
                return True

        return False

    @staticmethod
    def precedence(operator):
        """
        Determines the precedence of a logical operator.

        This method returns the precedence of a given operator used in propositional logic.
        Operators with lower numerical values have higher precedence.

        Precedence levels:
        - '¬' (NOT): 1
        - '∧' (AND): 2
        - '∨' (OR): 3
        - '→' (IMPLIES): 4
        - '↔' (BICONDITIONAL): 5

        If the operator is not recognized, a default precedence value of 6 is returned.

        Args:
            operator (str): A string representing the logical operator.

        Returns:
            int: The precedence level of the operator.
        """
        precedences = {
            '¬': 1,
            '∧': 2,
            '∨': 3,
            '→': 4,
            '↔': 5
        }
        return precedences.get(operator, 6)
