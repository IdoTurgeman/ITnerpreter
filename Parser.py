from LanguageConstants import TokenType
from ASTNodes import (Block, PrintStatement, VariableDeclaration,
                      BinaryOperation, UnaryOperation, Literal, Identifier, Assignment)


class Parser:
    """
    A parser that parses a series of tokens to generate an Abstract Syntax Tree (AST).
    The parser supports variable declarations, expressions, print statements, and basic operations.
    """

    PARSER_SUCCESS = 0
    PARSER_ERROR = 2

    def __init__(self, tokens):
        """
        Initialize the parser with a list of tokens.

        :param tokens: The list of tokens to parse
        """
        self.tokens = tokens
        self.current = 0
        self.ast = None  # To store the parsed AST

    def is_at_end(self):
        """
        Check if the parser has reached the end of the token stream.

        :return: True if at the end of the tokens, otherwise False
        """
        return self.peek().token_type == TokenType.EOF

    def parse(self):
        """
        Parse the entire token stream to produce an AST.

        :return: Parser.PARSER_SUCCESS if parsing was successful, Parser.PARSER_ERROR otherwise
        """
        try:
            statements = []
            while not self.is_at_end():
                statements.append(self.declaration())
            self.ast = Block(statements)
            return Parser.PARSER_SUCCESS
        except Exception as e:
            self.ast = None
            print(f"Parsing error: {e}")
            return Parser.PARSER_ERROR

    def print_ast(self, output):
        """
        Print the formatted AST to the provided output.

        :param output: The output stream (e.g., sys.stdout) to write the formatted AST to
        """
        def format_ast(node, indent=0):
            """
            Format the AST node as a string with indentation for printing.

            :param node: The AST node to format
            :param indent: The current level of indentation
            :return: A formatted string representation of the AST node
            """
            indent_str = " " * indent
            if isinstance(node, Block):
                formatted_statements = ",\n".join(format_ast(stmt, indent + 4) for stmt in node.statements)
                return f"Block([\n{indent_str}    {formatted_statements}\n{indent_str}])"
            elif isinstance(node, VariableDeclaration):
                initializer = format_ast(node.initializer, indent + 4) if node.initializer else "None"
                return f"VariableDeclaration(\n{indent_str}    name='{node.name}',\n{indent_str}    initializer={initializer}\n{indent_str})"
            elif isinstance(node, PrintStatement):
                expression = format_ast(node.expression, indent + 4)
                return f"PrintStatement(\n{indent_str}    expression={expression}\n{indent_str})"
            elif isinstance(node, Assignment):
                value = format_ast(node.value, indent + 4)
                return f"Assignment(\n{indent_str}    name='{node.name}',\n{indent_str}    value={value}\n{indent_str})"
            elif isinstance(node, BinaryOperation):
                left = format_ast(node.left, indent + 4)
                right = format_ast(node.right, indent + 4)
                return f"BinaryOperation(\n{indent_str}    left={left},\n{indent_str}    operator='{node.operator}',\n{indent_str}    right={right}\n{indent_str})"
            elif isinstance(node, UnaryOperation):
                operand = format_ast(node.operand, indent + 4)
                return f"UnaryOperation(\n{indent_str}    operator='{node.operator}',\n{indent_str}    operand={operand}\n{indent_str})"
            elif isinstance(node, Literal):
                return f"Literal({node.value})"
            elif isinstance(node, Identifier):
                return f"Identifier('{node.name}')"
            else:
                raise Exception(f"Unknown AST node type: {type(node).__name__}")

        if self.ast is not None:
            formatted_ast = format_ast(self.ast)
            output.write(formatted_ast + "\n")
        else:
            output.write("No valid AST to print.\n")

    def declaration(self):
        """
        Parse a variable declaration or a statement.

        :return: The parsed node representing the variable declaration or statement
        """
        if self.match(TokenType.VAR):
            return self.variable_declaration()
        return self.statement()

    def variable_declaration(self):
        """
        Parse a variable declaration.

        :return: A VariableDeclaration node representing the parsed variable declaration
        """
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")
        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        return VariableDeclaration(name=name.lexeme, initializer=initializer)

    def statement(self):
        """
        Parse a statement.

        :return: The parsed statement node
        """
        if self.match(TokenType.PRINT):
            return self.print_statement()
        return self.expression_statement()

    def print_statement(self):
        """
        Parse a print statement.

        :return: A PrintStatement node representing the parsed print statement
        """
        expr = self.expression()
        return PrintStatement(expr)

    def block(self):
        """
        Parse a block of statements inside braces.

        :return: A Block node representing the parsed block
        """
        statements = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return Block(statements)

    def expression_statement(self):
        """
        Parse an expression as a statement.

        :return: The parsed expression node
        """
        expr = self.expression()
        return expr

    def expression(self):
        """
        Parse an expression.

        :return: The parsed expression node
        """
        return self.assignment()

    def assignment(self):
        """
        Parse an assignment expression.

        :return: An Assignment node or other expression node if not an assignment
        """
        expr = self.addition()
        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expr, Identifier):
                return Assignment(expr.name, value)
            raise Exception(f"Invalid assignment target at token {equals.lexeme}.")
        return expr

    def addition(self):
        """
        Parse addition, subtraction, and nested expressions.

        :return: The parsed expression node
        """
        expr = self.multiplication()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous().lexeme
            right = self.multiplication()
            expr = BinaryOperation(left=expr, operator=operator, right=right)
        return expr

    def multiplication(self):
        """
        Parse multiplication, division, and nested expressions.

        :return: The parsed expression node
        """
        expr = self.unary()
        while self.match(TokenType.STAR, TokenType.SLASH):
            operator = self.previous().lexeme
            right = self.unary()
            expr = BinaryOperation(left=expr, operator=operator, right=right)
        return expr

    def unary(self):
        """
        Parse unary operators and parentheses.

        :return: The parsed unary expression or primary expression node
        """
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous().lexeme
            operand = self.unary()
            return UnaryOperation(operator=operator, operand=operand)
        return self.primary()

    def primary(self):
        """
        Parse primary expressions (literals, identifiers, parentheses).

        :return: The parsed primary expression node
        """
        if self.match(TokenType.NUMBER):
            return Literal(self.previous().literal)
        if self.match(TokenType.STRING):
            return Literal(self.previous().literal)
        if self.match(TokenType.IDENTIFIER):
            return Identifier(self.previous().lexeme)
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return expr
        raise Exception("Expected expression.")

    def match(self, *types):
        """
        Check if the current token matches any of the given types.

        :param types: The token types to match against
        :return: True if a match is found, otherwise False
        """
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def consume(self, token_type, error_message):
        """
        Consume a token of the specified type.

        :param token_type: The expected token type
        :param error_message: The error message to display if the token type does not match
        :return: The consumed token
        """
        if self.check(token_type):
            return self.advance()
        raise Exception(error_message)

    def check(self, token_type):
        """
        Check if the current token is of the specified type.

        :param token_type: The token type to check
        :return: True if the token matches the type, otherwise False
        """
        if self.is_at_end():
            return False
        return self.peek().token_type == token_type

    def advance(self):
        """
        Advance to the next token.

        :return: The previous token
        """
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def previous(self):
        """
        Get the previous token.

        :return: The previous token
        """
        return self.tokens[self.current - 1]

    def peek(self):
        """
        Get the current token.

        :return: The current token
        """
        return self.tokens[self.current]
