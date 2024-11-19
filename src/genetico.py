"""Modulo com funções de Evolucao"""
import random
from src.distancia import calcular_distancia, calcular_distancia_total
from src.simulador import simular, simular_tuple
from src.dia import ContadorDeTempo
from src.vento import Vento
from src.drone import Drone

class AlgoritmoGenetico:
    """Classe do algoritmo genético"""
    def __init__(self, ceps, tamanho_populacao, geracoes, taxa_mutacao, porcentagem_aleatoria):
        """
        Inicializa o Algoritmo Genético com os parâmetros fornecidos.
        
        :param ceps: Lista de coordenadas (ceps) que representam os locais.
        :param tamanho_populacao: Número de indivíduos na população.
        :param geracoes: Número de gerações para o algoritmo evoluir.
        :param taxa_mutacao: Taxa de mutação para alterar rotas ligeiramente.
        """
        self.distancias_cache = {}
        self.ceps = ceps
        self.tamanho_populacao = tamanho_populacao
        self.geracoes = geracoes
        self.taxa_mutacao = taxa_mutacao
        self.porcentagem_aleatoria = porcentagem_aleatoria
        self.primeiro = ceps[0]
        self.vento = Vento()
        self.drone = Drone()
        self.populacao = self.criar_populacao_inicial()

    def criar_populacao_inicial(self):
        """Cria a população inicial """
        populacao_inicial = set()
        while len(populacao_inicial) < self.tamanho_populacao:
            # Ajustado para garantir que o primeiro item fique fixo
            indices_meio = random.sample(range(1, len(self.ceps)), len(self.ceps) - 1)
            # Constrói a rota garantindo que o primeiro item seja fixo e o último seja aleatório
            rota = [0]+ indices_meio[1:] + [0]
            voo_velocidade = [random.randint(45, 60) for _ in range(len(rota))]
            dia = ContadorDeTempo(13, 5)

            # Simula o voo com a rota e coleta os dados
            self.drone.resetar_drone()
            velocidades, horarios, dias, pousos, tempos = simular(self, rota, dia, voo_velocidade)

            # Cria o indivíduo (tupla) com as informações da rota, velocidades, horários, etc.
            individuo = tuple(zip(rota, velocidades, horarios, dias, pousos, tempos))

            # Se o indivíduo não foi gerado ainda, adiciona à população
            if individuo not in populacao_inicial:
                populacao_inicial.add(individuo)

        # Retorna a população inicial como uma lista
        return list(populacao_inicial)

    def crossover(self, pai1, pai2):
        """Crossover baseado em ordem (OX)."""
        tamanho = len(pai1)
        inicio = random.randint(1, tamanho // 2)
        fim = random.randint(inicio, tamanho - 2)

        filho = [-1] * tamanho
        filho[inicio:fim] = pai1[inicio:fim]

        posicao = fim
        for gene in pai2:
            if gene not in filho:
                if posicao >= tamanho:
                    posicao = 1  # Ignora o primeiro ponto fixo
                filho[posicao] = gene
                posicao += 1

        filho[0], filho[-1] = pai1[0], pai1[-1]  # Garante pontos fixos
        return filho

    def mutacao(self, rota):
        """Mutação com inversão de segmento."""
        rota = list(rota)
        if random.random() < self.taxa_mutacao:
            i, j = sorted(random.sample(range(1, len(rota) - 1), 2))
            rota[i:j] = reversed(rota[i:j])  # Inversão de segmento

        if random.random() < self.taxa_mutacao:
            ponto = random.randint(1, len(rota) - 2)
            nova_velocidade = max(45, min(60, rota[ponto][1] + random.choice([-5, 5])))
            rota[ponto] = (rota[ponto][0], nova_velocidade, *rota[ponto][2:])

        return tuple(rota)

    def fitness(self):
        """
        Calcula a aptidão de cada rota com base na distância total percorrida.
        Quanto menor a distância, maior a aptidão.
        Retorna a população ordenada pela aptidão.
        """
        def calcular_aptidao(individuo):
            distancia_total = 0
            tempo_total = 0
            numero_pousos = 0
            for i, segmento in enumerate(individuo):
                _, _, _, _, pouso, tempo_segmento = segmento
                proximo_cep = individuo[(i + 1) % len(individuo)][0]
                distancia_total +=self.calcular_distancia_cache(segmento[0], proximo_cep)
                tempo_total += tempo_segmento
                if pouso:
                    numero_pousos += 1

            # Fórmula de aptidão: menor distância, menos pousos e menor tempo são melhores
            return distancia_total * 0.2 + (numero_pousos * 0.1) + tempo_total * 0.9

        # Ordena a população com base na aptidão (menor valor é melhor)
        return sorted(self.populacao, key=calcular_aptidao)

    def evoluir_populacao(self):
        """Evolui a população através de elitismo, crossover, mutação e população nova."""
        melhor_rota_encontrada = None
        menor_distancia = float('inf')

        for i in range(self.geracoes):
            print(f"Geracao {i + 1}")
            populacao_ordenada = self.fitness()

            if len(populacao_ordenada) < 2:
                raise ValueError("A população inicial ou gerada está vazia.")

            # Elitismo: mantém os melhores
            nova_populacao = populacao_ordenada[:2]

            # Gera indivíduos aleatórios para completar a população
            num_aleatorios = int(self.tamanho_populacao * self.porcentagem_aleatoria)
            while len(nova_populacao) < num_aleatorios + 2:
                rota = [0] + random.sample(range(1, len(self.ceps)), len(self.ceps) - 1) + [0]
                voo_velocidade = [random.randint(45, 60) for _ in range(len(rota))]
                dia = ContadorDeTempo(13, 5)

                self.drone.resetar_drone()
                velocidades, horarios, dias, pousos, tempos = simular(self, rota, dia, voo_velocidade)

                individuo = tuple(zip(rota, velocidades, horarios, dias, pousos, tempos))
                if individuo not in nova_populacao:
                    nova_populacao.append(individuo)

            # Completa a população com crossover e mutação
            metade_populacao = len(populacao_ordenada) // 2
            while len(nova_populacao) < self.tamanho_populacao:
                pai1, pai2 = random.sample(populacao_ordenada[:metade_populacao], 2)
                filho = self.mutacao(self.crossover(pai1, pai2))

                dia = ContadorDeTempo(13, 5)
                self.drone.resetar_drone()
                velocidades, horarios, dias, pousos, tempos = simular_tuple(self, filho, dia, [x[1] for x in filho])

                novo_individuo = [
                    (cep, vel, hor, d, p, temp)
                    for (cep, _, _, _, _, _), vel, hor, d, p, temp in zip(filho, velocidades, horarios, dias, pousos, tempos)
                ]
                nova_populacao.append(novo_individuo)

            self.populacao = nova_populacao

            for rota in self.populacao:
                distancia_atual = calcular_distancia_total(self.ceps, list(rota))
                if distancia_atual < menor_distancia:
                    menor_distancia = distancia_atual
                    melhor_rota_encontrada = rota

        return melhor_rota_encontrada, menor_distancia

    def calcular_distancia_cache(self, cep1, cep2):
        """Retorna a distância entre dois CEPs, utilizando cache para evitar cálculos repetidos."""
        if (cep1, cep2) not in self.distancias_cache:
            distancia = calcular_distancia(self.ceps[cep1], self.ceps[cep2])
            self.distancias_cache[(cep1, cep2)] = distancia
            self.distancias_cache[(cep2, cep1)] = distancia  # Distância é simétrica
        return self.distancias_cache[(cep1, cep2)]
