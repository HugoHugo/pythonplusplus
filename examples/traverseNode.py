import ast

tree = ast.parse("1 + 2")
for node in ast.walk(tree):
    print(ast.dump(node))

#Output:
#Module(body=[Expr(value=BinOp(left=Num(n=1), op=Add(), right=Num(n=2)))])
#Expr(value=BinOp(left=Num(n=1), op=Add(), right=Num(n=2)))
#BinOp(left=Num(n=1), op=Add(), right=Num(n=2))
#Num(n=1)
#Add()
#Num(n=2)
