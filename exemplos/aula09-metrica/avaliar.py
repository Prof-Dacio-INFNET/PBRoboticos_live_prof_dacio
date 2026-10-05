#!/usr/bin/env python3
"""Mede um detector sobre o video fixo e imprime a metrica declarada.

    python3 avaliar.py                       # todos os detectores
    python3 avaliar.py hsv_ingenuo           # um so
    python3 avaliar.py --video               # + gera saida_<detector>.avi com OSD
    python3 avaliar.py hsv_ingenuo --video   # um so, com video

O video de saida e OPCIONAL de proposito. Desenhar caixa e escrever texto
custa mais do que a propria deteccao neste exemplo -- se o desenho entrasse
na conta, a metrica de tempo mediria o OSD, nao o detector. Por isso ele fica
atras de um parametro E fora da janela cronometrada.

Essa separacao e uma regra geral de instrumentacao: **o que voce mede nao pode
incluir o custo de observar**. Vale para log, para print de depuracao e para
qualquer visualizacao que voce acrescente ao seu no ROS 2.

A METRICA principal desta disciplina, declarada antes de rodar qualquer coisa:

    taxa de alvo mantido = quadros em que o detector achou o alvo
                           com IoU >= 0.5, dividido pelos quadros
                           em que o alvo REALMENTE estava na cena

Declarar antes importa. Metrica escolhida depois de ver o resultado e a que
faz o seu detector parecer bom, e todo mundo sabe disso.
"""
import argparse
import csv
import statistics
import time

import cv2

from detectores import DETECTORES

IOU_MIN = 0.5
TRECHOS = [('normal', 0, 60), ('oclusao', 60, 90),
           ('distrator vermelho', 90, 150), ('luz caindo', 150, 240)]

VERDE, VERMELHO, AMBAR, BRANCO = (70, 220, 70), (48, 48, 235), (20, 170, 250), (245, 245, 245)


def _txt(img, s_, org, esc=0.5, cor=BRANCO, esp=1):
    """Texto com contorno preto, para ficar legivel sobre qualquer fundo.

    So ASCII: a fonte Hershey do OpenCV nao tem acento nem simbolo -- qualquer
    caractere fora do ASCII sai como '?'. E por isso que o OSD escreve
    'oclusao' e nao 'oclusão'.
    """
    cv2.putText(img, s_, org, cv2.FONT_HERSHEY_SIMPLEX, esc, (0, 0, 0), esp + 3, cv2.LINE_AA)
    cv2.putText(img, s_, org, cv2.FONT_HERSHEY_SIMPLEX, esc, cor, esp, cv2.LINE_AA)


def desenhar_osd(img, nome, k, total, trecho, verdade, caixa, escore, veredito, acum):
    """Anota o quadro. Chamada FORA da janela cronometrada, sempre."""
    h, w = img.shape[:2]
    cor_v = {'ACERTO': VERDE, 'PERDA': VERMELHO,
             'FALSO POSITIVO': VERMELHO, 'ausente (ok)': VERDE}[veredito]

    # verdade em ambar, sempre que existir
    if verdade is not None:
        x, y, cw, ch = verdade
        cv2.rectangle(img, (x, y), (x + cw, y + ch), AMBAR, 2)
        _txt(img, 'verdade', (x, max(14, y - 6)), 0.42, AMBAR)

    # deteccao: verde se valeu, vermelho se nao
    if caixa is not None:
        x, y, cw, ch = caixa
        cv2.rectangle(img, (x, y), (x + cw, y + ch), cor_v, 2)
        _txt(img, 'IoU %.2f' % escore, (x, min(h - 6, y + ch + 16)), 0.42, cor_v)

    # faixa superior: quem, onde, e o veredito do quadro
    cv2.rectangle(img, (0, 0), (w, 46), (24, 24, 28), -1)
    _txt(img, '%s' % nome, (10, 19), 0.55)
    _txt(img, 'quadro %3d/%d   %s' % (k, total - 1, trecho), (10, 38), 0.44, (185, 185, 190))
    _txt(img, veredito, (w - 210, 30), 0.68, cor_v, 2)

    # faixa inferior: a metrica ACUMULADA ate aqui
    cv2.rectangle(img, (0, h - 34), (w, h), (24, 24, 28), -1)
    mantido = 100.0 * acum['acerto'] / max(acum['presente'], 1)
    fp = 100.0 * acum['fp'] / max(acum['ausente'], 1)
    _txt(img, 'alvo mantido %5.1f%% (%d/%d)    falso positivo %5.1f%% (%d/%d)'
         % (mantido, acum['acerto'], acum['presente'], fp, acum['fp'], acum['ausente']),
         (10, h - 12), 0.46)


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


def avaliar(nome, fn, rotulos, video='cena.avi', gravar=False):
    aquecer(fn, video)
    cap = cv2.VideoCapture(video)
    if not cap.isOpened():
        raise SystemExit("nao abri %s -- rode 'python3 gerar_video.py' antes" % video)

    por_trecho = {t[0]: {'presente': 0, 'acerto': 0, 'ausente': 0, 'fp': 0} for t in TRECHOS}
    soma_iou, n_acerto, tempos = 0.0, 0, []
    acum = {'presente': 0, 'acerto': 0, 'ausente': 0, 'fp': 0}
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or len(rotulos)
    escritor = None
    if gravar:
        l, a = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        escritor = cv2.VideoWriter('saida_%s.avi' % nome,
                                   cv2.VideoWriter_fourcc(*'MJPG'),
                                   cap.get(cv2.CAP_PROP_FPS) or 20, (l, a))
        if not escritor.isOpened():
            raise SystemExit('nao consegui abrir o VideoWriter de saida')
    k = 0
    while True:
        ok, img = cap.read()
        if not ok:
            break
        # ---------- JANELA CRONOMETRADA: so o detector ----------
        t0 = time.perf_counter()
        caixa = fn(img)
        tempos.append((time.perf_counter() - t0) * 1000.0)
        # ---------- fim da janela. Nada abaixo entra na conta. ----------

        verdade = rotulos.get(k)
        trecho = next(t[0] for t in TRECHOS if t[1] <= k < t[2])
        d = por_trecho[trecho]
        escore = iou(caixa, verdade)
        if verdade is not None:
            d['presente'] += 1
            acum['presente'] += 1
            if escore >= IOU_MIN:
                d['acerto'] += 1
                acum['acerto'] += 1
                n_acerto += 1
                soma_iou += escore
                veredito = 'ACERTO'
            else:
                veredito = 'PERDA'
        else:
            d['ausente'] += 1
            acum['ausente'] += 1
            if caixa is not None:
                d['fp'] += 1
                acum['fp'] += 1
                veredito = 'FALSO POSITIVO'
            else:
                veredito = 'ausente (ok)'

        if escritor is not None:
            desenhar_osd(img, nome, k, total, trecho, verdade, caixa,
                         escore, veredito, acum)
            escritor.write(img)
        k += 1
    cap.release()
    if escritor is not None:
        escritor.release()

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
    if escritor is not None:
        print("  video anotado        : saida_%s.avi" % nome)
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
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('detectores', nargs='*', default=[],
                    help='quais medir (padrao: todos)')
    ap.add_argument('--video', action='store_true',
                    help='gera saida_<detector>.avi com as caixas e o OSD. '
                         'NAO entra na medicao de tempo')
    ap.add_argument('--entrada', default='cena.avi', help='video de entrada')
    args = ap.parse_args()

    rotulos = carregar_rotulos()
    alvos = args.detectores or list(DETECTORES)
    placar = {}
    for nome in alvos:
        if nome not in DETECTORES:
            raise SystemExit("detector desconhecido: %s (tenho: %s)"
                             % (nome, ', '.join(DETECTORES)))
        placar[nome] = avaliar(nome, DETECTORES[nome], rotulos,
                               video=args.entrada, gravar=args.video)
    if len(placar) > 1:
        print("\n=== placar (taxa de alvo mantido) ===")
        for nome, v in sorted(placar.items(), key=lambda x: -x[1]):
            print("  %-18s %5.1f%%" % (nome, v))


if __name__ == '__main__':
    main()
