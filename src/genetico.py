"""Modulo com funções de Evolucao"""
import random
from src.distancia import calcular_distancia, calcular_distancia_total
from src.simulador import simular, simular_tuple
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
            voo_velocidade = [random.randint(30, 60) for _ in range(len(rota))]
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
        """Função de crossover para gerar um filho considerando todas as rotas e velocidades"""
        # Remove o primeiro e o último elementos
        inicio_pai1, fim_pai1 = pai1[0], pai1[-1]

        pai1_corte = pai1[1:-1]  # Elementos intermediários de pai1
        pai2_corte = pai2[1:-1]  # Elementos intermediários de pai2

        # Define pontos de início e fim para o crossover
        inicio = random.randint(0, len(pai1_corte) - 2)
        fim = random.randint(inicio + 1, len(pai1_corte) - 1)

        # Inicializa o filho com parte das rotas e velocidades do pai1
        filho_segmento = pai1_corte[inicio:fim]
        filho_segmento = list(filho_segmento)
        # Adiciona os pontos de pai2 que não estão no segmento
        for ponto in pai2_corte:
            if ponto not in filho_segmento:
                filho_segmento.append(ponto)

        # Garante que o filho tenha a mesma quantidade de pontos que o pai
        if len(filho_segmento) < len(pai1_corte):
            for ponto in pai1_corte:
                if ponto not in filho_segmento:
                    filho_segmento.append(ponto)

        # Reconstrói a rota completa adicionando os elementos removidos
        filho_completo = [inicio_pai1] + filho_segmento + [fim_pai1]

        return filho_completo

    def mutacao(self, rota):
        """Função de mutação para alterar o cep e a velocidade da rota,
        garantindo que o primeiro e o último ponto não sejam alterados."""
        rota = list(rota)  # Converte a rota para lista para permitir alterações

        # Remove o primeiro e o último ponto
        inicio = rota[0]
        fim = rota[-1]
        rota_intermediaria = rota[1:-1]

        # Aplica a mutação nos pontos intermediários
        for i, ponto in enumerate(rota_intermediaria):
            if random.random() < self.taxa_mutacao:
                # Escolhe um índice aleatório dentro dos intermediários
                j = random.randint(0, len(rota_intermediaria) - 1)

                # Realiza a troca de cep e velocidade entre i e j
                cep_i, velocidade_i, horario_i, dia_i, pouso_i, tempo_i = rota_intermediaria[i]
                cep_j, velocidade_j, horario_j, dia_j, pouso_j, tempo_j = rota_intermediaria[j]

                rota_intermediaria[i] = (cep_j, velocidade_i, horario_i, dia_i, pouso_i, tempo_i)
                rota_intermediaria[j] = (cep_i, velocidade_j, horario_j, dia_j, pouso_j, tempo_j)

        # Modificar aleatoriamente a velocidade de um ponto intermediário
        for i, ponto in enumerate(rota_intermediaria):
            if random.random() < self.taxa_mutacao:
                # Modifica aleatoriamente a velocidade
                nova_velocidade = random.randint(30, 60)
                cep, _, horario, dia, pouso, tempo = ponto
                rota_intermediaria[i] = (cep, nova_velocidade, horario, dia, pouso, tempo)

        # Recompõe a rota com os pontos fixos no início e no fim
        rota_mutada = [inicio] + rota_intermediaria + [fim]

        # Retorna a rota mutada como tupla
        return tuple(rota_mutada)

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
            for segmento in individuo:
                _, _, _, _, pouso, tempo_segmento = segmento
                distancia_total += calcular_distancia(
                    self.ceps[segmento[0]],
                    self.ceps[individuo[(individuo.index(segmento) + 1) % len(individuo)][0]]
                )
                tempo_total += tempo_segmento
                if pouso:
                    numero_pousos += 1# Fórmula de aptidão: menor distância e pousos são melhores
            return distancia_total + (numero_pousos * 2) + tempo_total * 4

        # Ordena a população com base na aptidão (menor valor é melhor)
        return sorted(self.populacao, key=calcular_aptidao)

    def evoluir_populacao(self):
        """Evolui a população através de elitismo, crossover e mutação"""
        print("Populacao Inicial Criada")
        melhor_rota_encontrada = None
        menor_distancia = float('inf')
        for i in range(self.geracoes):
            print("Geracao", i + 1)
            # Ordena a população pela aptidão (menor distância)
            populacao_ordenada = self.fitness()

            # Verifica se a população está vazia
            if len(populacao_ordenada) < 2:
                raise ValueError("A população inicial ou gerada está vazia.")

            #Seleciona os dois melhores indivíduos (elitismo)
            nova_populacao = populacao_ordenada[:2]
            pai1, pai2 = nova_populacao[0], nova_populacao[1]  # Pais já estão na nova_populacao

            # Gera o restante da nova população com crossover e mutação
            while len(nova_populacao) < self.tamanho_populacao:
                filho = self.crossover(pai1, pai2)  # Aplica crossover
                filho_m = self.mutacao(filho)  # Aplica mutação
                # Recalcula as variáveis dependentes (velocidade, ângulo, tempo, pousos, etc.)
                dia = ContadorDeTempo(13, 5)  # Inicializa o contador de tempo
                self.drone.resetar_drone()  # Recarga o drone
                velocidades, horarios, dias, pousos, tempos = simular_tuple(self,
                                                                            filho_m,
                                                                            dia,
                                                                            [x[1] for x in filho_m])
                # Cria um novo indivíduo com as informações recalculadas
                novo_individuo = [
                    (cep, velocidade, horario, dias, pouso, tempo)
                    for (cep, _, _, _, _, _), velocidade, horario, dias, pouso, tempo in zip(
                        filho_m,
                        velocidades,
                        horarios,
                        dias,
                        pousos,
                        tempos)
                ]
                nova_populacao.append(novo_individuo)
            self.populacao = nova_populacao

            # Atualiza a melhor solução encontrada
            for rota in self.populacao:
                distancia_atual = calcular_distancia_total(self.ceps, list(rota))
                if distancia_atual < menor_distancia:
                    menor_distancia = distancia_atual
                    melhor_rota_encontrada = rota

        return melhor_rota_encontrada, menor_distancia
