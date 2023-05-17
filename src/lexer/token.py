from src.lexer.token_type import TokenType

class Token:
    def __init__(self, type_: TokenType, lexeme: str, literal, line: int) -> None:
        self.type = type_
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f"{self.type} {self.lexeme} {self.literal}"
