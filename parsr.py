from sys import exit

# Nodes for Parser
class Number():
    def __init__(self, tkn):
        self.tkn = tkn

    def __repr__(self):
        return f"{self.tkn}"

class Op():
    def __init__(self, left, op, right):
        self.left = left
        self.op   = op
        self.right  = right

    def __repr__(self):
        return f"({self.left} {self.op} {self.right})" if self.left else f"{self.op} {self.right}"

# Parser Class
class Parser():
    def __init__(self, tkn_list):
        self.tkns = tkn_list
        self.tknidx = 0
        self.curr_tkn = self.tkns[self.tknidx]

    def next_tkn(self):
        if self.tknidx >= len(self.tkns) - 1:
            return None
        self.tknidx += 1
        self.curr_tkn = self.tkns[self.tknidx]
        return True


    def parse(self):
        return self.expr()
    
    def factor(self):
        curr = self.curr_tkn
        if curr.type == "NUMBER":
            self.next_tkn()
            return Number(curr)
        elif curr.type == "LPAREN":
            self.next_tkn()
            inside_bracket = self.expr()
            if self.curr_tkn.type == "RPAREN":
                self.next_tkn()
                return inside_bracket

    def term(self):
        left = self.factor()
        while self.curr_tkn.type == "MULTIPLY" or  self.curr_tkn.type == "DIVIDE":
            op = self.curr_tkn
            if self.next_tkn():
                right = self.factor()
                left = Op(left, op, right)
            else:
                print("Invalid Syntax")
                exit()
        return left
    
    def expr(self):
        left = self.term()
        while self.curr_tkn.type == "ADD" or  self.curr_tkn.type == "SUBTRACT":
            op = self.curr_tkn
            if self.next_tkn():
                right = self.term()
                left = Op(left, op, right)
            else:
                print("Invalid Syntax")
                exit()
        return left

    def valErr(self, val):
        if val is None:
            print("Value Error")
            exit()
        else:
            return val