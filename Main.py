from Expr2 import Expr
from Expr2 import Attr
from Expr2 import Select
from Expr2 import Rel
from Expr2 import Const
from Expr2 import Project
from Expr2 import Join
from Expr2 import Table
from Expr2 import Rename
from Expr2 import Union
from Expr2 import Diff
import sqlite3

"""print(Select(Attr("A1"), Const("Charles"), Rel("R1")))
print(Project([Attr("A1"), Attr("A2")], Select(Attr("A1"), Const("Charles"), Rel("R1"))))
print(Select(Attr("A1"), Const("Charles"), Project([Attr("A2")], Rel("R1"))))
print(Project([Attr("A1")], Rel("R1")).sort())
print(Select(Attr("A1"), Const("Charles"), Rel("R1")).sort())
print("\n")"""

def SPJRUD2sqlite3(pathDB, command):
    c=connexion(pathDB)
    tables=createTables(c, retTables(c))
    if(command.validation(tables)):
        #printTables(pathDB)
        retCommand=str(command)[1:-1]
        for i in range(len(c.execute(retCommand).fetchall())):
            command.table.attrs+=[c.execute(retCommand).fetchall()[i]]
        command.display()

def createTable(command, tables):
    print(command.sort())

def printTables(pathDB):
    c=connexion(pathDB)
    tables=createTables(c, retTables(c))
    for i in range(len(tables)):
        tables[i].display()

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
    c.execute('''create table R1(A1 text, A2 real, A3 real)''')
    c.execute("insert into R1 values('Charles', 3, 20)")
    c.execute("insert into R1 values('Maxime', 20, 20)")
    c.execute("insert into R1 values('Guillaume', 3, 5)")

    c.execute("drop table R2")
    c.execute('''create table R2(A4 real, A2 real, A5 text)''')
    c.execute("insert into R2 values(123, 1, 'ALLE')")
    c.execute("insert into R2 values(124, 2, 'RADAR')")
    c.execute("insert into R2 values(126, 3, 'BIS')")

    c.execute("drop table R3")
    c.execute('''create table R3(E1 real, E2 real, A5 text)''')
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
        retTables+=[Table(name, attrNames, attrTypes)]#, attrs)]
    return retTables

def tests():
    
    print("SELECT TESTS")
    SPJRUD2sqlite3('myDB.db', Select(Attr('A1'), Const('"Charles"'), Rel('R1')))
    SPJRUD2sqlite3('myDB.db', Select(Attr('A2'), Attr('A3'), Rel('R1')))
    SPJRUD2sqlite3('myDB.db', Select(Attr('A1'), Attr('A2'), Rel('R2')))
    SPJRUD2sqlite3('myDB.db', Select(Attr('A1'), Const(3), Rel('R1')))
    
    print("\nPROJECT TESTS")
    SPJRUD2sqlite3('myDB.db', Project([Attr('A2'), Attr('A1'), Attr('A3')], Rel('R1')))
    SPJRUD2sqlite3('myDB.db', Project([Attr('A4'), Attr('A1')], Rel('R1')))
    
    print("\nJOIN TESTS")
    SPJRUD2sqlite3('myDB.db', Join(Project([Attr('A2'), Attr('A1')], Rel('R1')), Rel('R2')))
    SPJRUD2sqlite3('myDB.db', Join(Rel('R1'), Rename([Attr('E1')], [Const('A1')], Rel('R3'))))
    
    print("\nRENAME TESTS")
    SPJRUD2sqlite3('myDB.db', Rename([Attr('A1'), Attr('A2')], [Const('E1'), Const('E2')], Rel('R1')))
    SPJRUD2sqlite3('myDB.db', Rename([Attr('A1'), Attr('A5')], [Const('E1'), Const('A2')], Rel('R1')))
    SPJRUD2sqlite3('myDB.db', Rename([Attr('A1'), Attr('A2')], [Const('E1'), Const('A3')], Rel('R1')))
    
    print("\nUNION TESTS")
    SPJRUD2sqlite3('myDB.db', Union(Project([Attr('A1'), Attr('A2')], Rel('R1')), Project([Attr('A2'), Attr('A1')], Rel('R1'))))
    SPJRUD2sqlite3('myDB.db', Union(Select(Attr('A1'), Const('"Charles"'), Rel('R1')), Select(Attr('A2'), Const(20), Rel('R1'))))
    SPJRUD2sqlite3('myDB.db', Union(Rel('R1'), Rel('R2')))
    SPJRUD2sqlite3('myDB.db', Union(Rel('R1'), Rename([Attr('E1')], [Const('A1')], Rel('R3'))))
    
    print("\nDIFFERENCE TESTS")
    SPJRUD2sqlite3('myDB.db', Diff(Project([Attr('A1'), Attr('A2')], Rel('R1')), Project([Attr('A2'), Attr('A1')], Select(Attr('A1'), Const("'Charles'"), Rel('R1')))))
    SPJRUD2sqlite3('myDB.db', Diff(Rel('R1'), Rel('R2')))
    SPJRUD2sqlite3('myDB.db', Diff(Rel('R1'), Rename([Attr('E1')], [Const('A1')], Rel('R3'))))
    

tests()
