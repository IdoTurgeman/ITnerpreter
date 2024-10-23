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

    # Language Identifiers
    AND = "AND"
    CLASS = "CLASS"
    FALSE = "FALSE"
    ELSE = "ELSE"
    FOR = "FOR"
    FUN = "FUN"
    IF = "IF"
    NULL = "NULL"
    OR = "OR"
    PRINT = "PRINT"
    RETURN = "RETURN"
    SUPER = "SUPER"
    THIS = "THIS"
    TRUE = "TRUE"
    VAR = "VAR"   
    WHILE = "WHILE"
    ELIF = "ELIF"

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
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "elif": TokenType.ELIF,
    "null": TokenType.NULL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}
