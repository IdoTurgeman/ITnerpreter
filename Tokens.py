class Token:
    def __init__(self, token_type: str, lexeme, literal) -> None:
        self.token_type = token_type
        self.lexeme: str = lexeme
        self.literal = literal

    def __str__(self) -> str:
        if self.lexeme is None:
            return f"{self.token_type:<15}\t{self.literal:<8}"

        return f"{self.token_type:<15}\t{self.lexeme:<8}\t{self.literal}"

class ErrorToken:
    def __init__(self, line_number: int, error_description: str) -> None:
        self.error_description = error_description
        self.line_number = line_number

    def __str__(self) -> str:
        return f"[line {self.line_number}] Error: {self.error_description}"