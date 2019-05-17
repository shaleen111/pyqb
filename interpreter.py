from utils import BasicError


class SymbolTable():
    def __init__(self, parent=None):
        self.symbols = dict()
        self.parent = parent

    def get_var(self, name):
        val = self.symbols.get(name)
        if val is None and self.parent:
            val = self.parent.get_var(name)
        return val

    def set_var(self, name, value):
        self.symbols[name] = value


class Interpreter:
    def __init__(self):
        self.symbol_tbl = SymbolTable()

    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        method = getattr(self, method_name, self.err_visit)
        return method(node)

    def err_visit(self, node):
        node_name = type(node).__name__
        raise BasicError(f"Interpreter Error: AST Node {node_name} Undefined",
                         node.pos_start, node.pos_end)

    def visit_Number(self, node):
        return node.tkn.value

    def visit_Op(self, node):
        if node.left:
            left = self.visit(node.left)
        else:
            left = 0
        right = self.visit(node.right)
        op_type = node.op.type

        if op_type == "MULTIPLY":
            return left*right
        elif op_type == "DIVIDE":
            return left/right
        elif op_type == "ADD":
            return left+right
        elif op_type == "SUBTRACT":
            return left-right
        elif op_type == "POWER":
            return left**right
        elif op_type == "EQUAL":
            return int(left == right)
        elif op_type == "NEQUAL":
            return int(left != right)
        elif op_type == "LEQ":
            return int(left <= right)
        elif op_type == "GEQ":
            return int(left >= right)
        elif op_type == "GREATERTHAN":
            return int(left > right)
        elif op_type == "LESSTHAN":
            return int(left < right)
        elif op_type == "OR":
            return int(left or right)
        elif op_type == "AND":
            return int(left and right)
        raise BasicError("Interpreter Error: Operation Not Defined",
                         node.pos_start, node.pos_end)

    def visit_VarSet(self, node):
        val = self.visit(node.value)
        self.symbol_tbl.set_var(node.tkn.value, val)
        return val

    def visit_VarGet(self, node):
        get = self.symbol_tbl.get_var(node.tkn.value)
        if get is None:
            raise BasicError("Symbol Error: Symbol not Found",
                             node.pos_start, node.pos_end)
        return get

    def visit_IfCondition(self, node):
        for branch in node.cases:
            condition = self.visit(branch["condition"])
            if condition:
                return self.visit(branch["expr"])
        if node.elsecase:
            return self.visit(node.elsecase)

    def exec(self, root):
        return self.visit(root)
