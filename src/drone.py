import math

#TODO Implementar o modo esportivo de maneira correta
class Drone:
    def __init__(self):
        self.autonomia = 1800  # em segundos (30 minutos = 1800 segundos)
        self.bateria = self.autonomia  # em segundos, começando cheia
        self.pouso = False 
        self.parar = False

    def calcular_tempo_voo(self, distancia, velocidade):
        """Calcula o tempo de voo entre duas coordenadas em segundos"""
        # Convertendo a velocidade de Km/h para Km/s
        velocidade_kmps = velocidade / 3600  # Km/s
        # Tempo de voo = distância / velocidade
        tempo_voo = distancia / velocidade_kmps  # em segundos

        return math.ceil(tempo_voo)  # arredonda para cima

    def ajustar_velocidade_com_vento(self, velocidade, vento_velocidade, vento_direcao, angulo_voo):
        """Ajusta a velocidade do drone de acordo com a direção e velocidade do vento"""
        # Aplique o efeito do vento na velocidade
        angulo_vento = math.radians(vento_direcao)
        angulo_voo_rad = math.radians(angulo_voo)

        # Fórmula simplificada para ajuste de velocidade com vento
        efeito_vento = math.cos(angulo_voo_rad - angulo_vento) * vento_velocidade

        velocidade_ajustada = velocidade + efeito_vento

        return velocidade_ajustada

    #TODO
    def calcular_consumo_bateria(self, tempo_voo, velocidade):
        """Calcula o consumo de bateria durante o voo considerando o modo esportivo"""
        # O modo esportivo consome mais energia. Vamos aumentar o consumo de bateria para esse caso.
        if velocidade  > 30:
            tempo_esportivo = tempo_voo * (30/velocidade) ** 3 
            return tempo_esportivo
        return tempo_voo


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
    
#TODO
    def realizar_voo(self, distancia, velocidade, vento_velocidade, vento_direcao, angulo_voo, tempoRestante):
        """Simula o voo do drone, calcula a distância, tempo e consumo de bateria"""   
        self.pouso = False 
        self.parar = False    
        
        # Ajustar a velocidade conforme o vento
        velocidade_ajustada = self.ajustar_velocidade_com_vento(velocidade, vento_velocidade, vento_direcao, angulo_voo)
        # Calcular o tempo de voo
        tempo_voo = self.calcular_tempo_voo(distancia, velocidade_ajustada)
        
        #Verificar se sobra tempo para voar e chagar la para retirar foto
        if (tempo_voo + 60) > tempoRestante:
            self.parar = True
        else:
            # Calcular o consumo de bateria
            consumo_bateria = self.calcular_consumo_bateria(tempo_voo, velocidade_ajustada)
            # Verificar se há autonomia suficiente
            if not self.verificar_autonomia(tempo_voo, consumo_bateria):
                return self.pouso, self.parar
        
        return tempo_voo, self.pouso, self.parar
