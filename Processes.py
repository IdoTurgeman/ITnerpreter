import sys
from typing import List
from Tokenizer import Tokenizer
from Parser import Parser

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