from utils import BasicError, RELATIONAL_OPERATORS

################################################
# Nodes for Parser
################################################


# Base Node Class
class Node():
    def __init__(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end


# Number Node
class Number(Node):
    def __init__(self, tkn):
        self.tkn = tkn

        super().__init__(self.tkn.pos_start, self.tkn.pos_end)

    def __repr__(self):
        return f"{self.tkn}"


# Binary and Unary Operation Node
# All properties should be of type token
class Op(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

        if self.left:
            super().__init__(self.left.pos_start, self.right.pos_end)
        else:
            super().__init__(self.op.pos_start, self.right.pos_end)

    def __repr__(self):
        if self.left:
            return f"({self.left} {self.op} {self.right})"
        else:
            return f"({self.op} {self.right})"


# Node to get value of a variable
class VarGet(Node):
    def __init__(self, tkn):
        self.tkn = tkn

        super().__init__(self.tkn.pos_start, self.tkn.pos_end)

    def __repr__(self):
        return f"{self.tkn}"


# Node to set the value of a variable
class VarSet(Node):
    def __init__(self, tkn, value):
        self.tkn = tkn
        self.value = value

        super().__init__(self.tkn.pos_start, self.tkn.pos_end)

    def __repr__(self):
        return f"{self.tkn} = {self.value}"


class IfCondition(Node):
    def __init__(self, cases, elsecase):
        self.cases = cases
        self.elsecase = elsecase

        if self.elsecase:
            super().__init__(self.cases[0]["condition"].pos_start,
                             self.elsecase.pos_end)
        else:
            super().__init__(self.cases[0]["condition"].pos_start,
                             self.cases[len(self.cases) - 1]["expr"].pos_end)

    def __repr__(self):
        if self.elsecase:
            return f"cases : {self.cases}, else : {self.elsecase}"
        else:
            return f"cases : {self.cases}"


class WhileLoop(Node):
    def __init__(self, condition, expr):
        self.condition = condition
        self.expr = expr
        super().__init__(self.condition.pos_start, self.expr.pos_end)

    def __repr__(self):
        return f"condition : {self.condition}, exprsn : {self.expr}"

################################################
# Parser
################################################


# Parser Class
class Parser():
    def __init__(self):
        pass

    # Advances position in token_list
    # May throw error if at the last index of
    # string and flag is enabled
    def next_tkn(self, throw_error=False):
        if self.tknidx >= len(self.tkns) - 1:
            if throw_error:
                raise BasicError("Invalid Syntax: Incomplete Expression",
                                 self.curr_tkn.pos_start,
                                 self.curr_tkn.pos_end)
            else:
                return
        self.tknidx += 1
        self.curr_tkn = self.tkns[self.tknidx]
        return True

    def expect(self, tkntypes):
        curr = self.curr_tkn
        t = curr.type
        if t in tkntypes:
            return
        else:
            raise BasicError(f"Invalid Syntax: Expected {tkntypes} not {t}",
                             curr.pos_start, curr.pos_end)

    # Recursive Descent Implementation of Parser
    def parse(self, tkn_list):
        if len(tkn_list) > 0:
            self.tkns = tkn_list
            self.tknidx = 0
            self.curr_tkn = self.tkns[self.tknidx]
            return self.expr()
        else:
            raise BasicError("Invalid Syntax: Must Enter Something", 0, 0)

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

    def parse_if(self):
        self.next_tkn(True)
        cases = list()
        condition = self.bin_op(self.comp_expr, ("AND", "OR"))
        self.expect("KEYWORD_THEN")
        self.next_tkn(True)
        expr = self.expr()
        cases.append({"condition": condition, "expr": expr})

        while self.curr_tkn.type == "KEYWORD_ELSEIF":
            cases = cases + self.parse_if()

        return cases

    def atom(self):
        # atom : NUMBER | LPAREN expr RPAREN | IDENTIFIER
        curr = self.curr_tkn
        self.expect(("NUMBER", "LPAREN", "IDENTIFIER", "KEYWORD_IF",
                     "KEYWORD_WHILE"))

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

        elif curr.type == "KEYWORD_IF":
            all_cases = self.parse_if()
            elsecase = None

            if self.curr_tkn.type == "KEYWORD_ELSE":
                self.next_tkn(True)
                elsecase = self.expr()
            self.expect("KEYWORD_ENDIF")
            curr = IfCondition(all_cases, elsecase)

        elif curr.type == "KEYWORD_WHILE":
            self.next_tkn(True)
            condition = self.bin_op(self.comp_expr, ("AND", "OR"))
            expr = self.expr()
            self.expect("KEYWORD_WEND")
            curr = WhileLoop(condition, expr)

        self.next_tkn()
        return curr

    def power(self):
        # power : atom (^ atom)*
        return self.bin_op(self.atom, ("POWER"))

    def factor(self):
        curr = self.curr_tkn

        # Adds support for negative numbers
        if curr.type in ("ADD", "SUBTRACT"):
            self.next_tkn(True)
            return Op(None, curr, self.power())
        return self.power()

    def term(self):
        # term : power ((MULTIPLY|DIVIDE) power)*
        return self.bin_op(self.factor, ("MULTIPLY", "DIVIDE"))

    def arith_expr(self):
        return self.bin_op(self.term, ("ADD", "SUBTRACT"))

    def comp_expr(self):
        return self.bin_op(self.arith_expr, RELATIONAL_OPERATORS)

    def expr(self):
        # expr : term ((MULTIPLY|DIVIDE) term)*
        #      : KEYWORD:LET IDENTIFIER EQ expr
        if self.curr_tkn.type == "KEYWORD_LET":
            self.next_tkn(True)
            self.expect("IDENTIFIER")
            var_token = self.curr_tkn
            self.next_tkn(True)
            self.expect("EQUAL")
            self.next_tkn(True)

            return VarSet(var_token, self.expr())
        elif self.curr_tkn.type == "IDENTIFIER":
            var_token = self.curr_tkn
            self.next_tkn()
            if self.curr_tkn.type == "EQUAL":
                self.next_tkn(True)
                return VarSet(var_token, self.expr())
            else:
                self.tknidx -= 1
                self.curr_tkn = self.tkns[self.tknidx]
        return self.bin_op(self.comp_expr, ("AND", "OR"))
