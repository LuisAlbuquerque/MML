from math import log
from functools import reduce

# ler o dataset
with open("winequality-red.csv") as fd:
    data = list(map(lambda x: x.strip("\n").split(";"),fd.readlines()))

# -- defines ---

RESULTADO = 11
VAL = 6

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

def inpureza1(x):
    return 4*reduce(lambda a,b: a*b, x)

def inpureza2(x):
    return 2*min(x)

def inpureza3(x):
    try:
        return reduce(lambda a,b: -(a)*log(2,a) -(b)*log(2,b),x)
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

print(separa_all(data,11)[0])
#print(contagem_all(separa_all(data,5)))
#a = contagem_all(separa_all(data,5))
#print(inpureza_all(a,inpureza2))


arvore = {}
separator = 0
separators = []
count = 1

arvore[0] = [data]

#print(contagem(data))
#print(possiblidades(2,data))



