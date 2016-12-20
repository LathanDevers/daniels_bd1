#CONSTS
ALL="ALL"

#TABLE
class Table:
    def __init__(self, name, attrNames, attrTypes, attrs):
        self.name=name
        self.attrNames=attrNames
        self.attrTypes=attrTypes
        self.attrs=attrs
    def __str__(self):
        ret=""
        ret+=self.name
        ret+="\n"
        ret+="-"*len(self.name)+"\n"
        for i in range(len(self.attrNames)):
            ret+=str(self.attrNames[i])+" "*(10-len(str(self.attrNames[i])))
        ret+="\n"
        ret+="-"*30
        ret+="\n"
        for i in range(len(self.attrs)):
            for j in range(len(self.attrs[i])):
                for h in range(len(self.attrs[i][j])):
                    ret+=str(self.attrs[i][j][h])+" "*(10-len(str(self.attrs[i][j][h])))
                ret+="\n"
            ret+="\n"
        ret+="\n"
        return ret
    def sort(self):
        pass
    def setAttrName(self, oldName, newName):
        for i in range(len(self.attrNames)):
            if self.attrNames[i]==oldName:
                self.attrNames[i]=newName
                return True
            else:
                return False

#HERITAGE
class Expr:
    def __init__(self, expr1):
        self.expr1=expr1
    def __str__(self):
        return str(self.expr1)
    def sort():
        return ALL
    def validate(attrNames):
        return True
    def find(n, tab):
        for i in range(len(tab)):
            if n==tab[i]:
                return True
        return False
    def comp(tab1, tab2):
        for i in range(len(tab1)):
            if find(tab1[i], tab2)==False:
                return False
        return True
    
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
        Expr.__init__(self, expr1)
        self.expr2=expr2
        self.expr3=expr3
    def __str__(self):
        return "(select * from {} where {}={})".format(self.expr3, self.expr1, self.expr2)
    def sort(self):
        return self.expr3.sort()
    def validate():
        for i in self.expr3.sort():
            if self.expr1==self.expr3.sort()[i]:
                return True
        return False

class Project(Expr):
    def __init__(self, attrs, expr1):
        Expr.__init__(self, expr1)
        self.attrs=attrs
    def __str__(self):
        getStr="(select "
        for i in range(len(self.attrs)-1):
            getStr+=str(self.attrs[i])+", "
        getStr+="{} from {})".format(self.attrs[-1], self.expr1)
        return getStr
    def sort(self):
        sortL=[]
        for i in self.attrs:
            sortL.append(str(i))
        return sortL
    def validate():
        return comp(self.attrs, self.expr1.sort())

class Join(Expr):
    def __init__(self, expr1, expr2):
        Expr.__init__(self, expr1)
        self.expr2=expr2
    def __str__(self):
        return "(select * from "+str(self.expr1)+" natural join "+str(self.expr2)+")"
    def sort(self):
        return self.expr1.sort()+self.expr2.sort()
        
            

class Rename(Expr):
    def __init__(self, expr1, expr2, expr3):
        pass
    def __str__(self):
        pass

class Union(Expr):
    def __init__(self, expr1, expr2):
        pass
    def __str__(self):
        pass
    def sort():
        return self.expr1.sort()
    def validate():
        if self.expr1.sort()!=self.expr2.sort():
            return False
        return True

class Diff(Expr):
    def __init__(self, expr1, expr2):
        pass
    def __str__(self):
        pass
    def sort():
        return self.expr1.sort()
    def validate():
        if self.expr1.sort()!=self.expr2.sort():
            return False
        return True
    
