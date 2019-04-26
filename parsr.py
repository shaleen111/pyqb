
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
# All properties should be of type token
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


# Node to get value of a variable
class VarGet():
    def __init__(self, tkn):
        self.tkn = tkn

    def __repr__(self):
        return f"{self.tkn}"


# Node to set the value of a variable
class VarSet():
    def __init__(self, tkn, value):
        self.tkn = tkn
        self.value = value

    def __repr__(self):
        return f"{self.tkn} = {self.value}"

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
            raise Exception("Invalid Input: Must Enter Something")

    # Advances position in token_list
    # May throw error if at the last index of
    # string and flag is enabled
    def next_tkn(self, throw_error=False):
        if self.tknidx >= len(self.tkns) - 1:
            if throw_error:
                raise Exception("Invalid Syntax: Incomplete Expression")
            else:
                return
        self.tknidx += 1
        self.curr_tkn = self.tkns[self.tknidx]
        return True

    def expect(self, tkntypes):
        curr = self.curr_tkn.type
        if curr in tkntypes:
            return
        else:
            raise Exception(f"Invalid Syntax: Expected {tkntypes} not {curr}")

    # Recursive Descent Implementation of Parser
    def parse(self):
        return self.expr()

    # Abstractions for binary operation parsing
    # for use with expr and term and power functions
    def bin_op(self, func, ops):
        left = func()

        # Allow chainging of operations
        while self.curr_tkn.type in ops:
            op = self.curr_tkn
            self.next_tkn(True)
            right = func()
            left = Op(left, op, right)

        return left

    def atom(self):
        # atom : NUMBER | LPAREN expr RPAREN | IDENTIFIER
        curr = self.curr_tkn
        self.expect(("NUMBER", "LPAREN", "IDENTIFIER"))

        if curr.type == "NUMBER":
            curr = Number(curr)

        # Add support for variables
        elif curr.type == "IDENTIFIER":
            curr = VarGet(curr)

        # Adds support for brackets
        elif curr.type == "LPAREN":
            self.next_tkn(True)
            inside_bracket = self.expr()
            self.expect("RPAREN")
            curr = inside_bracket
        self.next_tkn()
        return curr

    def power(self):
        # power : atom (^ atom)*
        return self.bin_op(self.atom, ("POWER"))

    def factor(self):
        curr = self.curr_tkn

        # Adds support for negative numbers
        if val in ("ADD", "SUBTRACT"):
            self.next_tkn(True)
            val = Op(None, val, self.power())
            return val
        return self.power()

    def term(self):
        # term : power ((MULTIPLY|DIVIDE) power)*
        return self.bin_op(self.power, ("MULTIPLY", "DIVIDE"))

    def expr(self):
        # expr : term ((MULTIPLY|DIVIDE) term)*
        #      : KEYWORD:LET IDENTIFIER EQ expr
        if self.curr_tkn.type == "KEYWORD":
            self.next_tkn(True)
            self.expect("IDENTIFIER")
            var_token = self.curr_tkn
            self.next_tkn(True)
            self.expect("EQUAL")
            self.next_tkn(True)

            return VarSet(var_token, self.expr())
        else:
            return self.bin_op(self.term, ("ADD", "SUBTRACT"))
