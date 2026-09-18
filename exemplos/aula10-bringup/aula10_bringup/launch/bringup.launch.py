"""Um comando sobe o sistema inteiro. E' este o formato que o G3.0 cobra.

    ros2 launch aula10_bringup bringup.launch.py
    ros2 launch aula10_bringup bringup.launch.py --show-args
    ros2 launch aula10_bringup bringup.launch.py modelo:=false
    ros2 launch aula10_bringup bringup.launch.py params:=/caminho/armadilha.yaml

Tres coisas que este arquivo demonstra, e que voce vai precisar no TP3:

  compor       IncludeLaunchDescription traz o launch de um subsistema inteiro,
               com os argumentos que ele precisa. O bringup nao repete nos.
  parametrizar params: vem de fora, entao o MESMO launch sobe o sistema de
               teste e o de bancada. Launch com caminho fixo nao se reaproveita.
  condicionar  IfCondition liga e desliga pedacos. Aqui, o modelo do robo, que
               depende do pacote da Aula 9 estar compilado.

E uma que ele NAO faz, de proposito: ordenar. Ver o comentario no fim.
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg = get_package_share_directory('aula10_bringup')
    padrao = os.path.join(pkg, 'config', 'sistema.yaml')

    params = LaunchConfiguration('params')
    ns = LaunchConfiguration('ns')
    modelo = LaunchConfiguration('modelo')

    # O URDF vem do pacote da Aula 9. Procurar o share de OUTRO pacote e' o
    # padrao: nunca escreva /home/voce/ros2_ws/... dentro de um launch.
    try:
        desc = get_package_share_directory('meu_robo_description')
        urdf = os.path.join(desc, 'urdf', 'meu_robo.urdf')
    except Exception:
        urdf = ''

    acoes = [
        DeclareLaunchArgument('params', default_value=padrao,
                              description='YAML de parametros do sistema'),
        DeclareLaunchArgument('ns', default_value='percepcao',
                              description='namespace da percepcao'),
        DeclareLaunchArgument('modelo', default_value='true',
                              description='subir o modelo do robo (precisa de '
                                          'meu_robo_description compilado)'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg, 'launch', 'percepcao.launch.py')),
            launch_arguments={'params': params, 'ns': ns}.items(),
        ),
    ]

    if urdf:
        descricao = ParameterValue(Command(['cat ', urdf]), value_type=str)
        acoes += [
            Node(package='robot_state_publisher', executable='robot_state_publisher',
                 name='robot_state_publisher', output='screen',
                 condition=IfCondition(modelo),
                 parameters=[{'robot_description': descricao}]),
            Node(package='joint_state_publisher', executable='joint_state_publisher',
                 name='joint_state_publisher',
                 condition=IfCondition(modelo)),
        ]

    return LaunchDescription(acoes)


# SOBRE ORDEM, que e' a duvida que sempre aparece:
#
# Nada aqui espera nada. O launch dispara todos os processos e segue. O
# supervisor quase sempre sobe antes do detector e passa alguns segundos sem
# receber dado -- e isso e' CORRETO, nao e' defeito.
#
# Em ROS 2 o grafo e' descoberto, nao montado em ordem: os nos se encontram
# quando se encontram. Um no que so funciona se subir depois de outro vai
# quebrar no dia em que a maquina estiver mais lenta. A solucao e' o no
# tolerar a ausencia do outro, como o supervisor faz.
#
# Se voce REALMENTE precisar de ordem (raro, e quase sempre sinal de desenho
# errado), existe RegisterEventHandler com OnProcessStart. Use como ultimo
# recurso, nao como primeiro.
