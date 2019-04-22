from error import err

################################################
# Nodes for Parser
################################################


# Number Node
class Number():
    def __init__(self, tkn):
        self.tkn = tkn

    def __repr__(self):
        return f"{self.tkn}"


# Binary and Unary Operation Node
class Op():
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        if self.left:
            return f"({self.left} {self.op} {self.right})"
        else:
            return f"({self.op} {self.right})"

################################################
# Parser
################################################


# Parser Class
class Parser():
    def __init__(self, tkn_list):
        if len(tkn_list) > 0:
            self.tkns = tkn_list
            self.tknidx = 0
            self.curr_tkn = self.tkns[self.tknidx]
        else:
            err("Must Enter Something")

    # Advances position in token_list
    # May throw error if at the last index of
    # string and flag is enabled
    def next_tkn(self, throw_error=False):
        if self.tknidx >= len(self.tkns) - 1:
            if throw_error:
                err("Invalid Syntax: Incomplete Expression")
            else:
                return
        self.tknidx += 1
        self.curr_tkn = self.tkns[self.tknidx]
        return True

    # Recursive Descent Implementation of Parser
    def parse(self):
        return self.expr()

    # Factor refers to any number or
    # anything inside paranthesis
    def factor(self):
        curr = self.curr_tkn
        if curr.type == "NUMBER":
            self.next_tkn()
            return Number(curr)
        elif curr.type == "LPAREN":
            self.next_tkn(True)
            inside_bracket = self.expr()
            if self.curr_tkn.type == "RPAREN":
                self.next_tkn()
                return inside_bracket
            else:
                err("Invalid Syntax: Expected )")
        # Line adds support for negative numbers
        # ie. -5,3,-2 are all valid inputs
        elif curr.type in ("ADD", "SUBTRACT"):
            self.next_tkn(True)
            return Op(None, curr, self.expr())
        else:
            err(f"Invalid Syntax: {curr.type} is not a UNARY OPERATOR")

    # Term is used to refer to multiplication/division
    def term(self):
        left = self.factor()
        while self.curr_tkn.type in ("MULTIPLY", "DIVIDE"):
            op = self.curr_tkn
            self.next_tkn(True)
            right = self.factor()
            left = Op(left, op, right)
        return left

    # Expression is used to refer to Add/Subtract
    # It should be the root node of the AST
    def expr(self):
        left = self.term()
        while self.curr_tkn.type in ("ADD", "SUBTRACT"):
            op = self.curr_tkn
            self.next_tkn(True)
            right = self.term()
            left = Op(left, op, right)
        return left
