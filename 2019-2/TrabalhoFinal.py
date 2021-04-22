#Teoria de Grafos
#Daniella Vasconcellos e Guilherme Costa
#Trabalho Final
#18/10/2019

from collections import defaultdict
import os
os.system("cls")

"""
Notas:
- g.grafo[verticeOrigem].get(verticeDestino) // Retorna o valor de um peso
"""

class Grafo:
    def __init__(self):
        self.grafo = defaultdict(dict) 

    #Adiciona Aresta
    def addAresta(self, origem, destino, valor, tipo):         #Adicionando arestas direcionadas. Com o método update ele é capaz de adicionar dicionários até mesmo a dicionários já existentes              
        if (tipo =='rodoviario'):
            self.grafo[origem].update({destino:2*valor})             
        
        elif (tipo =='hidroviario'):
            self.grafo[origem].update({destino:valor}) 

        elif(tipo =='divisao nodo'): #Para o cálculo de fluxo
            self.grafo[origem].update({destino:valor})           

        else: #Para testes do código caso algo dê errado
            print('Tipo invalido. Tentativa de adicao de aresta: {}, {}'.format(origem, destino))

######################################################
#--------------- INICIANDO O GRAFO ------------------#

grafo = Grafo()
grafo.addAresta("Porto Alegre1", "Porto Alegre2", 50, "divisao nodo")
grafo.addAresta("Rio Grande1", "Rio Grande2", 16, "divisao nodo")
grafo.addAresta("Passo Fundo", "Porto Alegre1", 240, "rodoviario")
grafo.addAresta("Cruz Alta", "Porto Alegre1", 360, "rodoviario")
grafo.addAresta("Cruz Alta", "Rio Grande1", 500, "hidroviario")
grafo.addAresta("Porto Alegre", "Passo Fundo", 240, "rodoviario")
grafo.addAresta("Rio Grande2", "Porto", 0, "")