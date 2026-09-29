#!/usr/bin/env python3
"""Confere o mundo antes de voce confiar nele. Nao precisa de ROS 2.

    python3 testar.py

Um simulador errado e' pior que nenhum: ele produz numero, e numero convence.
Estes quatro testes existem para que a deriva que a aula discute seja a deriva
do modelo, e nao um defeito do mapa ou da integracao.
"""
import math
import sys

import numpy as np

sys.path.insert(0, 'aula11_mundo')
from aula11_mundo.mapa import Mundo                                   # noqa: E402
from aula11_mundo.simular import simular                              # noqa: E402

falhas = []


def conferir(nome, ok, detalhe=''):
    print(f'  {"ok  " if ok else "FALHA"}  {nome}{"  — " + detalhe if detalhe else ""}')
    if not ok:
        falhas.append(nome)


print('1. o laser mede a parede certa')
m = Mundo()
for nome, ang, esperado in (('oeste', math.pi, 1.80),
                            ('norte', math.pi / 2, 3.80),
                            ('sul', -math.pi / 2, 3.80)):
    d = float(m.medir(2.0, 4.0, 0.0, [ang])[0])
    conferir(f'parede {nome} a {esperado:.2f} m', abs(d - esperado) <= 0.03,
             f'medido {d:.2f} m')

print('2. o feixe que passa pela porta nao inventa parede')
d = float(m.medir(2.0, 4.0, 0.0, [0.0], alcance_max=6.0)[0])
conferir('leste, pela porta, fora de alcance', not np.isfinite(d), f'medido {d}')

print('3. sem deriva, a odometria e a verdade coincidem')
_, _, rv, ro, der, _ = simular(segundos=40, deriva_pct=0.0, quieto=True)
conferir('deriva identicamente zero', max(der) == 0.0, f'max {max(der):.4f} m')

print('4. com deriva, o erro cresce com o caminho e o robo nunca entra na parede')
mundo, _, rv, ro, der, _ = simular(segundos=90, deriva_pct=3.0, quieto=True)
caminho = sum(math.hypot(b[0] - c[0], b[1] - c[1]) for b, c in zip(rv, rv[1:]))
conferir('deriva final > 10 cm', der[-1] > 0.10, f'{der[-1]:.2f} m em {caminho:.1f} m')
conferir('deriva da 2a metade > da 1a', max(der[len(der) // 2:]) > max(der[:len(der) // 2]),
         f'{max(der[:len(der)//2]):.2f} -> {max(der[len(der)//2:]):.2f} m')
conferir('nenhuma pose verdadeira dentro de parede',
         not any(mundo.ocupado(x, y) for x, y, _ in rv))

print()
if falhas:
    print(f'{len(falhas)} FALHA(S): ' + '; '.join(falhas))
    raise SystemExit(1)
print('todos os testes passaram.')
