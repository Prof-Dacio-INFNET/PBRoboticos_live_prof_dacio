"""Tres detectores para o MESMO video, para poder comparar.

Nenhum deles e o ponto da aula. O ponto e que so da para dizer qual e melhor
porque os tres rodam sobre o mesmo video e sao medidos pela mesma regua.
"""
import cv2
import numpy as np

# Vermelho ocupa as DUAS pontas do circulo de matiz.
FAIXAS = (((0, 120, 70), (10, 255, 255)),
          ((170, 120, 70), (180, 255, 255)))


def _mascara(img, s_min=120, v_min=70):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    m = None
    for (h0, _, _), (h1, _, _) in FAIXAS:
        parcial = cv2.inRange(hsv,
                              np.array([h0, s_min, v_min], np.uint8),
                              np.array([h1, 255, 255], np.uint8))
        m = parcial if m is None else cv2.bitwise_or(m, parcial)
    return cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))


AREA_ESPERADA = 3600.0        # o alvo tem raio 34 px -> pi*34^2

def _maior_caixa(mascara, area_min):
    """Pega a MAIOR mancha acima de um piso. E a heuristica da Aula 3."""
    cnts, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    melhor, melhor_area = None, 0.0
    for c in cnts:
        a = cv2.contourArea(c)
        if a >= area_min and a > melhor_area:
            melhor, melhor_area = c, a
    return None if melhor is None else cv2.boundingRect(melhor)


def _caixa_por_area(mascara, esperada=AREA_ESPERADA, tolerancia=0.55):
    """Pega a mancha com area mais PROXIMA da esperada, dentro da tolerancia.

    A mudanca em relacao a _maior_caixa e de uma linha e de conceito: sai
    "o maior" e entra "o que tem o tamanho certo". Custa conhecer o tamanho
    do alvo -- e voce conhece, porque e o SEU projeto.
    """
    cnts, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    melhor, melhor_erro = None, 1e9
    for c in cnts:
        a = cv2.contourArea(c)
        erro = abs(a - esperada) / esperada
        if erro <= tolerancia and erro < melhor_erro:
            melhor, melhor_erro = c, erro
    return None if melhor is None else cv2.boundingRect(melhor)


def hsv_ingenuo(img):
    """Maior mancha vermelha. E o detector da Aula 3, sem nenhuma defesa."""
    return _maior_caixa(_mascara(img), area_min=200)


def hsv_com_area(img):
    """Escolhe pela area ESPERADA em vez de pela maior.

    Uma ideia a mais. Repare, na medicao, exatamente o quanto ela compra --
    e o que ela NAO compra.
    """
    return _caixa_por_area(_mascara(img))


def hsv_adaptativo(img):
    """Baixa o limiar de brilho quando a cena escurece.

    Nao e sofisticado: e o minimo que um detector precisa fazer para nao
    desistir quando a luz muda. A medicao mostra se vale a complexidade.
    """
    v_medio = float(cv2.cvtColor(img, cv2.COLOR_BGR2HSV)[:, :, 2].mean())
    v_min = max(20, int(0.55 * v_medio))
    return _caixa_por_area(_mascara(img, s_min=90, v_min=v_min))


DETECTORES = {
    'hsv_ingenuo': hsv_ingenuo,
    'hsv_com_area': hsv_com_area,
    'hsv_adaptativo': hsv_adaptativo,
}
