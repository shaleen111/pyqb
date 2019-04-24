class Interpreter:
    def __init__(self, root):
        self.root = root

    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        method = getattr(self, method_name, err_visit)
        return method(node)

    def err_visit(self, node):
        raise Exception(f"Error: Unknown AST Node {type(node).__name__}")

    def visit_Number(self, node):
        return self.root.tkn.value

    def visit_Op(self, node):
        if self.left:
            left = self.visit(node.left)
        else:
            left = 0
        right = self.visit(node.right)
        op_type = node.op.type

        if op == "MULTIPLY":
            return left*right
        elif op == "DIVIDE":
            return left/right
        elif op == "ADD":
            return left+right
        elif op == "SUBTRACT":
            return left-right

    def exec(self):
        return self.visit(self.root)
