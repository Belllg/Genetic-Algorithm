import math


def distancia(lat1, lon1, lat2, lon2):
    # Converte latitude e longitude de graus para radianos
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Calcula a diferença entre as coordenadas
    dLat = lat2 - lat1
    dLon = lon2 - lon1

    # Aplica a fórmula de Haversine
    a = math.sin(dLat / 2)**2 + math.cos(lat1) * \
        math.cos(lat2) * math.sin(dLon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Raio médio da Terra em quilômetros
    raio = 6371.0
    distancia = raio * c

    return distancia


def calcular_distancia_total(rota, cidades):
    distancia_total = 0
    for i in range(len(rota) - 1):
        distancia_total += distancia(cidades[rota[i]], cidades[rota[i + 1]])
    # Retornar à cidade de origem
    distancia_total += distancia(cidades[rota[-1]], cidades[rota[0]])
    return distancia_total
