
class ASTNode:
    """Base class for all AST nodes."""
    pass

class Block(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class Literal(ASTNode):
    def __init__(self, value):
        self.value = value

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

class BinaryOperation(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class UnaryOperation(ASTNode):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

class VariableDeclaration(ASTNode):
    def __init__(self, name, initializer=None):
        self.name = name
        self.initializer = initializer

class Assignment(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class PrintStatement(ASTNode):
    def __init__(self, expression):
        self.expression = expression


# class Null(ASTNode):
#     pass
#
# class IfStatement(ASTNode):
#     def __init__(self, condition, then_branch, else_branch=None):
#         self.condition = condition
#         self.then_branch = then_branch
#         self.else_branch = else_branch
#
# class WhileLoop(ASTNode):
#     def __init__(self, condition, body):
#         self.condition = condition
#         self.body = body
#
# class ForLoop(ASTNode):
#     def __init__(self, initializer, condition, increment, body):
#         self.initializer = initializer
#         self.condition = condition
#         self.increment = increment
#         self.body = body
#
# class LogicalOperation(ASTNode):
#     def __init__(self, left, operator, right):
#         self.left = left
#         self.operator = operator
#         self.right = right
#
# class FunctionDeclaration(ASTNode):
#     def __init__(self, name, parameters, body):
#         self.name = name
#         self.parameters = parameters
#         self.body = body
#
# class FunctionCall(ASTNode):
#     def __init__(self, callee, arguments):
#         self.callee = callee
#         self.arguments = arguments
#
# class ClassDeclaration(ASTNode):
#     def __init__(self, name, superclass, methods):
#         self.name = name
#         self.superclass = superclass
#         self.methods = methods
#
# class This(ASTNode):
#     pass
#
# class Super(ASTNode):
#     def __init__(self, method_name):
#         self.method_name = method_name
#
# class ReturnStatement(ASTNode):
#     def __init__(self, value):
#         self.value = value
#
