from token import Token, TokenType

def number(sub):
    return float(sub) if "." in sub else int(sub)

token_list = []

token_list.append(TokenType("NUMBER", "[+|-]?[\d]+(\.[\d]+)?", number))

token_list.append(TokenType("MULTIPLY", "\*"))
token_list.append(TokenType("DIVIDE", "\/"))
token_list.append(TokenType("SUBTRACT", "\-"))
token_list.append(TokenType("ADD", "\+"))