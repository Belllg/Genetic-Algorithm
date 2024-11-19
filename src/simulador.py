"""Simular acao"""
from src.distancia import calcular_angulo, calcular_distancia

def simular(self, rota, dia, voo_velocidade):
    """Verificar rota e velocidade com o drone"""
    velocidades, horarios, dias, pousos, tempos = [], [], [], [], []
    i = 0
    while i < len(rota):  # Condição correta para percorrer todos os elementos de 0 a len(rota)-1
        # Verifica se é o último item, para fazer a conexão de volta ao início
        if i == len(rota) - 1:
            cep1 = rota[i]  # O último item
            cep2 = rota[0]  # Conecta de volta ao primeiro item
        else:
            cep1 = rota[i]  # Item atual
            cep2 = rota[i + 1]  # Próximo item
        # Calcula o ângulo de voo e a distância entre os pontos
        voo_angulo = calcular_angulo(self.ceps[cep1], self.ceps[cep2])
        distancia = calcular_distancia(self.ceps[cep1], self.ceps[cep2])

        # Obtemos o vento para o dia e horário atual
        vento = self.vento.obter_vento(dia.obter_dia(), dia.obter_horario())
        vento_velocidade, vento_direcao = vento["velocidade"], vento["direcao"]

        #Realizamos o Voo
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
        i += 1  # Avança para o próximo índice

    return velocidades, horarios, dias, pousos, tempos

def simular_tuple(self, rota, dia, voo_velocidade):
    """Mesmo que anterior so que para evolucao"""
    velocidades, horarios, dias, pousos, tempos = [], [], [], [], []
    i = 0

    while i < len(rota):  # Condição correta para percorrer todos os elementos de 0 a len(rota)-1
        # Verifica se é o último item, para fazer a conexão de volta ao início
        if i == len(rota) - 1:
            cep1 = rota[i][0]  # O último item
            cep2 = rota[0][0]  # Conecta de volta ao primeiro item
        else:
            cep1 = rota[i][0]  # Item atual
            cep2 = rota[i + 1][0]  # Próximo item

        voo_angulo = calcular_angulo(self.ceps[cep1], self.ceps[cep2])
        distancia = calcular_distancia(self.ceps[cep1], self.ceps[cep2])

        # Obtém o vento para o dia e horário atual
        vento = self.vento.obter_vento(dia.obter_dia(), dia.obter_horario())
        vento_velocidade, vento_direcao = vento["velocidade"], vento["direcao"]

        # Realiza o voo
        tempo_voo, velocidade, pouso, parar = self.drone.realizar_voo(
            distancia,
            voo_velocidade[i],  # Aqui você usa a velocidade do voo fornecida
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
        i += 1  # Avança para o próximo índice

    return velocidades, horarios, dias, pousos, tempos
