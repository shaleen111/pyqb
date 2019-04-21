from lexer import Lexer
from parsr import Parser


def number(sub):
    return float(sub) if "." in sub else int(sub)

if __name__ == "__main__":
    while True:
        # Obtain Input
        inp = input(">")
        if inp.lower() == "exit":
            break

        # Generate Lexer
        lex = Lexer(inp)
        lex.register("NUMBER", "[\d]+(\.[\d]+)?", number)
        lex.register("MULTIPLY", "\*")
        lex.register("DIVIDE", "\/")
        lex.register("SUBTRACT", "\-")
        lex.register("ADD", "\+")
        lex.register("LPAREN", "\(")
        lex.register("RPAREN", "\)")
        tokens = lex.tokenize()
        print(tokens)

        # Parse the Output of the Lexer
        print(Parser(tokens).parse())
