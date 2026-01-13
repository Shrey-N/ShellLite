
class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent
    def get(self, name):
        if name in self.variables: return self.variables[name]
        if self.parent: return self.parent.get(name)
        raise NameError(f"Var '{name}' not found")
    def set(self, name, val):
        self.variables[name] = val

class Interpreter:
    def __init__(self):
        print("DEBUG: MINIMAL INTERPRETER LOADED")
        self.global_env = Environment()
        self.current_env = self.global_env
        self.functions = {}
        self.builtins = {
            'str': str,
            'print': print
        }
    def visit(self, node):
        print(f"Visiting {type(node).__name__}")
        return None
