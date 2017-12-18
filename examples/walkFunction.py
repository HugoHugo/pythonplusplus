import ast
tree = ast.parse(open("mockPyFunction.py").read())
#print len(tree)
#print (dir(tree.body[0]))
walkedTree = ast.walk(tree)
for i in walkedTree:
  print ast.dump(i)
  #print(ast.dump(i))
  #print ast.dump(i)
  #print 1
#print len(ast.dump(tree.body[0].args))
#print ast.dump(tree.body[0].args)

#print(ast.dump(tree))
#print(ast.dump(tree.body[0].body[-1]))



