from lexer import Lexer
from parsr import Parser
from interpreter import Interpreter


def number(sub):
    return float(sub) if "." in sub else int(sub)


def main():
    while True:
        # Obtain Input
        inp = input(">")
        if inp.lower() == "exit()":
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
        lex.register("POWER", "\^")

        try:
            tokens = lex.tokenize()
            print(tokens)

            # Parse the Output of the Lexer and Interpret it
            ast = Parser(tokens).parse()
            print(ast)
            ex_resut = Interpreter(ast).exec()
            print(ex_resut)
        except Exception as e:
            print(e)
            continue

if __name__ == "__main__":
    main()
