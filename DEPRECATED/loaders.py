import re
from lark import Lark
import json


def wrapInverse(doc, lwrap="~(~", rwrap="~)~"):
    start = 0
    pattern = "\{\{([\S\s]*?)\}\}"
    s = ""
    for match in re.finditer(pattern, doc):
        if match.start() != start:
            s += lwrap + doc[start : match.start()] + rwrap
        s += match.group()
        start = match.end()
    print("WRAP",len(s))
    return s


# LOAD GRAMMAR FROM FILE
def loadParser(grammar_file="fullstache/fullstache.grammar.txt"):
    with open(grammar_file, "r") as f:
        grammar = f.read()
    # parse grammar
    parser = Lark(grammar)
    return parser


# LOAD OBJECT FILE
def loadTemplate(file_dir="template.txt"):
    with open(file_dir, "r") as f:
        template = f.read()

    template = wrapInverse(template)
    return template


# LOAD USER DATA
def loadUserData(data_file="user_data.json"):
    with open(data_file, "r") as f:
        data = json.load(f)
    return data
