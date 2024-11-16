import csv
from datetime import datetime, timedelta
from src.distancia import calcularDistancia
from src.drone import Drone

class SimulacaoVoo:
    def __init__(self, ceps, ventos, tempo_max_dia=13*3600, dias=5):
        """
        Inicializa a simulação de voo.

        :param drone: Instância da classe Drone.
        :param ceps: Lista de tuplas contendo CEP, latitude e longitude.
        :param ventos: Dicionário com velocidades e direções do vento por dia e horário.
        :param ponto_inicial: CEP do ponto inicial e final do voo.
        :param tempo_max_dia: Tempo máximo de voo diário em segundos (13 horas).
        :param dias: Quantidade máxima de dias para completar a simulação.
        """
        self.drone = Drone()
        self.ceps = ceps
        self.ventos = ventos  # Estrutura: {1: {"06:00:00": {"velocidade": 10, "direcao": 90}, ...}, ...}
        self.tempo_max_dia = tempo_max_dia
        self.dias = dias
        self.solucao = []
        self.ponto_inicial = self.ceps[0]

    def obter_vento(self, dia, horario):
        """Obtém as condições de vento para o dia e horário dados."""
        return self.ventos.get(dia, {}).get(horario, {"velocidade": 0, "direcao": 0})

    def executar_simulacao(self):
        """Executa a simulação de voo."""
        dia = 1
        horario_atual = datetime.strptime("06:00:00", "%H:%M:%S")
        tempo_restante_dia = self.tempo_max_dia

        # Inicializar no ponto de partida
        ponto_atual = self.ponto_inicial
        ceps_restantes = self.ceps[:]

        while ceps_restantes and dia <= self.dias:
            proxima_coordenada = ceps_restantes.pop(0)
            lat1, lon1 = ponto_atual['latitude'], ponto_atual['longitude'] 
            lat2, lon2 = proxima_coordenada['latitude'], proxima_coordenada['longitude']

            # Obter vento atual
            vento = self.obter_vento(dia, horario_atual.strftime("%H:%M:%S"))
            vento_velocidade = vento["velocidade"]
            vento_direcao = vento["direcao"]

            # Calcular distância
            distancia = calcularDistancia(ponto_atual, proxima_coordenada)

            # Realizar voo
            tempo_voo, velocidade, pouso, parar = self.drone.realizar_voo(
                distancia, 30, vento_velocidade, vento_direcao, 0, tempo_restante_dia
            )

            # Verificar pouso ou parada
            if parar:
                # Resetar o horário e o tempo restante para o novo dia
                horario_atual = datetime.strptime("06:00:00", "%H:%M:%S")
                tempo_restante_dia = self.tempo_max_dia
                ponto_atual = self.ponto_inicial
                ceps_restantes.insert(0, proxima_coordenada)  # Recoloca o CEP atual na fila
                dia += 1
            else:
                # Verifica se há tempo suficiente para concluir o voo e ainda retirar foto
                if tempo_restante_dia < tempo_voo + 60:
                    parar = True
                else:
                    # Atualizar horário e tempo restante
                    horario_atual += timedelta(seconds=tempo_voo + 60)
                    tempo_restante_dia -= tempo_voo + 60

                    # Adicionar voo à solução
                    self.solucao.append({
                        "CEP inicial": ponto_atual[0],
                        "Latitude inicial": lat1,
                        "Longitude inicial": lon1,
                        "Dia do voo": dia,
                        "Hora inicial": (horario_atual - timedelta(seconds=tempo_voo + 60)).strftime("%H:%M:%S"),
                        "Velocidade": velocidade,
                        "CEP final": proxima_coordenada[0],
                        "Latitude final": lat2,
                        "Longitude final": lon2,
                        "Pouso": "SIM" if pouso else "NÃO",
                        "Hora final": horario_atual.strftime("%H:%M:%S"),
                    })

                    # Atualizar ponto atual
                    ponto_atual = proxima_coordenada

            # Verifica se o limite de dias foi atingido
            if dia > self.dias:
                print("Limite de dias atingido.")
                break

    def salvar_csv(self, nome_arquivo="solucao_voo.csv"):
        """Salva a solução da simulação em um arquivo CSV."""
        with open(nome_arquivo, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=[
                "CEP inicial", "Latitude inicial", "Longitude inicial", "Dia do voo", "Hora inicial",
                "Velocidade", "CEP final", "Latitude final", "Longitude final", "Pouso", "Hora final"
            ])
            writer.writeheader()
            writer.writerows(self.solucao)

        print(f"Solução salva em {nome_arquivo}.")


