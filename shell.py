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
    lex.register("EQUAL", "=")
    lex.register("NEQUAL", "<>")
    lex.register("LEQ", "<=")
    lex.register("GEQ", ">=")
    lex.register("GREATERTHAN", ">")
    lex.register("LESSTHAN", "<")
    lex.register("AND", "[Aa][Nn][dD]")
    lex.register("OR", "[Oo][Rr]")
    lex.register("KEYWORD_LET", "[lL][eE][tT]")
    lex.register("KEYWORD_IF", "[iI][fF]")
    lex.register("KEYWORD_ELSEIF", "[Ee][Ll][Ss][Ee][Ii][Ff]")
    lex.register("KEYWORD_ELSE", "[Ee][Ll][Ss][Ee]")
    lex.register("KEYWORD_THEN", "[Tt][Hh][Ee][Nn]")
    lex.register("IDENTIFIER", "[A-Za-z0-9_]+")

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
            print(ast)
            ex_resut = interp.exec(ast)
            print(ex_resut)
        except Exception as e:
            e.gen_err(inp)
            continue

if __name__ == "__main__":
    main()
