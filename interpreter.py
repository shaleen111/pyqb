from utils import BasicError


class SymbolTable():
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def get_var(self, name):
        val = self.symbols.get(name)
        if val is None:
            if self.parent:
                val = self.parent.get_var(name)
        return val

    def set_var(self, name, value):
        self.symbols[name] = value


class Interpreter:
    def __init__(self, root):
        self.root = root
        self.symbol = SymbolTable()

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
        # elif op_type == "POWER":
        #     return left**right
        raise BasicError("Interpreter Error: Operation Not Defined",
                         node.pos_start, node.pos_end)

    def visit_VarSet(self, node):
        return self.symbol.set_var(node.tkn.value, node.value)

    def visit_VarGet(self, node):
        vars = self.symbol.get_var(node.tkn.value)
        if vars is None:
            raise BasicError("Symbol Error: Symbol not Found",
                             node.pos_start, node.pos_end)

    def exec(self):
        return self.visit(self.root)
