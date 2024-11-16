"""Modulo para calcular distancias"""
import math

def distancia(cep1, cep2):
    """Usa a fórmula de Haversine para calcular a distância"""
    # Convertendo as coordenadas de graus para radianos
    lat1, lon1 = math.radians(cep1['latitude']), math.radians(cep1['longitude'])
    lat2, lon2 = math.radians(cep2['latitude']), math.radians(cep2['longitude'])

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
    """Calcula a distância total da rota, garantindo que todas as distâncias entre pontos sejam menores que 15 km."""
    distancia_total = 0
    for i in range(len(rota) - 1):
        # Verifica a distância entre os pontos consecutivos
        dist = distancia(ceps[rota[i]], ceps[rota[i + 1]])
        if dist > 15:  # Se a distância for maior que 15 km, a rota é inválida
            return float('inf')  # Retorna infinito, indicando que a rota não é viável
        distancia_total += dist
    # Também verifica a distância entre o último e o primeiro ponto
    dist = distancia(ceps[rota[-1]], ceps[rota[0]])
    if dist > 15:  # Verifica a última distância da rota
        return float('inf')
    distancia_total += dist
    return distancia_total
