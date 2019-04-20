from lexer import Lexer
from tokens import token_list
from parsr import Parser

if __name__ == "__main__":
    while True:
        inp = input(">")
        if inp == "exit":
            break
        lex = Lexer(inp, token_list)
        l = lex.tokenize()
        print(l)
        print(Parser(l).parse())