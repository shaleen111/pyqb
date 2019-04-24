from interpreter import Interpreter
from lexer import Lexer
from parser import Parser


def number(sub):
    return float(sub) if "." in sub else int(sub)


def main():
    while True:
        # Obtain Input
        inp = input(">")
        if inp.lower() == "":
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

        try:
            tokens = lex.tokenize()
            print(tokens)

            # Parse the Output of the Lexer
            print(Interpreter(Parser(tokens).parse()).exec())
        except Exception as e:
            print(e)
            continue

if __name__ == "__main__":
    main()
