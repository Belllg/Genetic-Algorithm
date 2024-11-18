"""Modulo com funções de Evolucao"""
import random
from src.distancia import calcular_distancia, calcular_distancia_total, calcular_angulo
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
            velocidades, horarios, dias, pousos, tempos = self.simular(rota, dia, voo_velocidade)

            # Cria o indivíduo (tupla) com as informações da rota, velocidades, horários, etc.
            individuo = tuple(zip(rota, velocidades, horarios, dias, pousos, tempos))

            # Se o indivíduo não foi gerado ainda, adiciona à população
            if individuo not in populacao_inicial:
                populacao_inicial.add(individuo)

            print("Rota Criada")

        # Retorna a população inicial como uma lista
        return list(populacao_inicial)

    def simular(self, rota, dia, voo_velocidade):
        """Verificar rota e velocidade com o drone"""
        velocidades, horarios, dias, pousos, tempos = [], [], [], [], []
        i = 0
        while i < len(rota) - 1:
            cep1 = rota[i]
            cep2 = rota[i + 1]
            voo_angulo = calcular_angulo(self.ceps[cep1], self.ceps[cep2])
            distancia = calcular_distancia(self.ceps[cep1], self.ceps[cep2])
            vento = self.vento.obter_vento(dia.obter_dia(), dia.obter_horario())
            vento_velocidade, vento_direcao = vento["velocidade"], vento["direcao"]
            tempo_voo, velocidade, pouso, parar = self.drone.realizar_voo(
                distancia,
                voo_velocidade[i],
                vento_velocidade,
                vento_direcao,
                voo_angulo,
                dia.obter_tempo_restante()
            )
            dia.passar_tempo(tempo_voo)

            pousos.append(pouso)
            velocidades.append(velocidade)
            horarios.append(dia.obter_horario_formatado())
            dias.append(dia.obter_dia())

            # Se o voo foi bem-sucedido, atualiza o tempo total
            tempo_total = dia.obter_tempo_total() if tempo_voo != 0 else 99999999
            tempos.append(tempo_total)

            # Se o drone deve parar, avançamos o dia e repetimos a iteração
            if parar:
                dia.avancar_dia()
                i -= 1  # Reduz o índice para repetir a iteração anterior
                i = max(i, 0)#garante que ele n chegue a zero
            i += 1  # Avança para o próximo índice

        return velocidades, horarios, dias, pousos, tempos

    def crossover(self, pai1, pai2):
        """Função de crossover para gerar um filho considerando rotas"""
        inicio = random.randint(0, len(pai1) - 2)
        fim = random.randint(inicio, len(pai1) - 1)

        # Inicializa o filho como lista com os segmentos do pai1
        filho = list(pai1[inicio:fim])

        # Adiciona segmentos de pai2 que não estão no filho
        for segmento in pai2:
            if segmento not in filho:
                filho.append(segmento)

        return tuple(filho)  # Retorna como tupla, se necessário

    def mutacao(self, rota):
        """Função de mutação para alterar uma rota, incluindo as velocidades e os ângulos"""
        rota = list(rota)  # Converte a rota para lista para permitir alterações

        # Primeira iteração corrigida para usar apenas o índice 'i'
        for i, _ in enumerate(rota):
            if random.random() < self.taxa_mutacao:
                # Escolhe um índice aleatório para troca
                j = random.randint(0, len(rota) - 1)
                rota[i], rota[j] = rota[j], rota[i]  # Troca os elementos

        # Recalcular as velocidades e ângulos para todos os pontos da rota
        for i, _ in enumerate(rota):
            if i < len(rota) - 1:
                proximo_idx = rota[i + 1][0]
            else:  # Último ponto, conecta ao primeiro
                proximo_idx = rota[0][0]

            # Atualiza cada elemento da rota com nova velocidade e ângulo
            rota[i] = (
                rota[i][0],
                random.randint(30, 60),  # Nova velocidade aleatória
                calcular_angulo(self.ceps[rota[i][0]], self.ceps[proximo_idx])
            )

        return tuple(rota)  # Retorna como tupla, se necessário

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
