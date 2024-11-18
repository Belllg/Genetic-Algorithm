"""Simula a passagem de tempo"""

class ContadorDeTempo:
    """Simula a passagem de tempo"""
    def __init__(self, horas_por_dia, dias):
        """
        Inicializa o contador de tempo.
        :param horas_por_dia: Número de horas por dia.
        :param dias: Número de dias para a simulação.
        """
        self.horas_por_dia = horas_por_dia
        self.dias = dias
        self.segundos_por_dia = horas_por_dia * 3600  # Converte horas em segundos
        self.total_segundos = 0  # Tempo total em segundos
        self.dia_atual = 1
        self.hora_atual = 0  # Hora inicial do dia, em segundos

    def obter_horario_formatado(self):
        """Retorna o horário atual no formato HH:MM."""
        hora = self.hora_atual // 3600  # Horas
        minuto = (self.hora_atual % 3600) // 60  # Minutos
        return f"{int(hora + 6):02}:{int(minuto):02}"#Soma 6 para hora aparecer com 6+

    def obter_horario(self):
        """Retorna o horário atual sem formatar."""
        return self.hora_atual

    def obter_dia(self):
        """Retorna o dia atual."""
        return self.dia_atual

    def obter_tempo_restante(self):
        """Obter tem restante"""
        return self.segundos_por_dia - self.hora_atual

    def obter_tempo_total(self):
        """Obtem o tempo total"""
        return self.total_segundos

    def passar_tempo(self, segundos):
        """
        Avança o contador de tempo em segundos.
        :param segundos: Quantidade de segundos a avançar.
        """
        self.total_segundos += segundos
        self.hora_atual += segundos

        # Verificar se avançou para o próximo dia
        if self.hora_atual >= self.segundos_por_dia:
            self.hora_atual = 0
            self.avancar_dia()

    def avancar_dia(self):
        """Avança para o próximo dia."""
        if self.dia_atual <= self.dias:
            self.dia_atual += 1
            self.hora_atual = 0  # Reseta para o início do dia
