"Classe principal de algoritmo genetico"
import time
from src.genetico import AlgoritmoGenetico
from src.csv_manager import CoordenadasCSV, gerar_solucao, salvar_csv

inicio = time.time()

ceps_list = CoordenadasCSV('data/coordenadas.csv').carregar_csv()
#ceps_list = CoordenadasCSV('data/coordenadasMenores.csv').carregar_csv()

ag = AlgoritmoGenetico(ceps_list, tamanho_populacao=1200, geracoes=130, taxa_mutacao=0.03)
melhor_rota, distancia_minima = ag.evoluir_populacao()

fim = time.time()
solucao = gerar_solucao(melhor_rota, ceps_list)
salvar_csv(solucao)
print("Distância mínima:", distancia_minima)
print("Tempo para rodar o programa:", inicio - fim)
