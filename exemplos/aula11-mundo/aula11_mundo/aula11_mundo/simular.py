"""Roda o mundo inteiro sem ROS 2, e desenha o resultado.

Serve para tres coisas: ver o mundo antes de subir qualquer no; conferir a
logica do piloto sem esperar o colcon; e -- se o seu ambiente estiver quebrado
no dia -- ainda assim produzir a figura da deriva, que e' o que a aula discute.

    python3 simular.py                          # da pasta do exemplo
    python3 simular.py --deriva 0 --segundos 60
"""
import argparse
import math

import numpy as np

from .mapa import Mundo, desenhar
from .nucleo import Piloto, aplicar_deriva, passo_diferencial


def livre(mundo, x, y, raio):
    return not any(mundo.ocupado(x + raio * math.cos(a), y + raio * math.sin(a))
                   for a in np.linspace(0, 2 * math.pi, 8, endpoint=False))


def simular(segundos=90.0, deriva_pct=3.0, dt=0.05, alcance=6.0, feixes=360,
            pose0=(2.0, 4.0, 0.0), raio=0.20, quieto=False):
    mundo = Mundo()
    angulos = np.linspace(-math.pi, math.pi, feixes, endpoint=False)
    piloto = Piloto()

    verdadeira = tuple(pose0)
    odom = tuple(pose0)
    rastro_v, rastro_o, derivas = [verdadeira], [odom], []

    passos_por_scan = max(1, int(round((1 / 5.0) / dt)))    # laser a 5 Hz
    v = w = 0.0
    leituras = mundo.medir(*verdadeira, angulos, alcance_max=alcance)

    for n in range(int(segundos / dt)):
        if n % passos_por_scan == 0:
            leituras = mundo.medir(*verdadeira, angulos, alcance_max=alcance)
            v, w, evento = piloto.decidir(angulos, leituras, r_max=alcance)
            if evento and not quieto:
                print(f'  t={n * dt:6.2f}s  {evento}')

        nova = passo_diferencial(verdadeira, v, w, dt)
        verdadeira = nova if livre(mundo, nova[0], nova[1], raio) \
            else (verdadeira[0], verdadeira[1], nova[2])
        odom = aplicar_deriva(odom, v, w, dt, deriva_pct)

        rastro_v.append(verdadeira)
        rastro_o.append(odom)
        derivas.append(math.hypot(verdadeira[0] - odom[0], verdadeira[1] - odom[1]))

    return mundo, angulos, rastro_v, rastro_o, derivas, leituras


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--segundos', type=float, default=90.0)
    ap.add_argument('--deriva', type=float, default=3.0, help='erro de odometria em %%')
    ap.add_argument('--saida', default='simulacao.png')
    ap.add_argument('--quieto', action='store_true')
    a = ap.parse_args()

    mundo, angulos, rv, ro, derivas, leituras = simular(
        segundos=a.segundos, deriva_pct=a.deriva, quieto=a.quieto)

    caminho = sum(math.hypot(b[0] - c[0], b[1] - c[1]) for b, c in zip(rv, rv[1:]))
    print()
    print(f'percorrido    : {caminho:.1f} m')
    print(f'colisoes      : {"nenhuma" if min(_folga(mundo, rv)) > 0 else "houve contato"}')
    print(f'deriva final  : {derivas[-1]:.2f} m  ({100 * derivas[-1] / max(caminho, 1e-9):.1f}% do caminho)')
    print(f'deriva maxima : {max(derivas):.2f} m')
    print(f'png           : {desenhar(mundo, rv[-1], leituras, angulos, a.saida, rastro=rv, rastro_odom=ro)}')


def _folga(mundo, rastro):
    return [0 if mundo.ocupado(x, y) else 1 for x, y, _ in rastro]


if __name__ == '__main__':
    main()
