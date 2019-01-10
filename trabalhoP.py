from math import log
from functools import reduce



# ler o dataset
with open("winequality-red.csv") as fd:
    data = list(map(lambda x: x.strip("\n").split(";"),fd.readlines()))





# -- defines ---

#coluna com a classe que queremos prever na árvore de decisão
RESULTADO = 11

#valor a considerar como separador entre sim e não
VAL = 6

#neste momento, nada
#mudar estes comentários quando mudar, ou eliminar se for inutil
SEP = []

#---------------





# ---Opcoes-----
TIPO = 0 # regrressao
#TIPO = 1 # mudar para classificao

HEADER = 1 # se tem uma linha com identificadores de coluna
#HEADER = 0 # caso nao tenha
# --------------




# transformar arvore de regressao numa de classificacao

# funcao que define o criterio para classificar um dado valor
# como sim ou como nao

#Notas Ezequiel:
#sim = True; não = False
#apesar de ser obvio, é importante dizer em algum lugar

def cond(string,val):
    if(int(string)>val): return True
    return False

# funcao que transforma um dataset de regressao
# num de classificacao, usando a funcao cond 
# definida acima como criterio
def reg_to_class():
    for x in range(len(data)-HEADER):
        data[x+HEADER][RESULTADO] = cond(data[x+HEADER][RESULTADO],VAL)

# se a flag TIPO for 1
# transforma o dataset num de regressao
if(TIPO):        
    reg_to_class()

# ---------------




# Calcula todas as possiblidades de valores
# para uma determinada coluna

#Notas Ezequiel: cria uma set matemático(lista sem repetidos) única com o valor da coluna ind
#Efetivamente, retira uma coluna de uma matriz 
#e coloca numa lista todos os valores dela que sejam únicos

def getColumnUniqueFromMatrix(index,matrix):
    return list(set(map(lambda x: x[index],matrix[HEADER:])))


#Mesmo que a anterior, 
#mas retorna com o valor da coluna que foi retirada adicionado

#Notas Ezequiel:
#Como o nome sugere, é para uso de debug

def getColumnUniqueFromMatrixDebug(index,matrix):
    a = {}
    column = getColumnUniqueFromMatrix(index,matrix)
    a[matrix[0][index]] = column
    return a




# Para uma determinada lista
# calcula o numero de linhas é que têm 
# como resultado um determinado atributo
# calculando para todos os atributos possiveis
# classificacao:
#   [(sim: nº de ocurências de sim),(não: nº de ocurências de não)]

# Regressão:
#   [(v1: nº de ocurências de v1),...,(vn: nº de ocurências de vn)]

#Notas Ezequiel:
#retorna uma lista de pares (atributo,ocorrencias de atributo)
#como está definida, retorna uma lista com os pares (atributo,nº occorrências do atributo)
#da coluna com o atributo a prever
#i.e., retorna uma contagem de que valores únicos da classe a prever temos no csv




#Nota adicional: que raio é que tens contra chamar à "lista" o que é: uma matriz?




def contagemDeClasse(matrix):
    keys = getColumnUniqueFromMatrix(RESULTADO,matrix)
    #--init dic--
    dic = {}
    for k in keys:
        dic[k] = 0
    for x in matrix[HEADER:]:
        dic[x[RESULTADO]] += 1
    return list(map(lambda x: (x,dic[x]),keys))


#Mesmo que a anterior, 
#mas retorna com o valor da coluna RESULTADO adicionada
#para clareza adicional

#Notas Ezequiel:
#Como o nome sugere, é para uso de debug

def contagemDeClasseDebug(matrix):
    a = {}
    classeCont = contagemDeClasse(matrix)
    a[matrix[0][RESULTADO]] = classeCont
    return a


# Aplica a função constagem
# a uma lista de uma listas de listas

#Notas Ezequiel:
#usa contagemDeClasse numa lista com várias matrizes
def contagemDeClasseMultiplasMatrizes(matrix):
    return list(map(lambda x: contagemDeClasse(x),matrix))






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

# Calcula as impurezas de uma lista de contagens
def inpureza_all(lista, fun):
    return list(map(lambda x: fun(x),lista))

# Separa as linhas que têm  
# valor val na coluna ind
def separa(lista,ind,val):
    res = []
    for x in lista[HEADER:]:
        if(x[ind] == val):
            res.append(x)
    return res

# Cria uma lista de listas
# onde cada lista tem todas as listas 
# de um determinado atributo
# cada lista corresponde a um atributo difrente
def separa_all(lista,ind):
    res = []
    for x in getColumnUniqueFromMatrix(ind,lista):
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
arvore[1] = [(0,a[0])]
#print(c)
#print(inpureza_all(c,inpureza1))
print(contagemDeClasse(data))
print(contagemDeClasseDebug(data))
#print(getColumnUniqueFromMatrix(2,data))
#print(getColumnUniqueFromMatrixDebug(2,data))



