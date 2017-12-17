import ast

#Global variables

arrayCounter=0
#Sturcture to store the datatypes for variables since the AST does not do this
#may not be an appropriate solution when we start working on functions
varTypeStore = {}
#used for indentation for structures such as if, for, while, and functions
indentationLevel = 0

#Set datatype of variable
def setType(var, varType):
    varTypeStore[var] = varType
    return

#return datatype of node
#at this point, this function should only be used with the ast.Assign datatype
def getType(tree):
    if isinstance(tree, ast.Num):
        if type(tree.n) == type(0.234): #does not matter what number as long as float
            return("float")
        return("int")
    elif isinstance(tree, ast.Str):
        return("string")
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

    if isinstance(tree, ast.List):
        global arrayCounter
        type = getType(tree.elts[0])
        stringTrans += type + " defArray" + str(arrayCounter) + "[] = {"
        arrayCounter += 1

        for i in range(0,len(tree.elts)):
            if(i== len(tree.elts)-1):
                stringTrans += translate(tree.elts[i])
                break
            stringTrans += translate(tree.elts[i]) + ","
        stringTrans += "}"
        return stringTrans

    elif isinstance(tree, ast.While):
        stringTrans = "while("
        stringTrans += translate(tree.test)
        stringTrans += ") {\n"
        stringTrans += translateCodeBlock(tree.body)
        stringTrans += "\n"*indentationLevel + "}"
        return stringTrans


    elif isinstance(tree, ast.For): #'for in range' type of loop
        if tree.iter.func.id == "range":
            stringTrans = "for(int " + tree.target.id + "="
            v1 = translate(tree.iter.args[0])
            v2 = translate(tree.iter.args[1])
            stringTrans += v1 + "; " + tree.target.id + " < " + v2 + "; ++" + tree.target.id + ") {\n"
            stringTrans += translateCodeBlock(tree.body)
            stringTrans += "\n"*indentationLevel + "}"
            return stringTrans
        return "Not defined"

    elif isinstance(tree, ast.Try):
        stringTrans = "try{ \n"
        stringTrans += translateCodeBlock(tree.body)
        stringTrans += "   \n      }"
        if tree.handlers:
            stringTrans += " catch(...){\n"
            stringTrans += translateCodeBlock(tree.handlers)
            return stringTrans
        return stringTrans

    elif isinstance(tree, ast.Expr):
        stringTrans = ""
        stringTrans += translate(tree.value)
        return stringTrans

    elif isinstance(tree, ast.ExceptHandler):
        stringTrans = ""
        stringTrans += translateCodeBlock(tree.body)
        stringTrans += "\n"*indentationLevel + "}"
        return stringTrans
    #variables
    elif isinstance(tree, ast.Assign):
        varType = ""
        if(tree.targets[0].id not in varTypeStore.keys()): #if the variable's type is not yet tracked
            varType = getType(tree.value) + " "
            setType(tree.targets[0].id, varType)
        stringTrans += varType + translate(tree.targets[0]) + " = " + translate(tree.value)
        return(stringTrans)
    elif isinstance(tree, ast.Name):
        return(tree.id)

    #Integers
    elif isinstance(tree, ast.Num):
        return(str(tree.n))
    elif isinstance(tree, ast.BinOp):
        if(isinstance(tree.op, ast.Pow)):
            stringTrans += "pow(" + translate(tree.left) + translate(tree.op) + translate(tree.right) + ")"
            return stringTrans
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
    elif isinstance(tree, ast.Pow):
        return(",")
    #TODO: still need decimal numbers
    #TODO: still need these operators:
    #elif isinstance(tree, ast.FloorDiv) "//"
    #elif isinstance(tree, ast.Pow) "**"

    #strings
    elif isinstance(tree, ast.Str):
        return('"' + tree.s + '"')

    #Booleans
    elif isinstance(tree, ast.NameConstant):
        return(str(tree.value).lower())
    elif isinstance(tree, ast.BoolOp):
        if(isinstance(tree.op, ast.And) and (isinstance(tree.values[1], ast.BoolOp))):
            if isinstance(tree.values[1].op, ast.Or):
                stringTrans += translate(tree.values[0]) + translate(tree.op) + "(" + translate(tree.values[1]) + ")"
                return(stringTrans)
        stringTrans += translate(tree.values[0]) + translate(tree.op) + translate(tree.values[1])
        return(stringTrans)
    elif isinstance(tree, ast.UnaryOp):
        if isinstance (tree.operand, ast.NameConstant): #checking order of operations
            stringTrans += translate(tree.op) + translate(tree.operand)
        else:
            stringTrans += translate(tree.op) + "(" + translate(tree.operand) + ")"
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

    #if statements
    elif isinstance(tree, ast.If):
        stringTrans += "if(" + translate(tree.test) + "){\n"
        stringTrans += translateCodeBlock(tree.body) + "\t"*indentationLevel + "}"
        stringTrans += translateElseIf(tree.orelse)
        return stringTrans
    else:
        return stringTrans


def translateElseIf(tree):
    stringTrans = ""
    if(not tree): #if there is not else or elif
        return stringTrans
    elif(isinstance(tree[0], ast.If)): #if there is an elif
        stringTrans += "else if(" + translate(tree[0].test) + "){\n"
        stringTrans += translateCodeBlock(tree[0].body) + "\t"*indentationLevel + "}"
        stringTrans += translateElseIf(tree[0].orelse)
        return stringTrans
    else: #if there is an else
        stringTrans += "else{\n"
        stringTrans += translateCodeBlock(tree) + "\t"*indentationLevel + "}"
        return stringTrans


#Breaks down code block into lines and translates each line separately
def translateCodeBlock(tree):
    transString = ""
    global indentationLevel
    indentationLevel += 1
    for i in tree:
        transString += "\t"*indentationLevel + translate(i)
        if isinstance(i, ast.If):
            transString += "\n"
        else:
            transString += ";\n"
    indentationLevel -= 1
    return(transString)

#Fetch python code and create ast
#TODO: Allow user to choose file
tree = ast.parse(open("./examples/mockPyLists.py").read())

#TODO: Write to file instead of printing to stdout
print("#include <iostream>")
print("#include <string>")
print("#include <math.h>")
print("using namespace std;")
print("int main(){")
print(translateCodeBlock(tree.body))
print("\treturn 0;")
print("}")


#write to output file
#


# print(ast.dump(tree))