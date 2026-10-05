#!/usr/bin/env python3
"""Valida todo link interno e toda ancora do site construido, contra o HTML real.

O mkdocs --strict pega link para pagina inexistente, mas NAO pega ancora
quebrada: um "#secao-que-nao-existe" passa no build e leva o aluno para o topo
da pagina sem avisar. Este conferidor abre o HTML gerado, coleta todos os id=
de verdade, e cobra cada href contra eles.

Rode DEPOIS de mkdocs build.

    ./tools/montar-docs.sh && mkdocs build --strict && python3 tools/conferir-links.py
"""
import pathlib, re, sys
from urllib.parse import urldefrag, unquote

SITE = pathlib.Path('site').resolve()
_cfg = pathlib.Path('mkdocs.yml').read_text(encoding='utf-8')
_m = re.search(r'^site_url:\s*(\S+)', _cfg, re.M)
BASE = _m.group(1).rstrip('/').split('/', 3)[3] if (_m and _m.group(1).count('/') > 2) else ''
print('base do site:', repr(BASE))
href_re = re.compile(r'<a\b[^>]*?href="([^"]+)"', re.I)
id_re = re.compile(r'\bid="([^"]+)"')

paginas = sorted(SITE.rglob('*.html'))
ids = {p: set(id_re.findall(p.read_text(encoding='utf-8', errors='ignore'))) for p in paginas}

quebrados, ancoras, n_links, n_anc = [], [], 0, 0
for p in paginas:
    txt = p.read_text(encoding='utf-8', errors='ignore')
    for href in href_re.findall(txt):
        if href.startswith(('http://', 'https://', 'mailto:', 'javascript:', '#', 'data:')):
            if href.startswith('#'):
                n_anc += 1
                if unquote(href[1:]) not in ids[p]:
                    ancoras.append(f'{p.relative_to(SITE)} -> {href}')
            continue
        alvo, frag = urldefrag(href)
        n_links += 1
        if alvo.startswith('/'):
            # caminho absoluto da raiz do site publicado: /<base>/...
            rel = unquote(alvo).lstrip('/')
            if BASE and rel.startswith(BASE + '/'):
                rel = rel[len(BASE) + 1:]
            elif BASE and rel == BASE:
                rel = ''
            destino = (SITE / rel).resolve()
        else:
            destino = (p.parent / unquote(alvo)).resolve()
        if destino.is_dir():
            destino = destino / 'index.html'
        if not destino.exists():
            quebrados.append(f'{p.relative_to(SITE)} -> {href}')
            continue
        if frag and destino.suffix == '.html':
            n_anc += 1
            if unquote(frag) not in ids.get(destino, set(id_re.findall(destino.read_text(encoding="utf-8", errors="ignore")))):
                ancoras.append(f'{p.relative_to(SITE)} -> {href}')

for t, lst in (('LINKS QUEBRADOS', quebrados), ('ANCORAS INEXISTENTES', ancoras)):
    if lst:
        print(f'{t} ({len(lst)}):')
        for x in sorted(set(lst)):
            print('  ', x)

print(f'{n_links} links internos / {n_anc} ancoras — {"OK" if not (quebrados or ancoras) else "FALHOU"}')
sys.exit(1 if (quebrados or ancoras) else 0)
