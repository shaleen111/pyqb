class Token():
    def __init__(self, type :str, value, regx):
        self.type = type
        self.value = value
        self.regx = regx        
    
    def __str__(self):
        return f"{self.type} : {self.value}"

if __name__ == "__main__":
    tk = Token(TK_INTEGER, 2)
    print(tk)