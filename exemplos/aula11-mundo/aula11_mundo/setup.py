from setuptools import setup
import os
from glob import glob

package_name = 'aula11_mundo'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Dacio Moreira de Souza',
    maintainer_email='dacioms@gmail.com',
    description='Mundo minimo sem Gazebo, com deriva de odometria mensuravel.',
    license='MIT',
    entry_points={
        'console_scripts': [
            'mundo = aula11_mundo.mundo:main',
            'piloto = aula11_mundo.piloto:main',
            'simular = aula11_mundo.simular:main',
        ],
    },
)
