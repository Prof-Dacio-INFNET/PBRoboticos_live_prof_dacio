#!/usr/bin/env python3
"""Mede um detector sobre o video fixo e imprime a metrica declarada.

    python3 avaliar.py                       # todos os detectores
    python3 avaliar.py hsv_ingenuo           # um so

A METRICA principal desta disciplina, declarada antes de rodar qualquer coisa:

    taxa de alvo mantido = quadros em que o detector achou o alvo
                           com IoU >= 0.5, dividido pelos quadros
                           em que o alvo REALMENTE estava na cena

Declarar antes importa. Metrica escolhida depois de ver o resultado e a que
faz o seu detector parecer bom, e todo mundo sabe disso.
"""
import csv
import statistics
import sys
import time

import cv2

from detectores import DETECTORES

IOU_MIN = 0.5
TRECHOS = [('normal', 0, 60), ('oclusao', 60, 90),
           ('distrator vermelho', 90, 150), ('luz caindo', 150, 240)]


def iou(a, b):
    if a is None or b is None:
        return 0.0
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    x0, y0 = max(ax, bx), max(ay, by)
    x1, y1 = min(ax + aw, bx + bw), min(ay + ah, by + bh)
    inter = max(0, x1 - x0) * max(0, y1 - y0)
    uniao = aw * ah + bw * bh - inter
    return inter / float(uniao) if uniao > 0 else 0.0


def carregar_rotulos(caminho='rotulos.csv'):
    rot = {}
    with open(caminho) as f:
        for l in csv.DictReader(f):
            k = int(l['quadro'])
            rot[k] = (int(l['x']), int(l['y']), int(l['w']), int(l['h'])) \
                if l['presente'] == '1' else None
    return rot


def aquecer(fn, video='cena.avi', quadros=15):
    """Roda o detector algumas vezes ANTES de cronometrar.

    Sem isto, o primeiro detector medido paga sozinho o custo de aquecer cache
    e alocar buffers, e aparece mais lento do que e. A ordem da medicao
    contamina a medida -- e isso vale para qualquer benchmark, nao so aqui.
    """
    cap = cv2.VideoCapture(video)
    for _ in range(quadros):
        ok, img = cap.read()
        if not ok:
            break
        fn(img)
    cap.release()


def avaliar(nome, fn, rotulos, video='cena.avi'):
    aquecer(fn, video)
    cap = cv2.VideoCapture(video)
    if not cap.isOpened():
        raise SystemExit("nao abri %s -- rode 'python3 gerar_video.py' antes" % video)

    por_trecho = {t[0]: {'presente': 0, 'acerto': 0, 'ausente': 0, 'fp': 0} for t in TRECHOS}
    soma_iou, n_acerto, tempos = 0.0, 0, []
    k = 0
    while True:
        ok, img = cap.read()
        if not ok:
            break
        t0 = time.perf_counter()
        caixa = fn(img)
        tempos.append((time.perf_counter() - t0) * 1000.0)

        verdade = rotulos.get(k)
        trecho = next(t[0] for t in TRECHOS if t[1] <= k < t[2])
        d = por_trecho[trecho]
        if verdade is not None:
            d['presente'] += 1
            s = iou(caixa, verdade)
            if s >= IOU_MIN:
                d['acerto'] += 1
                n_acerto += 1
                soma_iou += s
        else:
            d['ausente'] += 1
            if caixa is not None:
                d['fp'] += 1
        k += 1
    cap.release()

    presente = sum(d['presente'] for d in por_trecho.values())
    ausente = sum(d['ausente'] for d in por_trecho.values())
    acerto = sum(d['acerto'] for d in por_trecho.values())
    fp = sum(d['fp'] for d in por_trecho.values())

    print("\n=== %s ===" % nome)
    print("  taxa de alvo mantido : %5.1f%%   (%d de %d quadros com alvo)"
          % (100.0 * acerto / max(presente, 1), acerto, presente))
    print("  falso positivo       : %5.1f%%   (%d de %d quadros SEM alvo)"
          % (100.0 * fp / max(ausente, 1), fp, ausente))
    print("  IoU medio nos acertos: %5.2f" % (soma_iou / max(n_acerto, 1)))
    # MEDIANA, nao media: um quadro lento isolado (o sistema operacional
    # resolveu fazer outra coisa) desloca a media e nao diz nada sobre o
    # detector. A mediana ignora o susto.
    print("  custo                : %5.2f ms/quadro (mediana; p90 %.2f)"
          % (statistics.median(tempos), sorted(tempos)[int(0.9 * len(tempos))]))
    print("  --- por trecho (a media esconde ONDE falhou) ---")
    for t, _, _ in TRECHOS:
        d = por_trecho[t]
        if d['presente']:
            print("    %-20s %5.1f%% mantido" % (t, 100.0 * d['acerto'] / d['presente']))
        else:
            print("    %-20s alvo ausente; %d falso(s) positivo(s) em %d"
                  % (t, d['fp'], d['ausente']))
    return 100.0 * acerto / max(presente, 1)


def main():
    rotulos = carregar_rotulos()
    alvos = sys.argv[1:] or list(DETECTORES)
    placar = {}
    for nome in alvos:
        if nome not in DETECTORES:
            raise SystemExit("detector desconhecido: %s (tenho: %s)"
                             % (nome, ', '.join(DETECTORES)))
        placar[nome] = avaliar(nome, DETECTORES[nome], rotulos)
    if len(placar) > 1:
        print("\n=== placar (taxa de alvo mantido) ===")
        for nome, v in sorted(placar.items(), key=lambda x: -x[1]):
            print("  %-18s %5.1f%%" % (nome, v))


if __name__ == '__main__':
    main()
