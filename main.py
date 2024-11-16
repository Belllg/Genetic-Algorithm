"Classe principal de algoritmo genetico"
import time
from src.genetico import AlgoritmoGenetico
from src.csvManager import CoordenadasCSV

inicio = time.time()

ceps_list = CoordenadasCSV('data/coordenadas.csv').carregar_csv()
#ceps_list = CoordenadasCSV('data/coordenadasMenores.csv').carregar_csv()

ag = AlgoritmoGenetico(ceps_list, tamanho_populacao=50, geracoes=10, taxa_mutacao=0.03, taxa_genes_antigos=0.8)
melhor_rota, distancia_minima = ag.evoluir_populacao()

fim = time.time()
print("Melhor rota:", melhor_rota)
print("Distância mínima:", distancia_minima)
print("Tempo para rodar o programa:", inicio - fim)