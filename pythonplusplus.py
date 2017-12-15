import ast


#Sturcture to store the datatypes for variables since the AST does not do this
#may not be an appropriate solution when we start working on functions
varTypeStore = {}

#Set datatype of variable
def setType(var, varType):
    varTypeStore[var] = varType
    return

#return datatype of node
#at this point, this function should only be used with the ast.Assign datatype
def getType(tree):
    if isinstance(tree, ast.Num):
        return("int")
    elif(tree == True or tree == False):
        return("bool")
    elif isinstance(tree, ast.NameConstant):
        return(getType(tree.value))
    elif isinstance(tree, ast.BinOp):
        return(getType(tree.left))
    elif isinstance(tree, ast.Name):
        return(varTypeStore[tree.id])
    else:
        return("")


#recusively traverses the AST and checks the datatype of each node.
#Depending on the datatype, translate returns a string corresponding to each node
def translate(tree):
    stringTrans = ""
    if isinstance(tree, ast.Assign):
        varType = getType(tree.value)
        setType(tree.targets[0].id, varType)
        stringTrans += varType + " " + translate(tree.targets[0]) + " = " + translate(tree.value)
        return(stringTrans)
    elif isinstance(tree, ast.Num):
        return(str(tree.n))
    elif isinstance(tree, ast.NameConstant):#boolean
        return(str(tree.value).lower())
    elif isinstance(tree, ast.Name):
        return(tree.id)
    elif isinstance(tree, ast.BinOp):
        stringTrans += translate(tree.left) + translate(tree.op) + translate(tree.right)
        return stringTrans
    elif isinstance(tree, ast.Add):
        return(" + ")
    elif isinstance(tree, ast.Sub):
        return(" - ")
    elif isinstance(tree, ast.Mult):
        return(" * ")
    elif isinstance(tree, ast.Div):
        return(" / ")
    elif isinstance(tree, ast.Mod):
        return(" % ")
    #TODO: still need these operators
    #elif isinstance(tree, ast.FloorDiv) "//"
    #elif isinstance(tree, ast.Pow) "**"
    else:
        return stringTrans


#Breaks down code block into lines and translates each line separately
def translateCodeBlock(tree):
    for i in tree.body:
        print( "\t" + translate(i) + ";")


#Fetch python code and create ast
#TODO: Allow user to choose file
tree = ast.parse(open("./examples/mockPy.py").read())

#TODO: Write to file instead of printing to stdout
print("#include <iostream>")
print("using namespace std;")
print("int main(){")
translateCodeBlock(tree)
print("\treturn 0;")
print("}")


#write to output file
