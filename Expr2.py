#TABLE
class Table:
    def __init__(self, name, attrNames, attrTypes):#, attrs):
        self.name=name
        self.attrNames=attrNames
        self.attrTypes=attrTypes
        self.attrs=[]
    def getType(self, attribute):
        for i in range(len(self.attrNames)):
            if attribute==self.attrNames[i]:
                return self.attrTypes[i]
    def getUnit(self, attrName):
        for i in range(len(self.attrNames)):
            if attrName==self.attrNames[i]:
                return i
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

#Expression
class Expr:
    def __init__(self):
        self.tables=[]
    def validation(self, tables):
        self.tables=tables
    def find(n, tab):
        for i in range(len(tab)):
            if n==tab[i]:
                return True
        return False
    def comp(tab1, tab2):
        for i in range(len(tab1)):
            if Expr.find(tab1[i], tab2)==False:
                return False
        return True
    
#Atomes
class Rel(Expr):
    def __init__(self, name):
        self.table=[]
        self.name=name
        Expr.__init__(self)
    def validation(self, tables):
        self.tables=tables
        for i in range(len(tables)):
            if self.tables[i].name==self.name:
                self.table=self.tables[i]
                return True
        print("ERROR NO TABLE NAMED {}".format(self.name))
        return False
    def display(self):
        self.table.display()
    def __str__(self):
        return self.name
        
        
class Const:
    def __init__(self, value):
        self.value=value
        self.atk=0
    def __str__(self):
        return str(self.value)
    def getType(self):
        if type(self.value)==type(10.0) or type(self.value)==type(10):
            return "real"
        if type(self.value)==type(""):
            return "text"
        
class Attr:
    def __init__(self, name):
        self.name=name
        self.atk=1
        
#Expressions
class Select(Expr):
    def __init__(self, attr, comp, expr1):
        Expr.__init__(self)
        self.attr=attr
        self.comp=comp
        self.expr1=expr1
        self.table=[]
    def validation(self, tables):
        Expr.validation(self, tables)
        self.expr1.validation(tables)
        self.table=self.expr1.table
        self.table.name=str(self)
        try:
            if self.comp.atk==0:
                if self.attr.name in self.expr1.table.attrNames and self.table.getType(self.attr.name)==self.comp.getType():
                    """
                    new_attrs=[]
                    i=self.table.getUnit(self.attr.name)
                    for j in range(len(self.table.attrs)):
                        if self.table.attrs[j][i]==self.comp.value:
                            new_attrs+=[self.table.attrs[j]]
                    self.table.attrs=new_attrs
                    """
                    return True
                elif (self.attr.name in self.expr1.table.attrNames)==False:
                    print("ERROR AT SELECT ATTRIBUTE {} NOT IN {}".format(self.attr.name, self.expr1.table.attrNames))
                    print("Select( Attr({}), Const({}), Rel({}))".format(self.attr.name, self.comp, self.expr1.name))
                    return False
                elif self.table.getType(self.attr.name)!=self.comp.getType():
                    print("ERROR CONST {} TYPE {} IS NOT TYPE {}".format(self.comp.value, self.comp.getType(), self.table.getType(self.attr.name)))
                    return False
            elif self.comp.atk==1:
                if self.attr.name in self.expr1.table.attrNames and self.comp.name in self.expr1.table.attrNames and self.table.getType(self.attr.name)==self.table.getType(self.comp.name):
                    return True
                elif (self.attr.name in self.expr1.table.attrNames)==False:
                    print("ERROR AT SELECT ATTRIBUTE {} NOT IN {}".format(self.attr.name, self.expr1.table.attrNames))
                    print("Select( Attr({}), Const({}), Rel({}))".format(self.attr.name, self.comp, self.expr1.name))
                    return False
                elif self.table.getType(self.attr.name)!=self.table.getType(self.comp.name):
                    print("ERROR ATTR {} TYPE {} IS NOT TYPE {}".format(self.comp.name, self.table.getType(self.comp.name), self.table.getType(self.attr.name)))
                    return False
        except:
            return False
    def display(self):
        self.expr1.table.display()
    def __str__(self):#TODO changer str en traduction et mettre str Select(...)
        if self.comp.atk==0:
            return '(select * from {} where {}={})'.format(self.expr1, self.attr.name, self.comp.value)
        elif self.comp.atk==1:
            return '(select * from {} where {}={})'.format(self.expr1, self.attr.name, self.comp.name)
        
class Project:
    def __init__(self, attrs, expr1):
        self.db_attrs=[]
        self.attrs=attrs
        self.expr1=expr1
        Expr.__init__(self)
        for i in range(len(self.attrs)):
            self.db_attrs+=[self.attrs[i].name]
    def validation(self, tables):
        Expr.validation(self, tables)
        self.expr1.validation(tables)
        self.table=self.expr1.table
        try:
            if Expr.comp(self.db_attrs, self.table.attrNames):
                new_types=[]
                for i in range(len(self.db_attrs)):
                    for j in range(len(self.table.attrNames)):
                        if self.db_attrs[i]==self.table.attrNames[j]:
                            new_types+=self.table.attrTypes[j]
                #new_attrs=[
                """
                for i in range(len(self.table.attrs)):
                    new_attr1=[]
                    for j in tag:
                        new_attr1+=[self.table.attrs[i][j]]
                    new_attrs+=[new_attr1]
                """
                self.table.attrNames=self.db_attrs
                self.table.name=str(self)
                #self.table.attrs=new_attrs
                return True
            else:
                print("ERROR IN PROJECT ATTRIBUTES {} NOT IN {}".format(self.db_attrs, self.table.attrNames))
                return False
        except:
            return False
    def __str__(self):
        ret="(select"
        for i in range(len(self.table.attrNames)-1):
            ret+=" {},".format(self.table.attrNames[i])
        ret+=" {} from {})".format(self.table.attrNames[-1], self.expr1)
        return ret
    def display(self):
        self.table.display()
        
        
class Join:
    def __init__(self, expr1, expr2):
        self.db_attrs=[]
        self.expr1=expr1
        self.expr2=expr2
        Expr.__init__(self)
    def validation(self, tables):
        Expr.validation(self, tables)
        self.expr1.validation(tables)
        self.expr2.validation(tables)
        attrComm=[]
        tag=[]
        for i in range(len(self.expr1.table.attrNames)):
            for j in range(len(self.expr2.table.attrNames)):
                if self.expr2.table.attrNames[i]==self.expr1.table.attrNames[j]:
                    attrComm+=[self.expr2.table.attrNames[j]]
                    tag+=[i]
        print(tag)
        for i in range(len(attrComm)):
            if self.expr1.table.getType(attrComm[i])!=self.expr1.table.getType(attrComm[i]):
                print("Error in JOIN SECTION : {} TYPE {} NOT COMPATIBLE WITH {} TYPE {}".format(attrComm[i], self.expr1.table.getType(attrComm[i]), attrComm[i], self.expr2.table.getType(attrComm[i])))
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
        """
        newAttrs=self.expr1.table.attrs
        for i in range(len(self.expr2.table.attrs)):
            for j in range(len(self.expr2.table.attrs[i])):
                newAttrs[i]+=(self.expr2.table.attrs[i][j],)
        """
        newTypes=[]
        tempTypes=self.expr1.table.attrTypes+self.expr2.table.attrTypes
        for i in range(len(tempTypes)):
            if i in tag2:
                newTypes+=[tempTypes[i]]
        self.table=Table(str(self), newAttrsNames, newTypes)#, newAttrs)
        return True
    def __str__(self):
        return "(select * from {} natural join {})".format(self.expr1, self.expr2)
    def display(self):
        self.table.display()
        
class Rename:
    def __init__(self, attrNames1, attrNames2, expr1):
        self.attrNames1=attrNames1
        self.attrNames2=attrNames2
        self.expr1=expr1
        Expr.__init__(self)
    def validation(self, tables):
        Expr.validation(self, tables)
        self.expr1.validation(tables)
        self.table=self.expr1.table
        self.attrCompNames=[]
        for i in range(len(self.attrNames1)):
            if self.attrNames1[i].name not in self.table.attrNames:
                print("ERROR IN RENAME {} not in {}".format(self.attrNames1[i].name, self.table.attrNames))
                return False
        for i in range(len(self.expr1.table.attrNames)):
            self.attrCompNames+=[self.expr1.table.attrNames[i]]
        for i in range(len(self.expr1.table.attrNames)):
            for j in range(len(self.attrNames1)):
                if self.expr1.table.attrNames[i]==self.attrNames1[j].name:
                    self.table.attrNames[i]=self.attrNames2[j].value
        for i in range(len(self.table.attrNames)):
            if self.table.attrNames[i] in (self.table.attrNames[:i]+self.table.attrNames[i+1:]):
                print("ERROR IN RENAME REDUNDANCY ERROR {} in {}".format(self.table.attrNames[i], self.table.attrNames[:i]+self.table.attrNames[i+1:]))
                return False
        self.table.name=str(self)
        return True
    def __str__(self):
        ret="(select "
        for i in range(len(self.table.attrNames)):
            if self.table.attrNames[i]==self.attrCompNames[i]:
                ret+="{}".format(self.table.attrNames[i])
            else:
                ret+="{} as {}".format(self.attrCompNames[i], self.table.attrNames[i])
            ret+=", "
        ret=ret[:-2]+" from {})".format(self.expr1)
        return ret
    def display(self):
        self.table.display()
 
class Union:
    def __init__(self, expr1, expr2):
        self.expr1=expr1
        self.expr2=expr2
        Expr.__init__(self)
        
class Diff:
    def __init__(self, expr1, expr2):
        pass
