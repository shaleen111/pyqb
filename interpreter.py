vars = {}


class Interpreter:
    def __init__(self, root):
        self.root = root

    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        method = getattr(self, method_name, self.err_visit)
        return method(node)

    def err_visit(self, node):
        node_name = type(node).__name__
        raise Exception(f"Interpreter Error: Unknown AST Node {node_name}")

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
        raise Exception("Interpreter Error: Operation Not Defined")

    def visit_VarSet(self, node):
        name = node.tkn.value
        val = self.visit(node.value)
        vars[name] = val
        return vars[name]

    def visit_VarGet(self, node):
        return vars[node.tkn.value]

    def exec(self):
        return self.visit(self.root)
