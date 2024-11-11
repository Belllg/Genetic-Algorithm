import math


def distancia(cidade1, cidade2):
    # Convertendo as coordenadas de graus para radianos
    lat1, lon1 = math.radians(cidade1[0]), math.radians(cidade1[1])
    lat2, lon2 = math.radians(cidade2[0]), math.radians(cidade2[1])

    # Diferenças entre latitudes e longitudes
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Fórmula de Haversine
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * \
        math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Raio da Terra em quilômetros
    R = 6371.0

    # Distância entre as duas cidades
    distancia = R * c
    return distancia


def calcular_distancia_total(rota, cidades):
    distancia_total = 0
    for i in range(len(rota) - 1):
        distancia_total += distancia(cidades[rota[i]], cidades[rota[i + 1]])
    # Retornar à cidade de origem
    distancia_total += distancia(cidades[rota[-1]], cidades[rota[0]])
    return distancia_total
