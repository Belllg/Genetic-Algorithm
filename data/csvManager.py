import csv

class CoordenadasCSV:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo

    def carregar_csv(self):
        coordenadas = []
        with open(self.caminho_arquivo, mode='r', encoding='utf-8') as file:
            leitor = csv.DictReader(file)
            next(leitor)
            for linha in leitor:
                # Convertendo os valores de latitude e longitude para float
                coordenadas.append({
                    'cep': int(linha['cep']),
                    'latitude': float(linha['latitude']),
                    'longitude': float(linha['longitude'])
                })
        return coordenadas
