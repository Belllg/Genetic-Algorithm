import unittest
from unittest.mock import mock_open, patch
from src.csvManager import CoordenadasCSV  # Supondo que a classe CoordenadasCSV está em src/coordenadas.py

class TestCoordenadasCSV(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="cep,latitude,longitude\n1,10.0,20.0\n2,12.0,22.0\n")
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


    @patch("builtins.open", new_callable=mock_open, read_data="cep,latitude,longitude\n1,10.0,20.0\n2,not_a_number,22.0\n")
    def test_carregar_csv_com_dado_invalido(self, mock_file):
        """Testa o caso onde o CSV contém dados inválidos."""
        coordenadas_csv = CoordenadasCSV("caminho_ficticio.csv")
        with self.assertRaises(ValueError):  # Espera-se uma exceção quando o dado é inválido
            coordenadas_csv.carregar_csv()

    @patch("builtins.open", new_callable=mock_open, read_data="cep,latitude,longitude\n1,10.0,20.0\n2,12.0,22.0\n")
    def test_chamada_do_metodo_carregar_csv(self, mock_file):
        """Verifica se a função de carregar_csv foi chamada corretamente."""
        coordenadas_csv = CoordenadasCSV("caminho_ficticio.csv")
        coordenadas_csv.carregar_csv()
        
        mock_file.assert_called_once_with("caminho_ficticio.csv", mode='r', encoding='utf-8')

if __name__ == "__main__":
    unittest.main()
