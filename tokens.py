import token

def no_val(val):
    return None

def integer(val):
    return int(val)

def floating_point(val):
    return float(val)

tokens = []

tokens.append(TokenType("Integer", "[\d]+", integer))
tokens.append(TokenType("Float", "[\d]+\.[\d]", floating_point))

tokens.append(TokenType("MULTIPLY"))
tokens.append(TokenType("DIVIDE"))
tokens.append(TokenType("SUBTRACT"))
tokens.append(TokenType("ADD"))