import ast

tree = ast.parse(open("exampleCode.py").read())
lines = tree.body
for nodes in lines:
    print(ast.dump(nodes))
