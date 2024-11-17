"""Modulo com funções de Evolucao"""
import random
from src.distancia import calcularDistancia, calcular_distancia_total, calcular_angulo
from src.dia import ContadorDeTempo
from src.vento import Vento
from src.drone import Drone

class AlgoritmoGenetico:
    """Classe do algoritmo genético"""
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
        self.vento = Vento()
        self.drone = Drone()
        self.populacao = self.criar_populacao_inicial()
        

    def criar_populacao_inicial(self):
        """Cria a população inicial composta por rotas embaralhadas, garantindo unicidade e incluindo parâmetros de voo"""
        tempo_maximo = 3600 * 13 * 5
        populacao_inicial = []
        while len(populacao_inicial) < self.tamanho_populacao:
            rota = random.sample(range(len(self.ceps)), len(self.ceps))
            dia = ContadorDeTempo(13, 5)
            velocidades = []  # Velocidades aleatórias entre 30 e 60 km/h
            horarios = []
            dias = []
            pousos = []
            valides = []
            tempos = []
            for i in range(len(rota) - 1):
                valido = True
                cep1 = rota[i]
                cep2 = rota[i + 1]
                voo_angulo = calcular_angulo(self.ceps[cep1], self.ceps[cep2])
                voo_velocidade = random.randint(30, 60) 
                distancia = calcularDistancia(self.ceps[cep1], self.ceps[cep2])
                vento = self.vento.obter_vento(dia.obter_dia(), dia.obter_horario())
                vento_velocidade, vento_direcao = vento["velocidade"], vento["direcao"]
                tempo_voo, velocidade, pouso, parar = self.drone.realizar_voo( distancia, voo_velocidade, vento_velocidade, vento_direcao, voo_angulo, dia.obter_tempo_restante())
                pousos.append(pouso)
                dia.passar_tempo(tempo_voo)
                velocidades.append(velocidade)
                horarios.append(dia.obter_horario_formatado)
                dias.append(dia.obter_dia)
                tempo_total = dia.obter_tempo_Total()
                tempos.append(tempo_total)
                if parar:
                    dia.avancar_dia()
                if distancia > 15 or tempo_total > tempo_maximo:
                    valido = False
                    valides.append(valido)
                    break
                valides.append(valido)
            individuo = list(zip(rota, velocidades, horarios, dias, pousos, valides, tempos))
            if individuo not in populacao_inicial:
                populacao_inicial.append(individuo)
    
        return populacao_inicial

    def crossover(self, pai1, pai2):
        """Função de crossover para gerar um filho considerando rotas, velocidades e ângulos"""
        inicio = random.randint(0, len(pai1) - 2)
        fim = random.randint(inicio, len(pai1) - 1)
        filho = pai1[inicio:fim]

        # Adiciona segmentos de pai2 que não estão no filho
        for segmento in pai2:
            if segmento not in filho:
                filho.append(segmento)
        return filho

    def mutacao(self, rota): 
        """Função de mutação para alterar uma rota ligeiramente, incluindo as velocidades e os ângulos"""
        for i in range(len(rota)):
            if random.random() < self.taxa_mutacao:
                # Escolhe um índice aleatório para troca
                j = random.randint(0, len(rota) - 1)
                rota[i], rota[j] = rota[j], rota[i]
        
        # Recalcular as velocidades e os ângulos para todos os pontos da rota
        for i in range(len(rota)):
            if i < len(rota) - 1:
                proximo_idx = rota[i + 1][0]
            else:  # Último ponto, conecta ao primeiro
                proximo_idx = rota[0][0]
            
            # Atualiza cada elemento da rota com nova velocidade e ângulo
            rota[i] = (
                rota[i][0],
                random.randint(30, 60),  # Nova velocidade aleatória
                self.calcular_angulo_entre_pontos(self.ceps[rota[i][0]], self.ceps[proximo_idx])
            )

    def fitness(self):
        """Calcula a aptidão de cada rota e retorna uma população ordenada pela aptidão"""
        return sorted(self.populacao, key=lambda rota: calcular_distancia_total(self.ceps, rota))

    def evoluir_populacao(self):
        """Evolui a população através de elitismo, crossover e mutação, com 20% da população gerada aleatoriamente."""
        melhor_rota_encontrada = None
        menor_distancia = float('inf')

        for _ in range(self.geracoes):
            # Ordena a população pela aptidão (menor distância)
            populacao_ordenada = self.fitness()

            # Verifica se a população está vazia
            if len(populacao_ordenada) < 2:
                raise ValueError("A população inicial ou gerada está vazia. Verifique a geração inicial de indivíduos.")

            # Seleciona os dois melhores indivíduos (elitismo)
            nova_populacao = populacao_ordenada[:2]
            pai1, pai2 = nova_populacao[0], nova_populacao[1]  # Pais já estão na nova_populacao
            
            # Gera o restante da nova população com crossover e mutação
            while len(nova_populacao) < self.tamanho_populacao :
                filho = self.crossover(pai1, pai2)
                self.mutacao(filho)
                nova_populacao.append(filho)

            self.populacao = nova_populacao

            # Atualiza a melhor solução encontrada
            for rota in self.populacao:
                distancia_atual = calcular_distancia_total(self.ceps, rota)
                if distancia_atual < menor_distancia:
                    menor_distancia = distancia_atual
                    melhor_rota_encontrada = rota

        return melhor_rota_encontrada, menor_distancia