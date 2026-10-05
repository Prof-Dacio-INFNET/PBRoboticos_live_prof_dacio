"""O mundo: uma grade de ocupacao e um laser que a enxerga.

Nada aqui depende de ROS 2. E' Python e numpy puros, de proposito: assim voce
pode desenhar o seu proprio mundo e ver o resultado sem subir nada.

    python3 simular.py                # da pasta do exemplo: desenha e mede

O mundo tem 12 x 8 metros, duas salas ligadas por uma porta, e obstaculos --
que e' exatamente o "cenario nao trivial" que o TP3 pede (>= 2 comodos,
obstaculos, laco fechado).
"""
import numpy as np

LARGURA_M, ALTURA_M = 12.0, 8.0
RESOLUCAO = 0.05                      # metros por celula


class Mundo:
    """Grade de ocupacao: True = parede, False = livre."""

    def __init__(self, resolucao: float = RESOLUCAO):
        self.res = resolucao
        self.nx = int(LARGURA_M / resolucao)
        self.ny = int(ALTURA_M / resolucao)
        self.grade = np.zeros((self.ny, self.nx), dtype=bool)
        self._construir()

    # ---------------------------------------------------------- construcao
    def _retangulo(self, x0, y0, x1, y1):
        i0, i1 = int(y0 / self.res), int(y1 / self.res)
        j0, j1 = int(x0 / self.res), int(x1 / self.res)
        self.grade[max(i0, 0):i1, max(j0, 0):j1] = True

    def _circulo(self, cx, cy, raio):
        ys, xs = np.mgrid[0:self.ny, 0:self.nx]
        d2 = ((xs + 0.5) * self.res - cx) ** 2 + ((ys + 0.5) * self.res - cy) ** 2
        self.grade |= d2 <= raio ** 2

    def _construir(self):
        e = 0.20                                    # espessura das paredes
        self._retangulo(0, 0, LARGURA_M, e)                       # sul
        self._retangulo(0, ALTURA_M - e, LARGURA_M, ALTURA_M)     # norte
        self._retangulo(0, 0, e, ALTURA_M)                        # oeste
        self._retangulo(LARGURA_M - e, 0, LARGURA_M, ALTURA_M)    # leste

        # parede divisoria com porta entre y=3.4 e y=4.6
        self._retangulo(6.0, 0, 6.0 + e, 3.4)
        self._retangulo(6.0, 4.6, 6.0 + e, ALTURA_M)

        # obstaculos
        self._retangulo(2.3, 1.8, 3.1, 2.6)
        self._retangulo(8.6, 5.2, 9.6, 5.8)
        self._circulo(3.6, 6.0, 0.35)

    # ---------------------------------------------------------- consultas
    def ocupado(self, x, y) -> bool:
        j, i = int(x / self.res), int(y / self.res)
        if not (0 <= i < self.ny and 0 <= j < self.nx):
            return True                              # fora do mundo e' parede
        return bool(self.grade[i, j])

    def medir(self, x, y, theta, angulos, alcance_max=6.0, passo=0.02):
        """Distancia ate a primeira parede em cada angulo. inf se nao achou.

        Marcha amostrada, vetorizada: um feixe e' uma linha de pontos, e a
        leitura e' o primeiro ponto ocupado. Simples e suficiente -- o erro
        maximo e' meio passo, aqui 1 cm.
        """
        d = np.arange(passo, alcance_max + passo, passo)          # (D,)
        ang = theta + np.asarray(angulos, dtype=float)            # (N,)
        xs = x + np.cos(ang)[:, None] * d[None, :]
        ys = y + np.sin(ang)[:, None] * d[None, :]

        j = (xs / self.res).astype(np.int32)
        i = (ys / self.res).astype(np.int32)
        fora = (i < 0) | (i >= self.ny) | (j < 0) | (j >= self.nx)
        np.clip(i, 0, self.ny - 1, out=i)
        np.clip(j, 0, self.nx - 1, out=j)

        bateu = self.grade[i, j] | fora                           # (N,D)
        tem = bateu.any(axis=1)
        primeiro = bateu.argmax(axis=1)                # argmax pega o 1o True
        return np.where(tem, d[primeiro], np.inf)


def desenhar(mundo, pose=None, leituras=None, angulos=None, caminho='mundo.png',
             escala=4, rastro=None, rastro_odom=None):
    """Salva um PNG do mundo. Existe para voce ver sem depender do RViz2."""
    import cv2
    img = np.full((mundo.ny, mundo.nx, 3), 245, np.uint8)
    img[mundo.grade] = (61, 33, 20)                               # BGR do NAVY
    # A grade cresce com y para cima; a imagem cresce com a linha para baixo.
    # Sem este flip, o fundo fica espelhado em relacao ao laser desenhado por
    # px() -- e o mapa parece certo ate voce reparar que o obstaculo trocou de
    # lado. Erro que nao da erro, como de costume.
    img = np.flipud(img).copy()
    img = cv2.resize(img, (mundo.nx * escala // 2, mundo.ny * escala // 2),
                     interpolation=cv2.INTER_NEAREST)
    k = (escala / 2) / mundo.res

    def px(x, y):
        return int(x * k), int(img.shape[0] - y * k)

    # Cinza: onde o robo esteve de verdade. Vermelho: onde a odometria acha que
    # ele esteve. O espaco entre as duas linhas e' a deriva, e e' o assunto.
    for tracado, cor, grossura in ((rastro, (150, 150, 150), 2),
                                   (rastro_odom, (60, 60, 220), 1)):
        if not tracado:
            continue
        for a, b in zip(tracado, tracado[1:]):
            cv2.line(img, px(*a[:2]), px(*b[:2]), cor, grossura, cv2.LINE_AA)

    if pose is not None and leituras is not None:
        x, y, th = pose
        for ang, dist in zip(angulos, leituras):
            if not np.isfinite(dist):
                continue
            cv2.line(img, px(x, y),
                     px(x + dist * np.cos(th + ang), y + dist * np.sin(th + ang)),
                     (17, 163, 252), 1)                           # AMBER
        cv2.circle(img, px(x, y), 5, (40, 40, 40), -1)
        cv2.line(img, px(x, y), px(x + 0.4 * np.cos(th), y + 0.4 * np.sin(th)),
                 (255, 255, 255), 2)

    cv2.imwrite(caminho, img)
    return caminho


if __name__ == '__main__':
    m = Mundo()
    angs = np.linspace(-np.pi, np.pi, 360, endpoint=False)
    pose = (2.0, 4.0, 0.0)
    leituras = m.medir(*pose, angs)
    finitas = leituras[np.isfinite(leituras)]
    print(f'grade        : {m.nx} x {m.ny} celulas ({LARGURA_M} x {ALTURA_M} m)')
    print(f'ocupacao     : {100 * m.grade.mean():.1f}% das celulas sao parede')
    print(f'feixes       : {len(angs)}, {len(finitas)} acertaram algo')
    print(f'distancia    : min {finitas.min():.2f} m / max {finitas.max():.2f} m')
    print('png          :', desenhar(m, pose, leituras, angs))
