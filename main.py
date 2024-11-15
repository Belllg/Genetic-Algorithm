"Classe principal de algoritmo genetico"
import time
from src.genetico import AlgoritmoGenetico

inicio = time.time()
# Exemplo de uso:
#ceps_list =[]
ceps_list = [
    (1, 0.0, 0.0), (2, 5.0, 2.0), (3, 5.0, 2.0), (4, 6.0, 6.0), (5, 6.0, 6.0),
    (6, 1.0, 2.0), (7, 6.0, 6.0), (8, 6.0, 6.0), (9, 6.0, 6.0), (10, 1.0, 2.0),
    (11, 2.0, 4.0), (12, 2.0, 4.0), (13, 6.0, 6.0), (14, 3.0, 5.0), (15, 6.0, 6.0),
    (16, 3.0, 5.0), (17, 3.0, 5.0), (18, 5.0, 2.0), (19, 1.0, 2.0), (20, 5.0, 2.0),
    (21, 2.0, 4.0), (22, 8.0, 3.0), (23, 3.0, 5.0), (24, 1.0, 2.0), (25, 1.0, 2.0),
    (26, 6.0, 6.0), (27, 2.0, 4.0), (28, 5.0, 2.0), (29, 1.0, 2.0), (30, 3.0, 5.0),
    (31, 1.0, 2.0), (32, 0.0, 0.0), (33, 3.0, 5.0), (34, 6.0, 6.0), (35, 2.0, 4.0),
    (36, 8.0, 3.0), (37, 2.0, 4.0), (38, 0.0, 0.0), (39, 0.0, 0.0), (40, 5.0, 2.0),
    (41, 0.0, 0.0), (42, 8.0, 3.0), (43, 5.0, 2.0), (44, 2.0, 4.0), (45, 8.0, 3.0),
    (46, 1.0, 2.0), (47, 8.0, 3.0), (48, 6.0, 6.0), (49, 2.0, 4.0), (50, 1.0, 2.0)
]
# Cria o objeto do Algoritmo Genético
ag = AlgoritmoGenetico(ceps_list, tamanho_populacao=100, geracoes=1200, taxa_mutacao=0.03, taxa_genes_antigos=0.7)

# Executa o Algoritmo Genético
melhor_rota, distancia_minima = ag.evoluir_populacao()
fim = time.time()

# Exibe a melhor rota e a distância mínima
print("Melhor rota:", melhor_rota)
print("Distância mínima:", distancia_minima)
print("Tempo para rodar o programa:", inicio - fim)