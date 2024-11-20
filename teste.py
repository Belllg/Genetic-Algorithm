import math
def ajustar_velocidade_com_vento(velocidade, vento_velocidade, vento_direcao, angulo_voo):
        """Ajusta a velocidade do drone de acordo com a direção e velocidade do vento"""
        # Aplique o efeito do vento na velocidade
        angulo_vento = math.radians(vento_direcao)
        angulo_voo_rad = math.radians(angulo_voo)

        # Fórmula simplificada para ajuste de velocidade com vento
        efeito_vento = math.cos(angulo_voo_rad - angulo_vento) * vento_velocidade

        velocidade_ajustada = velocidade + efeito_vento

        return velocidade_ajustada

print(ajustar_velocidade_com_vento(50, 10, 90, 90))