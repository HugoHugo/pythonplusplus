import ast
tree = ast.parse(open("mockPy.py").read())
print(ast.dump(tree))

#2*3
#Output:
#Module(body=[Expr(value=BinOp(left=Num(n=2), op=Mult(), right=Num(n=3)))])

#x=5
#Output:
#Module(body=[Assign(targets=[Name(id='x', ctx=Store())], value=Num(n=5))])

#x=5
#y=6
#x+y
#Output:
#Module(body=[Assign(targets=[Name(id='x', ctx=Store())], value=Num(n=5)), Assign(targets=[Name(id='y', ctx=Store())], value=Num(n=6)), Expr(value=BinOp(left=Name(id='x', ctx=Load()), op=Add(), right=Name(id='y', ctx=Load())))])
