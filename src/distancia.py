"""Modulo para calcular distancias"""
import math

def calcularDistancia(cep1, cep2):
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
    """Calcula a distância total considerando as velocidades e ângulos de voo"""
    distancia_total = 0
    for i in range(len(rota) - 1):
        cep1 = rota[i][0]
        cep2 = rota[i + 1][0]
        distancia = calcularDistancia( ceps[cep1],  ceps[cep2])
        
        # Ajustar a distância com base na velocidade e ângulo de voo
        velocidade = rota[i][1]
        angulo = rota[i][2]
        # Ajuste de distância com base na velocidade e ângulo
        distancia_total += distancia * (1 + (0.1 * velocidade / 30))  # Por exemplo, aumentando a distância com maior velocidade
    return distancia_total

def calcular_angulo(cep1, cep2):
    """
    Calcula o ângulo (bearing) entre dois pontos geográficos.
    
    :param lat1: Latitude do ponto 1 em graus.
    :param lon1: Longitude do ponto 1 em graus.
    :param lat2: Latitude do ponto 2 em graus.
    :param lon2: Longitude do ponto 2 em graus.
    :return: Ângulo em graus em relação ao norte verdadeiro.
    """

    lat1, lon1 = math.radians(cep1['latitude']), math.radians(cep1['longitude'])
    lat2, lon2 = math.radians(cep2['latitude']), math.radians(cep2['longitude'])

    # Converter coordenadas de graus para radianos
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lon = math.radians(lon2 - lon1)

    # Fórmula para calcular o ângulo
    x = math.sin(delta_lon) * math.cos(lat2_rad)
    y = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(delta_lon)
    angulo = math.atan2(x, y)

    # Converter de radianos para graus
    angulo = math.degrees(angulo)

    # Garantir que o ângulo seja positivo (0° a 360°)
    if angulo < 0:
        angulo += 360

    return angulo