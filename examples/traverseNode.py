import ast

tree = ast.parse("1 + 2")
for node in ast.walk(tree):
    print(ast.dump(node))
