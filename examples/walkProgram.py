import ast
tree = ast.parse(open("mockPy.py").read())
walkedTree = ast.walk(tree)
for i in walkedTree:
    print(ast.dump(i))


#Module(body=[Assign(targets=[Name(id='x', ctx=Store())], value=Num(n=5)), Assign(targets=[Name(id='y', ctx=Store())], value=Num(n=6)), Expr(value=BinOp(left=Name(id='x', ctx=Load()), op=Add(), right=Name(id='y', ctx=Load())))])
#Assign(targets=[Name(id='x', ctx=Store())], value=Num(n=5))
#Assign(targets=[Name(id='y', ctx=Store())], value=Num(n=6))
#Expr(value=BinOp(left=Name(id='x', ctx=Load()), op=Add(), right=Name(id='y', ctx=Load())))
#Name(id='x', ctx=Store())
#Num(n=5)
#Name(id='y', ctx=Store())
#Num(n=6)
#BinOp(left=Name(id='x', ctx=Load()), op=Add(), right=Name(id='y', ctx=Load()))
#Store()
#Store()
#Name(id='x', ctx=Load())
#Add()
#Name(id='y', ctx=Load())
#Load()
#Load()
