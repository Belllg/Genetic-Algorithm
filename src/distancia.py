"""Modulo para calcular distancias"""
import math

def distancia(cep1, cep2):
    """Usa a fórmula de Haversine para calcular a distância"""
    # Convertendo as coordenadas de graus para radianos
    lat1, lon1 = math.radians(cep1[1]), math.radians(cep1[0])
    lat2, lon2 = math.radians(cep2[1]), math.radians(cep2[0])

    # Diferenças entre latitudes e longitudes
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Fórmula de Haversine
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Raio da Terra em quilômetros
    r = 6371.0

    # Distância entre as duas ceps
    distancia_pontos = r * c
    return distancia_pontos


def calcular_distancia_total(rota, ceps):
    """Calcula a distancia de todas as rotas"""
    if not rota:  # Verifica se a lista está vazia
        return 0
    distancia_total = 0
    for i in range(len(rota) - 1):
        distancia_total += distancia(ceps[rota[i]], ceps[rota[i + 1]])
    # Retornar à cep de origem
    distancia_total += distancia(ceps[rota[-1]], ceps[rota[0]])
    return distancia_total
