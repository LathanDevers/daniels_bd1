########################################################################################################################
#               FICHIER CONTENANT LES DEFINITIONS DES FONCTIONS UTILISEES DANS LE FICHIER MAIN                         #
########################################################################################################################
#
# INDEX:
#
# CLASSES:
#
#   Table(self, name="", attrNames=[], attrTypes=[]):
#       name
#       attrNames
#       attrTypes
#       attrs
#       ---------
#       getType(self, attrName)
#       getPosition(self, attrName)
#       getAttrType(self, position)
#       getAttrName(self, position)
#       setName(self, newName)
#       setAttrNames(self, newAttrNames)
#       setAttrName(self, position, newAttrName)
#       setAttrTypes(self, newAttrTypes)
#       setAttrType(self, position, newAttrType)
#       display(self)
#
#   Expr(self):
#       table
#       expression
#       traduction
#       ----------
#       setExpression(self, newExpression)
#       setTraduction(self, newTraduction)
#       getTraduction(self)
#       display(self)
#
#   Rel(self, relName):Expr
#       name
#       ----
#       validation(self, tables)
#
#   Const(self, data):
#       data
#       atom
#       ----
#       getType(self)
#       getTraduction(self)
#
#   Attr(self, attrName):
#       name
#       atom
#       ----
#       getTraduction(self)
#
#   Select(self, attr, comp, expr):Expr
#       attr
#       comp
#       expr
#       ----
#       validation(self, tables)
#
#   Project(self, attrs, expr):Expr
#       attrs
#       expr
#       ----
#       validation(self, tables)
#
#   Join(self, expr1, expr2):Expr
#       expr1
#       expr2
#       ----
#       validation(self, tables)
#
#   Rename(self, attrNames1, attrNames2, expr):Expr
#       attrNames1
#       attrNames2
#       expr
#       ----
#       validation(self, tables)
#
#   Union(self, expr1, expr2):Expr
#       expr1
#       expr2
#       ----
#       validation(self, tables)
#
#   Diff(self, expr1, expr2):Expr
#       expr1
#       expr2
#       ----
#       validation(self, tables)
#
#########################################################################################################################

from Functions import *

#TABLE : class Table :

class Table:
    def __init__(self, name="", attrNames=[], attrTypes=[]):
        self.name=name
        self.attrNames=attrNames
        self.attrTypes=attrTypes
        self.attrs=[]
    def getType(self, attrName):
        return self.getAttrType(self.getPosition(attrName))
    def getPosition(self, attrName):
        for i in range(len(self.attrNames)):
            if attrName==self.getAttrName(i):
                return i
    def getAttrType(self, position):
        return self.attrTypes[position]
    def getAttrName(self, position):
        return self.attrNames[position]
    def setName(self, newName):
        self.name=newName
    def setAttrNames(self, newAttrNames):
        self.attrNames=newAttrNames
    def setAttrName(self, position, newAttrName):
        self.attrNames[position]=newAttrName
    def setAttrTypes(self, newAttrTypes):
        self.attrTypes=newAttrTypes
    def sefAttrType(self, position, newAttrType):
        self.attrTypes[position]=newAttrType
    def display(self):
        ret=""
        ret+=self.name
        ret+="\n"
        ret+="-"*len(self.name)+"\n"
        for i in range(len(self.attrNames)):
            tag=str(self.attrNames[i])+"("+str(self.attrTypes[i])+")"
            ret+=tag+" "*(10-(len(tag)))
        ret+="\n"
        ret+="-"*len(self.attrNames)*10
        ret+="\n"
        for i in range(len(self.attrs)):
            for j in range(len(self.attrs[i])):
                ret+=str(self.attrs[i][j])+" "*(10-len(str(self.attrs[i][j])))
            ret+="\n"
        ret+="\n"
        print(ret)
########################################################### END CLASS TABLE ###########################################################


#EXPRESSIONS : class Expr :

class Expr:
    def __init__(self):
        self.table=Table()
        self.expression=""
        self.traduction=""
    def setExpression(self, newExpression):
        self.expression=newExpression
    def __str__(self):
        return self.expression
    def validation(self, tables):
        self.tables=tables
    def setTraduction(self, newTraduction):
        self.traduction=newTraduction
    def getTraduction(self):
        return self.traduction
    def display(self):
        self.table.display()
########################################################### END CLASS EXPR ###########################################################

#EXPRESSIONS : ATOMES : class Rel :

class Rel(Expr):
    def __init__(self, relName):
        Expr.__init__(self)
        self.name=relName
    def validation(self, tables):
        Expr.validation(self, tables)
        self.setExpression("Rel({})".format(self.name))
        for i in range(len(tables)):
            if self.name==self.tables[i].name:
                self.table.setName(self.name)
                self.table.setAttrNames(self.tables[i].attrNames)
                self.table.setAttrTypes(self.tables[i].attrTypes)
                Expr.setTraduction(self, self.name)
                return True
        print("ERROR TABLE : \n{} :\n NO TABLE NAMED {}\n".format(self, self.name))
        return False
########################################################### END CLASS REL ###########################################################

#NOT EXPRESSIONS : ATOMES : class Const :

class Const:
    def __init__(self, data):
        self.data=data
        self.atom="const"
        if type(self.data)==type(10):
            self.type="integer"
        elif type(self.data)==type(1.0):
            self.type="real"
        elif type(self.data)==type("") or type(self.data)==type(''):
            self.type="text"
        else:
            self.type="blob"
    def __str__(self):
        return "Const({})".format(self.data)
    def getType(self):
        return self.type
    def getTraduction(self):
        if self.getType()=="text":
            return "'{}'".format(self.data)
        else:
            return self.data
########################################################### END CLASS CONST ###########################################################

#NOT EXPRESSIONS : ATOMES : class Attr :

class Attr:
    def __init__(self, name):
        self.name=name
        self.atom="attr"
    def __str__(self):
        return "Attr({})".format(self.name)
    def getTraduction(self):
        return self.name
########################################################### END CLASS ATTR ###########################################################

#EXPRESSIONS : NODES : class Select :

class Select(Expr):
    def __init__(self, attr, comp, expr):
        Expr.__init__(self)
        self.attr=attr
        self.comp=comp
        self.expr=expr
    def validation(self, tables):
        Expr.validation(self, tables)
        if self.expr.validation(tables):
            self.table.setAttrNames(self.expr.table.attrNames)
            self.table.setAttrTypes(self.expr.table.attrTypes)
            self.setExpression("Select({}, {}, {})".format(self.attr, self.comp, self.expr))
            if self.comp.atom=="const":
                if self.attr.name in self.expr.table.attrNames and self.table.getType(self.attr.name)==self.comp.getType():
                    self.setTraduction("(select * from {} where {}={})".format(self.expr.getTraduction(), self.attr.getTraduction(), self.comp.getTraduction()))
                    self.table.setName(self.getTraduction()[1:-1])
                    return True
                elif (self.attr.name in self.expr.table.attrNames)==False:
                    print("ERROR IN SELECT SECTION :\n{} :\nATTRIBUTE {} NOT IN {}\n".format(self, self.attr.name, self.expr.table.attrNames))
                    return False
                elif self.table.getType(self.attr.name)!=self.comp.getType():
                    print("ERROR IN SELECT SECTION :\n{} :\nCONST {} TYPE {} IS NOT TYPE {}\n".format(self, self.comp.data, self.comp.getType(), self.table.getType(self.attr.name)))
                    return False
            elif self.comp.atom=="attr":
                if self.attr.name in self.expr.table.attrNames and self.comp.name in self.expr.table.attrNames and self.table.getType(self.attr.name)==self.table.getType(self.comp.name):
                    self.setExpression("Select({}, {}, {})".format(self.attr, self.comp, self.expr))
                    self.setTraduction("(select * from {} where {}={})".format(self.expr.getTraduction(), self.attr.getTraduction(), self.comp.getTraduction()))
                    self.table.setName(self.getTraduction()[1:-1])
                    return True
                elif (self.attr.name in self.expr.table.attrNames)==False:
                    print("ERROR IN SELECT SECTION :\n{} :\nATTRIBUTE {} NOT IN {}\n".format(self, self.attr.name, self.expr.table.attrNames))
                    return False
                elif self.table.getType(self.attr.name)!=self.table.getType(self.comp.name):
                    print("ERROR IN SELECT SECTION :\n{} :\nATTRIBUTE {} TYPE {} IS NOT TYPE {}\n".format(self, self.comp.name, self.table.getType(self.comp.name), self.table.getType(self.attr.name)))
                    return False
        else:
            return False
########################################################### END CLASS SELECT ###########################################################

#EXPRESSIONS : NODES : class Project :

class Project(Expr):
    def __init__(self, attrs, expr):
        self.attrs=attrs
        self.expr=expr
        Expr.__init__(self)
    def validation(self, tables):
        Expr.validation(self, tables)
        if self.expr.validation(tables):
            tempExpr="Select(["
            for i in range(len(self.attrs)-1):
                tempExpr+="{}, ".format(self.attrs[i])
            tempExpr+="{}], {})".format(self.attrs[-1], self.expr)
            self.setExpression(tempExpr)
            attrNames=[]
            for i in range(len(self.attrs)):
                attrNames+=[self.attrs[i].name]
            self.table.setAttrNames(attrNames)
            if comp(self.table.attrNames, self.expr.table.attrNames):
                newTypes=[]
                for i in range(len(self.attrs)):
                    for j in range(len(self.expr.table.attrNames)):
                        if self.attrs[i].name==self.expr.table.attrNames[j]:
                            newTypes+=[self.expr.table.attrTypes[j]]
                self.table.setAttrTypes(newTypes)
                tempTrad="(select"
                for i in range(len(self.table.attrNames)-1):
                    tempTrad+=" {},".format(self.table.attrNames[i])
                tempTrad+=" {} from {})".format(self.table.attrNames[-1], self.expr.getTraduction())
                self.setTraduction(tempTrad)
                self.table.setName(self.getTraduction()[1:-1])
                return True
            else:
                print("ERROR IN PROJECT SECTION :\n{} :\nATTRIBUTE {} NOT IN {}\n".format(self, attrNames, self.expr.table.attrNames))
                return False
        else:
            return False
########################################################### END CLASS PROJECT ###########################################################

#EXPRESSIONS : NODES : class Join :

class Join(Expr):
    def __init__(self, expr1, expr2):
        self.expr1=expr1
        self.expr2=expr2
        Expr.__init__(self)
    def validation(self, tables):
        Expr.validation(self, tables)
        if self.expr1.validation(tables) and self.expr2.validation(tables):
            attrComm=[]
            tag=[]
            self.setExpression("Join({}, {})".format(self.expr1, self.expr2))
            for i in range(len(self.expr1.table.attrNames)):
                for j in range(len(self.expr2.table.attrNames)):
                    if self.expr2.table.attrNames[j]==self.expr1.table.attrNames[i]:
                        attrComm+=[self.expr2.table.attrNames[j]]
                        tag+=[i]
            for i in range(len(attrComm)):
                if self.expr1.table.getType(attrComm[i])!=self.expr2.table.getType(attrComm[i]):
                    print("ERROR IN JOIN SECTION :\n{} :\nATTRIBUTE {} TYPE {} IS NOT {} TYPE {}\n".format(self, attrComm[i], self.expr1.table.getType(attrComm[i]), attrComm[i], self.expr2.table.getType(attrComm[i])))
                    return False
            newAttrsNames=self.expr1.table.attrNames+self.expr2.table.attrNames
            tag2=[]
            for i in range(len(newAttrsNames)):
                if i not in tag:
                    tag2+=[i]
            newAttrsNames.reverse()
            for i in range(len(attrComm)):
                newAttrsNames.remove(attrComm[i])
            newAttrsNames.reverse()
            newTypes=[]
            tempTypes=self.expr1.table.attrTypes+self.expr2.table.attrTypes
            for i in range(len(tempTypes)):
                if i in tag2:
                    newTypes+=[tempTypes[i]]
            self.table=Table("", newAttrsNames, newTypes)
            self.setTraduction("(select * from {} natural join {})".format(self.expr1.getTraduction(), self.expr2.getTraduction()))
            self.table.setName(self.getTraduction()[1:-1])
            return True
        else:
            return False
########################################################### END CLASS JOIN ###########################################################

#EXPRESSIONS : NODES : class Rename :

class Rename(Expr):
    def __init__(self, attrNames1, attrNames2, expr):
        self.attrNames1=attrNames1
        self.attrNames2=attrNames2
        self.expr=expr
        Expr.__init__(self)
    def validation(self, tables):
        Expr.validation(self, tables)
        if self.expr.validation(tables):
            self.attrCompNames=[]
            self.table.setAttrNames(self.expr.table.attrNames)
            tempExpr="Rename(["
            for i in range(len(self.attrNames1)-1):
                tempExpr+="{}, ".format(self.attrNames1[i])
            tempExpr+="{}], [".format(self.attrNames1[-1])
            for i in range(len(self.attrNames2)-1):
                tempExpr+="{}, ".format(self.attrNames2[i])
            tempExpr+="{}], {})".format(self.attrNames2[-1], self.expr)
            self.setExpression(tempExpr)
            for i in range(len(self.attrNames1)):
                if self.attrNames1[i].name not in self.expr.table.attrNames:
                    print("ERROR IN RENAME SECTION :\n{} :\nATTRIBUTE {} NOT IN {}\n".format(self, self.attrNames1[i].name, self.expr.table.attrNames))
                    return False
            for i in range(len(self.expr.table.attrNames)):
                self.attrCompNames+=[self.expr.table.attrNames[i]]
            for i in range(len(self.expr.table.attrNames)):
                for j in range(len(self.attrNames1)):
                    if self.expr.table.attrNames[i]==self.attrNames1[j].name:
                        self.table.attrNames[i]=self.attrNames2[j].data
            for i in range(len(self.table.attrNames)):
                if self.table.attrNames[i] in (self.table.attrNames[:i]+self.table.attrNames[i+1:]):
                    print("ERROR IN RENAME SECTION :\n{} :\nREDUNDANCY ERROR NAME {} IN {}\n".format(self, self.table.attrNames[i], self.table.attrNames[:i]+self.table.attrNames[i+1:]))
                    return False
            self.table.setAttrTypes(self.expr.table.attrTypes)
            tempTrad="(select "
            for i in range(len(self.table.attrNames)):
                if self.table.attrNames[i]==self.attrCompNames[i]:
                    tempTrad+="{}".format(self.table.attrNames[i])
                else:
                    tempTrad+="{} as {}".format(self.attrCompNames[i], self.table.attrNames[i])
                tempTrad+=", "
            tempTrad=tempTrad[:-2]+" from {})".format(self.expr.getTraduction())
            self.setTraduction(tempTrad)
            self.table.setName(self.getTraduction()[1:-1])
            return True
        else:
            return False
########################################################### END CLASS RENAME ###########################################################

#EXPRESSIONS : NODES : class Union :

class Union(Expr):
    def __init__(self, expr1, expr2):
        self.expr1=expr1
        self.expr2=expr2
        Expr.__init__(self)
    def validation(self, tables):
        Expr.validation(self, tables)
        if self.expr1.validation(tables) and self.expr2.validation(tables):
            tempExpr="Union({}, {})".format(self.expr1, self.expr2)
            self.setExpression(tempExpr)
            for i in range(len(self.expr1.table.attrNames)):
                if find(self.expr1.table.attrNames[i], self.expr2.table.attrNames) and self.expr1.table.getType(self.expr1.table.attrNames[i])!=self.expr2.table.getType(self.expr1.table.attrNames[i]):
                    print("ERROR IN UNION SECTION :\n{} :\nATTRIBUTE {} TYPE {} IS NOT {} TYPE {}\n".format(self, self.expr1.table.attrNames[i], self.expr1.table.getType(self.expr1.table.attrNames[i]), self.expr1.table.attrNames[i], self.expr2.table.getType(self.expr1.table.attrNames[i])))
                    return False
                elif not(find(self.expr1.table.attrNames[i], self.expr2.table.attrNames)):
                    print("ERROR IN UNION SECTION :\n{} :\n{} NOT IN {}\n".format(self, self.expr1.table.attrNames, self.expr2.table.attrNames))
                    return False
            self.table.setAttrNames(self.expr1.table.attrNames)
            tempTrad="select "
            tempTrad+=", ".join(self.table.attrNames)
            tempTrad1=tempTrad+" from {}".format(self.expr1.getTraduction())
            tempTrad2=tempTrad+" from {}".format(self.expr2.getTraduction())
            tempTrad="("+tempTrad1+" union "+tempTrad2+")"
            self.setTraduction(tempTrad)
            self.table.setAttrTypes(self.expr1.table.attrTypes)
            self.table.setName(self.getTraduction()[1:-1])
            return True
        else:
            return False
########################################################### END CLASS UNION ###########################################################

#EXPRESSIONS : NODES : class Diff :

class Diff(Expr):
    def __init__(self, expr1, expr2):
        self.expr1=expr1
        self.expr2=expr2
        Expr.__init__(self)
    def validation(self, tables):
        Expr.validation(self, tables)
        if self.expr1.validation(tables) and self.expr2.validation(tables):
            self.table.setAttrNames(self.expr1.table.attrNames)
            self.setExpression("Diff({}, {})".format(self.expr1, self.expr2))
            for i in range(len(self.expr1.table.attrNames)):
                if find(self.expr1.table.attrNames[i], self.expr2.table.attrNames) and self.expr1.table.getType(self.expr1.table.attrNames[i])!=self.expr2.table.getType(self.expr1.table.attrNames[i]):
                    print("ERROR IN DIFFERENCE SECTION :\n{} :\nATTRIBUTE {} TYPE {} IS NOT {} TYPE {}\n".format(self, self.expr1.table.attrNames[i], self.expr1.table.getType(self.expr1.table.attrNames[i]), self.expr1.table.attrNames[i], self.expr2.table.getType(self.expr1.table.attrNames[i])))
                    return False
                elif not(find(self.expr1.table.attrNames[i], self.expr2.table.attrNames)):
                    print("ERROR IN DIFFERENCE SECTION :\n{} :\n{} NOT IN {}\n".format(self, self.expr1.table.attrNames, self.expr2.table.attrNames))
                    return False
            self.table.setAttrTypes(self.expr1.table.attrTypes)
            tempTrad="select "
            tempTrad+=", ".join(self.table.attrNames)
            tempTrad1=tempTrad+" from {}".format(self.expr1.getTraduction())
            tempTrad2=tempTrad+" from {}".format(self.expr2.getTraduction())
            tempTrad="("+tempTrad1+" except "+tempTrad2+")"
            self.setTraduction(tempTrad)
            self.table.setName(self.getTraduction()[1:-1])
            return True
        else:
            return False
########################################################### END CLASS DIFF ###########################################################
            
