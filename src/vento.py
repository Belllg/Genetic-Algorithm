"""Carregar Vento"""
class Vento:
    """Classe para representar e obter as condições de vento."""

    def __init__(self):
        """:param ventos: Dicionário com os ventos por dia e horário."""
        self.ventos = {
        1: {  # Dia 1
            "06:00:00": {
                "velocidade": 17,
                "direcao": 67.5
            },
            "09:00:00": {
                "velocidade": 18,
                "direcao": 90
            },
            "12:00:00": {
                "velocidade": 19,
                "direcao": 90
            },
            "15:00:00": {
                "velocidade": 19,
                "direcao": 90
            },
            "18:00:00": {
                "velocidade": 20,
                "direcao": 90
            },
        },
        2: {  # Dia 2
            "06:00:00": {
                "velocidade": 20,
                "direcao": 90
            },
            "09:00:00": {
                "velocidade": 19,
                "direcao": 90
            },
            "12:00:00": {
                "velocidade": 16,
                "direcao": 90
            },
            "15:00:00": {
                "velocidade": 19,
                "direcao": 90
            },
            "18:00:00": {
                "velocidade": 21,
                "direcao": 90
            },
        },
        3: {  # Dia 3
            "06:00:00": {
                "velocidade": 15,
                "direcao": 67.5
            },
            "09:00:00": {
                "velocidade": 17,
                "direcao": 45
            },
            "12:00:00": {
                "velocidade": 8,
                "direcao": 45
            },
            "15:00:00": {
                "velocidade": 20,
                "direcao": 90
            },
            "18:00:00": {
                "velocidade": 16,
                "direcao": 90
            },
        },
        4: {  # Dia 4
            "06:00:00": {
                "velocidade": 3,
                "direcao": 247.5
            },
            "09:00:00": {
                "velocidade": 3,
                "direcao": 247.5
            },
            "12:00:00": {
                "velocidade": 7,
                "direcao": 247.5
            },
            "15:00:00": {
                "velocidade": 7,
                "direcao": 202.5
            },
            "18:00:00": {
                "velocidade": 10,
                "direcao": 90
            },
        },
        5: {  # Dia 5
            "06:00:00": {
                "velocidade": 4,
                "direcao": 45
            },
            "09:00:00": {
                "velocidade": 5,
                "direcao": 67.5
            },
            "12:00:00": {
                "velocidade": 4,
                "direcao": 45
            },
            "15:00:00": {
                "velocidade": 8,
                "direcao": 90
            },
            "18:00:00": {
                "velocidade": 15,
                "direcao": 90
            },
        },
    }

    def obter_vento(self, dia, horario):
        """Obtém as condições de vento para o dia e horário dados."""
        if not isinstance(horario, int) or horario < 0:
            raise ValueError("O parâmetro 'horario' deve ser um número inteiro não negativo.")
        if dia > 6:
            return 0, 90

        # Calcula a hora em formato inteiro (não precisa somar 6)
        hora = horario // 3600 # Hora inteira

        # Ajuste para a chave de horário
        hora_str = f"{hora:02d}:00:00"  # Formata para 'hh:00:00'

        # Tenta acessar o vento no dicionário
        vento = self.ventos.get(dia, {}).get(hora_str, {"velocidade": 0, "direcao": 0})

        # Retorna a tupla com velocidade e direção
        return vento["velocidade"], vento["direcao"]
