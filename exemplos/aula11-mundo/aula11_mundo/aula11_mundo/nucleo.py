"""A logica do robo, sem ROS 2 nenhum.

Mesma ideia do contrato do detector da Aula 10: o miolo nao precisa saber em que
sistema esta rodando. Aqui isso paga duas vezes -- o `simular.py` roda esta
logica sem instalar nada, e os nos ROS 2 rodam a MESMA logica, entao o que voce
depura offline e' o que vai para o robo.
"""
import math

import numpy as np


def passo_diferencial(pose, v, w, dt):
    """Integra um robo de tracao diferencial por dt segundos."""
    x, y, th = pose
    return (x + v * math.cos(th) * dt,
            y + v * math.sin(th) * dt,
            th + w * dt)


def min_setor(angulos, leituras, a0, a1, r_min=0.05, r_max=math.inf):
    """Menor leitura valida entre dois angulos (radianos, no referencial do robo)."""
    ang = np.asarray(angulos)
    lei = np.asarray(leituras, dtype=float)
    dentro = (ang >= a0) & (ang <= a1) & (lei > r_min) & (lei < r_max) & np.isfinite(lei)
    return float(lei[dentro].min()) if dentro.any() else math.inf


class Piloto:
    """Reativo: anda reto, gira quando fecha na frente. Sem mapa, sem destino.

    O que ele NAO tem e' a lista do que o Nav2 acrescenta: nao sabe onde esta,
    nao sabe para onde vai, nao planeja rota e nao se recupera de falha.
    """

    def __init__(self, velocidade=0.35, giro=0.9, parada_m=0.75, cone_graus=35.0):
        self.velocidade = velocidade
        self.giro = giro
        self.parada_m = parada_m
        self.cone = math.radians(cone_graus)
        self.girando = 0.0          # 0 = reto; +1 = esquerda; -1 = direita

    def decidir(self, angulos, leituras, r_max=math.inf):
        """Devolve (v, w, evento). `evento` e' None ou um texto para log."""
        frente = min_setor(angulos, leituras, -self.cone, self.cone, r_max=r_max)

        if self.girando:
            # Histerese: so' volta a andar com folga. Sem isso, o robo treme na
            # fronteira da decisao e nunca sai do lugar.
            if frente > self.parada_m * 1.6:
                self.girando = 0.0
                return self.velocidade, 0.0, f'frente livre ({frente:.2f} m): seguindo'
            return 0.0, self.girando * self.giro, None

        if frente < self.parada_m:
            lado = math.radians(60)
            esq = min_setor(angulos, leituras, self.cone, self.cone + lado, r_max=r_max)
            dir_ = min_setor(angulos, leituras, -self.cone - lado, -self.cone, r_max=r_max)
            self.girando = 1.0 if esq > dir_ else -1.0
            onde = 'a esquerda' if self.girando > 0 else 'a direita'
            return 0.0, self.girando * self.giro, f'obstaculo a {frente:.2f} m: girando para {onde}'

        return self.velocidade, 0.0, None


def aplicar_deriva(pose_odom, v, w, dt, deriva_pct):
    """Integra a odometria com erro sistematico de escala.

    E' o erro de quem mediu o raio da roda com regua: pequeno, constante, e que
    NAO se cancela -- ele se acumula. Por isso a odometria sozinha nunca fecha
    um laco, e por isso existe o SLAM.
    """
    k = 1.0 + deriva_pct / 100.0
    return passo_diferencial(pose_odom, v * k, w * k, dt)
