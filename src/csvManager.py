import csv

class CoordenadasCSV:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo

    def carregar_csv(self):
        coordenadas = []
        with open(self.caminho_arquivo, mode='r', encoding='utf-8') as file:
            leitor = csv.DictReader(file)
            for linha in leitor:
                if linha:  # Verifica se há dados na linha antes de adicionar
                    coordenadas.append({
                        'cep': int(linha['cep']),
                        'latitude': float(linha['latitude']),
                        'longitude': float(linha['longitude'])
                    })
        return coordenadas

    def salvar_csv(self, solucao, nome_arquivo="solucao_voo.csv"):
        """Salva a solução da simulação em um arquivo CSV."""
        with open(nome_arquivo, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=[
                "CEP inicial", "Latitude inicial", "Longitude inicial", "Dia do voo", "Hora inicial",
                "Velocidade", "CEP final", "Latitude final", "Longitude final", "Pouso", "Hora final"
            ])
            writer.writeheader()
            writer.writerows(solucao)

        print(f"Solução salva em {nome_arquivo}.")