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
        self.vento = Vento()
        self.drone = Drone()
        self.populacao = self.criar_populacao_inicial()

    def criar_populacao_inicial(self):
        """Cria a população inicial """
        populacao_inicial = set()
        while len(populacao_inicial) < self.tamanho_populacao:
             # Gera uma rota aleatória
            rota = random.sample(range(len(self.ceps)), len(self.ceps))
            voo_velocidade = [random.randint(30, 60) for _ in range(len(self.ceps))]
            dia = ContadorDeTempo(13, 5)

            # Simula o voo com a rota e coleta os dados
            self.drone.resetar_drone()
            velocidades, horarios, dias, pousos, tempos = simular(self, rota, dia, voo_velocidade)

            # Cria o indivíduo (tupla) com as informações da rota, velocidades, horários, etc.
            individuo = tuple(zip(rota, velocidades, horarios, dias, pousos, tempos))

            # Se o indivíduo não foi gerado ainda, adiciona à população
            if individuo not in populacao_inicial:
                populacao_inicial.add(individuo)

            print("Rota Criada")

        # Retorna a população inicial como uma lista
        return list(populacao_inicial)

    def crossover(self, pai1, pai2):
        """Função de crossover para gerar um filho considerando rotas e velocidades"""
        # Define pontos de início e fim para o crossover
        inicio = random.randint(0, len(pai1) - 2)
        fim = random.randint(inicio + 1, len(pai1) - 1)

        # Inicializa o filho com parte da rota e velocidades do pai1
        filho_rota = list(pai1[inicio:fim])
        filho_velocidades = list([p[1] for p in pai1[inicio:fim]])

        # Adiciona os pontos e velocidades de pai2 que não estão no filho
        for i, ponto in enumerate(pai2):
            if ponto not in filho_rota:
                filho_rota.append(ponto)
                filho_velocidades.append(pai2[i][1])  # Adiciona a velocidade correspondente de pai2

        # Garante que o filho tenha a mesma quantidade de pontos e velocidades que os pais
        if len(filho_rota) < len(pai1):
            for i, ponto in enumerate(pai1):
                if ponto not in filho_rota:
                    filho_rota.append(ponto)
                    filho_velocidades.append(pai1[i][1])

        # Agora, criamos a nova população de maneira correta
        filho = []
        for i, ponto in enumerate(filho_rota):
            # Para cada ponto da rota, cria-se uma tupla (cep, velocidade, horario, pouso, tempo)
            filho.append((filho_rota[i][0],   # Cep
                        filho_velocidades[i],  # Velocidade
                        ponto[2],  # Horário do ponto (substitua conforme necessário)
                        ponto[3],  # dias (substitua conforme necessário)
                        ponto[4],  # Pouso (substitua conforme necessário)
                        ponto[5]))  # Tempo (substitua conforme necessário)
        return filho

    def mutacao(self, rota):
        """Função de mutação para alterar o cep e a velocidade da rota"""
        rota = list(rota)  # Converte a rota para lista para permitir alterações

        # Aplica a troca de cep e velocidade com probabilidade de mutação
        for i, ponto in enumerate(rota):  # Percorre cada elemento da rota
            if random.random() < self.taxa_mutacao:
                j = random.randint(0, len(rota) - 1)  # Escolhe um índice aleatório
                # Troca o cep e a velocidade de i e j
                cep_i, velocidade_i, horario_i, dia_i, pouso_i, tempo_i = rota[i]
                cep_j, velocidade_j, horario_j, dia_j, pouso_j, tempo_j = rota[j]

                # Realiza a troca dos cêps e das velocidades, mas mantém os outros valores
                rota[i] = (cep_j, velocidade_i, horario_i, dia_i, pouso_i, tempo_i)
                rota[j] = (cep_i, velocidade_j, horario_j, dia_j, pouso_j, tempo_j)

        # Modificar aleatoriamente a velocidade de um ponto da rota
        for i, ponto in enumerate(rota):  # Percorre cada ponto da rota
            if random.random() < self.taxa_mutacao:
                # Modifica aleatoriamente a velocidade de um ponto específico
                nova_velocidade = random.randint(30, 60)  # Velocidade aleatória entre 30 e 60
                cep, _, horario, dias, pouso, tempo = ponto  # Pega os outros valores da tupla sem modificar
                rota[i] = (cep, nova_velocidade, horario, dias, pouso, tempo)  # Atualiza a tupla apenas com a nova velocidade

        # Retorna a rota mutada como tupla
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
            for segmento in individuo:
                _, _, _, _, pouso, tempo_segmento = segmento
                distancia_total += calcular_distancia(
                    self.ceps[segmento[0]],
                    self.ceps[individuo[(individuo.index(segmento) + 1) % len(individuo)][0]]
                )
                tempo_total += tempo_segmento
                if pouso:
                    numero_pousos += 1# Fórmula de aptidão: menor distância e pousos são melhores
            return distancia_total + (numero_pousos * 1000) + tempo_total

        # Ordena a população com base na aptidão (menor valor é melhor)
        return sorted(self.populacao, key=calcular_aptidao)

    def evoluir_populacao(self):
        """Evolui a população através de elitismo, crossover e mutação"""
        print("Populacao Inicial Criada")
        melhor_rota_encontrada = None
        menor_distancia = float('inf')
        for _ in range(self.geracoes):
            # Ordena a população pela aptidão (menor distância)
            populacao_ordenada = self.fitness()

            # Verifica se a população está vazia
            if len(populacao_ordenada) < 2:
                raise ValueError("A população inicial ou gerada está vazia.")

            # Seleciona os dois melhores indivíduos (elitismo)
            nova_populacao = populacao_ordenada[:2]
            pai1, pai2 = nova_populacao[0], nova_populacao[1]  # Pais já estão na nova_populacao

            # Gera o restante da nova população com crossover e mutação
            while len(nova_populacao) < self.tamanho_populacao:
                filho = self.crossover(pai1, pai2)  # Aplica crossover
                filho_m = self.mutacao(filho)  # Aplica mutação
                print(filho_m)
                # Recalcula as variáveis dependentes (velocidade, ângulo, tempo, pousos, etc.)
                dia = ContadorDeTempo(13, 5)  # Inicializa o contador de tempo
                self.drone.resetar_drone()  # Recarga o drone
                velocidades, horarios, dias, pousos, tempos = simular_tuple(self,
                                                                            filho_m,
                                                                            dia,
                                                                            [x[1] for x in filho_m])

                # Cria um novo indivíduo com as informações recalculadas
                novo_individuo = [
                    (cep, velocidade, horario, dias, pouso, tempo)  # Combinando os dados de filho_m com as variáveis recalculadas
                    for (cep, _, _, _, _, _), velocidade, horario, dias, pouso, tempo in zip(filho_m, velocidades, horarios, dias, pousos, tempos)
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
