"""Modulo para calcular distancias"""
import math

def calcular_distancia(cep1, cep2):
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

def calcular_distancia_total(ceps, rota):
    """Calcula a distância total"""
    distancia_total = 0
    for i in range(len(rota) - 1):
        cep1 = rota[i][0]
        cep2 = rota[i + 1][0]
        distancia = calcular_distancia( ceps[cep1],  ceps[cep2])
        distancia_total += distancia
        # Por exemplo, aumentando a distância com maior velocidade
    return distancia_total

def calcular_angulo(cep1, cep2):
    """
    Calcula o ângulo (bearing) entre dois pontos geográficos.

    :param cep1: Dicionário com as coordenadas do ponto 1 ('latitude', 'longitude')
    :param cep2: Dicionário com as coordenadas do ponto 2 ('latitude', 'longitude')
    :return: Ângulo em graus em relação ao norte verdadeiro.
    """

    lat1, lon1 = math.radians(cep1['latitude']), math.radians(cep1['longitude'])
    lat2, lon2 = math.radians(cep2['latitude']), math.radians(cep2['longitude'])

    # Diferença de longitude
    delta_lon = lon2 - lon1

    # Fórmula para calcular o ângulo
    x = math.sin(delta_lon) * math.cos(lat2)
    y = (math.cos(lat1) * math.sin(lat2)
         - math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon))
    angulo = math.atan2(x, y)

    # Converter de radianos para graus
    angulo = math.degrees(angulo)

    # Garantir que o ângulo seja positivo (0° a 360°)
    if angulo < 0:
        angulo += 360

    if abs(delta_lon) == math.pi:  # Isso corresponde a 180 graus
        angulo = 180
    return angulo
