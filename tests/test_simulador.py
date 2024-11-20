"""Simulador testes"""
import unittest
from unittest.mock import MagicMock
from src.vento import Vento
from src.drone import Drone
from src.simulador import simular, simular_tuple

class TestSimulacaoVoo(unittest.TestCase):
    """Classe teste simulador"""
    def setUp(self):
        """Teste simulador"""
        # Criaremos mocks para as dependências
        self.rota = ['cep1', 'cep2']
        self.dia_mock = MagicMock()
        self.dia_mock.obter_dia.return_value = 2
        self.dia_mock.obter_horario.return_value = 12*3600
        self.dia_mock.obter_tempo_restante.return_value = 3600  # Exemplo: tempo restante de 1 hora
        self.dia_mock.obter_horario_formatado.return_value = '12:00'
        self.dia_mock.obter_tempo_total.return_value = 0  # Inicializa com tempo total zero
        self.dia_mock.passar_tempo.return_value = None
        self.dia_mock.avancar_dia.return_value = None
        self.vento = Vento()
        self.drone = Drone()

        # Mock para a classe principal que chama os métodos
        self.ceps = {
            'cep1': {'cep': 1, 'latitude': 10.0, 'longitude': 20.0},  
            'cep2': {'cep': 2, 'latitude': 30.0, 'longitude': 40.0}, 
        }

    def test_simular(self):
        """test_simular"""
        # Definindo os parâmetros para o teste
        rota = ['cep1', 'cep2']
        dia = self.dia_mock
        voo_velocidade = [50, 60]

        # Chamando a função simular diretamente
        velocidades, horarios, dias, pousos, _ = simular(self, rota, dia, voo_velocidade)

        # Verificando se o retorno é conforme o esperado
        self.assertEqual(len(velocidades), 2)
        self.assertEqual(velocidades[0], 0)
        self.assertEqual(pousos[0], False)
        self.assertEqual(horarios[0], '12:00')
        self.assertEqual(dias[0], 2)  # Dia retornado pela mock do objeto dia

    def test_simular_tuple(self):
        """test_simular_tuple"""
        # Testando a função 'simular_tuple'
        rota = [('cep1', None), ('cep2', None)]
        dia = self.dia_mock
        voo_velocidade = [50, 60]

        # Chamando a função simular_tuple diretamente
        velocidades, _, _, pousos, tempos = simular_tuple(self, rota, dia, voo_velocidade)

        # Verificando o retorno
        self.assertEqual(len(velocidades), 2)
        self.assertEqual(tempos[0], 0)  # Espera-se tempo total zero inicialmente
        self.assertEqual(pousos[0], False)

if __name__ == '__main__':
    unittest.main()
