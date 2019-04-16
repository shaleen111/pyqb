import re

class Token(): 
    # Token type will have a name, a value
    def __init__(self, type_name :str, value):
        self.type = type_name
        self.value = value

    def __repr__(self):
        return f"{self.type}:{self.value}" # if not self.value is None else f"{self.type}"

class TokenType():
    # Token Type will accept Token Name and Regx
    # Regx will be a regex filter string used to determine whether
    # or not the object found is a particular type of Token
    def __init__(self, name :str, regx :str, modifier=None):
        self.name = name
        self.regx = regx 
        self.modifier = modifier
    
    # Identify whether the substring from the program, psub
    # is a particular type of Token
    def identify(self, psub):
        return re.match(self.regx, psub)
    
    # Create a Token whose value is in/the psub
    # Func is a function that can be used to modify the value of the
    # Token
    def make(self, psub):
        tk = Token(self.name, self.identify(psub).group(0))
        if self.modifier:
            tk.value = self.modifier(tk.value)
        return tk