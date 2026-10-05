"""Supervisor: diz se o sistema esta vivo, e nao se o launch subiu sem erro.

Duas coisas que ele demonstra, e as duas sao o ponto da aula:

1. LAUNCH NAO SEQUENCIA. Este no quase sempre comeca ANTES do detector. Ele nao
   trava nem morre por isso -- ele reporta 'sem dado ainda' e se recupera
   sozinho quando o outro chega. Um no que exige ordem de subida e' um no que
   vai quebrar no sistema de verdade, onde a ordem nao e' sua.

2. SUBIR NAO E' FUNCIONAR. O supervisor mede a taxa recebida e compara com o
   minimo declarado. 'ros2 node list' prova que o no existe; so a medida prova
   que ele trabalha.
"""
import time
from collections import deque

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Supervisor(Node):
    def __init__(self):
        super().__init__('supervisor')

        self.declare_parameter('janela_s', 5.0)
        self.declare_parameter('taxa_minima_hz', 1.0)

        self.janela = self.get_parameter('janela_s').value
        self.minima = self.get_parameter('taxa_minima_hz').value

        self.chegadas: deque = deque()
        self.ja_recebeu = False

        self.create_subscription(String, 'alvo', self.ouvir, 10)
        self.create_timer(self.janela, self.relatar)

        self.get_logger().info(
            f'vigiando {self.resolve_topic_name("alvo")} | '
            f'janela={self.janela}s minimo={self.minima}Hz')

    def ouvir(self, _msg):
        self.chegadas.append(time.monotonic())
        if not self.ja_recebeu:
            self.ja_recebeu = True
            self.get_logger().info('primeiro dado recebido: o sistema fechou o circuito')

    def relatar(self):
        agora = time.monotonic()
        while self.chegadas and agora - self.chegadas[0] > self.janela:
            self.chegadas.popleft()

        taxa = len(self.chegadas) / self.janela

        if not self.ja_recebeu:
            # Nao e' erro ainda: pode ser so' que o detector ainda esta subindo.
            self.get_logger().warn(
                'nenhum dado ate agora -- o detector subiu? "ros2 topic list"')
        elif taxa < self.minima:
            self.get_logger().warn(
                f'taxa {taxa:.2f}Hz ABAIXO do minimo {self.minima:.2f}Hz')
        else:
            self.get_logger().info(f'taxa {taxa:.2f}Hz (minimo {self.minima:.2f}Hz) ok')


def main():
    rclpy.init()
    no = Supervisor()
    try:
        rclpy.spin(no)
    except KeyboardInterrupt:
        pass
    finally:
        no.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
