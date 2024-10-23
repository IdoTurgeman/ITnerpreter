from ASTNodes import (Block, PrintStatement, VariableDeclaration,
                      BinaryOperation, UnaryOperation, Literal, Identifier, Assignment)
from LanguageConstants import TokenType

class Interpreter:
    """
    An interpreter that executes an Abstract Syntax Tree (AST).
    It evaluates variable declarations, expressions, print statements, assignments, and basic operations.

    Attributes:
        environment (dict): A dictionary to store variable values during execution.
    """

    INTERPRETER_SUCCESS = 0
    INTERPRETER_ERROR = 3

    def __init__(self):
        """
        Initialize the interpreter with an empty environment.
        """
        self.environment = {}  # A dictionary to store variable values

    def interpret(self, node):
        """
        Interpret and execute the given AST node.

        :param node: The root node of the AST to interpret
        :return: INTERPRETER_SUCCESS if execution was successful, INTERPRETER_ERROR otherwise
        """
        try:
            self._interpret(node)
            return Interpreter.INTERPRETER_SUCCESS
        except Exception as e:
            print(f"Runtime error: {e}")
            return Interpreter.INTERPRETER_ERROR

    def _interpret(self, node):
        """
        Dispatch execution based on the type of AST node.

        :param node: The AST node to interpret
        :return: The result of the execution, if applicable
        """
        if isinstance(node, Block):
            return self.execute_block(node)
        elif isinstance(node, VariableDeclaration):
            return self.execute_variable_declaration(node)
        elif isinstance(node, PrintStatement):
            return self.execute_print_statement(node)
        elif isinstance(node, Assignment):
            return self.execute_assignment(node)
        elif isinstance(node, BinaryOperation):
            return self.evaluate_binary_operation(node)
        elif isinstance(node, UnaryOperation):
            return self.evaluate_unary_operation(node)
        elif isinstance(node, Literal):
            return node.value
        elif isinstance(node, Identifier):
            return self.environment.get(node.name, None)
        else:
            raise Exception(f"Unsupported AST node type: {type(node).__name__}")

    def execute_block(self, block):
        """
        Execute each statement in the block.

        :param block: The Block node containing the statements to execute
        """
        for statement in block.statements:
            self._interpret(statement)

    def execute_variable_declaration(self, node):
        """
        Execute a variable declaration by evaluating the initializer and storing the variable.

        :param node: The VariableDeclaration node to execute
        :raises Exception: If a variable with the same name already exists
        """
        # Check if the variable already exists
        if node.name in self.environment:
            raise Exception(f"Variable '{node.name}' is already defined.")

        # Evaluate the initializer, if any, and store the variable in the environment
        value = self._interpret(node.initializer) if node.initializer else None
        self.environment[node.name] = value

    def execute_print_statement(self, node):
        """
        Execute a print statement by evaluating the expression and printing the result.

        :param node: The PrintStatement node to execute
        """
        value = self._interpret(node.expression)
        print(value)

    def execute_assignment(self, node):
        """
        Execute an assignment by evaluating the value and updating the variable in the environment.

        :param node: The Assignment node to execute
        :raises Exception: If the variable is not defined
        """
        value = self._interpret(node.value)
        if node.name in self.environment:
            self.environment[node.name] = value
        else:
            raise Exception(f"Variable '{node.name}' is not defined.")

    def evaluate_binary_operation(self, node):
        """
        Evaluate a binary operation by evaluating its operands and applying the operator.

        :param node: The BinaryOperation node to evaluate
        :return: The result of the binary operation
        :raises Exception: If the operation is unsupported or encounters an error
        """
        left = self._interpret(node.left)
        right = self._interpret(node.right)

        # Convert numeric strings to float if possible
        if isinstance(left, str):
            try:
                left = float(left)
            except ValueError:
                pass

        if isinstance(right, str):
            try:
                right = float(right)
            except ValueError:
                pass

        # Perform the binary operation
        if node.operator == TokenType.PLUS:
            return left + right
        elif node.operator == TokenType.MINUS:
            return left - right
        elif node.operator == TokenType.STAR:
            return left * right
        elif node.operator == TokenType.SLASH:
            if right == 0:
                raise Exception("Division by zero.")
            return left / right
        else:
            raise Exception(f"Unsupported binary operator: {node.operator}")

    def evaluate_unary_operation(self, node):
        """
        Evaluate a unary operation by applying the operator to the operand.

        :param node: The UnaryOperation node to evaluate
        :return: The result of the unary operation
        :raises Exception: If the operation is unsupported or encounters an error
        """
        operand = self._interpret(node.operand)

        # Convert numeric string to float if possible
        if isinstance(operand, str):
            try:
                operand = float(operand)
            except ValueError:
                raise Exception(f"Cannot perform unary operation on a non-numeric string: '{operand}'")

        # Perform the unary operation
        if node.operator == TokenType.MINUS:
            return -operand
        elif node.operator == TokenType.BANG:
            return not operand
        else:
            raise Exception(f"Unsupported unary operator: {node.operator}")
