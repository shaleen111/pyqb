import tokens
from re import match, compile

class Lexer():
    # Initializes lexer
    # Debug mode will show line numbers for errors
    def __init__(self, program, tokenl):
        self.program = program
        self.position = 0
        self.tokens = tokenl
    
    def next_token(self):
        if self.position > len(self.program):
            return None
        
        white_space =  compile("\s+").match(self.program, self.position)
        if white_space:
            self.position = white_space.end()
        
        for tkn in self.tokens:
            currP = self.program[self.position:]
            ptkn = tkn.identify(currP)
            if ptkn:
                t = tkn.make(currP)
                self.position += ptkn.end()
                return t
  
    def tokenize(self):
        list_token = []
        while True:
            tkn = self.next_token()
            if tkn is None:
                break
            list_token.append(tkn)
        return list_token
    

if __name__ == "__main__":
    l = Lexer(input(">") , tokens.token_list)
    print(l.tokenize())