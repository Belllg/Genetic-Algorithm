"""Teste Unitario do Vento"""
import unittest
from src.vento import Vento

class TestVento(unittest.TestCase):
    """Classe para testar o vento"""
    def setUp(self):
        """Cria uma instância da classe Vento antes de cada teste."""
        self.vento = Vento()

    def test_obter_vento_valido(self):
        """Testa a obtenção de vento para um dia e horário válidos."""

        # Testando o dia 1, às 06:00:00
        resultado = self.vento.obter_vento(1, 6 * 3600)  # 06:00:00 em segundos
        self.assertEqual(resultado, (17, 67.5))

        # Testando o dia 3, às 09:00:00
        resultado = self.vento.obter_vento(3, 9 * 3600)  # 09:00:00 em segundos
        self.assertEqual(resultado, (17, 45))

        # Testando o dia 4, às 12:00:00
        resultado = self.vento.obter_vento(4, 12 * 3600)  # 12:00:00 em segundos
        self.assertEqual(resultado, (7, 247.5))

    def test_obter_vento_dia_invalido(self):
        """Testa a obtenção de vento para um dia inválido (maior que 5)."""
        # Testando um dia inválido (ex: dia 7)
        resultado = self.vento.obter_vento(7, 6 * 3600)  # 06:00:00 em segundos
        self.assertEqual(resultado, (0, 90))

    def test_obter_vento_horario_nao_existente(self):
        """Testa o comportamento para um horário que não existe no dia.""" 
        # Testando um horário inexistente para o dia 2 (ex: 04:00:00)
        resultado = self.vento.obter_vento(2, 4 * 3600)  # 04:00:00 em segundos
        self.assertEqual(resultado, (0, 0))


if __name__ == '__main__':
    unittest.main()
