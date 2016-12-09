#EXPRESSIONS
class Expr:
    def __init__(self, expr1):
        self.expr1=expr1
    def __str__(self):
        return str(self.expr1)
    def sort(self):
        pass
#ATOMES
class Attr:
    def __init__(self, attr):
        self.attr=attr
    def __str__(self):
        return str(self.attr)

class Rel:
    def __init__(self, rel):
        self.rel=rel
    def __str__(self):
        return str(self.rel)
    def sort(self):
        return None

class Const:
    def __init__(self, const):
        self.const=const
    def __str__(self):
        return str(self.const)

class Select(Expr):
    def __init__(self, expr1, expr2, expr3):
        Expr.__init__(self, expr1)
        self.expr2=expr2
        self.expr3=expr3
    def __str__(self):
        return "(Select * from {} where {}={}) ".format(self.expr3, self.expr1, self.expr2)
    def sort(self):
        return None

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
    pass

class Rename(Expr):
    pass

class Union(Expr):
    pass

class Diff(Expr):
    pass
    
