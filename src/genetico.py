import random
from distancia import calcular_distancia_total

# Função para calcular a distância entre duas cidades


def criar_rota(cidades):
    rota = list(range(len(cidades)))
    random.shuffle(rota)
    return rota

# Função de crossover para misturar rotas dos pais


def crossover(pai1, pai2):
    inicio = random.randint(0, len(pai1) - 2)
    fim = random.randint(inicio, len(pai1) - 1)
    filho = pai1[inicio:fim]

    # Adiciona cidades de pai2 que não estão no filho
    for cidade in pai2:
        if cidade not in filho:
            filho.append(cidade)
    return filho

# Função de mutação para alterar uma rota ligeiramente


def mutacao(rota, taxa_mutacao=0.1):
    for i in range(len(rota)):
        if random.random() < taxa_mutacao:
            j = random.randint(0, len(rota) - 1)
            rota[i], rota[j] = rota[j], rota[i]

# Função para selecionar rotas com base na aptidão (distância total)


def selecao(populacao, cidades):
    populacao_ordenada = sorted(
        populacao, key=lambda rota: calcular_distancia_total(rota, cidades))
    return populacao_ordenada[:len(populacao)//2]

# Função principal do Algoritmo Genético para TSP


def algoritmo_genetico(cidades, tamanho_populacao=100, geracoes=500, taxa_mutacao=0.1):
    # Cria uma população inicial
    populacao = [criar_rota(cidades) for _ in range(tamanho_populacao)]
    melhor_rota = None
    menor_distancia = float('inf')

    # Evolui a população por um número definido de gerações
    for _ in range(geracoes):
        # Avalia e seleciona metade da população
        populacao = selecao(populacao, cidades)

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
            distancia_atual = calcular_distancia_total(rota, cidades)
            if distancia_atual < menor_distancia:
                menor_distancia = distancia_atual
                melhor_rota = rota

    return melhor_rota, menor_distancia


# Exemplo de coordenadas de cidades
# cidades = [(0, 0), (1, 2), (2, 4), (3, 5), (5, 2), (6, 6), (8, 3)]
cidades = [
    (0.0, 0.0),
    (1.0, 2.0),
    (2.0, 4.0),
    (3.0, 5.0),
    (5.0, 2.0),
    (6.0, 6.0),
    (8.0, 3.0)
]

# Executa o Algoritmo Genético para resolver o TSP
melhor_rota, distancia_minima = algoritmo_genetico(cidades)

# Exibe a melhor rota e a distância mínima
print("Melhor rota:", melhor_rota)
print("Distância mínima:", distancia_minima)
