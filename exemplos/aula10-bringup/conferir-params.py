#!/usr/bin/env python3
"""Diz se o seu YAML de parametros vai REALMENTE chegar nos seus nos.

Por que isto existe: quando a chave do YAML nao casa com o nome completo do no,
o ROS 2 nao reclama. O no sobe com os valores padrao do codigo, o launch nao
acusa nada, e voce passa a tarde ajustando um arquivo que ninguem le. E' a
falha silenciosa mais cara do TP3.

Nao precisa de ROS 2 instalado. Precisa dos nomes COMPLETOS dos seus nos, que
sao exatamente o que o "ros2 node list" imprime com o sistema no ar.

    ros2 launch aula10_bringup bringup.launch.py        # num terminal
    ros2 node list                                      # noutro, copie a saida

    python3 conferir-params.py config/sistema.yaml /percepcao/detector
    ros2 node list | python3 conferir-params.py config/sistema.yaml -

A regra que ele aplica e' a do ROS 2:
    /**            casa com qualquer no, em qualquer profundidade
    /*             casa com um nivel de namespace
    /ns/no         casa so' com aquele no, naquele namespace
    no             e' o mesmo que /no -- portanto NAO casa com /ns/no
"""
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit('falta o pyyaml:  sudo apt install python3-yaml')

VERDE, VERMELHO, AMARELO, FIM = '\033[32m', '\033[31m', '\033[33m', '\033[0m'


def chave_para_regex(chave: str) -> re.Pattern:
    """Converte uma chave do YAML no padrao de nome de no que ela representa."""
    if not chave.startswith('/'):
        chave = '/' + chave
    partes = [p for p in chave.split('/') if p]
    pedacos = []
    for p in partes:
        if p == '**':
            pedacos.append(r'(?:/[^/]+)*')
        elif p == '*':
            pedacos.append(r'/[^/]+')
        else:
            pedacos.append('/' + re.escape(p))
    return re.compile('^' + ''.join(pedacos) + '$')


def params_do_no(doc: dict, no: str) -> tuple[dict, list[str]]:
    """Parametros que o no recebe, e as chaves que os entregaram, em ordem."""
    efetivos: dict = {}
    origens: list[str] = []
    for chave, corpo in doc.items():
        if not isinstance(corpo, dict) or 'ros__parameters' not in corpo:
            continue
        if chave_para_regex(str(chave)).match(no):
            efetivos.update(corpo['ros__parameters'] or {})
            origens.append(str(chave))
    return efetivos, origens


def main() -> int:
    if len(sys.argv) < 3:
        sys.exit(__doc__.strip().splitlines()[0] + '\n\nuso: conferir-params.py <arquivo.yaml> <no> [no ...]  (ou - para ler do stdin)')

    caminho, alvos = sys.argv[1], sys.argv[2:]
    if alvos == ['-']:
        alvos = [l.strip() for l in sys.stdin if l.strip().startswith('/')]
    if not alvos:
        sys.exit('nenhum nome de no recebido')

    with open(caminho, encoding='utf-8') as fh:
        doc = yaml.safe_load(fh) or {}

    chaves = [k for k, v in doc.items()
              if isinstance(v, dict) and 'ros__parameters' in v]
    print(f'arquivo : {caminho}')
    print(f'chaves  : {", ".join(chaves) if chaves else "(nenhuma chave com ros__parameters)"}')
    print()

    orfas = set(chaves)
    problema = False

    for no in alvos:
        efetivos, origens = params_do_no(doc, no)
        orfas -= set(origens)
        if efetivos:
            print(f'{VERDE}OK{FIM}   {no}')
            print(f'       casou com: {", ".join(origens)}')
            for k, v in sorted(efetivos.items()):
                print(f'       {k} = {v}')
        else:
            problema = True
            print(f'{VERMELHO}NADA{FIM} {no}')
            print(f'       nenhuma chave deste YAML casa com este no.')
            print(f'       ele vai subir com os valores PADRAO do codigo, sem aviso.')
            ns = no.rsplit('/', 1)[0] or '/'
            print(f'       curas: troque a chave por "{no}:" ou use "/**:"')
            print(f'              (o namespace deste no e\' "{ns}")')
        print()

    if orfas:
        problema = True
        print(f'{AMARELO}SOBRANDO{FIM} chaves que nao casaram com no nenhum:')
        for c in sorted(orfas):
            print(f'       {c}  -- nome errado, ou o no nao esta no ar')
        print()

    if problema:
        print('Veredito: este YAML NAO esta inteiramente chegando aos nos.')
        return 1
    print('Veredito: todos os nos recebem parametros deste arquivo.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
