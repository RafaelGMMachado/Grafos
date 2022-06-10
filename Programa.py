#############################################################################
# Nome: Trabalho de Teoria dos Grafos
# Autor: Rafael Machado
# Data: 30/03/2022
# Resumo: Identificar as características de um Grafo a partir da sua matriz de adjascência.
#############################################################################

import os

RESET = "\033[0;0m"
NEGRITO = "\033[;1m"
RED = "\033[1;31m"
BLUE = "\033[1;34m"

def main():
    arquivo = open("A.txt", "r")
    conteudo = arquivo.readlines()
    arquivo.close()
    for n in range(len(conteudo)):
        conteudo[n] = conteudo[n].split()
    conteudo = list(filter(None, conteudo)) #Filtra a lista para remover itens vazios

    existe, graus, soma = SeqGraus(conteudo)
    if not existe:
        exit()
        
    NArestas(soma)
    simples = GrafoSimples(conteudo)
    GrafoCompleto(conteudo, simples)
    GrafoRegular(graus)

    bipartido, x, y = GrafoBipartido(conteudo)
    GrafoBipartidoCompleto(simples, bipartido, x, y)
    
def SeqGraus(Matriz): # Verifica a sequência dos graus do Grafo
    graus = []
    for linha in range(len(Matriz)):
        graus.append(0)
        for coluna in range(len(Matriz)):
            if linha == coluna:
                graus[linha] += (int(Matriz[linha][coluna])*2)
            else:
                graus[linha] += int(Matriz[linha][coluna])

    soma = 0
    for item in range(len(graus)):
        soma += graus[item]

    if soma%2 == 1:
        print(NEGRITO + RED + "\nO grafo não existe!\n" + RESET)
        return False, graus, soma
    else:
        graus = decrescente(graus)
        print(NEGRITO + "\nSequência dos graus do grafo:", end=" " + RESET)
        print(*graus, sep=", ")
        return True, graus, soma

def decrescente(graus):
    graus = sorted(graus) # Organizar itens em ordem crescente
    graus = graus[::-1] # Inverter a lista
    return graus


def NArestas(SomaGraus): # Verifica o número de arestas do Grafo
    arestas = SomaGraus/2
    print(NEGRITO + "Número de arestas do grafo:", end=" " + RESET)
    print(int(arestas))

def VerLacos(Matriz): # Verifica se existem laços ou arestas múltiplas no grafo
    lacos = []
    Amultiplas = []

    for linha in range(len(Matriz)):
        for coluna in range(linha, len(Matriz)): # Duas estruturas de repetição para passar pelos itens da matriz
            if linha == coluna and int(Matriz[linha][coluna]) > 0: # Se o valor da célula for maior que 0 ela é um laço
                lacos.append("v{0}".format (linha+1))
            elif int(Matriz[linha][coluna]) > 1: # Se o valor da célula for maior que 1 ela é aresta multipla
                Amultiplas.append("v{0} e v{1}".format (linha+1, coluna+1))

    return lacos, Amultiplas

def GrafoSimples(Matriz):
    lacos, Amultiplas = VerLacos(Matriz)

    if lacos and Amultiplas:
        print(NEGRITO + "\nO grafo é simples?" + RED + " Não" + RESET)
        print("O grafo não é simples pois apresenta laços e arestas múltiplas!\n")
        printLacos(lacos, Amultiplas)
        return False

    elif lacos or Amultiplas:
        if lacos: # Se a lista não estiver vazia, o grafo tem laços
            print(NEGRITO + "\nO grafo é simples?" + RED + " Não" + RESET)
            print("O grafo não é simples pois apresenta laços!\n")

        if Amultiplas: # Se a lista não estiver vazia, o grafo tem Arestas Múltiplas
            print(NEGRITO + "\nO grafo é simples?" + RED + " Não" + RESET)
            print("O grafo não é simples pois apresenta arestas múltiplas!\n")

        printLacos(lacos, Amultiplas)
        return False
    else:
        print(NEGRITO + "\nO grafo é simples?" + BLUE + " Sim" + RESET)
        print("O grafo é simples pois não apresenta laços nem arestas multiplas!\n")
        return True
def printLacos (lacos, Amultiplas):
    if lacos:
        print(NEGRITO + "Vértices com laços:", end=" " + RESET)
        print(*lacos, sep=", ")
    else:
        print("O grafo não tem laços")

    if Amultiplas:
        print(NEGRITO + "Vértices com arestas múltiplas:", end=" " + RESET)
        print(*Amultiplas, sep=", ")
    else:
        print("O grafo não tem arestas múltiplas")
    print("")

def GrafoCompleto(Matriz, simples):
    if not simples:
        completo = False
    else:
        completo = True
        for linha in range(len(Matriz)):
            for coluna in range(len(Matriz)):
                if linha == coluna and int(Matriz[linha][coluna]) != 0: # Se o valor da célula for maior que 0 ela é um laço
                    completo = False
                    break
                elif linha != coluna and int(Matriz[linha][coluna]) != 1: # Se o valor da célula for maior que 1 ela é aresta multipla
                    completo = False
                    break
    if completo:
        print(NEGRITO + "O grafo é completo?" + BLUE + " Sim" + RESET)
        print("O grafo é completo pois é simples e cada vértice é adjacente a todos os outros vértices")
    else:
        print(NEGRITO + "O grafo é completo?" + RED + " Não" + RESET)
        if not simples:
            print("O grafo não é completo pois não é simples")
        else:
            print("O grafo não é completo pois, apesar de ser simples, nem todos os vértices são adjacentes a todos os outros vértices")

def GrafoRegular(graus):
    regular = True
    for item in graus:
        if graus[0] == item:
            pass
        else:
            regular = False
            break
    
    if regular:
        print(NEGRITO + "\nO grafo é regular?" + BLUE + " Sim" + RESET)
        print("O grafo é regular pois todos os vértices tem o mesmo grau")
    else:
        print(NEGRITO + "\nO grafo é regular?" + RED + " Não" + RESET)
        print("O grafo não é regular pois nem todos os vértices tem o mesmo grau")

def GrafoBipartido (Matriz):
    x = [0]
    y = []
    bipar = True
    # Dar uma verificada sobre quando tiver laços
    for linha in range(len(Matriz)):
        for coluna in range(len(Matriz)):
            if linha in x and int(Matriz[linha][coluna]) != 0 and coluna not in y:
                if coluna in x:
                    bipar = False
                else:
                    y.append(coluna)
            elif linha in y and int(Matriz[linha][coluna]) != 0 and coluna not in x:
                if coluna in y:
                    bipar = False
                else:
                    x.append(coluna)
    if bipar:
        print(NEGRITO + "\nO grafo é bipartido?" + BLUE + " Sim" + RESET)
        print("O grafo é bipartido pois os vértices podem ser divididos em dois conjuntos disjuntos")
        printbiparticao(x, y)
        return True, x, y
    else:
        print(NEGRITO + "\nO grafo é bipartido?" + RED + " Não" + RESET)
        print("O grafo não é bipartido pois os vértices não podem ser divididos em dois conjuntos disjuntos")
        return False, False, False

def GrafoBipartidoCompleto (simples, bipartido, x, y):
    if simples and bipartido:
        print(NEGRITO + "\nO grafo é bipartido completo?" + BLUE + " Sim" + RESET)
        print("O grafo é bipartido completo pois é simples e bipartido")
        printbiparticao(x, y)
    else:
        print(NEGRITO + "\nO grafo é bipartido completo?" + RED + " Não" + RESET)
        if not bipartido:
            print("O grafo não é bipartido completo pois não é bipartido")
        elif not simples:
            print("O grafo não é bipartido completo pois, apesar de ser bipartido, ele não é simples")


def printbiparticao (x, y):
    print(NEGRITO + "Bipartição:" + RESET)
    print("X = {", end="")
    for v in x:
        if v == x[-1]:
            print("v{0}".format (v+1), end="}\n")
        else:
            print("v{0}".format (v+1), end=", ")

    print("Y = {", end="")
    for v in y:
        if v == y[-1]:
            print("v{0}".format (v+1), end="}\n")
        else:
            print("v{0}".format (v+1), end=", ")

main()