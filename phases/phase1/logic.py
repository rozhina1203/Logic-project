# phases/phase1/main.py

from ..base_phase import BasePhase

class Node():
            def __init__(self, val):
                self.value = val
                self.left = None
                self.right = None
                
class Phase1(BasePhase):
    """
    Implements Phase 1: Well-Formed Formula (WFF) validation and Parse Tree generation.
    """

    """state "S" defines start
    state "N" defines negative "¬"
    state "P" defines proposition 
    state "O" defines operators
    state "L" defines left parenthese
    state "R" defines right parenthese"""
    

    def is_valid(self, expr) -> bool:
        state = 'S'
        fstack = list()
        tokens = self.tokenize(expr)
        
        for c in tokens:
            if c == '(':
                fstack.append('(')
            
            elif c == ')':
                if not fstack:
                    return False
                fstack.pop()

            if state == 'S':
                if c == '¬':
                    state = 'N'
                elif c == '(':
                    state = 'L'
                elif c.isalpha():
                    state = 'P'
                else:
                    return False
                
            elif state == 'N':
                if c == '¬':
                    state = 'N'
                elif c == '(':
                    state = 'L'
                elif c.isalpha():
                    state = 'P'
                else:
                    return False
            
            elif state == 'P':
                if c in {'∧', '∨', '→', '↔'}:
                    state = 'O'
                elif c == ')':
                    state = 'R'
                else:
                    return False
                
            elif state == 'O':
                if c == '¬':
                    state = 'N'
                elif c.isalpha():
                    state = 'P'
                elif c == '(':
                    state = 'L'
                else:
                    return False

            elif state == 'L':
                if c == '¬':
                    state = 'N'
                elif c == '(':
                    state = 'L'
                elif c.isalpha():
                    state = 'P'
                else:
                    return False

            elif state == 'R':
                if c in {'∧', '∨', '→', '↔'}:
                    state = 'O'
                elif c == ')':   
                    state = 'R'
                else:
                    return False
        return state in {'P', 'R'} and not fstack
    def tokenize(self, expr):
        tokens = []
        for ch in expr:
            if ch == ' ':
                continue
            else:
                tokens.append(ch)
        return tokens
    
    def is_operator(self, c):
        return c in ['¬', '∧', '∨', '→', '↔']
    
    def presedence(self, op):
        if op == '¬':
            return 1
        if op == '∧':
            return 2
        if op == '∨':
            return 3
        if op == '→':
            return 4
        if op == '↔':
            return 5
        return 100
    
    def parse_tree(self, expr):
        tokens = self.tokenize(expr)
        operators = []
        proposition = []

        def pop_op():
            op = operators.pop()
            if op == '¬':
                right = proposition.pop()
                node = Node(op)
                node.right = right
                proposition.append(node)
            else:
                right = proposition.pop()
                left = proposition.pop()
                node = Node(op)
                node.left = left
                node.right = right
                proposition.append(node)

        for t in tokens:
            if t == '(':
                operators.append(t)
            elif t == ')':
                while operators[-1] != '(':
                    pop_op()
                operators.pop()
            elif self.is_operator(t):
                while (operators and operators[-1] != '(' and self.presedence(operators[-1]) <= self.presedence(t)):
                    pop_op()
                operators.append(t)
            elif t.isalpha():
                proposition.append(Node(t))
            else:
                pass
        
        while operators:
            pop_op()
        
        return proposition[-1]
    
    def preorder(self, node, depth = 0):
        if node is None:
            return ''
        
        result = str('  ' * depth + str(node.value)) + '\n'
        left = self.preorder(node.left, depth+1)
        right = self.preorder(node.right, depth+1)

        if left:
            result +=  left
        if right:
            result += right

        return result
    
    
    def process(self, input_data: str) -> str:
        result_content = "Ha Ha"
        if self.is_valid(input_data):
            parsetree = self.parse_tree(input_data)
            result_content = self.preorder(parsetree)
            return "Valid Formula\n" + result_content
        else:
            return "Invalid Formula"
