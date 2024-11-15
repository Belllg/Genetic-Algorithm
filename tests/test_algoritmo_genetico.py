import unittest
from unittest.mock import patch
from src.genetico import AlgoritmoGenetico

class TestAlgoritmoGenetico(unittest.TestCase):

    def setUp(self):
        """Configura o ambiente antes de cada teste."""
        self.ceps = [(1, 0, 0), (2, 1, 1), (3, 2, 2), (4, 3, 3), (5, 4, 4)]
        self.tamanho_populacao = 10
        self.geracoes = 5
        self.taxa_mutacao = 0.1
        self.taxa_genes_antigos=0.8
        self.algoritmo = AlgoritmoGenetico(self.ceps, self.tamanho_populacao, self.geracoes, self.taxa_mutacao, self.taxa_genes_antigos)

    def test_criar_populacao_inicial(self):
        """Testa se a população inicial tem o tamanho correto e se as rotas são únicas."""
        populacao_inicial = self.algoritmo.criar_populacao_inicial()
        self.assertEqual(len(populacao_inicial), self.tamanho_populacao)
        
        # Verifica se todas as rotas são diferentes (usando tuplas para comparação)
        rotas_unicas = len(populacao_inicial) == len(set(tuple(rota) for rota in populacao_inicial))
        self.assertTrue(rotas_unicas)


    @patch('src.distancia.calcular_distancia_total')
    def test_fitness(self, mock_calcular_distancia):
        """Testa se o cálculo de fitness está funcionando corretamente (ordenando por distância)."""
        # Mock da função calcular_distancia_total
        mock_calcular_distancia.return_value = 0.0
        self.algoritmo.populacao = [[0, 1, 2], [2, 1, 0]]
        populacao_ordenada = self.algoritmo.fitness()
        
        # Como estamos mockando a distância para ser 0.0, a população não deve ser alterada
        self.assertEqual(populacao_ordenada, [[0, 1, 2], [2, 1, 0]])

    def test_crossover(self):
        """Testa se a função de crossover está gerando filhos corretamente."""
        pai1 = [0, 1, 2, 3, 4]
        pai2 = [4, 3, 2, 1, 0]
        filho = self.algoritmo.crossover(pai1, pai2)
        
        # Verifica se o filho contém elementos dos pais
        self.assertTrue(all(cep in pai1 + pai2 for cep in filho))
        self.assertEqual(len(filho), len(pai1))

    def test_mutacao(self):
        """Testa se a função de mutação está alterando a rota de forma correta."""
        rota = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        rota_original = rota[:]
        self.algoritmo.taxa_mutacao = 5.0 
        self.algoritmo.mutacao(rota)
        
        # Verifica se a rota foi alterada, mas mantém o mesmo tamanho
        self.assertNotEqual(rota, rota_original)
        self.assertEqual(len(rota), len(rota_original))

    @patch('src.distancia.calcular_distancia_total')
    def test_evoluir_populacao(self, mock_calcular_distancia):
        """Testa se o algoritmo está evoluindo a população corretamente e retornando a melhor rota."""
        
        # Simula distâncias variadas com base na rota
        def mock_calcular_distancia_func(rota, ceps):
            return sum(abs(ceps[i][0] - ceps[rota[i]][0]) + abs(ceps[i][1] - ceps[rota[i]][1]) for i in range(len(rota)))
        
        mock_calcular_distancia.side_effect = mock_calcular_distancia_func
        
        melhor_rota, melhor_distancia = self.algoritmo.evoluir_populacao()
        
        # Verifica se a melhor rota e distância foram retornadas
        self.assertIsNotNone(melhor_rota)
        self.assertIsInstance(melhor_distancia, float)
        self.assertGreater(melhor_distancia, 0.0)  # Verifica se a distância não é zero, o que indicaria erro na evolução

if __name__ == '__main__':
    unittest.main()
