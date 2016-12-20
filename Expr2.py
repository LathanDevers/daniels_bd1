#TABLE
class Table:
    def __init__(self, name, attrNames, attrTypes, attrs):
        self.name=name
        self.attrNames=attrNames
        self.attrTypes=attrTypes
        self.attrs=attrs
    def getType(self, attribute):
        for i in range(len(self.attrNames)):
            if attribute==self.attrNames[i]:
                return self.attrTypes[i]
    def display(self):
        ret=""
        ret+=self.name
        ret+="\n"
        ret+="-"*len(self.name)+"\n"
        for i in range(len(self.attrNames)):
            ret+=str(self.attrNames[i])+" "*(10-len(str(self.attrNames[i])))
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
    def __str__(self):
        return str(self.value)
    def getType(self):
        if type(self.value)==type(10):
            return "real"
        if type(self.value)==type(""):
            return "text"
        
class Attr:
    def __init__(self, name):
        self.name=name
        
#Expressions
class Select(Expr):
    def __init__(self, attr, const, expr1):
        Expr.__init__(self)
        self.attr=attr
        self.const=const
        self.expr1=expr1
        self.table=[]
    def validation(self, tables):
        Expr.validation(self, tables)
        self.expr1.validation(tables)
        self.table=self.expr1.table
        try:
            if self.attr.name in self.expr1.table.attrNames and self.table.getType(self.attr.name)==self.const.getType():
                new_attrs=[]
                for i in range(len(self.table.attrNames)):
                    if self.attr.name==self.table.attrNames[i]:
                        for j in range(len(self.table.attrs)):
                            if self.table.attrs[j][i]==self.const.value:
                                new_attrs+=[self.table.attrs[j]]
                self.table.attrs=new_attrs
                return True
            elif (self.attr.name in self.expr1.table.attrNames)==False:
                print("ERROR AT SELECT ATTRIBUTE {} NOT IN {}".format(self.attr.name, self.expr1.table.attrNames))
                return False
            elif self.table.getType(self.attr.name)!=self.const.getType():
                print("ERROR CONST {} TYPE {} IS NOT TYPE {}".format(self.const.value, self.const.getType(), self.table.getType(self.attr.name)))
                return False
        except:
            pass
    def display(self):
        self.expr1.table.display()
    def __str__(self):
        return '(select * from {} where {}={})'.format(self.expr1, self.attr.name, self.const.value)
        
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
                tag=[]
                for i in range(len(self.db_attrs)):
                    for j in range(len(self.table.attrNames)):
                        if self.db_attrs[i]==self.table.attrNames[j]:
                            tag+=[j]
                new_attrs=[]
                for i in range(len(self.table.attrs)):
                    new_attr1=[]
                    for j in tag:
                        new_attr1+=[self.table.attrs[i][j]]
                    new_attrs+=[new_attr1]
                self.table.attrNames=self.db_attrs
                self.table.attrs=new_attrs
                return True
            else:
                print("ERROR IN PROJECT ATTRIBUTES {} NOT IN {}".format(self.db_attrs, self.table.attrNames))
                return False
        except:
            pass
    def __str__(self):
        ret="(select"
        for i in range(len(self.db_attrs)-1):
            ret+=" {},".format(self.db_attrs[i])
        ret+=" {} from {})".format(self.db_attrs[-1], self.expr1.name)
        return ret
    def display(self):
        self.table.display()
        
        
class Join:
    def __init__(self, expr1, expr2):
        self.expr1=expr1
        self.expr2=expr2
        Expr.__init__(self)
    def validation(self, db_attrs):
        #self.expr1.validation(db_attrs)
        #self.expr2.validation(db_attrs)
        self.db_attrs=self.expr1.db_attrs+self.expr2.db_attrs
        Expr.validation(self, self.db_attrs)
        
class Rename:
    def __init__(self, expr1, expr2, expr3):
        pass
 
class Union:
    def __init__(self, expr1, expr2):
        pass
        
class Diff:
    def __init__(self, expr1, expr2):
        pass


#Project([Attr('A1'), Attr('A2')], Rel('R1')).validation(['A1', 'A2', 'A3'])
#Select(Eq(Attr('A1'), Const('AZ')), Rel('R1')).validation(['A1', 'A2'])
#Select(Eq(Attr('A1'), Const('z')), Select(Eq(Attr('A2'), Const('e')), Rel('R1'))).validation(['A1', 'A2', 'A3', 'A4'])
