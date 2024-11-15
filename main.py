"Classe principal de algoritmo genetico"
import time
from src.genetico import AlgoritmoGenetico

inicio = time.time()
# Exemplo de uso:
ceps_list = [(0.0, 0.0), (5.0, 2.0), (5.0, 2.0), (6.0, 6.0), (6.0, 6.0),  (1.0, 2.0), (6.0, 6.0), (6.0, 6.0), (6.0, 6.0), (1.0, 2.0),  (2.0, 4.0), (2.0, 4.0), (6.0, 6.0), (3.0, 5.0), (6.0, 6.0),  (3.0, 5.0), (3.0, 5.0), (5.0, 2.0), (1.0, 2.0), (5.0, 2.0),  (2.0, 4.0), (8.0, 3.0), (3.0, 5.0), (1.0, 2.0), (1.0, 2.0),  (6.0, 6.0), (2.0, 4.0), (5.0, 2.0), (1.0, 2.0), (3.0, 5.0),  (1.0, 2.0), (0.0, 0.0), (3.0, 5.0), (6.0, 6.0), (2.0, 4.0),  (8.0, 3.0), (2.0, 4.0), (0.0, 0.0), (0.0, 0.0), (5.0, 2.0),  (0.0, 0.0), (8.0, 3.0), (5.0, 2.0), (2.0, 4.0), (8.0, 3.0),  (1.0, 2.0), (8.0, 3.0), (6.0, 6.0), (2.0, 4.0), (1.0, 2.0)]
# Cria o objeto do Algoritmo Genético
ag = AlgoritmoGenetico(ceps_list, tamanho_populacao=50, geracoes=2000, taxa_mutacao=0.03, taxa_genes_antigos=0.8)

# Executa o Algoritmo Genético
melhor_rota, distancia_minima = ag.evoluir_populacao()
fim = time.time()

# Exibe a melhor rota e a distância mínima
print("Melhor rota:", melhor_rota)
print("Distância mínima:", distancia_minima)
print("Tempo para rodar o programa:", inicio - fim)