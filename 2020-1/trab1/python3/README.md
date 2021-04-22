# Algoritmos em Python3

## Pacotes do projeto

Pacotes do projeto:

- Modelos: Classes básicas que serão manipuladas, a principio mantive a modelagem do Grafo utilizando uma matriz de adjacência. Futuramente pode ser que eu precise criar uma classe Nó e outra Aresta.
- Arquivos: Realizam a leitura e escrita de Grafos em arquivos externos. Padrão adotado nos arquivos:
```txt
0: 1 2 3
1: 1 2
2: 0
3: 1 3
```
O número anterior aos dois pontos representa o nó de origem. Os números após os dois pontos ':' indicam para quais nós esse grafo vai. No momento grafos com pesos das arestas não conseguem ser lidos.
- Algoritmos: Algoritmos da disciplina de grafos que irão rodas em cima das classes do pacote de modelos.

### Modelos

Pacote com as classes básicas

Para importar uma classe de pacote, basta incluir no começo do fonte:

    from models.NomeClasse import NomeClasse

### Algoritmos

Pacote com os algoritmos que irão rodar em cima das classes básicas

Para importar uma classe de pacote, basta incluir no começo do fonte:

    from algoritmos.NomeClasse import NomeClasse