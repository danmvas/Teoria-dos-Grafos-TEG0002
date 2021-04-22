from graphviz import Graph


class Grafo:

    def __init__(self, direcionado=True):
        self.__matrizAdjacente = {}  # inicializado como dicionário vazio
        self.__pesos = {}  # inicializado como dicionário vazio
        self.__direcionado = direcionado  # booleano, com padrão verdadeiro

    def setDirecionado(self):
        self.__direcionado = True

    def setNaoDirecionado(self):
        self.__direcionado = False

    def isDirecionado(self):  # retorna se o direcionado é true ou false
        return self.__direcionado

    def getNumeroNos(self):  # retorna o número dos nós dado o tamanho da matriz adjacente
        return len(self.__matrizAdjacente)

    def __novaLinha(self, tam):  # método privado?
        lista = []  # incializada uma lista vazia
        for i in range(tam):
            lista.append(0)  # sempre adicionando no topo (pilha!)
        return lista  # retorna a lista agora com a nova linha adicionada

    def getMatrizAdjacente(self):
        return self.__matrizAdjacente  # retorna o dicionário que é a matriz adjacente

    def getMatrizPesos(self):
        return self.__pesos  # retorna o dicionário da matriz que são os pesos

    def insereNo(self):  # inserindo um nó
        # o máximo é o número dos nós dado o tamanho da matriz adjacente
        max = self.getNumeroNos()
        # cria uma lista da matriz adjacente com o número máximo, que recebe a lista feita com o número (max) de linhas
        self.__matrizAdjacente[max] = self.__novaLinha(max)
        # cria uma lista de pesos com o numero máximo, que recebe a lista feita com o número (max) de linhas
        self.__pesos[max] = self.__novaLinha(max)
        if self.getNumeroNos() > 0:  # se o número de nós for maior do que 0...
            for no in self.__matrizAdjacente:  # para cada nó na matriz adjacente
                self.__matrizAdjacente[no].append(0)
            for no in self.__pesos:  # para cada nó nos pesos
                self.__pesos[no].append(0)

    def removerNo(self, no):  # removendo um nó
        # procurando o index do nó passado como parâmetro
        index = self.procuraIndex(no)
        for i in self.__matrizAdjacente.keys():
            self.__matrizAdjacente[i].pop(index)
        self.__matrizAdjacente.pop(no)
        for i in self.__pesos.keys():
            self.__pesos[i].pop(index)
        self.__pesos.pop(no)

    def procuraIndex(self, no):
        cont = 0
        for i in self.__matrizAdjacente.keys():
            if i == no:
                return cont
            else:
                cont += 1
        raise Exception('No não existe')

    def insereArco(self, a1, a2, peso):
        if(a1 < self.getNumeroNos() and a2 < self.getNumeroNos()):
            self.__matrizAdjacente.get(a1)[a2] = 1
            self.__pesos[a1][a2] = int(peso)
            if not self.isDirecionado():
                self.__matrizAdjacente[a2][a1] = 1
                self.__pesos[a2][a1] = int(peso)
        else:
            raise Exception('No não existe')

    def transformaEmNaoDirecionado(self):
        max = len(self.__matrizAdjacente)
        for i in range(0, max):
            for j in range(0, max):
                if self.__matrizAdjacente[i][j] == 1:
                    self.__matrizAdjacente[j][i] = 1
                    self.__pesos[j][i] = self.__pesos[i][j]
        self.setNaoDirecionado()

    def removeArco(self, no1, no2):
        if no1 > self.getNumeroNos() or no2 > self.getNumeroNos():
            # o arco não existe se qualquer um dos nós é de um número maior que o máximo da lista
            raise Exception('Arco não existe')
        else:
            self.__matrizAdjacente[no1][no2] = 0
            self.__pesos[no1][no2] = 0
            if not self.isDirecionado():  # se o grafo não for direcionado, remove o inverso também
                self.__matrizAdjacente[no2][no1] = 0
                self.__pesos[no2][no1] = 0

    def grau(self, no):
        # retorna a soma da linha do nó passado como parâmetro, retornando o grau dele
        return sum(self.__matrizAdjacente[no])

    def __criaArrayVisitados(self, numerico=False):
        visitados = []
        tipo = None
        if(not numerico):
            tipo = False
        else:
            tipo = 0
        for i in range(self.getNumeroNos()):
            visitados.append(tipo)
        return visitados

    def todosVisitados(self, lista: list):  # verifica se todos os nós foram visitados
        for i in lista:  # percorrendo a lista toda
            if i is not True:
                return False
        return True

    def quantidadeVisitados(self, lista: list):
        cont = 0
        for i in lista:
            if i is True:
                cont += 1
        return cont

    def isInCaminho(self, caminho, no):
        for i in caminho:
            if i == no:
                return True
        return False

    def __listaPesos(self):  # pega todas os pesos das arestas e ordena pelo peso
        pesos = []
        matriz = self.__pesos
        for i in matriz.keys():
            for j in range(i, len(matriz[i])):
                if i == j:
                    pass
                if matriz[i][j] != 0:
                    tripla = []
                    tripla.append(i)
                    tripla.append(j)
                    tripla.append(matriz[i][j])
                    pesos.append(tripla)
        return sorted(pesos, key=lambda x: x[2], reverse=False)

    def __rec(self, no, visitados, origem):
        visitados[no] += 1
        for i in range(self.getNumeroNos()):
            if i != no:
                if self.__matrizAdjacente[no][i] == 1 and visitados[i] < 2:
                    if visitados[i] == 0:
                        self.__rec(i, visitados, origem)
                    else:
                        visitados[i] = 2

    def possuiCiclo(self, no, origem):
        visitados = self.__criaArrayVisitados(numerico=True)
        self.__rec(no, visitados, origem)
        if visitados[no] > 1:
            return True
        else:
            return False

##############################################################################################################

    # ALGORITMO DA ÁRVORE DE CUSTO MÍNIMO!! #

    def arvoreCustoMinimo(self):
        custo = 0
        resultado = []
        cont = 0
        visitados = self.__criaArrayVisitados()
        self.__resursaoDFS(0, visitados, cont, None, resultado, custo)
        pilha = []
        solucoes = {}
        i = 0
        while i != len(resultado):
            if resultado[i].startswith('e'):
                resultado[i] = resultado[i].replace('e', '')
            elif resultado[i].startswith('s'):
                resultado[i] = resultado[i].replace('s', '')
            elif resultado[i] not in pilha:
                pilha.append(resultado[i])
                i += 1
            else:
                aux = pilha[-1]
                pilha.pop(-1)
                if aux != resultado[i]:
                    if str(aux).startswith('c'):
                        custo = aux.replace('c', '')
                        if custo not in solucoes.keys():
                            resul = pilha.copy()
                            solucoes[custo] = resul
                else:
                    i += 1
        menor = str(min([int(k) for k in solucoes.keys()]))
        solucao = {}
        solucao['custo'] = menor
        matriz = []
        for i in range(self.getNumeroNos()):
            lista = []
            for i in range(self.getNumeroNos()):
                lista.append(0)
            matriz.append(lista)
        for i in range(0, len(solucoes[menor])-1):
            matriz[i][i+1] = 1
        matriz[0][-1] = 1
        solucao['matriz'] = matriz
        return solucao

##############################################################################################################

    # ALGORITMO DOS MINIMOS SUCESSIVOS!! #

    def minimos(self):

        # aponta pra cada nó
        for i in range(len(self.__matrizAdjacente)):

            visitados = self.__criaArrayVisitados()

            grafo = Grafo(direcionado=False)

            min = 9999999
            no = 0

            # inserindo nó pra cada iteração
            for j in range(len(self.__matrizAdjacente)):
                grafo.insereNo()

            for j in range(len(self.__matrizAdjacente)):
                aresta = []  # teste da dani

                for k in range(len(self.__matrizAdjacente)):
                    aux = []
                    aux.append(j)
                    aux.append(k)
                    aux.append(self.__pesos[j][k])
                    pesos.append(aux)

            # esse for todo nao tinha que tar dentro do k ou do j?
            for aresta in pesos[1:]:
                grau1 = g1.grau(aresta[0])
                grau2 = g1.grau(aresta[1])
                if grau1 == 1 and grau2 == 1:
                    if self.todosVisitados(visitados):
                        g1.insereArco(aresta[0], aresta[1], aresta[2])
                        custo += aresta[2]
                        break
                    else:
                        g1.insereArco(aresta[0], aresta[1], aresta[2])
                        if g1.possuiCiclo(aresta[0], aresta[0]):
                            g1.removeArco(aresta[0], aresta[1])
                        elif g1.possuiCiclo(aresta[1], aresta[1]):
                            g1.removeArco(aresta[0], aresta[1])
                        else:
                            visitados[int(aresta[0])] = True
                            visitados[int(aresta[1])] = True
                            custo += aresta[2]
                elif grau1 < 2 and grau2 < 2:
                    g1.insereArco(aresta[0], aresta[1], aresta[2])
                    visitados[int(aresta[0])] = True
                    visitados[int(aresta[1])] = True
                    custo += aresta[2]

##############################################################################################################

        # ALGORITMO DE ORDENAÇÃO POR PESOS DAS ARESTAS!! #

    def ordenacaoPeso(self, takeo=False, arcoExtra=[]):
        solucao = {}
        custo = 0
        g1 = Grafo(direcionado=False)
        pesos = self.__listaPesos()  # pesos recebe a matriz de todos os pesos dos nós
        visitados = self.__criaArrayVisitados()
        custo += pesos[0][2]
        for i in range(self.getNumeroNos()):
            g1.insereNo()
        g1.insereArco(pesos[0][0], pesos[0][1], pesos[0][2])
        visitados[int(pesos[0][0])] = True
        visitados[int(pesos[0][1])] = True
        g1.insereArco(pesos[0][0], pesos[0][1], pesos[0][2])
        for aresta in pesos[1:]:
            grau1 = g1.grau(aresta[0])
            grau2 = g1.grau(aresta[1])
            if grau1 == 1 and grau2 == 1:
                if self.todosVisitados(visitados):
                    g1.insereArco(aresta[0], aresta[1], aresta[2])
                    custo += aresta[2]
                    break
                else:
                    g1.insereArco(aresta[0], aresta[1], aresta[2])
                    if g1.possuiCiclo(aresta[0], aresta[0]):
                        g1.removeArco(aresta[0], aresta[1])
                    elif g1.possuiCiclo(aresta[1], aresta[1]):
                        g1.removeArco(aresta[0], aresta[1])
                    else:
                        visitados[int(aresta[0])] = True
                        visitados[int(aresta[1])] = True
                        custo += aresta[2]
            elif grau1 < 2 and grau2 < 2:
                g1.insereArco(aresta[0], aresta[1], aresta[2])
                visitados[int(aresta[0])] = True
                visitados[int(aresta[1])] = True
                custo += aresta[2]
        if takeo:
            cont = 0
            index = []
            for i in range(self.getNumeroNos()):
                if g1.grau(i) == 2:
                    cont += 1
                else:
                    index.append(i)
            if cont != self.getNumeroNos() and len(index) == 2:
                for i in pesos:
                    if i[0] == index[0]:
                        if i[1] == index[1]:
                            arcoExtra.extend(i)
                            custo += i[2]
                    elif i[1] == index[0]:
                        if i[0] == index[1]:
                            arcoExtra.extend(i)
                            custo += i[2]
        solucao['grafo'] = g1
        solucao['custo'] = custo
        return solucao

##############################################################################################################

    def getVizinhos(self, no):
        vizinhos = []
        for i in range(self.getNumeroNos()):
            if self.__matrizAdjacente[no][i] == 1:
                vizinhos.append(i)
        return vizinhos

    def __resursaoDFS(self, no, visitados, nivel, pai, resultado, custo):
        if pai is not None:
            custo = custo + self.__pesos[pai][no]
        visitados[no] = True
        resultado.append('e'+str(no))
        if nivel == self.getNumeroNos() - 1:
            if self.__matrizAdjacente[no][0] == 1:
                custo += self.__pesos[no][0]
                resultado.append('c'+str(custo))
            else:
                resultado.append('n')
        for i in range(self.getNumeroNos()):
            if i != no:
                if self.__matrizAdjacente[no][i] == 1 and visitados[i] is False:
                    self.__resursaoDFS(i, visitados, nivel+1,
                                       no, resultado, custo)
                    resultado.append('s'+str(i))
                    visitados[i] = False

    def __str__(self):
        grafo = 'X '
        for no in self.__matrizAdjacente.keys():
            grafo += str(no) + ' '
        grafo += "\n"
        i = 0
        for no in self.__matrizAdjacente.keys():
            grafo += str(no) + ' '
            for elemento in self.__matrizAdjacente[no]:
                grafo += str(elemento)
                grafo += str(" ")
            i += 1
            grafo += '(' + str(self.grau(no)) + ')'
            grafo += "\n"
        return grafo

    def __nomes(self):
        nomes = ''
        # até o número de chaves do dicionário de pesos -> dicionario { valor, chave ; valor 1, chave1 }
        for no in self.__pesos.keys():
            nomes += str(no) + ' '  # nome adiciona o número do nó na aresta
        nomes += "\n"
        return nomes

    def stringPesos(self, nomes=''):  # retorna os pesos de cada nó em uma string
        grafo = 'X '
        if nomes != '':
            grafo += nomes
        else:
            grafo += self.__nomes()
        i = 0
        for no in self.__pesos.keys():
            grafo += str(no) + ' '
            for elemento in self.__pesos[no]:
                grafo += str(elemento)
                grafo += str(" ")
            i += 1
            grafo += '(' + str(self.grau(no)) + ')'
            grafo += "\n"
        return grafo

    # função para gerar as fotos no formato do Graphviz!
    def toGraphviz(self, caminho, percurso=[]):
        self.__dot = Graph(engine='circo')
        for no in self.__matrizAdjacente.keys():
            self.__dot.node(str(no))
        if self.__direcionado:
            for i in range(self.getNumeroNos()):
                for j in range(self.getNumeroNos()):
                    if(self.__matrizAdjacente[i][j] == 1):
                        self.__dot.edge(str(i), str(
                            j), label=str(self.__pesos[i][j]))
        else:
            for i in range(self.getNumeroNos()):
                for j in range(i, self.getNumeroNos()):
                    if(self.__matrizAdjacente[i][j] == 1):
                        self.__dot.edge(str(i), str(
                            j), label=str(self.__pesos[i][j]))

        self.__dot.render(caminho, view=False, format='jpg')
