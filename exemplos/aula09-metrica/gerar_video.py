#!/usr/bin/env python3
"""Gera um video FIXO com rotulos conhecidos, para medir detector.

    python3 gerar_video.py            # -> cena.avi + rotulos.csv

Por que gerar em vez de filmar: para medir um detector voce precisa saber a
resposta certa em cada quadro. Rotular video real e caro e chato; gerar um
cenario onde voce DESENHOU o alvo te da rotulo perfeito de graca.

Isso nao substitui dado real -- substitui a falta dele no dia em que voce
precisa validar o seu METODO de medicao. Um medidor que erra no cenario
sintetico vai errar mais no real, e voce descobre agora, nao na entrega.

A cena tem quatro trechos, e cada um quebra o detector de um jeito diferente:
  0- 59  normal, so o alvo e um distrator AZUL
 60- 89  OCLUSAO: o alvo passa atras de uma barra. Rotulo = ausente
 90-149  entra um distrator VERMELHO MAIOR -- "a maior mancha" aponta errado
150-239  a luz CAI ate ~22% -- limiar fixo de brilho para de enxergar o alvo
"""
import csv
import math

import cv2
import numpy as np

L, A, N, FPS = 640, 480, 240, 20
ALVO_R = 34


def cena(k):
    """Devolve (imagem, rotulo). Rotulo = (presente, x, y, w, h)."""
    img = np.full((A, L, 3), 60, np.uint8)
    cv2.rectangle(img, (0, int(A * 0.80)), (L, A), (85, 85, 85), -1)

    # ---- alvo: vermelho, atravessa a cena da esquerda para a direita ----
    t = k / float(N)
    ax = int(60 + t * (L - 120))
    ay = int(A * 0.42 + 60 * math.sin(k / 12.0))
    cv2.circle(img, (ax, ay), ALVO_R, (32, 32, 215), -1)

    # ---- distrator azul: sempre presente, nunca deve ser detectado ----
    cv2.circle(img, (int(L * 0.5 + 180 * math.cos(k / 18.0)), int(A * 0.68)),
               28, (205, 115, 30), -1)

    presente = 1
    # ---- 60-89: oclusao ----
    if 60 <= k < 90:
        cv2.rectangle(img, (int(L * 0.30), 0), (int(L * 0.30) + 150, A), (70, 70, 72), -1)
        if int(L * 0.30) - ALVO_R < ax < int(L * 0.30) + 150 + ALVO_R:
            presente = 0

    # ---- 90-149: distrator VERMELHO MAIOR que o alvo ----
    # De proposito: "a maior mancha vermelha" passa a apontar para o lugar errado.
    if 90 <= k < 150:
        cv2.circle(img, (int(L * 0.20), int(A * 0.28)), 46, (28, 28, 200), -1)

    # ---- 150+: a luz cai ----
    if k >= 150:
        fator = 1.0 - 0.78 * ((k - 150) / float(N - 150))
        img = np.clip(img.astype(np.float32) * fator, 0, 255).astype(np.uint8)

    rot = (presente, ax - ALVO_R, ay - ALVO_R, 2 * ALVO_R, 2 * ALVO_R) if presente \
        else (0, 0, 0, 0, 0)
    return img, rot


def main():
    # MJPG em .avi: funciona em qualquer OpenCV, sem codec externo.
    vw = cv2.VideoWriter('cena.avi', cv2.VideoWriter_fourcc(*'MJPG'), FPS, (L, A))
    if not vw.isOpened():
        raise SystemExit('nao consegui abrir o VideoWriter')
    with open('rotulos.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['quadro', 'presente', 'x', 'y', 'w', 'h'])
        for k in range(N):
            img, rot = cena(k)
            vw.write(img)
            w.writerow([k] + list(rot))
    vw.release()
    print('cena.avi   %d quadros, %dx%d @ %d fps' % (N, L, A, FPS))
    print('rotulos.csv  rotulo por quadro (presente, x, y, w, h)')


if __name__ == '__main__':
    main()
