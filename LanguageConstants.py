
class TokenType:
    # Literal Types
    STRING = "STRING"
    NUMBER = "NUMBER"
    IDENTIFIER = "IDENTIFIER"
    
    # Comparison Operators
    EQUAL = "EQUAL"
    EQUAL_EQUAL = "EQUAL_EQUAL"
    BANG_EQUAL = "BANG_EQUAL"
    BANG = "BANG"
    LESS_EQUAL = "LESS_EQUAL"
    LESS = "LESS"
    GREATER_EQUAL = "GREATER_EQUAL"
    GREATER = "GREATER"

    # Delimiters
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    LEFT_BRACE = "LEFT_BRACE"
    RIGHT_BRACE = "RIGHT_BRACE"
    SEMICOLON = "SEMICOLON"
    COMMA = "COMMA"
    DOT = "DOT"

    # Arithmetic Operators
    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"
    SLASH = "SLASH"

    # Other
    COMMENT = "COMMENT"
    WHITESPACE = "WHITESPACE"
    EOF = "EOF"


SUPPORTED_TOKENS = {
    "(": TokenType.LEFT_PAREN,
    ")": TokenType.RIGHT_PAREN,
    "{": TokenType.LEFT_BRACE,
    "}": TokenType.RIGHT_BRACE,
    ".": TokenType.DOT,
    ",": TokenType.COMMA,
    "-": TokenType.MINUS,
    "+": TokenType.PLUS,
    "*": TokenType.STAR,
    ";": TokenType.SEMICOLON,
    "\"": TokenType.STRING,
    "/" : {"/": TokenType.COMMENT, None: TokenType.SLASH},
    "=": {"=": TokenType.EQUAL_EQUAL, None: TokenType.EQUAL},
    "!": {"=": TokenType.BANG_EQUAL, None: TokenType.BANG},
    "<": {"=": TokenType.LESS_EQUAL, None: TokenType.LESS},
    ">": {"=": TokenType.GREATER_EQUAL, None: TokenType.GREATER},
    " ": TokenType.WHITESPACE,
    "\t": TokenType.WHITESPACE,
    None: TokenType.EOF,
}

LANGUAGE_IDENTIFIERS = {
    "and": "AND",
    "class": "CLASS",
    "else": "ELSE",
    "false": "FALSE",
    "for": "FOR",
    "fun": "FUN",
    "if": "IF",
    "nil": "NIL",
    "or": "OR",
    "print": "PRINT",
    "return": "RETURN",
    "super": "SUPER",
    "this": "THIS",
    "true": "TRUE",
    "var": "VAR",
    "while": "WHILE",
}
