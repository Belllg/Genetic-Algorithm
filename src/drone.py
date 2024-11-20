"""Funcoes e classe do drone"""
import math

class Drone:
    """Drone"""
    def __init__(self):
        self.autonomia = 1800  # em segundos (30 minutos = 1800 segundos)
        self.bateria = self.autonomia  # em segundos, começando cheia
        self.pouso = False
        self.parar = False

    def resetar_drone(self):
        """Reseta o drone"""
        self.autonomia = 1800  # em segundos (30 minutos = 1800 segundos)
        self.bateria = self.autonomia  # em segundos, começando cheia
        self.pouso = False
        self.parar = False

    def calcular_tempo_voo(self,
                           distancia,
                           velocidade,
                           vento_velocidade,
                           vento_direcao,
                           angulo_voo,
                           tempo_restante):
        """Calcula o tempo de voo entre duas coordenadas em segundos"""

        max_iteracoes = 31
        iteracoes = 0
        while  iteracoes < max_iteracoes:
            iteracoes += 1
            if velocidade < 30:
                return 0, 30, 0
            # Ajustar a velocidade considerando o vento
            velocidade_ajustada = self.ajustar_velocidade_com_vento(
                velocidade,
                vento_velocidade,
                vento_direcao,
                angulo_voo)
            # Convertendo a velocidade ajustada de km/h para km/s
            if velocidade_ajustada <= 0:
                return 0, 30, 0
            velocidade_kmps = velocidade_ajustada / 3600  # Km/s
            # Calcula o tempo de voo
            tempo_voo = distancia / velocidade_kmps  # em segundos
            # Calcula o consumo de bateria para o tempo e velocidade
            consumo_bateria = self.calcular_consumo_bateria(tempo_voo, velocidade)
            # Calcula o alcance do robô com a bateria disponível
            alcance = consumo_bateria * velocidade_kmps

            if (tempo_voo + 120) > tempo_restante:
                self.parar = True

            if alcance >= distancia and self.verificar_autonomia(consumo_bateria):
                break  # Condição satisfeita, saímos do loop

            # Verifica se o alcance é suficiente para a distância desejada
            if alcance >= distancia and alcance <= 15:
                break  # Condição satisfeita, saímos do loop
            velocidade -= 1
        if iteracoes > max_iteracoes:
            print ("Alcance, Distancia, Bateria",alcance, distancia, self.bateria)
            print("Fracasso")
            return 0, 30, 0
        # Retorna os valores calculados
        return math.ceil(tempo_voo), velocidade, consumo_bateria

    def ajustar_velocidade_com_vento(self, velocidade, vento_velocidade, vento_direcao, angulo_voo):
        """Ajusta a velocidade do drone de acordo com a direção e velocidade do vento"""
        # Aplique o efeito do vento na velocidade
        angulo_vento = math.radians(vento_direcao)
        angulo_voo_rad = math.radians(angulo_voo)

        # Fórmula simplificada para ajuste de velocidade com vento
        efeito_vento = math.cos(angulo_voo_rad - angulo_vento) * vento_velocidade

        velocidade_ajustada = velocidade + efeito_vento

        return velocidade_ajustada

    def calcular_consumo_bateria(self, tempo_voo, velocidade):
        """Calcula o tempo de operação"""
        # Velocidade de referência (30 km/h)
        velocidade_normal = 30  # km/h
        capacidade_bateria = 1800  # Tempo total de autonomia a 30 km/h

        if velocidade == 30:
            # Se a velocidade for 30 km/h, o consumo é diretamente proporcional ao tempo de voo.
            consumo = tempo_voo  # Nenhum ajuste necessário
        else:
            # Ajuste da autonomia considerando a fórmula do tempo esportivo
            autonomia_ajustada = capacidade_bateria * (velocidade_normal / velocidade) ** 3
            consumo = capacidade_bateria / autonomia_ajustada
            consumo = tempo_voo * consumo

        return consumo

    def verificar_autonomia(self, consumo_bateria):
        """Verifica se a autonomia do drone é suficiente para o voo"""
        # Se o consumo total for maior que a autonomia do drone, o drone precisa pousar para recarga
        if consumo_bateria > self.bateria:
            self.pouso = True
            self.bateria = self.autonomia
            return False
        return True

    def realizar_voo(self,
                     distancia,
                     velocidade,
                     vento_velocidade,
                     vento_direcao,
                     angulo_voo,
                     tempo_restante):
        """Simula o voo do drone, calcula a distância, tempo e consumo de bateria"""
        if distancia > 15:
            return 0, 0, False, False
        self.pouso = False
        self.parar = False
        # Calcular o tempo de voo
        tempo_voo, velocidade, consumo_bateria = self.calcular_tempo_voo(
            distancia,
            velocidade,
            vento_velocidade,
            vento_direcao,
            angulo_voo,
            tempo_restante
        )
        self.bateria -= consumo_bateria  # Subtrai o consumo da bateria
        #Verificar se sobra tempo para voar e chagar la para retirar foto
        if (tempo_voo + 60) > tempo_restante:
            self.parar = True

        return tempo_voo, velocidade, self.pouso, self.parar
