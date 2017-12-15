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
    elif isinstance(tree, ast.BoolOp):
        return("bool")
    elif isinstance(tree, ast.UnaryOp):
        return("bool")
    elif isinstance(tree, ast.Compare):
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

    #variables
    if isinstance(tree, ast.Assign):
        varType = getType(tree.value)
        setType(tree.targets[0].id, varType)
        stringTrans += varType + " " + translate(tree.targets[0]) + " = " + translate(tree.value)
        return(stringTrans)
    elif isinstance(tree, ast.Name):
        return(tree.id)

    #Integers
    elif isinstance(tree, ast.Num):
        return(str(tree.n))
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
    #TODO: still need decimal numbers
    #TODO: still need these operators:
    #elif isinstance(tree, ast.FloorDiv) "//"
    #elif isinstance(tree, ast.Pow) "**"

    #Booleans
    elif isinstance(tree, ast.NameConstant):
        return(str(tree.value).lower())
    elif isinstance(tree, ast.BoolOp):
        stringTrans += translate(tree.values[0]) + translate(tree.op) + translate(tree.values[1])
        return(stringTrans)
    elif isinstance(tree, ast.UnaryOp):
        stringTrans += translate(tree.op) + translate(tree.operand)
        return(stringTrans)
    elif isinstance(tree, ast.Compare):
        stringTrans += translate(tree.left) + translate(tree.ops[0]) + translate(tree.comparators[0])
        return(stringTrans)
    elif isinstance(tree, ast.And):
        return(" && ")
    elif isinstance(tree, ast.Or):
        return(" || ")
    elif isinstance(tree, ast.Not):
        return("!")
    elif isinstance(tree, ast.Eq):
        return(" == ")
    elif isinstance(tree, ast.NotEq):
        return(" != ")
    elif isinstance(tree, ast.Gt):
        return(" > ")
    elif isinstance(tree, ast.Lt):
        return(" < ")
    elif isinstance(tree, ast.GtE):
        return(" >= ")
    elif isinstance(tree, ast.LtE):
        return(" <= ")
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
