from error import Error
from re import compile

# Class for Tokens
class Token(): 
    # Token type will have a name, a value
    def __init__(self, type_name, value):
        self.type = type_name
        self.value = value

    def __repr__(self):
        return f"{self.type}:{self.value}"

# Class for Lexer
class Lexer():
    # Initializes lexer
    # Skip refers to any stream of chars to be ignored by lexer
    def __init__(self, program, token_types=list(), skip="\s+"):
        self.program = program
        self.position = 0
        self.token_types = token_types 
        self.skip = skip
    
    # Goes to next token
    def next_token(self):
        # Checks if we are at the very end of the program to be lexed
        if self.position >= len(self.program):
            return None
        
        # Ignore whitespace
        skipped =  compile(self.skip).match(self.program, self.position)
        if skipped:
            self.position = skipped.end()
        
        # Splice the program based on the value of position
        # Iterates through the list of tokens to check if any token is found
        for tkn_t in self.token_types:
            regx_result = compile(tkn_t["regx"]).match(self.program, self.position)
            if regx_result:
                tkn = Token(tkn_t["name"], regx_result.group(0))
                if tkn_t["mod"]:
                    tkn.value = tkn_t["mod"](tkn.value)
                self.position = regx_result.end()
                return tkn
        Error("Unknown Token", "Lexer").call(f"col {self.position+1}")
    
    # Return List of Tokens
    def tokenize(self):
        list_token = []
        while True:
            # Go through the string 
            # Generating Tokens 
            # Unti EOL
            tkn = self.next_token()
            if tkn is None:
                break
            list_token.append(tkn)
        return list_token
    
    # Register token types for a lexer
    def register(self, name, regx, modifier=None):
        self.token_types.append({"name":name, "regx":regx, "mod":modifier})