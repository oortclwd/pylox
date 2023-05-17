from typing import List

from src.error import error
from src.lexer.token import Token
from src.lexer.token_type import TokenType


keywords = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}


class Scanner:
    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens: List[TokenType] = []
        self.start = 0
        self.current = 0
        self.line = 1
    
    def scan_tokens(self):
        while not self._is_at_end():
            self.start = self.current
            self._scan_token()
        
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens
    
    def _scan_token(self):
        c: str= self._advance()
        if c == "(":
            self._add_token(TokenType.LEFT_PAREN)
        elif c == ")":
            self._add_token(TokenType.RIGHT_PAREN)
        elif c == "{":
            self._add_token(TokenType.LEFT_BRACE)
        elif c == "}":
            self._add_token(TokenType.RIGHT_BRACE)
        elif c == ",":
            self._add_token(TokenType.COMMA)
        elif c == ".":
            self._add_token(TokenType.DOT)
        elif c == "-":
            self._add_token(TokenType.MINUS)
        elif c == "+":
            self._add_token(TokenType.PLUS)
        elif c == ";":
            self._add_token(TokenType.SEMICOLON)
        elif c == "*":
            self._add_token(TokenType.STAR)
        elif c == "!":
            token = TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG
            self._add_token(token)
        elif c == "=":
            token = TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL
            self._add_token(token)
        elif c == "<":
            token = TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS
            self._add_token(token)
        elif c == ">":
            token = TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER
            self._add_token(token)
        elif c == "/":
            if self._match("/"):
                while self._peek() != "\n" and not self._is_at_end():
                    self._advance()
            else:
                self._add_token(TokenType.SLASH)
        elif c in " \r\t":
            pass
        elif c == "\n":
            self.line += 1
        elif c == '"':
            self._string()
        elif c.isdigit():
            self._number()
        elif c.isalpha() or c == "_":
            self._identifier()
        else:
            error(self.line, f"Unexpected character {c}")

    def _advance(self) -> str:
        result = self.source[self.current]
        self.current += 1
        return result
    
    def _add_token(self, token_type: TokenType, literal=None):
        self.tokens.append(Token(token_type, self.source[self.start:self.current], literal, self.line))

    def _is_at_end(self):
        return self.current >= len(self.source)
    
    def _match(self, expected):
        if self._is_at_end() or self.source[self.current] != expected:
            return False
        
        self.current += 1
        return True

    def _peek(self):
        if self._is_at_end(): return "\0"
        return self.source[self.current]

    def _string(self):
        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == "\n":
                self.line += 1
            self._advance()
        
        if self._is_at_end():
            error(self.line, "Unterminated String.")
            return
        
        self._advance() # closing "

        value = self.source[self.start+1:self.current-1]
        self._add_token(TokenType.STRING, value)

    def _number(self):
        while self._peek().isdigit():
            self._advance()
        
        if self._peek() == "." and self._peek_next().isdigit():
            self._advance()

        while self._peek().isdigit():
            self._advance()

        self._add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def _peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"
    
        return self.source[self.current+1]
    
    def _identifier(self):
        while self._peek().isalnum() or self._peek() == "_":
            self._advance()
        text = self.source[self.start:self.current]
        self._add_token(keywords.get(text, TokenType.IDENTIFIER))
