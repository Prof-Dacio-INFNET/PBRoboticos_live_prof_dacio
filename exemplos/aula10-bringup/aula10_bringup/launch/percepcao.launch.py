"""O subsistema de percepcao: detector + supervisor, sob um namespace.

Este launch existe para ser INCLUIDO por outro. E' assim que um bringup grande
se mantem legivel: cada subsistema tem o seu arquivo, e o bringup so os compoe.

    ros2 launch aula10_bringup percepcao.launch.py
    ros2 launch aula10_bringup percepcao.launch.py ns:=frente
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, PushRosNamespace


def generate_launch_description():
    pkg = get_package_share_directory('aula10_bringup')
    padrao = os.path.join(pkg, 'config', 'sistema.yaml')

    params = LaunchConfiguration('params')
    ns = LaunchConfiguration('ns')

    return LaunchDescription([
        DeclareLaunchArgument('params', default_value=padrao,
                              description='arquivo YAML de parametros'),
        DeclareLaunchArgument('ns', default_value='percepcao',
                              description='namespace do subsistema'),

        # GroupAction + PushRosNamespace: o namespace vale para tudo que estiver
        # dentro do grupo. E' ele que permite subir DOIS detectores (frente e
        # re) sem colisao de nome -- e e' ele que quebra o YAML que nao usa /**.
        GroupAction([
            PushRosNamespace(ns),
            Node(package='aula10_bringup', executable='detector',
                 name='detector', parameters=[params], output='screen'),
            Node(package='aula10_bringup', executable='supervisor',
                 name='supervisor', parameters=[params], output='screen'),
        ]),
    ])
