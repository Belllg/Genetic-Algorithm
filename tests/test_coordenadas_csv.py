"""Teste Unitario do csv_manager"""
import unittest
import csv
import sys
import os
from unittest.mock import mock_open, patch
# Adiciona o diretório src ao caminho de busca de módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from csv_manager import CoordenadasCSV, salvar_csv, gerar_solucao

class TestCoordenadasCSV(unittest.TestCase):
    """"Teste de carregar csv"""
    @patch("builtins.open",
           new_callable=mock_open,
           read_data="cep,latitude,longitude\n1,10.0,20.0\n2,12.0,22.0\n")
    def test_carregar_csv(self, mock_file):
        """Testa a leitura de um arquivo CSV com coordenadas"""
        coordenadas_csv = CoordenadasCSV("caminho_ficticio.csv")
        coordenadas = coordenadas_csv.carregar_csv()  # Chama o método para carregar os dados

        for cps in coordenadas:
            print(cps)

        # Verifica se o número de coordenadas está correto
        self.assertEqual(len(coordenadas), 2)  # Agora estamos verificando a lista retornada

        # Verifica se os dados foram lidos corretamente
        self.assertEqual(coordenadas[0]['cep'], 1)
        self.assertEqual(coordenadas[0]['latitude'], 10.0)
        self.assertEqual(coordenadas[0]['longitude'], 20.0)

        self.assertEqual(coordenadas[1]['cep'], 2)
        self.assertEqual(coordenadas[1]['latitude'], 12.0)
        self.assertEqual(coordenadas[1]['longitude'], 22.0)

        # Verifica se o método open foi chamado corretamente
        mock_file.assert_called_once_with("caminho_ficticio.csv", mode='r', encoding='utf-8')

    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_carregar_csv_com_arquivo_vazio(self, mock_file):
        """Testa a leitura de um arquivo CSV vazio"""
        coordenadas_csv = CoordenadasCSV("caminho_ficticio.csv")
        coordenadas = coordenadas_csv.carregar_csv()

        # Verifica se a lista está vazia, já que o arquivo simulado está vazio
        self.assertEqual(coordenadas, [])
        mock_file.assert_called_once_with("caminho_ficticio.csv", mode='r', encoding='utf-8')

    @patch("builtins.open",
           new_callable=mock_open,
           read_data="cep,latitude,longitude\n1,10.0,20.0\n2,not_a_number,22.0\n")
    def test_carregar_csv_com_dado_invalido(self, mock_file):
        """Testa o caso onde o CSV contém dados inválidos."""
        coordenadas_csv = CoordenadasCSV("caminho_ficticio.csv")
        with self.assertRaises(ValueError):  # Espera-se uma exceção quando o dado é inválido
            coordenadas_csv.carregar_csv()
        mock_file.assert_called_once_with("caminho_ficticio.csv", mode='r', encoding='utf-8')

    @patch("builtins.open",
           new_callable=mock_open,
           read_data="cep,latitude,longitude\n1,10.0,20.0\n2,12.0,22.0\n")
    def test_chamada_do_metodo_carregar_csv(self, mock_file):
        """Verifica se a função de carregar_csv foi chamada corretamente."""
        coordenadas_csv = CoordenadasCSV("caminho_ficticio.csv")
        coordenadas_csv.carregar_csv()

        mock_file.assert_called_once_with("caminho_ficticio.csv", mode='r', encoding='utf-8')

    def test_salvar_csv(self):
        """Testa a função de salvar solução em CSV"""
        # Dados de exemplo para a solução
        solucao = [
            {
                "CEP inicial": 12345,
                "Latitude inicial": 19.937,
                "Longitude inicial": 43.941,
                "Dia do voo": 1,
                "Hora inicial": "06:00",
                "Velocidade": 50,
                "CEP final": 67890,
                "Latitude final": 19.939,
                "Longitude final": 43.944,
                "Pouso": "Sim",
                "Hora final": "06:30"
            }
        ]

        # Nome do arquivo onde a solução será salva
        nome_arquivo = "solucao_voo.csv"

        # Utiliza o mock do open para não criar o arquivo fisicamente
        with patch("builtins.open", new_callable=unittest.mock.mock_open) as mock_file:
            salvar_csv(solucao, nome_arquivo)
            mock_file.assert_called_once_with(nome_arquivo, mode="w", newline="", encoding='utf-8')
            handle = mock_file()
            writer = csv.DictWriter(handle, fieldnames=solucao[0].keys())
            writer.writeheader()
            writer.writerows(solucao)
            handle.write.assert_called()

    def test_gerar_solucao(self):
        """Testa a função de gerar solução para o CSV"""
        melhor_rota = [
            (0, 50, "06:00", 1, True),
            (1, 55, "06:30", 1, False),
        ]

        ceps = [
            {'cep': 12345, 'latitude': 19.937, 'longitude': 43.941},
            {'cep': 67890, 'latitude': 19.939, 'longitude': 43.944},
        ]

        # Gera a solução
        solucao = gerar_solucao(melhor_rota, ceps)

        # Verifica se a solução gerada tem a estrutura correta
        self.assertEqual(len(solucao), 1)

        # Verifica se as informações no dicionário estão corretas
        self.assertEqual(solucao[0]['CEP inicial'], 12345)
        self.assertEqual(solucao[0]['Latitude inicial'], 19.937)
        self.assertEqual(solucao[0]['Longitude inicial'], 43.941)
        self.assertEqual(solucao[0]['Dia do voo'], 1)
        self.assertEqual(solucao[0]['Hora inicial'], "06:00")
        self.assertEqual(solucao[0]['Velocidade'], 50)
        self.assertEqual(solucao[0]['CEP final'], 67890)
        self.assertEqual(solucao[0]['Latitude final'], 19.939)
        self.assertEqual(solucao[0]['Longitude final'], 43.944)
        self.assertEqual(solucao[0]['Pouso'], True)
        self.assertEqual(solucao[0]['Hora final'], "06:30")

if __name__ == "__main__":
    unittest.main()
