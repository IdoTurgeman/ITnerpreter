from collections import namedtuple
from typing import Union, List
from LanguageConstants import SUPPORTED_TOKENS, TokenType, LANGUAGE_IDENTIFIERS
from Tokens import Token, ErrorToken

class Tokenizer:
    TokenizerState = namedtuple('ScannerState', ['dictionary', 'token'])

    # ========== status codes ============
    SCANNER_SUCCESS = 0
    TOKENIZER_ERROR = 65
    STRING_CHAR = "\""
    NUMBER_DOT = "."

    # =========== supported tokens identifiers and names ===============
    def __init__(self, file_content: List[str]) -> None:
        self.file_content: List[str] = file_content
        self.tokens: List[Token] = []
        self.errors: List[ErrorToken] = []
        self.status_code = Tokenizer.SCANNER_SUCCESS

    def add_error_token(self, line_number, description, status_code) -> None:
        self.errors.append(ErrorToken(line_number, description))
        self.status_code = status_code

    def add_token(self, token_type, lexeme, literal="null") -> None:
        if token_type == TokenType.WHITESPACE:
            return
        self.tokens.append(Token(token_type, lexeme, literal))

    def set_current_state(self, dictionary=None, token: str = "") -> TokenizerState:
        """
        set new current state of the scanner, default set values to initialize
        :param dictionary: dictionary that should be set
        :param token: token to be set
        :return: the new state
        """
        if dictionary is None:
            dictionary = SUPPORTED_TOKENS
        return self.TokenizerState(dictionary=dictionary, token=token)

    def capture_string(self, current_state, char, line_number) -> Union[TokenizerState, bool]:
        """
        capture and handle all the string tokens
        :param current_state: current state
        :param char: current char
        :param line_number: current line number
        :return: current state and boolean in case of should continue the loop or not
        """
        if current_state.dictionary == self.STRING_CHAR:
            if char == self.STRING_CHAR:
                self.add_token(
                    SUPPORTED_TOKENS.get(self.STRING_CHAR),
                    self.STRING_CHAR + current_state.token + self.STRING_CHAR,
                    current_state.token
                )
                return self.set_current_state(), True
            else:
                current_state = self.set_current_state(dictionary=self.STRING_CHAR, token=current_state.token + char)
                return  current_state, True

        elif char == self.STRING_CHAR:
            current_state = self.set_current_state(dictionary=self.STRING_CHAR, token="")
            return current_state, True

        return current_state, False

    def capture_number(self, current_state, char, line_number) -> Union[TokenizerState, bool]:
        """
        capture and handle all the number tokens
        :param current_state: current state
        :param char: current char
        :param line_number: current line number
        :return: current state and boolean in case of should continue the loop or not
        """
        if current_state.dictionary == TokenType.NUMBER:
            # at least one number already found
            if char.isdigit():
                current_state = self.set_current_state(dictionary=TokenType.NUMBER, token=current_state.token + char)
                return current_state, True
            elif char == self.NUMBER_DOT:
                if self.NUMBER_DOT in current_state.token:
                    self.add_error_token(line_number, f"Unexpected character: {current_state.token}",
                                         self.TOKENIZER_ERROR)
                    return self.set_current_state(), True
                else:
                    current_state = self.set_current_state(dictionary=TokenType.NUMBER, token=current_state.token + char)
                    return current_state, True
            else:
                self.add_token(
                    TokenType.NUMBER,
                    current_state.token,
                    str(float(current_state.token))
                )
                current_state = self.set_current_state()

        elif char.isdigit() and current_state.dictionary == SUPPORTED_TOKENS:
            # capture the first number
            current_state = self.set_current_state(dictionary=TokenType.NUMBER, token=char)
            return current_state, True

        return current_state, False

    def capture_tokens(self, current_state, char, line_number) -> Union[TokenizerState, bool]:
        """
        capture and handle all the "regular" tokens
        :param current_state: current state
        :param char: current char
        :param line_number: current line number
        :return: current state and boolean in case of should return the prent func or not
        """
        current_state = self.set_current_state(current_state.dictionary, current_state.token + char)
        if char not in current_state.dictionary.keys():
            if current_state.dictionary == SUPPORTED_TOKENS:
                self.add_error_token(line_number, f"Unexpected character: {current_state.token}", self.TOKENIZER_ERROR)
                current_state = self.set_current_state()
                return current_state, False
            else:
                if None not in current_state.dictionary.keys():
                    self.add_error_token(line_number, f"Unexpected character: {current_state.token}",
                                         self.TOKENIZER_ERROR)
                    current_state = self.set_current_state()
                    return current_state, False
                else:
                    if current_state.dictionary.get(None) == TokenType.COMMENT:
                        return None, True
                    self.add_token(current_state.dictionary.get(None), current_state.token[:-1])
                    current_state = self.set_current_state(dictionary=None, token=current_state.token[-1])

        if char in current_state.dictionary.keys():
            val = current_state.dictionary.get(char)
            if isinstance(val, dict):
                current_state = self.set_current_state(dictionary=val, token=current_state.token)
            else:
                if val == TokenType.COMMENT:
                    return None, True
                self.add_token(val, current_state.token)
                current_state = self.set_current_state()
        else:
            self.add_error_token(line_number, f"Unexpected character: {char}", self.TOKENIZER_ERROR)
            current_state = self.set_current_state()

        return current_state, False

    def capture_identifier(self, current_state, char, line_number) -> Union[TokenizerState, bool]:
        """
        capture and handle all the identifier tokens
        :param current_state: current state
        :param char: current char
        :param line_number: current line number
        :return: current state and boolean in case of should continue the loop or not
        """
        if current_state.dictionary == TokenType.IDENTIFIER:
            if char.isalpha() or char.isdigit() or char == "_":
                current_state = self.set_current_state(dictionary=TokenType.IDENTIFIER, token=current_state.token + char)
                return current_state, True
            else:
                self.add_token(
                    LANGUAGE_IDENTIFIERS.get(current_state.token, TokenType.IDENTIFIER),
                    current_state.token
                )
                current_state = self.set_current_state()

        elif char.isalpha() or char.isdigit() or char == "_":
            if current_state.dictionary != SUPPORTED_TOKENS:
                self.add_token(current_state.dictionary.get(None), current_state.token)
            current_state = self.set_current_state(dictionary=TokenType.IDENTIFIER, token=char)
            return current_state, True

        return current_state, False

    def post_scanning_line(self, current_state, line_number) -> None:
        """
        function that handle the current state after iterating the entire content
        :param current_state: current state
        :param line_number: current line number
        :return: None
        """
        if current_state.token:
            if current_state.dictionary == self.STRING_CHAR:
                self.add_error_token(line_number, "Unterminated string.", self.TOKENIZER_ERROR)
            elif current_state.dictionary == TokenType.NUMBER:
                self.add_token(
                    TokenType.NUMBER,
                    current_state.token,
                    str(float(current_state.token))
                )
            elif current_state.dictionary == SUPPORTED_TOKENS:
                self.add_error_token(line_number, f"Unexpected character: {current_state.token}", self.TOKENIZER_ERROR)
            elif current_state.dictionary == TokenType.IDENTIFIER:
                self.add_token(
                    LANGUAGE_IDENTIFIERS.get(current_state.token, TokenType.IDENTIFIER),
                    current_state.token
                )
            else:
                self.add_token(current_state.dictionary.get(None), current_state.token)

    def tokenize_line(self, content: str, line_number: int) -> None:
        """
        scan a single line and tokenize it
        :param content: content to scan
        :param line_number: line number that scanned
        """
        current_state = self.set_current_state()
        for char in content:
            # numbers capture
            current_state, number_should_continue = self.capture_number(current_state, char, line_number)
            if number_should_continue:
                continue

            # string capture
            current_state, string_should_continue = self.capture_string(current_state, char, line_number)
            if string_should_continue:
                continue

            # identifiers capture
            current_state, identifier_should_continue = self.capture_identifier(current_state, char, line_number)
            if identifier_should_continue:
                continue

            # tokens capture
            current_state, tokens_should_return = self.capture_tokens(current_state, char, line_number)
            if tokens_should_return:
                return

        self.post_scanning_line(current_state, line_number)

    def tokenize(self) -> int:
        for idx, line in enumerate(self.file_content, start=1):
            self.tokenize_line(content=line.strip(), line_number=idx)

        self.add_token(SUPPORTED_TOKENS.get(None), None)
        return self.status_code

    def print_tokens(self, stdout, stderr) -> None:
        for idx, token in enumerate(self.tokens):
            print(f"{idx:<4}| {token}", file=stdout)

        for idx, err_token in enumerate(self.errors):
            print(f"{idx:<4}| {err_token}", file=stderr)
