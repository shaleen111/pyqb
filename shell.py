from lexer import Lexer
from parsr import Parser
from interpreter import Interpreter


def number(sub):
    return float(sub) if "." in sub else int(sub)


def main():
    lex = Lexer()
    parser = Parser()
    interp = Interpreter()

    lex.register("NUMBER", "[\d]+(\.[\d]+)?", number)
    lex.register("MULTIPLY", "\*")
    lex.register("DIVIDE", "\/")
    lex.register("SUBTRACT", "\-")
    lex.register("ADD", "\+")
    lex.register("LPAREN", "\(")
    lex.register("RPAREN", "\)")
    lex.register("POWER", "\^")
    lex.register("KEYWORD", "[lL][eE][tT]")
    lex.register("IDENTIFIER", "[A-Za-z0-9_]+")
    lex.register("EQUAL", "=")
    lex.register("NEQUAL", "<>")

    while True:

        # Obtain Input
        inp = input(">")
        if inp.lower() == "exit()":
            break

        try:
            tokens = lex.tokenize(inp)
            print(tokens)

            # Parse the Output of the Lexer and Interpret it
            ast = parser.parse(tokens)

            ex_resut = interp.exec(ast)
            print(ex_resut)
        except Exception as e:
            e.gen_err(inp)
            continue

if __name__ == "__main__":
    main()
