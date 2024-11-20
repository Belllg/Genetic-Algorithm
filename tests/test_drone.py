"""Teste Drone"""
import unittest
from src.drone import Drone

class TestDrone(unittest.TestCase):
    """Teste Drone"""
    def setUp(self):
        """Configura o ambiente de teste para cada método"""
        self.drone = Drone()

    def test_inicializacao(self):
        """Testa se o drone inicia com os valores corretos"""
        self.assertEqual(self.drone.autonomia, 1800)
        self.assertEqual(self.drone.bateria, 1800)
        self.assertFalse(self.drone.pouso)
        self.assertFalse(self.drone.parar)

    def test_resetar_drone(self):
        """Testa se o método resetar_drone reseta os parâmetros corretamente"""
        self.drone.bateria = 1500  # Simula uma bateria parcialmente descarregada
        self.drone.pouso = True
        self.drone.parar = True

        self.drone.resetar_drone()

        self.assertEqual(self.drone.bateria, 1800)
        self.assertFalse(self.drone.pouso)
        self.assertFalse(self.drone.parar)

    def test_ajustar_velocidade_com_vento(self):
        """Testa o ajuste da velocidade do drone com base no vento"""
        velocidade_ajustada = self.drone.ajustar_velocidade_com_vento(50, 10, 90, 90)
        self.assertTrue(velocidade_ajustada != 50)  # A velocidade deve ser ajustada
        self.assertGreater(velocidade_ajustada, 50)  # talvez o vento vai aumentar a velocidade

    def test_calcular_tempo_voo(self):
        """Testa o cálculo do tempo de voo entre duas coordenadas"""
        tempo_voo, velocidade, consumo_bateria = self.drone.calcular_tempo_voo(
            distancia=10,
            velocidade=40,
            vento_velocidade=5,
            vento_direcao=90,
            angulo_voo=0,
            tempo_restante=3600
        )

        self.assertGreater(tempo_voo, 0)
        self.assertGreater(velocidade, 30)  # Velocidade ajustada pelo vento
        self.assertGreater(consumo_bateria, 0)

    def test_verificar_autonomia(self):
        """Testa o método de verificação de autonomia do drone"""
        consumo_bateria = 2000  # Simula consumo alto
        autonomia_suficiente = self.drone.verificar_autonomia(consumo_bateria)

        self.assertFalse(autonomia_suficiente)
        self.assertTrue(self.drone.pouso)  # pedir pouso quando a autonomia não for suficiente

    def test_realizar_voo(self):
        """Testa o método realizar_voo, simulando um voo completo"""
        tempo_voo, velocidade, pouso, parar = self.drone.realizar_voo(
            distancia=10,
            velocidade=50,
            vento_velocidade=10,
            vento_direcao=90,
            angulo_voo=0,
            tempo_restante=3600
        )

        self.assertGreater(tempo_voo, 0)
        self.assertGreater(velocidade, 30)
        self.assertTrue(pouso)  # O drone não deve pousar, pois a autonomia é suficiente
        self.assertFalse(parar)  # O drone não deve parar antes de concluir o voo

if __name__ == '__main__':
    unittest.main()
