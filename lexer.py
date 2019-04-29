from re import compile
from utils import BasicError


# Class for Tokens
class Token():
    # Token type will have a name and a value
    def __init__(self, type_name, value, pos_start, pos_end):
        self.type = type_name
        self.value = value
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f"{self.type}:{self.value}"


# Class for Lexer
class Lexer():
    # Initializes lexer
    # Skip refers to any stream of chars to be ignored by lexer
    def __init__(self, token_types=list(), skip="\s+"):
        self.token_types = token_types
        self.skip = compile(skip)

    # Goes to next token
    def next_token(self):
        # Ignore whitespace
        skip_exist = self.skip.match(self.program, self.position)
        if skip_exist:
            self.position = skip_exist.end()

        # Checks if we are at the very end of the program to be lexed
        if self.position >= len(self.program):
            return None

        # Iterates through token_types to check if any token is found
        for tkn_t in self.token_types:
            result = tkn_t["regx"].match(self.program, self.position)
            if result:
                # Create a Token Object having value of the first match
                tkn = Token(tkn_t["name"], result.group(0),
                            self.position,
                            self.position + len(result.group(0)) - 1)
                # Check if user has provided a modifier function
                if tkn_t["mod"]:
                    tkn.value = tkn_t["mod"](tkn.value)
                self.position = result.end()
                return tkn
        raise BasicError(f"Lexer Error: Unknown Token at {self.position + 1}",
                         self.position, self.position)

    # Return List of Tokens
    def tokenize(self, program):
        self.program = program
        self.position = 0

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
        self.token_types.append({"name": name, "regx": compile(regx),
                                "mod": modifier})
