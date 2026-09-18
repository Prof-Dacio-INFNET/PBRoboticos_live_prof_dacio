"""Detector de mentira: publica achados sinteticos, sem camera e sem modelo.

O que ele tem de real sao os PARAMETROS. Este no existe para voce ver, com as
proprias maos, quando o config/*.yaml chega no no e quando ele e ignorado em
silencio -- que e a armadilha da Aula 10.

    ros2 run aula10_bringup detector
    ros2 run aula10_bringup detector --ros-args -p taxa_hz:=5.0
    ros2 param dump /detector
"""
import random

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Detector(Node):
    def __init__(self):
        super().__init__('detector')

        # Declarar e' obrigatorio: parametro nao declarado nao aparece no
        # param dump, nao pode ser setado, e o YAML que o mencione e' recusado.
        self.declare_parameter('taxa_hz', 2.0)
        self.declare_parameter('limiar_confianca', 0.50)
        self.declare_parameter('classe', 'objeto')

        taxa = self.get_parameter('taxa_hz').value
        self.limiar = self.get_parameter('limiar_confianca').value
        self.classe = self.get_parameter('classe').value

        self.pub = self.create_publisher(String, 'alvo', 10)
        self.create_timer(1.0 / taxa, self.tick)

        # Esta linha e' o instrumento da aula: ela imprime o que o no REALMENTE
        # recebeu. Se o numero aqui nao e' o do seu YAML, o YAML nao chegou.
        self.get_logger().info(
            f'no em {self.get_fully_qualified_name()} | '
            f'taxa_hz={taxa} limiar_confianca={self.limiar} classe={self.classe}')

    def tick(self):
        confianca = random.uniform(0.2, 1.0)
        if confianca < self.limiar:
            return                      # abaixo do limiar nao vira deteccao
        msg = String()
        msg.data = f'{self.classe} {confianca:.2f}'
        self.pub.publish(msg)


def main():
    rclpy.init()
    no = Detector()
    try:
        rclpy.spin(no)
    except KeyboardInterrupt:
        pass                            # Ctrl-C e' termino normal, nao erro
    finally:
        no.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
