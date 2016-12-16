from Expressions import Expr
from Expressions import Attr
from Expressions import Select
from Expressions import Rel
from Expressions import Const
from Expressions import Project
from Expressions import Join
import sqlite3

"""print(Select(Attr("A1"), Const("Charles"), Rel("R1")))
print(Project([Attr("A1"), Attr("A2")], Select(Attr("A1"), Const("Charles"), Rel("R1"))))
print(Select(Attr("A1"), Const("Charles"), Project([Attr("A2")], Rel("R1"))))
print(Project([Attr("A1")], Rel("R1")).sort())
print(Select(Attr("A1"), Const("Charles"), Rel("R1")).sort())
print("\n")"""

def printage(tables):
    for i in range(len(tables)):
        print("TABLE : {}".format(tables[i]))
        for raw in c.execute("select * from {}".format(tables[i])):
            print(raw)
        print("\n")

def printTable(table, attributes):
    attribute=attributes[0]
    for i in range(len(attributes[0])):
        print(attribute[i]+" "*(10-len(attribute[i])))

def retValue(n, command):
    for i in range(n, len(command)):
        if command[i]==")":
            return command[n:i]

def commands(command):
    expr=[]
    atom=[]
    for i in range(len(command), -1, -1):  
        if command[i:i+5]=="Attr(":
            value=retValue(i+5, command)
            atom=[Attr(value)]+atom
        if command[i:i+4]=="Rel(":
            value=retValue(i+4, command)
            expr=[Rel(value)]+expr
        if command[i:i+6]=="Const(":
            value=retValue(i+6, command)
            atom=[Const(value)]+atom
        if command[i:i+7]=="Select(":
            expr=[Select(atom[0], atom[1], expr[0])]+expr[1:]
            atom=[]
        if command[i:i+8]=="Project(":
            expr=[Project(atom, expr[0])]+expr[1:]
            atom=[]
        if command[i:i+5]=="Join(":
            expr=[Join(expr[0], expr[1])]+expr[2:]    
    return str(expr[0])[1:-1]

def retTables():
    tables=c.execute("select name from sqlite_master where type='table';").fetchall()
    ret=[]
    for i in range(len(tables)):
        ret+=[tables[i][0]]
    return ret

def retAttributes(tables):
    ret=[]
    for table in tables:
        r1=[]
        t1=[]
        t2=[]
        attributes=c.execute("pragma table_info({})".format(table))
        for attribute in attributes:
            t1+=[attribute[1]]
            t2+=[attribute[2]]
        r1+=[t1]
        r1+=[t2]
        ret+=[r1]
    return ret
        
        

conn=sqlite3.connect('myDB.db')
c=conn.cursor()
c.execute("drop table R1")
c.execute('''create table R1(A1 text, A2 float, A3 real)''')
c.execute("insert into R1 values('Charles', 3, 20)")
c.execute("insert into R1 values('Maxime', 20, 20)")
c.execute("insert into R1 values('Guillaume', 3, 5)")

c.execute("drop table R2")
c.execute('''create table R2(A4 real, A2 float, A5 text)''')
c.execute("insert into R2 values(123, 1, 'BON')")
c.execute("insert into R2 values(124, 2, 'TRESBON')")
c.execute("insert into R2 values(126, 3, 'MAUVAIS')")

def prompter():
    tables=retTables()
    print(tables)
    attributes=retAttributes(tables)
    print(attributes)
    printTable(tables[0], attributes[0])
    sql=False
    while(True):
        if sql==False:
            command=input("> ")
            if command!="":
                if command=="sql":
                    sql=True
                elif command=="exit":
                    print("goodbye ;)")
                    break
                else:
                    print(commands(command))
                    try:
                        for i in c.execute(commands(command)):
                            print(i)
                    except:
                        print("incorrect sqlite request !")
            else:
                printage(tables)
        else:
             command=input("sql > ")
             if command!="":
                if command=="exit":
                     print("goodbye")
                     break
                else:
                    print(command)
                    try:
                        for i in c.execute(command):
                            print(i)
                    except:
                        print("incorrect sqlite request !")

prompter()
