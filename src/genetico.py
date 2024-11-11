"""Modulo implementar AG"""
import random
from distancia import calcular_distancia_total

def criar_rota(ceps):
    """Embaralha rotas dos pais"""
    rota = list(range(len(ceps)))
    random.shuffle(rota)
    return rota

def crossover(pai1, pai2):
    """Função de mutação para alterar uma rota ligeiramente"""
    inicio = random.randint(0, len(pai1) - 2)
    fim = random.randint(inicio, len(pai1) - 1)
    filho = pai1[inicio:fim]

    # Adiciona ceps de pai2 que não estão no filho
    for cep in pai2:
        if cep not in filho:
            filho.append(cep)
    return filho

def mutacao(rota, taxa_mutacao=0.1):
    """Função para selecionar rotas com base na aptidão (distância total)"""
    for i, _ in enumerate(rota):  # Usando enumerate
        if random.random() < taxa_mutacao:
            j = random.randint(0, len(rota) - 1)
            rota[i], rota[j] = rota[j], rota[i]

def selecao(populacao, ceps):
    """Função de ordenar as rotas"""
    populacao_ordenada = sorted(
        populacao, key=lambda rota: calcular_distancia_total(rota, ceps))
    return populacao_ordenada[:len(populacao)//2]



def algoritmo_genetico(ceps, tamanho_populacao=100, geracoes=500, taxa_mutacao=0.1):
    """Logica principal do AG"""
    # Cria uma população inicial
    populacao = [criar_rota(ceps) for _ in range(tamanho_populacao)]
    melhor_rota_encontrada = None
    menor_distancia = float('inf')

    # Evolui a população por um número definido de gerações
    for _ in range(geracoes):
        # Avalia e seleciona metade da população
        populacao = selecao(populacao, ceps)

        # Cria uma nova geração com crossover e mutação
        nova_populacao = []
        while len(nova_populacao) < tamanho_populacao:
            pai1, pai2 = random.sample(populacao, 2)
            filho = crossover(pai1, pai2)
            mutacao(filho, taxa_mutacao)
            nova_populacao.append(filho)

        populacao = nova_populacao

        # Atualiza a melhor solução encontrada
        for rota in populacao:
            distancia_atual = calcular_distancia_total(rota, ceps)
            if distancia_atual < menor_distancia:
                menor_distancia = distancia_atual
                melhor_rota_encontrada = rota

    return melhor_rota_encontrada, menor_distancia

ceps_list = [
    (0.0, 0.0),
    (1.0, 2.0),
    (2.0, 4.0),
    (3.0, 5.0),
    (5.0, 2.0),
    (6.0, 6.0),
    (8.0, 3.0)
]

# Executa o Algoritmo Genético para resolver o TSP
melhor_rota, distancia_minima = algoritmo_genetico(ceps_list)

# Exibe a melhor rota e a distância mínima
print("Melhor rota:", melhor_rota)
print("Distância mínima:", distancia_minima)
