import ast

tree = ast.parse("1 + 2")
print("#include <iostream>")
print("using namespace std;")
print("int main() {")
program = " "
for node in ast.walk(tree):
    if isinstance(node, ast.Add):
        program += "+"
    elif isinstance(node, ast.Num):
        program += str(node.n)

print(program+";")
print(" return 0;")
print("}")
