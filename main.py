"Classe principal de algoritmo genetico"
from src.genetico import AlgoritmoGenetico

# Exemplo de uso:
ceps_list = [
    (0.0, 0.0),
    (1.0, 2.0),
    (2.0, 4.0),
    (3.0, 5.0),
    (5.0, 2.0),
    (6.0, 6.0),
    (8.0, 3.0)
]

# Cria o objeto do Algoritmo Genético
ag = AlgoritmoGenetico(ceps_list, tamanho_populacao=10, geracoes=50, taxa_mutacao=0.1)

# Executa o Algoritmo Genético
melhor_rota, distancia_minima = ag.evoluir_populacao()

# Exibe a melhor rota e a distância mínima
print("Melhor rota:", melhor_rota)
print("Distância mínima:", distancia_minima)
