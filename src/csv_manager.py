"""Todas funcoes relacionadas a CSV"""
import csv

class CoordenadasCSV:
    """Carregar cordendas"""
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo

    def carregar_csv(self):
        """Carregar o csv"""
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

def salvar_csv(solucao, nome_arquivo="solucao_voo.csv"):
    """Salva a solução da simulação em um arquivo CSV."""
    with open(nome_arquivo, mode="w", newline="", encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=[
            "CEP inicial", "Latitude inicial", "Longitude inicial", "Dia do voo", "Hora inicial",
            "Velocidade", "CEP final", "Latitude final", "Longitude final", "Pouso", "Hora final"
        ])
        writer.writeheader()
        writer.writerows(solucao)

    print(f"Solução salva em {nome_arquivo}.")

def gerar_solucao(melhor_rota, ceps):
    """Gera a solução formatada para salvar no CSV a partir da melhor rota e variáveis calculadas"""
    solucao = []

    # Cria um dicionário de coordenadas CEP → (latitude, longitude)
    coordenadas_dict = {coord['cep']: (coord['latitude'], coord['longitude']) for coord in ceps}

    for i in range(len(melhor_rota) - 1):
        cep_inicial, velocidade, horario_inicial, dia, pouso, _ = melhor_rota[i]
        cep_final, _, horario_final, _, _, _ = melhor_rota[i + 1]
        

        # Recupera as coordenadas dos CEPs
        lat_inicial, lon_inicial = coordenadas_dict.get(cep_inicial, (None, None))
        lat_final, lon_final = coordenadas_dict.get(cep_final, (None, None))

        # Adiciona as informações no formato adequado para o CSV
        solucao.append({
            "CEP inicial": cep_inicial,
            "Latitude inicial": lat_inicial,
            "Longitude inicial": lon_inicial,
            "Dia do voo": dia,  # Extraímos o dia da data/hora
            "Hora inicial": horario_inicial.split(' ')[1],  # Extraímos a hora da data/hora
            "Velocidade": velocidade,
            "CEP final": cep_final,
            "Latitude final": lat_final,
            "Longitude final": lon_final,
            "Pouso": pouso,
            "Hora final": horario_final
        })

    return solucao