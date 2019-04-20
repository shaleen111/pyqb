from error import Error
from re import match, compile
from token import TokenType, Token

class Lexer():

    # Initializes lexer
    # Debug mode will show line numbers for errors
    def __init__(self, program, token_types):
        self.program = program
        self.position = 0
        self.token_types = token_types
    
    # Goes to next token
    def next_token(self):
        # Checks if we are at the very end of the program to be lexed
        if self.position >= len(self.program):
            return None
        
        # Ignore whitespace
        white_space =  compile("\s+").match(self.program, self.position)
        if white_space:
            self.position = white_space.end()
        
        # Splice the program based on the value of position
        # Iterates through the list of tokens to check if any token is found
        for tkn_t in self.token_types:
            currP = self.program[self.position:]
            regx_result = tkn_t.identify(currP)
            if regx_result:
                tkn = tkn_t.make(currP)
                self.position += regx_result.end()
                return tkn
        Error("Unknown Token", "Lexer").call(f"col {self.position+1}")
    
    def tokenize(self):
        list_token = []
        while True:
            tkn = self.next_token()
            if tkn is None:
                break
            list_token.append(tkn)
        return list_token