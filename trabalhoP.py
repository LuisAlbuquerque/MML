from math import log
from functools import reduce

# ler o dataset
with open("winequality-red.csv") as fd:
    data = list(map(lambda x: x.strip("\n").split(";"),fd.readlines()))

# -- defines ---

RESULTADO = 11
VAL = 6
SEP = []

#---------------

# ---Opcoes-----
TIPO = 0 # regrressao
#TIPO = 1 # mudar para classificao

HEADER = 1 # se tem uma linha com identificadores de coluna
#HEADER = 0 # caso nao tenha
# --------------

# transformar arvore de regressao numa de classificacao

def cond(string,val):
    if(int(string)>val): return True
    return False

def reg_to_class():
    for x in range(len(data)-HEADER):
        data[x+HEADER][RESULTADO] = cond(data[x+HEADER][RESULTADO],VAL)

if(TIPO):        
    reg_to_class()

# ---------------
def possiblidades(ind,lista):
    return list(set(map(lambda x: x[ind],lista[HEADER:])))

def contagem(lista):
    keys = possiblidades(RESULTADO,lista)
    #--init dic--
    dic = {}
    for k in keys:
        dic[k] = 0
    for x in lista[HEADER:]:
        dic[x[RESULTADO]] += 1
    return list(map(lambda x: (x,dic[x]),keys))


def contagem_all(lista):
    return list(map(lambda x: contagem(x),lista))

# ----- funcoes de impureza -----

# calcular a probabilidade 
def P(val,poss):
    return(val/len(poss))

# (|)(Ps,Pn) = 4PsPn
# (|)(x1,...,xn) = 4 PIi (Pxi)

def inpureza1(x):
    try:
        return 4*reduce(lambda a,b: P(a[1],x) * P(b[1],x), x)
    except:
        return 0

# (|)(Ps,Pn) = min(Ps,Pn) * 2
# (|)(x1,...,xn) = min(Px1,...Pxn) * n

def inpureza2(x):
    try:
        return (len(x)) * min(list(map(lambda l: P(l,x),x)))
    except:
        return 0

# (|)(Ps,Pn) = -Ps*log2(Ps) -Pn*log2(Pn)
# (|)(x1,...,xn) = -Px1*log2(Px1) ... -Pxn*log2(Pxn)

def inpureza3(x):
    try:
        return reduce(lambda a,b: -P(a,x)*log(2,P(a,x)) -P(b,x)*log(2,P(b,x)),x)
    except:
        return 0

# (|)(x1,...,xn) = (1 - MAXi (Pi)) * (L/(L-1))

def inpureza4(x):
    try:
        return (1 - max(list(map(lambda l: P(l,x),x))) ) * (L/(L-1))
    except:
        return 0

# (|)(x1,...,xn) = - SUMi(Pi) * (1/log2(n))

def inpureza5(x):
    try:
        return -reduce(lambda a,b: P(a,x) + P(b,x),x) * (1/log(2,len(x)))
    except:
        return 0
#--------------------------------

def inpureza_all(lista, fun):
    return list(map(lambda x: fun(x),lista))

def separa(lista,ind,val):
    res = []
    for x in lista[HEADER:]:
        if(x[ind] == val):
            res.append(x)
    return res

def separa_all(lista,ind):
    res = []
    for x in possiblidades(ind,lista):
        res.append(separa(lista,ind,x))
    return res

#print(separa_all(data,11)[0])
#print(contagem_all(separa_all(data,5)))
#a = contagem_all(separa_all(data,5))
#print(inpureza_all(a,inpureza2))


arvore = {}
separator = 0
count = 1

arvore[0] = [(0,data)]

a = separa_all(data,separator)
c = contagem_all(a)
arvore[1] = [(0,a[0]),
#print(c)
print(inpureza_all(c,inpureza1))
#print(contagem(data))
#print(possiblidades(2,data))



