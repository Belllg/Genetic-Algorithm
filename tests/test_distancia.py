"""Teste das distancias"""
import unittest
from src.distancia import calcular_distancia, calcular_distancia_total, calcular_angulo

class TestDistancia(unittest.TestCase):
    """Testando a funcao distancia"""

    def test_same_location(self) -> None:
        """Testa a distância entre dois pontos iguais (deve ser 0 km)"""
        cep1 = {'cep': 1, 'latitude': 0.0, 'longitude': 0.0}
        cep2 = {'cep': 2, 'latitude': 0.0, 'longitude': 0.0}
        self.assertEqual(calcular_distancia(cep1, cep2), 0.0)

    def test_known_distance(self) -> None:
        """Testa a distância conhecida entre dois pontos"""
        # Distância entre São Paulo (BR) e Rio de Janeiro (BR)
        cep1 = {'cep': 1, 'latitude': -23.550520, 'longitude': -46.633308}  # São Paulo
        cep2 = {'cep': 2, 'latitude': -22.906847, 'longitude': -43.172896}  # Rio de Janeiro
        # Distância aproximada entre São Paulo e Rio de Janeiro: 360.0 km
        resultado = calcular_distancia(cep1, cep2)
        # Permite uma variação de 1 km
        self.assertAlmostEqual(resultado, 360.0, delta=5.0)

    def test_edge_case(self) -> None:
        """Testa casos limites (distâncias muito pequenas)"""
        cep1 = {'cep': 1, 'latitude': 0.0, 'longitude': 0.0}
        cep2 = {'cep': 2, 'latitude': 0.0001, 'longitude': 0.0001}  # Distância muito pequena
        resultado = calcular_distancia(cep1, cep2)
        # Espera-se uma distância muito pequena (em torno de 0.01 km)
        self.assertAlmostEqual(resultado, 0.01, delta=0.1)

    def test_distance_poles(self) -> None:
        """Testa a distância entre o Polo Norte e o Polo Sul"""
        cep1 = {'cep': 1, 'latitude': 90.0, 'longitude': 0.0}  # Polo Norte
        cep2 = {'cep': 2, 'latitude': -90.0, 'longitude': 0.0}  # Polo Sul
        # A distância entre o Polo Norte e o Polo Sul é aproximadamente 20000 km
        resultado = calcular_distancia(cep1, cep2)
        self.assertAlmostEqual(resultado, 20000.0, delta=100.0)

class TestDistanciaTotal(unittest.TestCase):
    """Teste da distancia Total de uma rota"""
    def setUp(self):
        """Configura o ambiente para os testes"""
        # Definindo alguns CEPs com coordenadas (latitude, longitude)
        self.ceps = {
            'cep1': {'cep': 1, 'latitude': 10.0, 'longitude': 20.0},  # latitude 10°, longitude 20°
            'cep2': {'cep': 2, 'latitude': 12.0, 'longitude': 22.0},  # latitude 12°, longitude 22°
            'cep3': {'cep': 3, 'latitude': 14.0, 'longitude': 24.0},  # latitude 14°, longitude 24°
            'cep4': {'cep': 4, 'latitude': 16.0, 'longitude': 26.0}   # latitude 16°, longitude 26°
        }

    def test_calcular_distancia_total_com_2_ceps(self):
        """Teste de caso com 2 pontos na rota"""
        rota = [('cep1', None), ('cep2', None)]
        resultado = calcular_distancia_total(self.ceps, rota)
        cep1_numero, cep2_numero = self.ceps['cep1'], self.ceps['cep2']
        distancia_esperada = calcular_distancia(cep1_numero, cep2_numero)
        self.assertAlmostEqual(resultado, distancia_esperada, places=2)

    def test_calcular_distancia_total_com_3_ceps(self):
        """Teste de caso com 3 pontos na rota"""
        rota = [('cep1', None), ('cep2', None), ('cep3', None)]
        resultado = calcular_distancia_total(self.ceps, rota)
        cep1_numero = self.ceps['cep1']
        cep2_numero = self.ceps['cep2']
        cep3_numero = self.ceps['cep3']
        distancia_esperada = (
            calcular_distancia(cep1_numero, cep2_numero) +
            calcular_distancia(cep2_numero, cep3_numero)
        )
        self.assertAlmostEqual(resultado, distancia_esperada, places=2)

    def test_calcular_distancia_total_com_4_ceps(self):
        """Teste de caso com 4 pontos na rota"""
        rota = [('cep1', None), ('cep2', None), ('cep3', None), ('cep4', None)]
        resultado = calcular_distancia_total(self.ceps, rota)
        cep1_numero = self.ceps['cep1']
        cep2_numero = self.ceps['cep2']
        cep3_numero = self.ceps['cep3']
        cep4_numero = self.ceps['cep4']
        distancia_esperada = (
            calcular_distancia(cep1_numero, cep2_numero) +
            calcular_distancia(cep2_numero, cep3_numero) +
            calcular_distancia(cep3_numero, cep4_numero)
        )
        self.assertAlmostEqual(resultado, distancia_esperada, places=2)

    def test_calcular_distancia_total_com_uma_rota(self):
        """Teste de caso com uma rota de apenas 1 ponto"""
        rota = ['cep1']
        resultado = calcular_distancia_total(self.ceps, rota)
        distancia_esperada = 0
        self.assertEqual(resultado, distancia_esperada)

    def test_calcular_distancia_total_com_rota_vazia(self):
        """Teste de caso com rota vazia"""
        rota = []
        resultado = calcular_distancia_total(self.ceps, rota)
        distancia_esperada = 0
        self.assertEqual(resultado, distancia_esperada)

class TestCalcularAngulo(unittest.TestCase):
    """Testes de Angulo"""
    def setUp(self):
        """Configuração inicial para os testes."""
        # Inicializa os dados de CEPs
        self.ceps = {
            'cep1': {'latitude': 40.748817, 'longitude': -73.985428},  # Nova York
            'cep2': {'latitude': 34.052235, 'longitude': -118.243683},  # Los Angeles
            'cep3': {'latitude': 51.5074, 'longitude': -0.1278},  # Londres
            'cep4': {'latitude': 48.8566, 'longitude': 2.3522},  # Paris
        }

    def test_calcular_angulo_entre_dois_pontos(self):
        """Teste de cálculo de ângulo entre dois pontos (NY e LA)"""
        cep1 = self.ceps['cep1']
        cep2 = self.ceps['cep2']
        resultado = calcular_angulo(cep1, cep2)
        angulo_esperado =  273.648  # Aproximadamente o ângulo esperado
        self.assertAlmostEqual(resultado, angulo_esperado, places=2)

    def test_calcular_angulo_entre_mesmo_local(self):
        """Teste quando os dois pontos são o mesmo (deve retornar 0)"""
        cep1 = self.ceps['cep1']
        cep2 = self.ceps['cep1']
        resultado = calcular_angulo(cep1, cep2)
        self.assertEqual(resultado, 0)

    def test_calcular_angulo_entre_norte_sul(self):
        """Teste para pontos no norte e no sul (180 graus)"""
        cep1 = {'latitude': 0, 'longitude': 0}  # Equador
        cep2 = {'latitude': 10, 'longitude': 0}  # Norte
        resultado = calcular_angulo(cep1, cep2)
        angulo_esperado = 0  # O ângulo de norte
        self.assertEqual(resultado, angulo_esperado)

    def test_calcular_angulo_entre_180_graus(self):
        """Teste para verificar o ângulo de 180 graus entre dois pontos diretamente opostos."""
        # Criando pontos opostos ao longo do meridiano
        cep1 = {'latitude': 0, 'longitude': 0}  # Ponto de referência
        cep2 = {'latitude': 0, 'longitude': 180}  # Ponto oposto ao redor do globo 

        resultado = calcular_angulo(cep1, cep2)
        angulo_esperado = 180  # O ângulo de 180° entre dois pontos opostos ao longo do globo
        
        self.assertEqual(resultado, angulo_esperado)

    def test_calcular_angulo_entre_pontos_distantes(self):
        """Teste entre Londres e Paris"""
        cep1 = self.ceps['cep3']
        cep2 = self.ceps['cep4']
        resultado = calcular_angulo(cep1, cep2)
        angulo_esperado = 148.11561  # Aproximadamente
        self.assertAlmostEqual(resultado, angulo_esperado, places=2)

    def test_calcular_angulo_entre_oeste_leste(self):
        """Teste entre NY e Londres (aproximadamente 74 graus)"""
        cep1 = self.ceps['cep1']
        cep2 = self.ceps['cep3']
        resultado = calcular_angulo(cep1, cep2)
        angulo_esperado = 51.241368  # Aproximadamente
        self.assertAlmostEqual(resultado, angulo_esperado, places=2)

if __name__ == '__main__':
    unittest.main()
