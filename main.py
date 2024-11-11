# A funcao de distannciai retorna km
import itertools

# Função para calcular a distância entre duas cidades


def distancia(cidade1, cidade2):
    x1, y1 = cidade1
    x2, y2 = cidade2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

# Função para calcular a distância total de uma determinada rota


def calcular_distancia_total(rota, cidades):
    distancia_total = 0
    for i in range(len(rota) - 1):
        distancia_total += distancia(cidades[rota[i]], cidades[rota[i + 1]])
    # Retornar à cidade de origem
    distancia_total += distancia(cidades[rota[-1]], cidades[rota[0]])
    return distancia_total

# Função principal para resolver o TSP usando força bruta


def tsp(cidades):
    # Obter todas as permutações possíveis das cidades
    num_cidades = len(cidades)
    rotas = itertools.permutations(range(num_cidades))

    # Encontrar a rota de menor distância
    melhor_rota = None
    menor_distancia = float('inf')
    for rota in rotas:
        distancia_atual = calcular_distancia_total(rota, cidades)
        if distancia_atual < menor_distancia:
            menor_distancia = distancia_atual
            melhor_rota = rota

    return melhor_rota, menor_distancia


# Exemplo de cidades com coordenadas (x, y)
cidades = [(0, 0), (1, 2), (2, 4), (3, 5), (5, 2)]

# Resolver o problema do caixeiro viajante
rota, distancia_minima = tsp(cidades)

# Exibir a rota e a distância mínima
print("Melhor rota:", rota)
print("Distância mínima:", distancia_minima)


# from src.distancia import haversine
