from Expressions import Expr
from Expressions import Attr
from Expressions import Select
from Expressions import Rel
from Expressions import Const
from Expressions import Project
import sqlite3

print(Select(Attr("A1"), Const("Charles"), Rel("R1")))
print(Project([Attr("A1"), Attr("A2")], Select(Attr("A1"), Const("Charles"), Rel("R1"))))
#print(Select(Attr("A1"), Const("Charles"), Project([Attr("A2")], Rel("R1"))))
print(Project([Attr("A1")], Rel("R1")).sort())
print(Select(Attr("A1"), Const("Charles"), Rel("R1")).sort())
print("\n")

conn=sqlite3.connect('myDB.db')
c=conn.cursor()
c.execute("drop table R1")
c.execute('''create table R1(A1 text, A2 float, A3 real)''')
c.execute("insert into R1 values('Charles', 3, 20)")
c.execute("insert into R1 values('Maxime', 20, 20)")
c.execute("insert into R1 values('Guillaume', 3, 5)")

print("Base de donnees : R1")
for raw in c.execute("select * from R1"):
    print(raw)
print("\n")
command=str(Select(Attr("A1"), Const(20), Rel("R1")))[1:-1]
print(str(Attr("A1").getType())+", "+str(Const(20).getType())+"="+str(Attr("A1").getType()==Const(20).getType()))
print(command)
for raw in c.execute(command):
    print(raw)
