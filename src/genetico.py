"""Modulo com funções de distancia"""
import random
from src.distancia import calcular_distancia_total

class AlgoritmoGenetico:
    """Classe do algoritmo genético"""
    def __init__(self, ceps, tamanho_populacao, geracoes, taxa_mutacao, taxa_genes_antigos):
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
        self.taxa_genes_antigos = taxa_genes_antigos
        self.populacao = self.criar_populacao_inicial()

    def criar_populacao_inicial(self):
        """Cria a população inicial composta por rotas embaralhadas."""
        populacao_inicial = []
        
        for _ in range(self.tamanho_populacao):
            rota = random.sample(range(len(self.ceps)), len(self.ceps))
            populacao_inicial.append(rota)
        
        return populacao_inicial

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

    def fitness(self):
        """Calcula a aptidão de cada rota e retorna uma população ordenada pela aptidão"""
        return sorted(self.populacao, key=lambda rota: calcular_distancia_total(rota, self.ceps))

    def evoluir_populacao(self):
        """Evolui a população através de elitismo, crossover e mutação, com 20% da população gerada aleatoriamente."""
        melhor_rota_encontrada = None
        menor_distancia = float('inf')

        for _ in range(self.geracoes):
            # Ordena a população pela aptidão (menor distância)
            populacao_ordenada = self.fitness()

            # Seleciona os dois melhores indivíduos (elitismo)
            nova_populacao = populacao_ordenada[:2]
            pai1, pai2 = nova_populacao[0], nova_populacao[1]  # Pais já estão na nova_populacao
            
            # Gera o restante da nova população com crossover e mutação
            while len(nova_populacao) < self.tamanho_populacao * self.taxa_genes_antigos:  # % da população vem de crossover e mutação
                filho = self.crossover(pai1, pai2)
                self.mutacao(filho)
                nova_populacao.append(filho)

            # Gera a população restante aleatoriamente
            while len(nova_populacao) < self.tamanho_populacao:
                rota_aleatoria = random.sample(range(len(self.ceps)), len(self.ceps))
                nova_populacao.append(rota_aleatoria)

            self.populacao = nova_populacao

            # Atualiza a melhor solução encontrada
            for rota in self.populacao:
                distancia_atual = calcular_distancia_total(rota, self.ceps)
                if distancia_atual < menor_distancia:
                    menor_distancia = distancia_atual
                    melhor_rota_encontrada = rota

        return melhor_rota_encontrada, menor_distancia
