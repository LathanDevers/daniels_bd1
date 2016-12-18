from Expressions import Expr
from Expressions import Attr
from Expressions import Select
from Expressions import Rel
from Expressions import Const
from Expressions import Project
from Expressions import Join
from Expressions import Table
import sqlite3

"""print(Select(Attr("A1"), Const("Charles"), Rel("R1")))
print(Project([Attr("A1"), Attr("A2")], Select(Attr("A1"), Const("Charles"), Rel("R1"))))
print(Select(Attr("A1"), Const("Charles"), Project([Attr("A2")], Rel("R1"))))
print(Project([Attr("A1")], Rel("R1")).sort())
print(Select(Attr("A1"), Const("Charles"), Rel("R1")).sort())
print("\n")"""

def SPJRUD2sqlite3(pathBD, command):
    c=connexion(pathBD)
    tables=createTables(c, retTables(c))
    
    retCommand=str(command)[1:-1]
    return retCommand

def printTables(pathDB):
    c=connexion(pathDB)
    tables=createTables(c, retTables(c))
    for i in range(len(tables)):
        print(tables[i])

def retTables(c):
    tables=c.execute("select name from sqlite_master where type='table';").fetchall()
    ret=[]
    for i in range(len(tables)):
        ret+=[tables[i][0]]
    return ret

def retAttributes(c, tables):
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

def connexion(path):
    conn=sqlite3.connect(path)
    c=conn.cursor()
    """c.execute("drop table R1")
    c.execute('''create table R1(A1 text, A2 float, A3 real)''')
    c.execute("insert into R1 values('Charles', 3, 20)")
    c.execute("insert into R1 values('Maxime', 20, 20)")
    c.execute("insert into R1 values('Guillaume', 3, 5)")

    c.execute("drop table R2")
    c.execute('''create table R2(A4 real, A2 float, A5 text)''')
    c.execute("insert into R2 values(123, 1, 'ALLE')")
    c.execute("insert into R2 values(124, 2, 'RADAR')")
    c.execute("insert into R2 values(126, 3, 'BIS')")

    c.execute("drop table R3")
    c.execute('''create table R3(E1 real, E2 float, A5 text)''')
    c.execute("insert into R3 values(15, 20, 'BON')")
    c.execute("insert into R3 values(18, 20, 'TRESBON')")
    c.execute("insert into R3 values(3, 20, 'MAUVAIS')")"""
    return c

def createTables(c, tables):
    attributes=retAttributes(c, tables)
    retTables=[]
    for i in range(len(tables)):
        name=tables[i]
        attrNames=attributes[i][0]
        attrTypes=attributes[i][1]
        attrs=[c.execute("select * from {}".format(name)).fetchall()]
        retTables+=[Table(name, attrNames, attrTypes, attrs)]
    return retTables
