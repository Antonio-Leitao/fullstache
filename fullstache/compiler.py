"""
ACCEPTS: tree and user data
SPITS: compiled code
"""


class Compiler:
    def __init__(self, user_data):
        self.data = user_data

    def interpret(self, t):
        self.__getattribute__(t)()

    def foo(self):
        print("foo")

    def compile(self, tree):
        for child in tree.children:
            self.compilation.append(self.interpret(child))
        return self.compilation


comp = Compiler(data)
comp.interpret("foo")
