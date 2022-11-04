from lark import Lark

grammar = """
?start:expr*

?expr : "{" "{" "#" VARIABLE "as" VARIABLE ["," VARIABLE] "}" "}" expr* "{""{" "/" "#" "}""}" -> enumerator 
      | "{" "{" VARIABLE "}" "}"
      | JUNK  -> clean


VARIABLE : /[a-zA-Z_$][a-zA-Z_\.0-9]*/
JUNK : /~\(~[\S\s]+?~\)~/ 

%import common.WS
%ignore WS
"""


def buildParser():
    return Lark(grammar)
