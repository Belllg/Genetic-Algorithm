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
        # Acessa o índice do CEP na melhor rota e usa esse índice para pegar o CEP
        index_inicial = melhor_rota[i][0]  # O valor de index é o número de 0 a 49
        index_final = melhor_rota[i + 1][0]  # O valor de index é o número de 0 a 49

        # Verifique se o índice está dentro do intervalo da lista de ceps
        if index_inicial >= len(ceps) or index_final >= len(ceps):
            print(f"Erro: índice fora do intervalo para os ceps. Índices: {index_inicial}, {index_final}, Tamanho da lista de ceps: {len(ceps)}")
            continue  # Ou raise um erro, dependendo da lógica que você deseja seguir

        # Recupera o CEP de acordo com o índice da melhor rota
        cep_inicial = ceps[index_inicial]['cep']
        cep_final = ceps[index_final]['cep']

        # Recupera as coordenadas dos CEPs
        lat_inicial, lon_inicial = coordenadas_dict.get(cep_inicial, (None, None))
        lat_final, lon_final = coordenadas_dict.get(cep_final, (None, None))

        # Adiciona as informações no formato adequado para o CSV
        solucao.append({
            "CEP inicial": cep_inicial,
            "Latitude inicial": lat_inicial,
            "Longitude inicial": lon_inicial,
            "Dia do voo": melhor_rota[i][3],  # Extraímos o dia da data/hora
            "Hora inicial": melhor_rota[i][2],  # Extraímos a hora da data/hora
            "Velocidade": melhor_rota[i][1],
            "CEP final": cep_final,
            "Latitude final": lat_final,
            "Longitude final": lon_final,
            "Pouso": melhor_rota[i][4],
            "Hora final": melhor_rota[i + 1][2]  # A hora final é de `melhor_rota[i + 1]`
        })

    return solucao
