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

def printage():
    print("Base de donnees : R1")
    for raw in c.execute("select * from R1"):
        print(raw)
    print("\n")
    command=str(Select(Attr("A2"), Const(20), Rel("R1")))[1:-1]
    print(command)
    for raw in c.execute(command):
        print(raw)

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
            expr=[Select(atom[0], atom[1], expr[0])]+expr
            expr=expr[:-1]
            atom=[]
        if command[i:i+8]=="Project(":
            expr=[Project(atom, expr[0])]+expr
            expr=expr[:-1]
            atom=[]
            
                
    print(str(expr[0])[1:-1])
        

conn=sqlite3.connect('myDB.db')
c=conn.cursor()
c.execute("drop table R1")
c.execute('''create table R1(A1 text, A2 float, A3 real)''')
c.execute("insert into R1 values('Charles', 3, 20)")
c.execute("insert into R1 values('Maxime', 20, 20)")
c.execute("insert into R1 values('Guillaume', 3, 5)")
"""c.execute("select typeof(A1) from R1")
print(c.fetchone())"""

def prompter():
    while(True):
        command=input("> ")
        if(command=="exit"):
            print("goodbye ;)")
            break
        commands(command)
        #printage()

prompter()
