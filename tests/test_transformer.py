import sys

sys.path.append("fullstache")

from interpreter import Fullstache

userdata = {
    "name": {"first": "MIKE", "last": "SHINODA"},
    "exists": "True",
    "persons": [{"age": 12}, {"age": 44}],
    "money": 32,
    "bool": {"variable": "True"},
}
fullstache = Fullstache()

doc = """
{{#persons as yolo}}iterated {{yolo.age}} and something else here {{yolo.age}}line{{/#}}
"""

result = fullstache.interpret(doc, userdata)

print(result)
