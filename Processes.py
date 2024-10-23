import sys
from typing import List
from Tokenizer import Tokenizer
from Parser import Parser
from Interpreter import Interpreter

def tokenization(file_content: List[str]) -> int:
    tokenizer = Tokenizer(file_content=file_content)
    status = tokenizer.tokenize()
    tokenizer.print_tokens(sys.stdout, sys.stderr)
    return status

def parsing(file_content: List[str]) -> int:
    tokenizer = Tokenizer(file_content=file_content)
    status = tokenizer.tokenize()
    if status == Tokenizer.TOKENIZER_ERROR:
        return status

    parser = Parser(tokenizer.tokens)
    status = parser.parse()
    parser.print_ast(sys.stdout)
    return status

def interpreting(file_content: List[str]) -> int:
    tokenizer = Tokenizer(file_content=file_content)
    if tokenizer.tokenize() != Tokenizer.TOKENIZER_SUCCESS:
        return Tokenizer.TOKENIZER_ERROR

    parser = Parser(tokenizer.tokens)
    if parser.parse() != Parser.PARSER_SUCCESS:
        return Parser.PARSER_ERROR

    interpreter = Interpreter()
    return interpreter.interpret(parser.ast)
