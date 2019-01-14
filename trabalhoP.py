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


# retira todos os valores de uma coluna de uma matriz

def getColumnFromMatrix(coluna,matriz):
    return list(map(lambda x: x[index],matrix[HEADER:]))



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
#retorna dita lista após ter aplicado a função a cada elemento dela
def contagemDeClasseMultiplasMatrizes(matrix):
    return list(map(lambda x: contagemDeClasse(x),matrix))





# ----- funcoes de impureza -----

# calcular a probabilidade 

#Notas Ezequiel:
#Dado uma classe pos com total de ocorrências N,
# o cálculo da probabilidade de 
# um certo evento com val ocorrências em pos
#é dado por val/N
#i.e., P(evento,pos) = val/N, onde val = nº ocorrências de evento em pos
def P(val,pos):
    N = sum(map(lambda x: x[1],pos))
    return(val/N)




# (|)(Ps,Pn) = 4PsPn
# (|)(x1,...,xn) = 4 PIi (Pxi)

#Notas Ezequiel:
#Esta é a implementação do Gini_index generalizado a N classes
#dado j entre 1 e N,
#calculamos a impureza de Gini_index através da formula
#Gini_index(N) =  1 - [ (P1*P1) + (P2*P2) + ... + (PJ*PJ) + ... + (PN*PN) ]
# de notar que o valor que obtemos acima não está normalizado, 
# i.e., para o máximo de indecisão não dá valor 1
#para se normalizar multiplica-se por N/(N-1)

def gini_index(x):
    N = len(x)
    try:
        return (1-reduce(lambda a,b: (P(a[1],x)**2) * (P(b[1],x)**2), x) ) / (N/(N-1))
        #return (1-reduce(lambda a,b: P(a[1],x) * P(b[1],x), x) ) / (N/(N-1))
    except:
        return 0

#versão antiga abaixo para caso de ser necessário revisitar

#def inpureza1(x):
#    print(x)
#    try:
#        return 4*reduce(lambda a,b: P(a[1],x) * P(b[1],x), x)
#    except:
#        return 0







# (|)(Ps,Pn) = min(Ps,Pn) * 2
# (|)(x1,...,xn) = min(Px1,...Pxn) * n

#notas do Ezequiel:
#missclassification como dito acima está errada
#de facto, para N classes,
# Missclassification(N) = 1 - maxi_1_N(Pi),
#onde maxi_1_N é o cálculo da probabilidade máxima da classe
# 1 até N
#Também se generaliza multiplicando por N/(N-1)

def missclassification(x):
    N = len(x)
    try:
        return (1 - max(list(map(lambda l: P(l[1],x),x))) ) / (N/(N-1))
    except:
        return 0


#versão antiga abaixo caso seja necessário revisitar

#def inpureza2(x):
#    try:
#        return (len(x)) * min(list(map(lambda l: P(l,x),x)))
#    except:
#        return 0









# (|)(Ps,Pn) = -Ps*log2(Ps) -Pn*log2(Pn)
# (|)(x1,...,xn) = -Px1*log2(Px1) ... -Pxn*log2(Pxn)


#Notas Ezequiel:
#Esta é a função de entropia
#dado N classes, calculamos 
#Entropia(N) = -(P1*log_2(P1)) - (P2*log_2(P2)) - ..... - (PN*log_2(PN))
#            = - ( (P1*log_2(P1)) + (P2*log_2(P2)) + ..... + (PN*log_2(PN)) )
#sendo que é normalizada desta vez multiplicando por 1/( log_2(N) )

def entropia(x):
    N = len(x)
    try:
        return (-reduce(lambda a,b: P(a[1],x)*log(P(a[1],x),2) + P(b[1],x)*log(P(b[1],x),2),x)) * ( 1 / (log(N,2)) )
    except:
        return 0





# (|)(x1,...,xn) = (1 - MAXi (Pi)) * (L/(L-1))

#def inpureza4(x):
#    try:
#        return (1 - max(list(map(lambda l: P(l,x),x))) ) * (L/(L-1))
#    except:
#        return 0

# (|)(x1,...,xn) = - SUMi(Pi*log2(Pi)) * (1/log2(n))

#def inpureza5(x):
#    try:
#        return -reduce(lambda a,b: P(a[1],x)*log(P(a[1],x),2) + P(b[1],x)*log(P(b[1],x),2),x) * (1/log(len(x),2))
#    except:
#        return 0
#--------------------------------




# Calcula as impurezas de uma lista de contagens

#Notas Ezequiel:
#dada uma lista de pares faz map de cada elemento
# da função fun

def inpureza_all(lista, fun):
    return list(map(lambda x: fun(x),lista))



# Separa as linhas que têm  
# valor val na coluna ind

#Notas Ezequiel:
#retorna todas as linhas de uma matriz cujo valor na coluna ind é val

def separa(matrix,ind,val):
    res = []
    for x in matrix[HEADER:]:
        if(x[ind] == val):
            res.append(x)
    return res





# Cria uma lista de listas
# onde cada lista tem todas as listas 
# de um determinado atributo
# cada lista corresponde a um atributo difrente

#Notas Ezequiel:
#aplica separa a uma lista de matrizes

def separa_all(listaMatrizes,ind):
    res = []
    for x in getColumnUniqueFromMatrix(ind,listaMatrizes):
        res.append(separa(listaMatrizes,ind,x))
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
c = contagemDeClasseMultiplasMatrizes(a)
arvore[1] = [(0,a[0])]


#print(c)

#print(inpureza_all(c,gini_index))
#print(inpureza_all(c,missclassification))
#print(inpureza_all(c,entropia))


#print(contagemDeClasse(data))
#print(contagemDeClasseDebug(data))


#print(getColumnUniqueFromMatrix(2,data))
#print(getColumnUniqueFromMatrixDebug(2,data))








#Notas Ezequiel: abaixo estão as funções que devem ser usadas para depois criar as árvores
#de notar que podem ter de ser alteradas

#NOTA IMPORTANTE: os atributos são assumidos estarem em matriz[HEADER][:RESULTADO] e
#as classes estarem em matriz[...][RESULTADO:]

#SEGUNDA NOTA IMPORTANTE: eu não sei trabalhar com a notação [X:], [:X] 
#, pelo que o que está abaixo provavelmente tem de ser alterado







#dada um valor, uma coluna e uma matriz
#retorna as linhas da matriz cujo valor em dada coluna é
#igual ao valor dado

#Nota Ezequiel: assume que a matriz contém os atributos em HEADERS


def retiraLinhasDaMatrizPorValorEmColuna(matriz,coluna,valor):
    matrizSemAtributos = matriz[HEADERS:]
    resultado = matriz[HEADER]
    for linha in matrizSemAtributos:
        if(linha[coluna] == valor): resultado.append(linha)
    return resultado


#função que faz o mesmo que a anterior, mas retira a coluna que
#lhe foi passada como parametro
def obtemLinhasDaMatrizPorValorEmColuna(matriz,coluna,valor):
    matrizSeparada = retiraLinhasDaMatrizPorValorEmColuna(matriz,coluna,valor)
    resultado = []
    for linha in matrizSeparada:
        valorARetirar = linha[coluna]
        resultado.append(linha.remove(valorARetirar))
    return resultado




#dada uma coluna e uma matriz separa a matrix pelos seus valores únicos e 
#retorna a matriz separada em várias sem a coluna que lhe foi passada

#Notas Ezequiel: assume-se que a matriz é uma lista de listas 
#e que a coluna é uma valor inteiro
#mais se assume que existem colunas suficientes na matriz para se retirar dita coluna

def separaMatrizPorColunaAtributo(matriz,coluna):
    valoresUnicosColuna = getColumnUniqueFromMatrix(coluna,matriz)
    resultado = []
    for valor in valoresUnicosColuna:
        resultado.append(obtemLinhasDaMatrizPorValorEmColuna(matriz,coluna,valor))
    return resultado
    

#Mesma função que a anterior, mas retorna um mapa com a associação entre
#os valores únicos do atributo e a divisão que lhe foi feita,

def separaMatrizPorColunaAtributoMapa(matriz,coluna):
    valoresUnicosColuna = getColumnUniqueFromMatrix(coluna,matriz)
    resultado = {}
    for valor in valoresUnicosColuna:
        resultado[valor] = obtemLinhasDaMatrizPorValorEmColuna(matriz,coluna,valor)
    return resultado




#dada o valor de um atributo e uma matriz com uma linha com nomes de atributos
#  separa a matriz por dito nome
#nota: assume que esse atributo existe na matriz, returnando vazio caso contrário


def separaMatrizPorNomeAtributo(matriz,atributo):
    atributos = matriz[HEADER][:RESULTADO]
    coluna = 0
    for atrAux in len(atributos):
        if(atributos[atrAux] == atributo): 
            coluna = atrAux
            break

    #Nota: escolher um dos métodos de retorno abaixo mais tarde
    
    #retorna uma lista com as matrizes da separação da matriz pelo atributo
    return separaMatrizPorColunaAtributo(matriz,coluna)

    #retorna um mapa que a cada valor único do atributo
    #associa a matriz que lhe está associada
    #return separaMatrizPorColunaAtributoMap(matriz,coluna)



#Dada a matriz a dividir e as funções de impureza e de ganho a usar, 
#calcula qual o atributo a fazer a divisão por
#e retorna a divisão com base nessa classe

#Notas Ezequiel: esta função assume que a função de ganho está
#feita como tendo 3 parametros: a impureza a usar, a matriz com os dados 
# e um atributo xi identificado pelo seu nome

#Nota adicional: esta função corresponde a um passo na divisão da árvore

#Nota adiconal 2: no futuro provavelmente será boa ideia
#retornar em vez de uma lista de matrizes um mapa que a cada 
#lista associa o nº de classes que têm(i.e., um dicionário)

#nota: retorna o atributo para a função recursive

def calculaAtributomelhor(matriz,funcaoImpureza,funcaoGanho):
    atributos = matriz[HEADER][:RESULTADO]
    classes = matriz[HEADER][RESULTADO:]
    maxGanho = 0
    atributoMaxGanho = matriz[HEADER][0]

    for atributo in atributos:
        ganhoAtributo = funcaoGanho(funcaoImpureza,matriz,atributo)
        if(ganhoAtributo>maxGanho):
            maxGanho = ganhoAtributo
            atributoMaxGanho = atributo
    
    return atributoMaxGanho,separaMatrizPorNomeAtributo(matriz,atributoMaxGanho)


#função auxiliar à recursiva abaixo
#serve para prunning à arvore

def prunningDeArvore(matriz):
    classes = contagemDeClasse(matriz)
    numeroElementosMatriz = len(matriz)
    for classe in classes:
        #se o número de elementos de qualquer classe for mais de 90% do total
        if( (classe[1] / numeroElementosMatriz) > 0.9):
            return True
    return False


    
#função que dada uma matriz, seus atributos e 2 funções(impureza e ganho) 
#cria a árvore de decisão revursivamente

#Notas Ezequiel:
#devido à importância desta função por favor confirmem que funciona devidamente
#enquanto que vou testar gostaria de ter confirmação de que funciona

#Nota2: esta função é recursiva

def calculaArvoreDecisaoDadaMatrizRec(matriz,atributos,funcaoImpureza,funcaoGanho):

    if( (not atributos) or (prunningDeArvore(matriz)) ):
        #Caso paragem: atributos == [] (i.e., não temos mais divisões possiveis)
        # ou o nº de elementos de uma classe supera uma certa percentagem(prunning)
        return matriz
    else:
        #caso recursivo: atributos ainda existem
        atributo,divisao = calculaAtributomelhor(matriz,funcaoImpureza,funcaoGanho)
        arvore = []
        novosAtributos = atributos.remove(atributo)
        for mat in divisao:
            arvore.append( 
                calculaArvoreDecisãoDadaMatrizRec(mat,novosAtributos,funcaoImpureza,funcaoGanho) 
            )
        #nota: devido a como está a ser construido,
        # a estrutura final será um lista de matrizes que corresponde a todas as divisões feitas
        #(pelo menos é essa a ideia)
        #,i.e., é uma lista com os ramos finais da árvore
        return arvore


#dada uma percentagem e uma matriz separa matriz através de percentagem
#, retornando 2 conjuntos de percentagem% e (100-percentagem)% 
# do tamanho do dataset original)

def divideMatrizPorPercentagem(matriz,percentagem):
    tamanho = len(matriz)
    tamanhoPercentagem = tamanho * (percentagem/100)
    return matriz[:tamanhoPercentagem],matriz[tamanhoPercentagem:]



#dada uma percentagem cria a árvore com as percentagem% primeiras entradas dos dados
#retorna tanto a árvore criada como os outros (100-percentagem)% dos dados

def calculaArvoreDecisaoParteMatriz(matriz,percentagem,funcaoImpureza,funcaoGanho):
    treino,teste = divideMatrizPorPercentagem(matriz,percentagem)
    arvore = calculaArvoreDecisãoDadaMatrizRec(matriz,funcaoImpureza,funcaoGanho)
    return arvore,teste

