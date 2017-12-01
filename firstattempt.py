import astdump

x=2
z=3
def f(y,z):
    return y+5


astdump.indented('2')
astdump.indented('2+3')
astdump.indented('f(4,3)')

#astdump.indented('2')
# Module
#  Expr
#    Num
#astdump.indented('2+3')
#Module
#  Expr
#    BinOp
#      Num
#      Add
#      Num
#astdump.indented('f(4,3)')
#Module
#  Expr
#    Call
#      Name
#        Load
#      Num
#      Num
