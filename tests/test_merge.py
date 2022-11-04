from lark import Transformer, Tree
from lark.visitors import Interpreter, merge_transformers

data = {"persons": [{"name": "MIKE", "age": 20}, {"name": "SHINODA", "age": 30}]}


class TBase(Transformer):
    def start(self, children):
        print(children)
        return children[0] + "bar"


class TImportedGrammar(Interpreter):
    def enum(self, children):
        print(children)
        return "foo"


composed_transformer = merge_transformers(TBase(), imported=TImportedGrammar())

t = Tree("start", [Tree("imported__enum", 
[Tree("variable",["persons"])])])

assert composed_transformer.transform(t) == "foobar"
print(composed_transformer.transform(t))
