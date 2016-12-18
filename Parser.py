import Main

def printTables(c):
    table=Main.retTables(c)
    tables=Main.createTables(c, table)
    attributes=Main.retAttributes(c, table)
    for i in range(len(tables)):
        print(tables[i])

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

def prompter():
    c=Main.connexion('myDB.db')
    printTables(c)
    sql=False
    while(True):
        tables=Main.retTables(c)
        Main.createTables(c, tables)
        if sql==False:
            command=input("> ")
            if command!="":
                if command=="sql":
                    sql=True
                elif command=="exit":
                    print("goodbye ;)")
                    break
                else:
                    print(Main.commands(command))
                    try:
                        for i in c.execute(Main.commands(command)):
                            print(i)
                        Main.createTable(c, command)
                    except:
                        print("incorrect SPJRUD request :'(")
            else:
                printTables(c)
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
                        print("incorrect sqlite request :'( !")

prompter()
