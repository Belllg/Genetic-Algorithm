"Classe principal de algoritmo genetico"
import time
from src.genetico import AlgoritmoGenetico
from src.simulacao import SimulacaoVoo
from src.csvManager import CoordenadasCSV

ventos = {
    1: {  # Dia 1
        "06:00:00": {"velocidade": 17, "direcao": 67.5},
        "09:00:00": {"velocidade": 18, "direcao": 90},
        "12:00:00": {"velocidade": 19, "direcao": 90},
        "15:00:00": {"velocidade": 19, "direcao": 90},
        "18:00:00": {"velocidade": 20, "direcao": 90},
    },
    2: {  # Dia 2
        "06:00:00": {"velocidade": 20, "direcao": 90},
        "09:00:00": {"velocidade": 19, "direcao": 90},
        "12:00:00": {"velocidade": 16, "direcao": 90},
        "15:00:00": {"velocidade": 19, "direcao": 90},
        "18:00:00": {"velocidade": 21, "direcao": 90},
    },
    3: {  # Dia 3
        "06:00:00": {"velocidade": 15, "direcao": 67.5},
        "09:00:00": {"velocidade": 17, "direcao": 45},
        "12:00:00": {"velocidade":  8, "direcao": 45},
        "15:00:00": {"velocidade": 20, "direcao": 90},
        "18:00:00": {"velocidade": 16, "direcao": 90},
    },
    4: {  # Dia 4
        "06:00:00": {"velocidade": 3, "direcao": 247.5},
        "09:00:00": {"velocidade": 3, "direcao": 247.5},
        "12:00:00": {"velocidade": 7, "direcao": 247.5},
        "15:00:00": {"velocidade": 7, "direcao": 202.5},
        "18:00:00": {"velocidade": 10, "direcao": 90},
    },
    5: {  # Dia 5
        "06:00:00": {"velocidade":  4, "direcao": 45},
        "09:00:00": {"velocidade":  5, "direcao": 67.5},
        "12:00:00": {"velocidade":  4, "direcao": 45},
        "15:00:00": {"velocidade":  8, "direcao": 90},
        "18:00:00": {"velocidade": 15, "direcao": 90},
    },
}
inicio = time.time()

ceps_list = CoordenadasCSV('data/coordenadas.csv').carregar_csv()
#ceps_list = CoordenadasCSV('data/coordenadasMenores.csv').carregar_csv()

ag = AlgoritmoGenetico(ceps_list, tamanho_populacao=50, geracoes=10, taxa_mutacao=0.03, taxa_genes_antigos=0.8)
melhor_rota, distancia_minima = ag.evoluir_populacao()
simulacao = SimulacaoVoo(melhor_rota, ventos)
simulacao.executar_simulacao()
fim = time.time()
print("Distância mínima:", distancia_minima)
print("Tempo para rodar o programa:", inicio - fim)


