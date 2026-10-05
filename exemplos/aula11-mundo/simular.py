#!/usr/bin/env python3
"""Roda o mundo inteiro sem ROS 2 e desenha o resultado.

Fica aqui, ao lado do testar.py, para que tudo o que nao precisa de ROS 2 rode
a partir desta pasta -- sem entrar no pacote e sem PYTHONPATH.

    python3 simular.py
    python3 simular.py --deriva 0 --segundos 60 --saida sem-deriva.png

Com o pacote compilado, o mesmo programa tambem atende por:

    ros2 run aula11_mundo simular
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / 'aula11_mundo'))

from aula11_mundo.simular import main                                 # noqa: E402

if __name__ == '__main__':
    main()
