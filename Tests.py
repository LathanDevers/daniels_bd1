#TESTS

from Main import *

def tests():
    
    print("SELECT TESTS")
    SPJRUD2sqlite3('myDB.db', Select(Attr('A1'), Const('Charles'), Rel('R1')))
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
    SPJRUD2sqlite3('myDB.db', Union(Select(Attr('A1'), Const('Charles'), Rel('R1')), Select(Attr('A2'), Const(20.0), Rel('R1'))))
    SPJRUD2sqlite3('myDB.db', Union(Rel('R1'), Rel('R2')))
    SPJRUD2sqlite3('myDB.db', Union(Rel('R1'), Rename([Attr('E1')], [Const('A1')], Rel('R3'))))
    
    print("\nDIFFERENCE TESTS")
    SPJRUD2sqlite3('myDB.db', Diff(Project([Attr('A1'), Attr('A2')], Rel('R1')), Project([Attr('A2'), Attr('A1')], Select(Attr('A1'), Const('Charles'), Rel('R1')))))
    SPJRUD2sqlite3('myDB.db', Diff(Rel('R1'), Rel('R2')))
    SPJRUD2sqlite3('myDB.db', Diff(Rel('R1'), Rename([Attr('E1')], [Const('A1')], Rel('R3'))))

    s=input("press enter to quit...")
    

tests()
