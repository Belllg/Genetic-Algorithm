from src.distancia import distancia, calcular_distancia_total
import unittest

#FIXME REFAZER 
class TestDistancia(unittest.TestCase):
    """Testando a funcao distancia"""

    def test_same_location(self) -> None:
        """Testa a distância entre dois pontos iguais (deve ser 0 km)"""
        cep1 = {'cep': 1, 'latitude': 0.0, 'longitude': 0.0}
        cep2 = {'cep': 2, 'latitude': 0.0, 'longitude': 0.0}
        self.assertEqual(distancia(cep1, cep2), 0.0)

    def test_known_distance(self) -> None:
        """Testa a distância conhecida entre dois pontos"""
        # Distância entre São Paulo (BR) e Rio de Janeiro (BR)
        cep1 = {'cep': 1, 'latitude': -23.550520, 'longitude': -46.633308}  # São Paulo
        cep2 = {'cep': 2, 'latitude': -22.906847, 'longitude': -43.172896}  # Rio de Janeiro
        # Distância aproximada entre São Paulo e Rio de Janeiro: 360.0 km
        resultado = distancia(cep1, cep2)
        # Permite uma variação de 1 km
        self.assertAlmostEqual(resultado, 360.0, delta=5.0)

    def test_edge_case(self) -> None:
        """Testa casos limites (distâncias muito pequenas)"""
        cep1 = {'cep': 1, 'latitude': 0.0, 'longitude': 0.0}
        cep2 = {'cep': 2, 'latitude': 0.0001, 'longitude': 0.0001}  # Distância muito pequena
        resultado = distancia(cep1, cep2)
        # Espera-se uma distância muito pequena (em torno de 0.01 km)
        self.assertAlmostEqual(resultado, 0.01, delta=0.1)

    def test_distance_poles(self) -> None:
        """Testa a distância entre o Polo Norte e o Polo Sul"""
        cep1 = {'cep': 1, 'latitude': 90.0, 'longitude': 0.0}  # Polo Norte
        cep2 = {'cep': 2, 'latitude': -90.0, 'longitude': 0.0}  # Polo Sul
        # A distância entre o Polo Norte e o Polo Sul é aproximadamente 20000 km
        resultado = distancia(cep1, cep2)
        self.assertAlmostEqual(resultado, 20000.0, delta=100.0)


class TestDistanciaTotal(unittest.TestCase):
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
        rota = ['cep1', 'cep2']
        resultado = calcular_distancia_total(rota, self.ceps)
        # Distância entre cep1 e cep2, e volta de cep2 para cep1
        # (cep1 -> cep2) + (cep2 -> cep1)
        distancia_esperada = 2 * \
            distancia(self.ceps['cep1'], self.ceps['cep2'])
        self.assertAlmostEqual(resultado, distancia_esperada, places=2)

    def test_calcular_distancia_total_com_3_ceps(self):
        """Teste de caso com 3 pontos na rota"""
        rota = ['cep1', 'cep2', 'cep3']
        resultado = calcular_distancia_total(rota, self.ceps)
        # Distâncias: cep1 -> cep2, cep2 -> cep3, e volta de cep3 para cep1
        distancia_esperada = (distancia(self.ceps['cep1'], self.ceps['cep2']) +
                              distancia(self.ceps['cep2'], self.ceps['cep3']) +
                              distancia(self.ceps['cep3'], self.ceps['cep1']))
        self.assertAlmostEqual(resultado, distancia_esperada, places=2)

    def test_calcular_distancia_total_com_4_ceps(self):
        """Teste de caso com 4 pontos na rota"""
        rota = ['cep1', 'cep2', 'cep3', 'cep4']
        resultado = calcular_distancia_total(rota, self.ceps)
        # Distâncias: cep1 -> cep2, cep2 -> cep3, cep3 -> cep4, e volta de cep4 para cep1
        distancia_esperada = (distancia(self.ceps['cep1'], self.ceps['cep2']) +
                              distancia(self.ceps['cep2'], self.ceps['cep3']) +
                              distancia(self.ceps['cep3'], self.ceps['cep4']) +
                              distancia(self.ceps['cep4'], self.ceps['cep1']))
        self.assertAlmostEqual(resultado, distancia_esperada, places=2)

    def test_calcular_distancia_total_com_uma_rota(self):
        """Teste de caso com uma rota de apenas 1 ponto"""
        rota = ['cep1']
        resultado = calcular_distancia_total(rota, self.ceps)
        # Não há movimento, então a distância deve ser zero.
        distancia_esperada = 0
        self.assertEqual(resultado, distancia_esperada)

    def test_calcular_distancia_total_com_rota_vazia(self):
        """Teste de caso com rota vazia"""
        rota = []
        resultado = calcular_distancia_total(rota, self.ceps)
        # Rota vazia, não há distâncias a calcular
        distancia_esperada = 0
        self.assertEqual(resultado, distancia_esperada)

if __name__ == '__main__':
    unittest.main()
