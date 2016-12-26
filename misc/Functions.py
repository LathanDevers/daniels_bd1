def find(n, tab):
    for i in tab:
        if n==i:
            return True
    return False

def comp(tab1, tab2):
        for i in range(len(tab1)):
            if find(tab1[i], tab2)==False:
                return False
        return True
