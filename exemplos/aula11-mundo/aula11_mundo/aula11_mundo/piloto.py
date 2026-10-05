"""O navegador mais burro que funciona: anda reto, gira quando fecha na frente.

Ele existe por dois motivos. O pratico: sem ninguem dirigindo, o robo nao anda,
e sem andar nao ha deriva nem mapa. O didatico: e' o contraste de que o Nav2
precisa.

Repare no que ele NAO tem. Nao sabe onde esta. Nao sabe para onde vai. Nao tem
mapa. Nao planeja rota. Nao se recupera quando trava. Cada uma dessas quatro
faltas vira um pedaco do Nav2 no TP4 -- localizacao, objetivo, planejador,
comportamentos de recuperacao. Vale reler esta lista quando chegarmos la.

A decisao em si mora em `nucleo.Piloto`, que nao importa rclpy: e' o mesmo
codigo que o `simular.py` roda sem ROS 2 nenhum.

    ros2 run aula11_mundo piloto
    ros2 param set /piloto velocidade 0.1
"""
import numpy as np
import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

from .nucleo import Piloto as PilotoNucleo


class NoPiloto(Node):
    def __init__(self):
        super().__init__('piloto')

        self.declare_parameter('velocidade', 0.35)
        self.declare_parameter('giro', 0.9)
        self.declare_parameter('parada_m', 0.75)
        self.declare_parameter('cone_graus', 35.0)

        self.piloto = PilotoNucleo()
        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.create_subscription(LaserScan, 'scan', self.decidir, 10)
        self.get_logger().info('piloto reativo no ar -- sem mapa e sem destino')

    def _sincronizar(self):
        """Parametros sao trocaveis em tempo de execucao; o nucleo nao sabe disso."""
        p = self.get_parameter
        self.piloto.velocidade = p('velocidade').value
        self.piloto.giro = p('giro').value
        self.piloto.parada_m = p('parada_m').value
        self.piloto.cone = np.radians(p('cone_graus').value)

    def decidir(self, scan: LaserScan):
        self._sincronizar()
        angulos = scan.angle_min + np.arange(len(scan.ranges)) * scan.angle_increment
        v, w, evento = self.piloto.decidir(angulos, scan.ranges, r_max=scan.range_max)
        if evento:
            self.get_logger().info(evento)
        msg = Twist()
        msg.linear.x, msg.angular.z = float(v), float(w)
        self.pub.publish(msg)


def main():
    rclpy.init()
    no = NoPiloto()
    try:
        rclpy.spin(no)
    except KeyboardInterrupt:
        pass
    finally:
        no.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
