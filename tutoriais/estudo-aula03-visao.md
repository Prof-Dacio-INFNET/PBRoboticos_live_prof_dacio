# Guia de estudo — Aula 3: imagem no grafo e segmentação por cor

**Semanas de 26/10 a 08/11 · Etapa 2 · turma live.** A aula de 1h30 leu o TP1 e mostrou o pipeline `câmera → segmentação → contagem → serviço` rodando; **este guia é onde você aprende a construir o seu**. Ele é guiado pela [tarefa da Aula 3](tarefa-aula03-visao.md) em duas partes (Parte A até **domingo 01/11**, Parte B até **domingo 08/11**, push na `dev`), pelo [TP1](../recursos/tp1.md) e pelo [Desafio 2](../recursos/desafios/desafio-02-visao.md) (opcional). Tempo total: **3h a 4h**, em três sessões — e a semana de 02/11, sem aula, existe para a terceira.

| Sessão | O quê | Tempo | Resultado |
|---|---|---|---|
| 1 (até 01/11) | Seções 1 e 2 — ler, reproduzir o exemplo com as saídas esperadas, medir a taxa | 60–80 min | o pipeline sobe no **seu** repositório; `taxas.md` escrito; `PROJETO.md` com o G1.1 |
| 2 (semana de 02/11) | Seção 3 (anatomia dos cinco arquivos) + passos 5–7 da tarefa | 90–120 min | duas classes do seu domínio, YAML, `/vision/status` com domínio |
| 3 (até 08/11) | Seções 5 e 6 — oclusão, autoavaliação, evidências, push | 40–60 min | G1.3 e G1.4 marcados; evidências em `docs/evidencias/aula03/` |

!!! tip "Como pedir ajuda"
    No Infnet.Online, com quatro itens: o **comando exato**, a **saída completa**, `lsb_release -a` e a saída de `ros2 topic info /camera/image_raw --verbose`. Antes disso, a seção 7 ("Se travar").

---

## 1. Leia antes (35 min)

| Fonte | O quê | Minutos | Depois você responde |
|---|---|---|---|
| [Página da Aula 3](../aulas/etapa02-aula03/index.md) | Partes 1 e 2 | 10 | por que a QoS padrão é errada para câmera; por que HSV; onde o vermelho mora |
| [TP1 — enunciado, checklist e gates](../recursos/tp1.md) | inteira | 10 | o que entregar em 13/11; o checklist de verificação por subcompetência; as datas dos sete gates |
| [README do exemplo `aula03-visao`](../exemplos/aula03-visao/index.md) | "Rodar", "Fontes de imagem", "Ajustar sem tocar no código", "Onde editar o quê" | 8 | o que cada nó faz; qual arquivo editar para cada mudança |
| Docs do Humble — [About QoS settings](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Quality-of-Service-Settings.html) | "QoS policies" e "QoS compatibilities" | 7 | o que `RELIABLE`, `BEST_EFFORT`, `KEEP_LAST` e `depth` significam; quais pares se conectam |

Dois conceitos que organizam tudo. **Tópico de imagem é fluxo**: a mensagem perdida já nasceu velha, por isso `BEST_EFFORT` + `KEEP_LAST(1)`; e perfis incompatíveis não dão erro — dão silêncio. **Cor é matiz, não RGB**: em HSV, "é vermelho" é uma faixa estreita em H, e a luz vira tolerância em V; no OpenCV H vai de 0 a 179 e o vermelho ocupa as duas pontas.

## 2. Reproduza o exemplo, passo a passo (45 min)

Você trabalha **no seu repositório**, na branch `dev`, e nunca dentro do repositório do material.

```bash
# ── uma vez por terminal ──────────────────────────────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"

cd "$PB_DIR" && git checkout dev && git pull
rm -rf /tmp/PBRoboticos_live_prof_dacio
cd /tmp && git clone --depth 1 https://github.com/Prof-Dacio-INFNET/PBRoboticos_live_prof_dacio.git
cp -r /tmp/PBRoboticos_live_prof_dacio/exemplos/aula03-visao/aula03_visao "$PB_WS/src/"
ls "$PB_WS/src/aula03_visao"
```

Esperado: `aula03_visao  config  launch  package.xml  resource  setup.cfg  setup.py`. Dentro de `aula03_visao/` (o módulo Python): `publicador_camera.py`, `ponte.py`, `segmentador_hsv.py`, `monitor.py`, `amostrar_hsv.py`.

**2.1 — Antes do ROS: o miolo de visão sem ROS.** É a forma mais rápida de ver o que o pipeline faz e de conferir que o seu OpenCV está são:

```bash
cd /tmp/PBRoboticos_live_prof_dacio/exemplos/aula03-visao && python3 teste_offline.py    # roda na cópia do material; não precisa do seu workspace
```

Esperado (não abre janela nenhuma — serve em qualquer rota):

```text
(limiares lidos de aula03_visao/config/segmentacao.yaml)
autoteste de sugerir_faixas: ok

frame   0: 2 objeto(s) vermelho(s) -> ok
frame   5: 2 objeto(s) vermelho(s) -> ok
…
frame  15: 1 objeto(s) vermelho(s) -> ATENCAO (sobreposicao/borda)
…
frames fora do esperado: 2/12 (alguns são normais quando os dois círculos se sobrepõem)
PNGs em /tmp/aula03_frame.png e /tmp/aula03_mascara.png
```

Dois vermelhos encontrados, o distrator azul ignorado, e **dois quadros com contagem 1**: é a oclusão aparecendo antes mesmo do ROS 2 entrar em cena (seção 5). Abra os dois PNGs. Se der `ModuleNotFoundError: cv2`: `sudo apt install python3-opencv` (pelo **apt**, nunca `pip install opencv-python` fora de um venv — a seção 7 explica o porquê).

**2.2 — Compilar e subir.**

```bash
cd "$PB_WS"
colcon build --packages-select aula03_visao --symlink-install && source install/setup.bash
ros2 launch aula03_visao visao.launch.py
```

Esperado no log, duas linhas que importam:

```text
[publicador_camera-1] [INFO] ... Publicando /camera/image_raw · fonte=sintetico · 640x480 @15fps · cv_bridge=sim (round-trip conferido no import)
[segmentador_hsv-2] [INFO] ... Segmentador no ar: /camera/image_raw -> /vision/segmented + /vision/contagem · serviço /vision/status
```

Se a primeira disser `cv_bridge=nao, conversão manual bgr8 | motivo: …`, **está certo também** — o `ponte.py` montou a mensagem à mão. Anote o motivo; é um dado para o relatório e, se for `KeyError: 16`, a seção 7 tem a cura.

**2.3 — Inspecionar o grafo (segundo terminal, com `source install/setup.bash`).**

```bash
ros2 node list                                    # /publicador_camera  /segmentador_hsv
ros2 topic list                                   # /camera/image_raw  /vision/contagem  /vision/segmented  (+ /parameter_events, /rosout)
ros2 topic info /camera/image_raw --verbose       # os dois perfis: Reliability: BEST_EFFORT nos dois lados
ros2 topic echo /vision/contagem --once           # data: 2
ros2 service call /vision/status std_srvs/srv/Trigger "{}"
```

Esperado no `service call`: `success=True, message='2 objeto(s) no ultimo frame (NNN frames processados)'`. Quando os dois círculos se cruzam, `data: 1` — guarde isso para a seção 5.

**2.4 — O sintoma cruel, de propósito.** Force um subscriber `RELIABLE` contra o publicador `BEST_EFFORT`: `ros2 topic echo /camera/image_raw --once --qos-reliability reliable`. O comando fica mudo — e o `rclpy` imprime um aviso de QoS incompatível, que é o máximo de erro que você vai ver. Sem a flag, o `echo` do Humble **descobre a QoS do publicador sozinho** e mostra o quadro (enorme — `Ctrl+C`); o seu nó, escrito com o `10` padrão do `create_subscription`, **não descobre nada**: é ele que fica mudo. Por isso o segmentador assina com `QOS_SENSOR`. Essa é a cura de "o tópico existe mas não chega nada" para o resto do semestre.

!!! warning "WSL2 e máquina única: duas curas antes de medir qualquer taxa"
    Numa máquina só, uma imagem de 640×480 (**900 kB**) viaja fragmentada em UDP, e o buffer de rede padrão do Linux (208 kB) é **menor que uma mensagem**: fragmentos se perdem, e com eles o quadro inteiro. Sintomas: `A message was lost!!!`, `/vision/contagem` a 2–8 Hz em vez de 15, `hz` com buracos de 0,5 a 2 s. Cura 1, em **todos** os terminais e no `~/.bashrc`: `export ROS_LOCALHOST_ONLY=1`. Cura 2, uma vez, com `sudo` (aumenta os buffers do kernel — a recomendação oficial de *DDS tuning* do ROS 2):

    ```bash
    sudo tee /etc/sysctl.d/60-ros2-imagem.conf >/dev/null <<'EOF'
    net.core.rmem_max=2147483647
    net.core.rmem_default=8388608
    net.core.wmem_max=2147483647
    net.core.wmem_default=8388608
    net.ipv4.ipfrag_time=3
    net.ipv4.ipfrag_high_thresh=134217728
    EOF
    sudo sysctl --system >/dev/null && sysctl net.core.rmem_default     # esperado: 8388608
    ```

    Reinicie o launch e confira `ros2 topic hz /vision/contagem` ≈ 15 Hz. No WSL2, se depois de um `wsl --shutdown` o valor voltar a `212992`, rode `sudo sysctl --system` de novo (ou habilite o systemd em `/etc/wsl.conf`).

**2.5 — Medir a taxa nas duas pontas.**

```bash
ros2 topic hz /vision/contagem                       # esperado: average rate: ~15.0
ros2 topic hz /camera/image_raw --window 30          # esperado: ~15.0 (ou menos — leia abaixo); o hz do Humble já assina com QoS de sensor
```

`/vision/contagem` é um `Int32`: medir é barato e o número é fiel. `/camera/image_raw` são ~900 kB por mensagem: o `hz` é um nó Python desserializando tudo isso, e **mede a si mesmo se afogando** — se der menos que a saída, desconfie da régua, não da câmera. No WSL2, `min:` negativo é o relógio saltando (seção 7). Escreva os números e a interpretação em `docs/evidencias/aula03/taxas.md`: é a Parte A da tarefa e o G1.2.

**2.6 — Ver a imagem e trocar a cor com o sistema no ar.**

```bash
ros2 run rqt_image_view rqt_image_view            # escolha /vision/segmented: máscara verde + caixas amarelas + "objetos: 2"
ros2 param list /segmentador_hsv                  # area_min  desenhar_contornos  h_max  h_max2  h_min  h_min2  s_min  v_min …
ros2 param set /segmentador_hsv h_min 100
ros2 param set /segmentador_hsv h_max 130         # os vermelhos apagam, o azul acende: "objetos: 1"
ros2 param set /segmentador_hsv h_min 0 ; ros2 param set /segmentador_hsv h_max 10
```

Nada foi recompilado nem reiniciado. O que mudou não estava no código — estava **fora** dele. É isso que o TP2 cobra, e é por isso que a Parte B exige zero constante de cor no `.py`.

**2.7 — Medir em vez de chutar.** Com o pipeline no ar:

```bash
ros2 run aula03_visao amostrar_hsv                # clique 4–6 vezes num círculo vermelho (inclusive na borda escura); tecle q
```

Esperado ao sair: um bloco de YAML com `h_min`/`h_max` e, para o vermelho, `h_min2`/`h_max2` — o amostrador detecta o vão no círculo de matiz e devolve as duas faixas. Sem janela gráfica: `ros2 run aula03_visao amostrar_hsv --ros-args -p imagem:=/caminho/foto.jpg`, ou, na cópia do material, `python3 teste_offline.py /caminho/foto.jpg`.

Terminou a sessão 1? Faça o **Passo 3 da tarefa** (declaração do G1.1 no `PROJETO.md`) e dê o push da Parte A.

## 3. Anatomia do código: os cinco arquivos (40 min)

Abra cada arquivo em `src/aula03_visao/aula03_visao/` e procure as linhas citadas. O objetivo é saber **onde mexer** na Parte B.

**`publicador_camera.py` — a boca do pipeline.** Três coisas para localizar: (1) `QOS_SENSOR = QoSProfile(reliability=BEST_EFFORT, history=KEEP_LAST, depth=1)` — o perfil de sensor, usado no `create_publisher`; (2) `frame_sintetico()` — a cena desenhada em código: dois círculos vermelhos em órbitas diferentes e um distrator azul; **é aqui que você desenha os seus dois objetos** se não tiver câmera; (3) `tick()` — chamado pelo timer a `1/fps`, publica `para_msg(frame, stamp=now)`. Repare no timer com relógio `STEADY_TIME`: o relógio de parede do WSL2 pode saltar, o monotônico não. E em `negociar_webcam()`: pedir `MJPG` 640×480 **antes** de capturar é o que evita 3 fps silenciosos pela USB.

**`ponte.py` — `cv_bridge` com plano B.** No import, faz um round-trip de teste (`ndarray → Image → ndarray`); se qualquer coisa falhar, `para_msg`/`para_cv` montam a mensagem à mão: `encoding='bgr8'`, `step = largura*3`, `data = frame.tobytes()`. Saber fazer isso na mão é o que separa quem usa a biblioteca de quem entende o que ela faz — e é o que você explica no relatório se o log disser `cv_bridge=nao`.

**`segmentador_hsv.py` — o miolo do TP1.** Um nó que ao mesmo tempo **assina** (`/camera/image_raw`, com `QOS_SENSOR` — tem de bater com o publisher), **publica** (`/vision/segmented` e `/vision/contagem`) e **atende um serviço** (`/vision/status`). Localize: os oito `declare_parameter` (é deles que vêm os limiares — nunca de constantes); `mascara()` com as duas `inRange` somadas por `bitwise_or` e a morfologia `OPEN` → `CLOSE`; `on_frame()` com `cvtColor`, `findContours(RETR_EXTERNAL)` e o filtro `contourArea >= area_min`; `on_status()` devolvendo a contagem numa string. Na Parte B você generaliza para **duas classes**: o trecho de referência é este —

```python
self.declare_parameter('classes', ['maduro', 'verde'])     # default NÃO vazio: o rclpy infere o tipo do default
self.classes = list(self.get_parameter('classes').value)
padroes = {'h_min': 0, 'h_max': 10, 'h_min2': 0, 'h_max2': 10, 's_min': 120, 'v_min': 70, 'area_min': 400.0}
for nome in self.classes:
    for p, v in padroes.items():
        self.declare_parameter(f'{nome}.{p}', v)             # vira maduro.h_min, verde.h_min … (aninhado no YAML)
self.pub_cont = {n: self.create_publisher(Int32, f'/vision/contagem/{n}', 10) for n in self.classes}
```

— e `mascara(hsv, classe)` lê `self.get_parameter(f'{classe}.{nome}').value` em vez dos nomes fixos. Para classes que não são vermelhas, `h_min2`/`h_max2` **iguais** a `h_min`/`h_max` fazem a segunda faixa ser redundante em vez de vazia. O `on_status()` passa a montar a frase com o domínio: `f'{self.dominio}: ' + ', '.join(f'{self.contagens[c]} {c}' for c in self.classes) + f', taxa {self.hz:.1f} Hz'`.

**`monitor.py` — o outro lado do serviço.** Um cliente que chama `/vision/status` a cada `periodo` segundos. Sobe com `monitor:=true` no launch. Serve para provar que o pipeline está vivo sem interface gráfica — e para você ver, no TP2, que serviço tem cliente.

**`launch/visao.launch.py` + `config/segmentacao.yaml`.** O launch declara `fonte` (`sintetico | webcam | video`) e `monitor`, e carrega o YAML no segmentador com `parameters=[params]`. O YAML é o único lugar dos limiares. Se você editar o YAML e nada mudar, o build foi sem `--symlink-install`: o launch lê `install/share/…`, você editou `src/`.

**`amostrar_hsv.py`.** A função pura `sugerir_faixas(amostras)` é a única com regra de negócio: ordena os matizes, procura o maior vão (considerando a volta 179→0) e devolve uma ou duas faixas, com folga em S e V. É por isso que o `teste_offline.py` consegue testá-la sem ROS.

## 4. Tarefa da semana (obrigatória, em duas partes)

**O que fazer:** o pipeline do exemplo, **com o seu nome**, detectando **as duas classes do seu domínio**, com os limiares medidos e em YAML, o `/vision/status` falando a língua do seu projeto, a taxa medida e interpretada, a oclusão registrada — tudo commitado na `dev`, com as evidências em `docs/evidencias/aula03/` e o `PROJETO.md` com o G1.1 declarado e os gates marcados.

**O que usar:** `exemplos/aula03-visao/` (copiado para o seu `ros2_ws/src/`); [renomear um pacote ROS 2](renomear-pacote-ros2.md); o trecho de duas classes da seção 3; o `amostrar_hsv` e o `teste_offline.py` para os limiares; a [página do TP1](../recursos/tp1.md) para a declaração e os gates.

**Como adequar ao seu projeto:** as duas classes vêm do domínio que você declarou (tampa azul × tampa verde, maduro × verde, capacete × colete…); a cena — sintética, foto, vídeo ou webcam — é a que você consegue sustentar até 13/11; a frase do `/vision/status` é a que o usuário do seu sistema gostaria de ler.

**Como saber que terminou:** `ros2 launch <seu_pacote> visao.launch.py` sobe; `ros2 topic echo /vision/contagem/<classeA> --once` e `…/<classeB>` devolvem os números da cena; `ros2 param set /segmentador_hsv <classeA>.h_min …` troca a detecção **sem recompilar**; o `service call` responde com o domínio; `docs/evidencias/aula03/` tem os cinco arquivos; `git log --oneline` na `dev` mostra commits começando por `G1.1`, `G1.2`, `G1.3`, `G1.4` — já no GitHub.

Passo a passo com as saídas esperadas: [tarefa da Aula 3](tarefa-aula03-visao.md).

## 5. O experimento que vale ouro (15 min)

Deixe `ros2 topic echo /vision/contagem` rodando e espere os dois círculos se cruzarem: `data: 2` vira `data: 1`. **Ninguém saiu de cena** — o sistema perdeu a capacidade de distinguir. Isso é oclusão, o problema número um de qualquer percepção real. Capture o quadro (`oclusao.png`) e escreva três linhas: o que aconteceu, por que (`findContours` devolve **um** contorno externo quando as máscaras se tocam), e o que você faria (área máxima além da mínima, razão de aspecto, memória entre quadros, `watershed`, ou um detector por aparência no TP2). Essas três linhas são um dos tópicos do checklist de verificação do TP1; o [Desafio 2](../recursos/desafios/desafio-02-visao.md) transforma a frase em número.

## 6. Autoavaliação (10 min)

Responda sem olhar; depois abra a resposta.

??? question "1. `ros2 topic list` mostra `/camera/image_raw`, `ros2 node info` mostra publisher e subscriber, e o `echo` não imprime nada. O que é, e qual comando prova?"
    QoS incompatível: o publicador é `BEST_EFFORT` e o subscriber pede `RELIABLE` (o `10` padrão do `create_subscription`); perfis incompatíveis não se conectam e, no máximo, geram um aviso. `ros2 topic info /camera/image_raw --verbose` mostra os dois perfis lado a lado; assinar com o perfil de sensor resolve. (O `echo` e o `hz` da linha de comando do Humble já se adaptam sozinhos — o seu nó, não.)

??? question "2. Por que a câmera usa `BEST_EFFORT` com profundidade 1, se `RELIABLE` garante entrega?"
    Porque um quadro retransmitido chega velho e atrasa os seguintes: a fila cresce, a latência também. Para sensor, o quadro mais recente vale mais que o quadro completo. `RELIABLE` é para comando e configuração, não para fluxo.

??? question "3. O seu objeto é vermelho e a contagem funciona "às vezes". Causa mais provável?"
    Uma faixa só de matiz. No OpenCV H vai de 0 a 179 e o vermelho ocupa as duas pontas — precisa de `h_min`/`h_max` (0–10) **e** `h_min2`/`h_max2` (170–179) somadas com `bitwise_or`.

??? question "4. A taxa de `/vision/contagem` é 15 Hz na cena sintética e cai para 4 Hz com a webcam em 1920×1080. Duas ações, e o que registrar?"
    Reduzir para 640×480 (e pedir `MJPG` antes de capturar) ou processar um quadro a cada N. Registrar os dois números e a interpretação em `taxas.md` — a queda é informação de projeto, não defeito a esconder. E conferir que não há `imshow` dentro do callback.

??? question "5. `ros2 param set /segmentador_hsv maduro.h_min 100` falha com erro de tipo, mas `classes` está declarado. O que olhar?"
    O default de `classes` — se for `[]`, o rclpy não consegue inferir o tipo do parâmetro e os `declare_parameter` aninhados nunca acontecem. Declare com uma lista não vazia (`['maduro', 'verde']`) e confira com `ros2 param list /segmentador_hsv`.

??? question "6. O log diz `cv_bridge=nao, conversão manual bgr8 | motivo: KeyError: 16`. A tarefa está comprometida?"
    Não: o `ponte.py` monta a mensagem à mão e o pipeline roda igual; a tarefa vale nos dois modos. A causa é um OpenCV ou NumPy de `pip` por baixo do `cv_bridge` do `apt`; a cura (seção 7) é **fora** do venv, porque os nós rodam com o `python3` do sistema.

## 7. Se travar

| Sintoma | Causa provável | Cura |
|---|---|---|
| tópico existe, o seu subscriber fica mudo | QoS incompatível (`BEST_EFFORT` × `RELIABLE`) | `ros2 topic info --verbose`; assine com `QOS_SENSOR` (o `echo`/`hz` do Humble se adaptam sozinhos) |
| `ModuleNotFoundError: cv2` | OpenCV não instalado no python do sistema | `sudo apt install python3-opencv` (apt; **não** `pip install opencv-python` fora de venv) |
| `ModuleNotFoundError: cv_bridge` | pacote ausente | o exemplo cai no modo manual sozinho; ou `sudo apt install ros-humble-cv-bridge` |
| `KeyError: 16` (com `AttributeError: _ARRAY_API not found` antes = NumPy 2; sem = OpenCV 5) | OpenCV/NumPy de `pip` em `~/.local` ou `/usr/local` por baixo do `cv_bridge` do `apt` | `python3 -c "import numpy, cv2; print(numpy.__file__, cv2.__file__)"`; se não vier de `/usr/lib/python3/dist-packages`: `python3 -m pip uninstall -y numpy opencv-python opencv-contrib-python opencv-python-headless` e `sudo apt install --reinstall python3-opencv python3-numpy`; confira com `python3 -c "from cv_bridge import CvBridge; print(16 in CvBridge().cvtype_to_name)"` → `True`. **Mexer no venv não resolve** |
| `rqt_image_view` não abre | WSL2: WSLg desatualizado · VirtualBox: Guest Additions ausente ou aceleração 3D ligada | `wsl --update` no PowerShell e reabrir · desligar 3D (VM desligada) / instalar Guest Additions. Plano B: `echo` da contagem + `teste_offline.py` |
| `ModuleNotFoundError: No module named 'PyQt5'` no `rqt_image_view` | venv ativado sem `--system-site-packages` | `deactivate` |
| webcam não abre | WSL2: falta `usbipd attach` · VirtualBox: Extension Pack + *Dispositivos → Webcams* | [câmera no WSL2](camera-wsl2-usbipd.md) · [VirtualBox](setup-ros2-humble-virtualbox.md#webcam-extension-pack-nao-usbipd) · enquanto isso `fonte:=sintetico` |
| webcam abre, 3 fps sem erro | YUYV 1080p pela USB/usbipd | o publicador já pede `MJPG` 640×480; confira a linha `webcam negociada:` no log |
| `hz` com `min:` negativo ou buracos de segundos | relógio do WSL2 saltando | [diagnóstico e cura](setup-ros2-humble-wsl2.md#o-relogio-do-wsl2-pode-saltar-e-isso-estraga-qualquer-medicao) |
| `A message was lost!!!`, `/vision/contagem` a 2–8 Hz, `hz` com buracos de 0,5–2 s | fragmentação UDP numa máquina só: buffer de rede do kernel (208 kB) menor que uma imagem (900 kB) | as duas curas da seção 2.4: `ROS_LOCALHOST_ONLY=1` em todos os terminais **e** o `sysctl` dos buffers; reinicie o launch; não dê `echo` em tópico de imagem |
| editou o YAML e nada muda | build sem `--symlink-install` | `colcon build --symlink-install`; edite só em `src/` |
| `Package not found` / `libexec directory … does not exist` | renomear incompleto (os cinco lugares; `setup.cfg` é o esquecido) | [renomear um pacote ROS 2](renomear-pacote-ros2.md); `rm -rf build install log` |
| máscara toda preta / toda branca | S/V altos demais · H largo demais ou fundo da cor do objeto | comece frouxo (S≥60, V≥40) e aperte · meça com o amostrador; troque o fundo |
| contagem pulando 1↔2 | `area_min` baixo ou falta `OPEN`; objetos se tocando | suba `area_min`; se é toque, **é oclusão: registre** |
| imagem do colega aparecendo | mesmo `ROS_DOMAIN_ID` | cada um com o seu número de 1 a 100 |
| `Exception ignored in: <function Future.__del__ …>` ao sair | ruído do `rclpy` no desligamento | ler `process has finished cleanly`; ignorar |
