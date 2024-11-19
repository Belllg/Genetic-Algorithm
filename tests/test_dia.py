"""Testes Unitarios do dia"""
import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from dia import ContadorDeTempo

class TestContadorDeTempo(unittest.TestCase):
    """Classe de testes"""
    def setUp(self):
        """Configura o ambiente de teste. Será executado antes de cada teste."""
        self.contador = ContadorDeTempo(horas_por_dia=24, dias=5)

    def test_inicializacao(self):
        """Testa a inicialização da classe ContadorDeTempo"""
        self.assertEqual(self.contador.horas_por_dia, 24)
        self.assertEqual(self.contador.dias, 5)
        self.assertEqual(self.contador.segundos_por_dia, 86400)  # 24 horas * 3600 segundos
        self.assertEqual(self.contador.total_segundos, 0)
        self.assertEqual(self.contador.dia_atual, 1)
        self.assertEqual(self.contador.hora_atual, 0)

    def test_obter_horario_formatado(self):
        """Testa o método obter_horario_formatado"""
        # Inicialmente, a hora deve ser 06:00 (porque a hora começa às 0 e soma-se 6)
        self.assertEqual(self.contador.obter_horario_formatado(), "06:00")

        # Passa 3600 segundos (1 hora) e verifica o horário formatado
        self.contador.passar_tempo(3600)
        self.assertEqual(self.contador.obter_horario_formatado(), "07:00")

        # Passa 60 minutos (3600 segundos) para verificar se o horário muda corretamente
        self.contador.passar_tempo(3600)
        self.assertEqual(self.contador.obter_horario_formatado(), "08:00")

    def test_obter_dia(self):
        """Testa o método obter_dia"""
        self.assertEqual(self.contador.obter_dia(), 1)

        # Passa 86400 segundos (1 dia completo)
        self.contador.passar_tempo(86400)
        self.assertEqual(self.contador.obter_dia(), 2)

        # Passa mais 86400 segundos (outro dia completo)
        self.contador.passar_tempo(86400)
        self.assertEqual(self.contador.obter_dia(), 3)

    def test_obter_tempo_restante(self):
        """Testa o método obter_tempo_restante"""
        # Antes de passar qualquer tempo,
        # o tempo restante deve ser igual a 86400 segundos (24 horas)
        self.assertEqual(self.contador.obter_tempo_restante(), 86400)

        # Passa 3600 segundos (1 hora)
        self.contador.passar_tempo(3600)
        self.assertEqual(self.contador.obter_tempo_restante(), 82800)  # 86400 - 3600

        # Passa mais 5000 segundos
        self.contador.passar_tempo(5000)
        self.assertEqual(self.contador.obter_tempo_restante(), 77800)

    def test_obter_tempo_total(self):
        """Testa o método obter_tempo_total"""
        # Inicialmente, o tempo total deve ser 0
        self.assertEqual(self.contador.obter_tempo_total(), 0)

        # Passa 3600 segundos (1 hora)
        self.contador.passar_tempo(3600)
        self.assertEqual(self.contador.obter_tempo_total(), 3600)

        # Passa mais 7200 segundos (2 horas)
        self.contador.passar_tempo(7200)
        self.assertEqual(self.contador.obter_tempo_total(), 10800)

    def test_avancar_dia(self):
        """Testa o método avancar_dia"""
        # Inicialmente, o dia atual é 1
        self.assertEqual(self.contador.dia_atual, 1)

        # Passa 86400 segundos (1 dia)
        self.contador.passar_tempo(86400)
        self.assertEqual(self.contador.dia_atual, 2)

        # Passa mais 86400 segundos (outro dia)
        self.contador.passar_tempo(86400)
        self.assertEqual(self.contador.dia_atual, 3)

        # Passa mais 86400 segundos, o dia deve ser 4
        self.contador.passar_tempo(86400)
        self.assertEqual(self.contador.dia_atual, 4)

        # Passa mais 86400 segundos, o dia deve ser 5 (último dia)
        self.contador.passar_tempo(86400)
        self.assertEqual(self.contador.dia_atual, 5)


    def test_passar_tempo_ao_exceder_dia(self):
        """Testa o comportamento do método passar_tempo quando ultrapassa um dia"""
        # Inicialmente, o horário é 06:00
        self.assertEqual(self.contador.obter_horario_formatado(), "06:00")

        # Passa 86400 segundos (um dia completo)
        self.contador.passar_tempo(86400)
        self.assertEqual(self.contador.obter_horario_formatado(), "06:00")  # Hora reiniciada

        # O dia deve ter avançado para 2
        self.assertEqual(self.contador.obter_dia(), 2)

if __name__ == '__main__':
    unittest.main()
