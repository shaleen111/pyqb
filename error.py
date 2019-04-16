from sys import exit

# Error Class
class Error():
    def __init__(self, text, type):
        self.text = text
        self.type = type
    
    def call(self, position):
        print(f"{self.type} Error at {position} : {self.text}")
        exit()