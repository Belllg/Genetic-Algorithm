import math

class Drone:
    def __init__(self):
        self.autonomia = 1800  # em segundos (30 minutos = 1800 segundos)
        self.bateria = self.autonomia  # em segundos, começando cheia
        self.pouso = False 
        self.parar = False

    def calcular_tempo_voo(self, distancia, velocidade, vento_velocidade, vento_direcao, angulo_voo):
        """Calcula o tempo de voo entre duas coordenadas em segundos"""
        while True:
            # Ajustar a velocidade considerando o vento
            velocidade_ajustada = self.ajustar_velocidade_com_vento(velocidade, vento_velocidade, vento_direcao, angulo_voo)
            # Convertendo a velocidade ajustada de km/h para km/s
            velocidade_kmps = velocidade_ajustada / 3600  # Km/s
            # Calcula o tempo de voo
            tempo_voo = distancia / velocidade_kmps  # em segundos
            # Calcula o consumo de bateria para o tempo e velocidade
            consumo_bateria = self.calcular_consumo_bateria(tempo_voo, velocidade)
            # Calcula o alcance do robô com a bateria disponível
            alcance = consumo_bateria * velocidade_kmps
            
            # Verifica se o alcance é suficiente para a distância desejada
            if alcance >= distancia:
                break  # Condição satisfeita, saímos do loop
            else:
                velocidade -= 1  # Reduz a velocidade se o alcance for insuficiente

        # Retorna os valores calculados
        return math.ceil(tempo_voo), velocidade, consumo_bateria

    def ajustar_velocidade_com_vento(self, velocidade, vento_velocidade, vento_direcao, angulo_voo):
        """Ajusta a velocidade do drone de acordo com a direção e velocidade do vento"""
        # Aplique o efeito do vento na velocidade
        print(f"Tipo de self.vento_direcao: {type(vento_direcao)}")
        angulo_vento = math.radians(vento_direcao)
        angulo_voo_rad = math.radians(angulo_voo)

        # Fórmula simplificada para ajuste de velocidade com vento
        efeito_vento = math.cos(angulo_voo_rad - angulo_vento) * vento_velocidade

        velocidade_ajustada = velocidade + efeito_vento

        return velocidade_ajustada

    def calcular_consumo_bateria(self, tempo_voo, velocidade):
        """Calcula o tempo de operação considerando a velocidade e ajustando proporcionalmente ao cubo da velocidade."""
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

    def verificar_autonomia(self, tempo_voo, tempoRestante, consumo_bateria):
        """Verifica se a autonomia do drone é suficiente para o voo"""
        # Se o consumo total for maior que a autonomia do drone, o drone precisa pousar para recarga
        if consumo_bateria > self.bateria:
            self.pouso = True
            self.bateria = self.autonomia  # Recarga total
            if((tempo_voo + 60 + 60) > tempoRestante):#Se apos recarga tem tempo sobrando par voar e tirar foto
                self.parar = True
                return False       
        self.bateria -= consumo_bateria  # Subtrai o consumo da bateria
        return True  # Tem autonomia suficiente
    
    def realizar_voo(self, distancia, velocidade, vento_velocidade, vento_direcao, angulo_voo, tempoRestante):
        """Simula o voo do drone, calcula a distância, tempo e consumo de bateria"""   
        self.pouso = False 
        self.parar = False    
    
        # Calcular o tempo de voo
        tempo_voo, velocidade, consumo_bateria = self.calcular_tempo_voo(distancia, velocidade, vento_velocidade, vento_direcao, angulo_voo)
        
        #Verificar se sobra tempo para voar e chagar la para retirar foto
        if (tempo_voo + 60) > tempoRestante:
            self.parar = True
        else:
            # Verificar se há autonomia suficiente
            if not self.verificar_autonomia(tempo_voo, tempoRestante, consumo_bateria):
                return self.pouso, self.parar
        
        return tempo_voo, velocidade, self.pouso, self.parar
