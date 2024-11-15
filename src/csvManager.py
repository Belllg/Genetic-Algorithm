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

