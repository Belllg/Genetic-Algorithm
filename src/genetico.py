"""Modulo com funções de distancia"""
import random
from distancia import calcular_distancia_total

class AlgoritmoGenetico:
    """Classe do algoritmo genetico"""
    def __init__(self, ceps, tamanho_populacao, geracoes, taxa_mutacao):
        """
        Inicializa o Algoritmo Genético com os parâmetros fornecidos.
        
        :param ceps: Lista de coordenadas (ceps) que representam os locais.
        :param tamanho_populacao: Número de indivíduos na população.
        :param geracoes: Número de gerações para o algoritmo evoluir.
        :param taxa_mutacao: Taxa de mutação para alterar rotas ligeiramente.
        """
        self.ceps = ceps
        self.tamanho_populacao = tamanho_populacao
        self.geracoes = geracoes
        self.taxa_mutacao = taxa_mutacao
        self.populacao = self.criar_populacao_inicial()

    def criar_rota(self):
        """Embaralha rotas dos pais"""
        rota = list(range(len(self.ceps)))
        random.shuffle(rota)
        return rota

    def crossover(self, pai1, pai2):
        """Função de crossover para gerar um filho"""
        inicio = random.randint(0, len(pai1) - 2)
        fim = random.randint(inicio, len(pai1) - 1)
        filho = pai1[inicio:fim]

        # Adiciona ceps de pai2 que não estão no filho
        for cep in pai2:
            if cep not in filho:
                filho.append(cep)
        return filho

    def mutacao(self, rota):
        """Função de mutação para alterar uma rota ligeiramente"""
        for i, _ in enumerate(rota):
            if random.random() < self.taxa_mutacao:
                j = random.randint(0, len(rota) - 1)
                rota[i], rota[j] = rota[j], rota[i]

    def selecao(self):
        """Função para selecionar as melhores rotas com base na distância"""
        populacao_ordenada = sorted(
            self.populacao, key=lambda rota: calcular_distancia_total(rota, self.ceps)
        )
        return populacao_ordenada[:len(self.populacao) // 2]

    def criar_populacao_inicial(self):
        """Cria a população inicial de rotas embaralhadas"""
        return [self.criar_rota() for _ in range(self.tamanho_populacao)]

    def evoluir_populacao(self):
        """Evolui a população através de crossover e mutação"""
        melhor_rota_encontrada = None
        menor_distancia = float('inf')

        for _ in range(self.geracoes):
            # Seleciona a metade superior da população
            self.populacao = self.selecao()

            nova_populacao = []
            while len(nova_populacao) < self.tamanho_populacao:
                pai1, pai2 = random.sample(self.populacao, 2)
                filho = self.crossover(pai1, pai2)
                self.mutacao(filho)
                nova_populacao.append(filho)

            self.populacao = nova_populacao

            # Atualiza a melhor solução encontrada
            for rota in self.populacao:
                distancia_atual = calcular_distancia_total(rota, self.ceps)
                if distancia_atual < menor_distancia:
                    menor_distancia = distancia_atual
                    melhor_rota_encontrada = rota

        return melhor_rota_encontrada, menor_distancia
