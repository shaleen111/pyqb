from lexer import Lexer
from tokens import token_list

if __name__ == "__main__":
    while True:
        inp = input(">")
        if inp == "exit":
            break
        lex = Lexer(inp, token_list)
        print(lex.tokenize())