from LanguageConstants import SUPPORTED_TOKENS, TokenType, LANGUAGE_IDENTIFIERS
from Tokens import Token
from typing import List
from Tokenizer import Tokenizer

def ParsingProcess(file_content: str) -> int:
    tokenizer = Tokenizer(file_content=file_content)
    status = tokenizer.tokenize()
    # tokenizer.print_tokens(sys.stdout, sys.stderr)
    if status == tokenizer.SCANNER_ERROR:
        return status

    parser = Parser(tokenizer.tokens)
    status = parser.parse()
    return status

class Parser:
    BOOLS_AND_NIL = ["TRUE", "FALSE", "NIL"]
    UNARY = ["MINUS", "BANG"]
    LITERALS = ["NUMBER", "STRING"]
    LEFTIES = ["LEFT_PAREN", "LEFT_BRACE"]
    RIGHTS = ["RIGHT_PAREN", "RIGHT_BRACE"]
    # INIT_STATE = "init"
    # IN_GROUP_STATE = "in_group"
    PARSER_SUCCESS = 0
    PARSER_ERROR = -1

    def __init__(self, tokens: List[Token]) -> None:
        self.tokens: List[Token] = tokens
        self.status_code = self.PARSER_SUCCESS

    # def set_current_state(self, content: Union[str | int]="", state: str=INIT_STATE, current_state: ParserState=None) -> ParserState:
    #     """
    #     set new current state of the parser, default set values to initialize
    #     :param current_state: current state of the parser
    #     :param state: current state
    #     :param content: content to be set
    #     :return: the new state
    #     """
    #     if state == self.IN_GROUP_STATE:
    #         if current_state is not None and current_state.state == self.IN_GROUP_STATE:
    #             return ParserState(state=self.IN_GROUP_STATE, content=current_state.content+1)
    #         else:
    #             return ParserState(state=state, content=1)

    #     return ParserState(state=state, content=content)

    def parse_expression(index):
        pass


    def parse_term(index):
        pass


    def parse_unary(self, index: int):
        token = self.tokens[index]
        if token.token_type in self.LITERALS:
            return token.literal, index+1

        if token.token_type == TokenType.LEFT_PAREN:
            expr, index = self.parse_expression(index + 1)
            if self.tokens[index].token_type != TokenType.RIGHT_PAREN:
                raise NotImplementedError # expected ) at end

            return expr, index+1 # consume the right parenthesis

        if token.token_type in self.UNARY:
            factor, index = self.parse_unary(index)
            return (token.lexeme, factor), index

        raise AssertionError # unexpected token

    def parse(self) -> int:
        return 0
    
    