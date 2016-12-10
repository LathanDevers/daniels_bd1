#CONSTS
ALL="ALL"

#HERITAGE
class Expr:
    def __init__(self, expr1):
        self.expr1=expr1
    def __str__(self):
        return str(self.expr1)
    def getType(self):
        return type(self.expr1)
    def sort(self):
        return ALL
    
#ATOMES
class Attr(Expr):
    def __init__(self, attr):
        Expr.__init__(self, attr)
    def __str__(self):
        return str(self.expr1)

class Rel(Expr):
    def __init__(self, rel):
        Expr.__init__(self, rel)
    def __str__(self):
        return str(self.expr1)
    def sort(self):
        return ALL

class Const(Expr):
    def __init__(self, const):
        Expr.__init__(self, const)
    def __str__(self):
        return str(self.expr1)

#EXPRESSIONS
class Select(Expr):
    def __init__(self, expr1, expr2, expr3):
        if (expr3.sort()==ALL or str(expr1) in expr3.sort()) and expr1.getType()==expr2.getType():
            Expr.__init__(self, expr1)
            self.expr2=expr2
            self.expr3=expr3
        elif expr1.getType()!=expr2.getType():
            print("error types : {} is {} and {} is {}".format(expr1, expr1.getType(), expr2, expr2.getType()))
        else:
            print("{} not in {}".format(expr1, expr2))
    def __str__(self):
        return "(Select * from {} where {}={})".format(self.expr3, self.expr1, self.expr2)
    def sort(self):
        return self.expr3.sort()

class Project(Expr):
    def __init__(self, attrs, expr1):
        Expr.__init__(self, expr1)
        self.attrs=attrs
    def __str__(self):
        getStr="(select "+str(self.attrs[0])+", "
        for i in range(1, len(self.attrs)):
            getStr+=str(self.attrs[i])+", "
        getStr+=" from {}) ".format(self.expr1)
        return getStr
    def sort(self):
        sortL=[]
        for i in self.attrs:
            sortL.append(str(i))
        return sortL

class Join(Expr):
    def __init__(self, expr1, expr2):
        pass

class Rename(Expr):
    pass

class Union(Expr):
    def __init__(self, expr1, expr2):
        pass

class Diff(Expr):
    pass
    
