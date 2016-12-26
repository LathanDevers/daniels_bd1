from SPJRUD import *
from misc.Tests import *
import sqlite3

def SPJRUD2sqlite3(pathDB, command):
    c=connexion(pathDB)
    tables=createTables(c, retTables(c))
    if(command.validation(tables)):
        retCommand=str(command.getTraduction())[1:-1]
        for i in range(len(c.execute(retCommand).fetchall())):
            command.table.attrs+=[c.execute(retCommand).fetchall()[i]]
        command.display()
    c.close()

def launchTests():
    tests()

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
    """
    c.execute("drop table R1")
    c.execute('''create table R1(A1 text, A2 real, A3 real)''')
    c.execute("insert into R1 values('Charles', 3, 20)")
    c.execute("insert into R1 values('Maxime', 20, 20)")
    c.execute("insert into R1 values('Guillaume', 3, 5)")

    c.execute("drop table R2")
    c.execute('''create table R2(A4 REAL, A2 real, A5 text)''')
    c.execute("insert into R2 values(123, 1, 'ALLE')")
    c.execute("insert into R2 values(124, 2, 'RADAR')")
    c.execute("insert into R2 values(126, 3, 'BIS')")

    c.execute("drop table R3")
    c.execute('''create table R3(E1 real, E2 real, A5 text)''')
    c.execute("insert into R3 values(15, 20, 'BON')")
    c.execute("insert into R3 values(18, 20, 'TRESBON')")
    c.execute("insert into R3 values(3, 20, 'MAUVAIS')")
    """
    return c

def createTables(c, tables):
    attributes=retAttributes(c, tables)
    retTables=[]
    for i in range(len(tables)):
        name=tables[i]
        attrNames=attributes[i][0]
        attrTypes=[]
        for j in attributes[i][1]:
            attrTypes+=[j.lower()]
        retTables+=[Table(name, attrNames, attrTypes)]
    return retTables
