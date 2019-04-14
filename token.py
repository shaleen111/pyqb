import re

class Token():
    # Token type will have a name, a value
    def __init__(self, type :str, value):
        self.type = type
        self.value = value
    
    def __str__(self):
        return f"{self.type} : {self.value}" if self.value else f"{self.type}"

class TokenType():
    # Token Type will accept Token Name and Regx
    # Regx will be a regex filter string used to determine whether
    # or not the object found is a particular type of Token
    def __init__(self, name :str, regx :str):
        self.name = name
        self.regx = regx
    
    # Identify whether the substring from the program, pobj
    # is a particular type of Token
    def identify(self, psub):
        return re.search(self.regx, psub)
    
    # Create a Token whose value is the pobj
    # Func is a function that can be used to modify the value of the
    # Token
    def make(self, psub,  func=None):
        tk = Token(self.name, psub)
        if func:
            tk.value = func(tk.value)
        return tk

# Some Tests for Code 
if __name__ == "__main__":
    def num(val):
        return None
    floating = TokenType("TK_FLOAT", "\*")
    a = input(">")
    tk = ""
    if floating.identify(a):
        tk = floating.make(a, num)
    print(tk)