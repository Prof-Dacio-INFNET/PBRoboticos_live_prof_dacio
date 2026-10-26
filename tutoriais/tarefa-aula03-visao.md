---
titulo: "Tarefa da Aula 3 — pipeline de visão do seu projeto (em duas partes)"
aula: 3
etapa: 2
data_aula: 2026-10-26
prazo_parte_a: 2026-11-01
prazo_parte_b: 2026-11-08
obrigatoria: true
vira_no_tp: "TP1 itens 1, 3 e 4 — gates G1.1 a G1.4"
---

# Tarefa da Aula 3 — pipeline de visão do seu projeto

**Publicada em 26/10/2026 · Parte A até domingo 01/11, 23h59 · Parte B até domingo 08/11, 23h59 · push na `dev`**

Esta tarefa não é um exercício avulso: o que você entregar aqui é, quase sem modificação, o que o **TP1 cobra nos itens 3 e 4** em 13/11, e ela fecha os gates **G1.1 a G1.4**. Ela vem em duas partes porque a semana de 02/11 não tem aula: a Parte B é a **tarefa guiada** dessa semana. Tempo: ~1h30 para a Parte A e ~2h30 para a Parte B, **depois** de estudar — o [guia de estudo da Aula 3](estudo-aula03-visao.md) explica cada arquivo que você vai mexer; comece por ele.

O exemplo da aula caça círculos vermelhos desenhados em código. O seu trabalho é fazer o mesmo pipeline caçar **o objeto do seu projeto** — duas classes — e provar que funciona.

<!-- PB:TAREFA-A03 -->
**Parte A (dom 01/11)**

- [ ] A1 pacote **seu** (renomeado) compilando limpo com `colcon build --symlink-install`
- [ ] A2 exemplo rodando como veio; `docs/evidencias/aula03/taxas.md` com `topic hz` nas duas pontas e a QoS de cada uma, **interpretados**
- [ ] A3 `PROJETO.md` com a declaração do G1.1 (domínio, usuário, duas classes, trilha, plano B) e o bloco de gates do TP1
- [ ] A4 commit(s) na `dev` com push

**Parte B (dom 08/11)**

- [ ] B1 **duas classes do seu domínio** segmentadas e contadas (cena sintética editada, foto, vídeo ou webcam), limiares **medidos** com `amostrar_hsv`
- [ ] B2 todos os limiares, áreas e caminhos em `config/*.yaml` — zero constante de cor no código; troca de classe com o sistema no ar
- [ ] B3 `/vision/status` respondendo com informação do **seu** domínio
- [ ] B4 oclusão reproduzida e registrada (print + 3 linhas)
- [ ] B5 evidências em `docs/evidencias/aula03/`: `pipeline.png`, `grafo.png`, `status.txt`, `oclusao.png`; commit na `dev` com push

## Parte A — até domingo 01/11

### Passo 1 — Adote o exemplo como seu

Copie, renomeie, compile, rode **antes** de mudar qualquer coisa. Rodar o exemplo intacto no seu workspace parece perda de tempo e é o oposto: quando algo quebrar depois da sua primeira alteração, você saberá que o problema é seu.

```bash
# ── uma vez por terminal ──────────────────────────────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"

rm -rf /tmp/PBRoboticos_live_prof_dacio
cd /tmp && git clone --depth 1 https://github.com/Prof-Dacio-INFNET/PBRoboticos_live_prof_dacio.git
cp -r /tmp/PBRoboticos_live_prof_dacio/exemplos/aula03-visao/aula03_visao "$PB_WS/src/percepcao_meu_projeto"
cd "$PB_WS"
colcon build --packages-select aula03_visao --symlink-install && source install/setup.bash
ros2 launch aula03_visao visao.launch.py            # ainda com o nome do exemplo: primeiro rode, depois renomeie
```

Escolha um nome que descreva o seu domínio, não a aula: `percepcao_estoque`, `visao_pomar`, `deteccao_epi`. O nome do pacote é a primeira coisa que o avaliador lê. Renomeie nos **cinco lugares** — a pasta do módulo Python, `<name>` no `package.xml`, `package_name` e os `entry_points` no `setup.py`, `resource/<nome>` e o **`setup.cfg`** (`script_dir`/`install_scripts`) — seguindo [renomear um pacote ROS 2](renomear-pacote-ros2.md). Toda edição acontece em `src/`; `build/` e `install/` são gerados.

```bash
cd "$PB_WS" && rm -rf build install log
colcon build --symlink-install && source install/setup.bash
ros2 launch percepcao_meu_projeto visao.launch.py   # com o SEU nome
```

!!! warning "Os dois erros do renomear"
    `Package not found` que sobrevive a recompilações: faltou `package.xml` ou `resource/<nome>`. `libexec directory .../lib/<nome> does not exist`: o `setup.cfg` ficou com o nome antigo — o quinto lugar, o mais esquecido.

### Passo 2 — Meça a taxa real (G1.2)

Este passo é o que separa "rodou" de "funciona". Com o pipeline em execução, em outro terminal:

```bash
ros2 topic hz /vision/contagem                                       # a régua leve: Int32, barato de medir
ros2 topic hz /camera/image_raw --qos-reliability best_effort --window 30   # a entrada (pesado: 900 kB por mensagem)
ros2 topic info /camera/image_raw --verbose                          # os perfis de QoS de cada ponta
```

Registre em `docs/evidencias/aula03/taxas.md`: a taxa de entrada, a de saída e a QoS de cada ponta. Depois responda, em duas ou três linhas, à pergunta que importa: **a taxa de saída caiu em relação à de entrada?** Se caiu, o seu processamento não acompanha a câmera, e isso é informação de projeto, não defeito a esconder. Se `hz` em `/camera/image_raw` não imprime nada, é QoS: faltou `--qos-reliability best_effort`. Se o `min:` vier **negativo**, é o relógio do WSL2 saltando — veja o guia, seção 7.

Copie o mesmo arquivo para `docs/evidencias/tp1/topic-hz.txt`: é a evidência do G1.2.

### Passo 3 — Declare o projeto (G1.1)

No `PROJETO.md`, cole e preencha a declaração e o bloco de gates que estão em [TP1 — enunciado, régua e gates](../recursos/tp1.md). As **duas classes** precisam ser distinguíveis por cor e de tamanhos parecidos. Alguns pares que funcionam:

| Domínio | Classe A | Classe B | Onde conseguir |
|---|---|---|---|
| Estoque / logística | caixa azul | caixa amarela | papel colorido, dois post-its grandes |
| Agrícola | fruto maduro (vermelho) | fruto verde | tomate cereja, ou dois círculos impressos |
| Segurança do trabalho | capacete amarelo | colete laranja | recorte de papel, foto no celular |
| Tráfego | sinal verde | sinal vermelho | imagem na tela do celular apontada para a webcam |
| Triagem / reciclagem | tampa azul | tampa verde | duas tampas de garrafa |

Uma classe só esconde o problema interessante: com uma classe, qualquer limiar que detecte alguma coisa parece funcionar.

### Passo 4 — Commit da Parte A

```bash
cd "$PB_DIR" && git add -A
git commit -m "G1.1: projeto declarado (<dominio>, classes <A> e <B>, trilha <S/H/R>)"
git commit --allow-empty -m "G1.2: imagem no grafo, taxas medidas em docs/evidencias/aula03/taxas.md"   # ou um commit por passo
git push origin dev
```

## Parte B — até domingo 08/11 (a semana sem aula)

### Passo 5 — Troque o alvo: as suas duas classes

Para descobrir os limiares HSV do seu objeto, não chute. Meça:

```bash
ros2 run percepcao_meu_projeto amostrar_hsv          # ao vivo, com o pipeline rodando: clique no objeto, tecle q, cole o YAML
ros2 run percepcao_meu_projeto amostrar_hsv --ros-args -p imagem:=/caminho/foto.jpg   # sobre uma foto
cd /tmp/PBRoboticos_live_prof_dacio/exemplos/aula03-visao && python3 teste_offline.py /caminho/foto.jpg   # nem precisa do ROS 2 no ar
```

Clique em vários pontos do objeto, **inclusive nas partes em sombra**: a faixa precisa cobrir o objeto real, não o objeto bem iluminado. Ao sair, o nó imprime o bloco de YAML pronto. Lembre da armadilha do vermelho: no OpenCV o matiz vai de **0 a 179**, e o vermelho ocupa as duas pontas — precisa de duas faixas (`h_min`/`h_max` e `h_min2`/`h_max2`).

!!! tip "Sem webcam? A tarefa continua valendo — inteira"
    Edite `frame_sintetico()` em `publicador_camera.py` para desenhar os **seus** dois objetos, com as suas cores e tamanhos, ou use `fonte:=video` com um clipe gravado no celular, ou uma foto no `teste_offline.py`. **A fonte sintética é aceita no TP1** desde que o relatório explique a escolha — o que se avalia é o pipeline. A câmera entra depois, pela sua rota: [usbipd no WSL2](camera-wsl2-usbipd.md), Extension Pack no [VirtualBox](setup-ros2-humble-virtualbox.md#webcam-extension-pack-nao-usbipd), `/dev/video0` no Ubuntu nativo. Não espere hardware para começar.

Agora faça o segmentador tratar **duas classes**. O caminho de referência: um parâmetro `classes` (lista de nomes) e, para cada classe, os seus limiares como parâmetros `nome.h_min`, `nome.h_max` …; uma máscara por classe; um publisher `/vision/contagem/<classe>` por classe. O guia de estudo, seção 4, mostra o trecho de código. A versão **achatada** (`classe_a_h_min`, `classe_b_h_min` …) é igualmente aceita: o que se avalia é "zero constante de cor no código", não a topologia do YAML.

### Passo 6 — Parâmetros fora do código

Nenhum limiar, nenhuma área mínima e nenhum caminho de dispositivo escrito como constante no `.py`. Tudo em `config/percepcao.yaml`, carregado pelo launch:

```yaml
segmentador_hsv:
  ros__parameters:
    classes: ['maduro', 'verde']
    maduro: {h_min: 0,  h_max: 10, h_min2: 170, h_max2: 180, s_min: 120, v_min: 70, area_min: 400.0}
    verde:  {h_min: 35, h_max: 85, h_min2: 35,  h_max2: 85,  s_min: 80,  v_min: 60, area_min: 400.0}
```

O teste de aceitação é objetivo — você consegue trocar a classe detectada com o sistema **em execução**, sem recompilar?

```bash
ros2 param set /segmentador_hsv maduro.h_min 100
ros2 param set /segmentador_hsv maduro.h_max 130
```

### Passo 7 — `/vision/status` com o seu domínio

O serviço do exemplo devolve uma contagem genérica. O seu deve devolver algo que faça sentido para quem usaria o sistema:

```text
"2 objeto(s) no ultimo frame (431 frames processados)"                        # genérico, do exemplo
"pomar setor 3: 2 maduros, 5 verdes, taxa 12.4 Hz, ultima deteccao ha 0.3 s"  # seu, com domínio
```

```bash
ros2 service call /vision/status std_srvs/srv/Trigger "{}" | tee docs/evidencias/aula03/status.txt
```

Devolver números dentro de uma string é feio e frágil. Guarde o incômodo: na Aula 4 você cria o seu próprio `.srv` com campos tipados, e a motivação é exatamente esta.

### Passo 8 — A oclusão

Faça as suas duas classes (ou dois objetos da mesma classe) se sobreporem — na cena sintética basta aproximar as órbitas; com câmera, aproxime os objetos. Capture o momento em que a contagem cai (`rqt_image_view` em `/vision/segmented` + `ros2 topic echo /vision/contagem`) em `docs/evidencias/aula03/oclusao.png` e escreva três linhas: o que aconteceu, por que, e o que você faria a respeito (área máxima, razão de aspecto, memória entre quadros, `watershed`). Essas três linhas vão para o relatório do TP1.

### Passo 9 — Evidências e commit da Parte B

| Arquivo em `docs/evidencias/aula03/` | O que mostra |
|---|---|
| `pipeline.png` | `rqt_image_view` em `/vision/segmented` com as duas classes marcadas |
| `grafo.png` | `rqt_graph` mostrando câmera → segmentador → contagem (+ status) |
| `status.txt` | a saída do `ros2 service call` com o seu domínio |
| `oclusao.png` | o quadro em que a contagem caiu, com as três linhas em `taxas.md` ou no próprio commit |

Copie `pipeline.png` para `docs/evidencias/tp1/segmentacao.png` e `grafo.png` para `docs/evidencias/tp1/rqt_graph.png`: são as evidências do G1.3 e do G1.4. Marque os dois gates no `PROJETO.md`.

```bash
git add -A && git commit -m "G1.3: segmentação de <A> e <B> com limiares medidos; YAML sem constantes"
git add -A && git commit -m "G1.4: /vision/status com domínio + rqt_graph; oclusão registrada"
git push origin dev
```

Um commit só está bom. Vários, um por passo, está melhor — a mensagem de commit é a única narrativa do seu processo que sobrevive até a arguição.

## O que esta tarefa fecha

Parte A: **G1.1** e **G1.2** (e o G1.0, se ainda não estava). Parte B: **G1.3** e **G1.4**. Sobram para a semana da Aula 4: o relatório (G1.5, qua 11/11) e a entrega (G1.6, sex 13/11). A [página do TP1](../recursos/tp1.md) tem o calendário inteiro.

## Se der errado

| Sintoma | O que verificar |
|---|---|
| `Package not found` depois de renomear | `package.xml` e `resource/<nome>`; `rm -rf build install log`; ver [renomear pacote](renomear-pacote-ros2.md) |
| `libexec directory .../lib/<pacote> does not exist` | o `setup.cfg` ficou com o nome antigo (`script_dir`/`install_scripts`) |
| `ros2 topic hz` sem saída em `/camera/image_raw` | QoS: acrescente `--qos-reliability best_effort`; confira com `ros2 topic info --verbose` |
| `hz` com `min:` negativo, ou buracos de segundos | relógio do WSL2 saltando — [diagnóstico e cura](setup-ros2-humble-wsl2.md#o-relogio-do-wsl2-pode-saltar-e-isso-estraga-qualquer-medicao) |
| `KeyError: 16` na conversão (com ou sem `AttributeError: _ARRAY_API not found` antes) | OpenCV ou NumPy de `pip` por baixo do `cv_bridge` do `apt`. O exemplo cai sozinho na conversão manual e a tarefa vale assim. Cura **fora do venv**: `python3 -m pip uninstall -y numpy opencv-python opencv-contrib-python opencv-python-headless` e `sudo apt install --reinstall python3-opencv python3-numpy` |
| parâmetro `classes` dá erro de tipo | o default não pode ser lista vazia: o rclpy infere o tipo do default — declare com `['a', 'b']` |
| editou o YAML e nada muda | build sem `--symlink-install`: o launch lê `install/share/`, você editou `src/` |
| máscara toda preta | `s_min`/`v_min` altos demais; comece frouxo (S≥60, V≥40) e aperte |
| máscara toda branca | faixa de matiz larga demais, ou objeto e fundo com a mesma cor — troque o fundo |
| contagem pulando entre 1 e 2 | `area_min` baixo, ou falta morfologia `OPEN`; se os objetos se tocam, é oclusão (registre) |
| tudo funciona, taxa em 2 Hz | resolução alta demais, ou `imshow` dentro do callback |
| `A message was lost!!!` no `echo` de imagem | fragmentação UDP; `export ROS_LOCALHOST_ONLY=1` em todos os terminais — e não dê `echo` em tópico de imagem |
| `Exception ignored in: <function Future.__del__ …>` ao sair | ruído do `rclpy` no desligamento; a linha que importa é `process has finished cleanly` |

Antes de pedir ajuda no Infnet.Online: o comando exato, a saída completa, o que você já tentou, `lsb_release -a` e a saída de `ros2 topic info --verbose`. Pergunta com diagnóstico é resolvida em minutos.
