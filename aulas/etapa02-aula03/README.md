# Aula 3 — O TP1, lido; e a imagem no grafo

**Segunda, 26/10/2026 · Zoom · 1h30 · Etapa 2 · turma live**

[:material-file-pdf-box: Slides da Aula 3 (PDF)](apresentacao-aula03.pdf){ .md-button .md-button--primary }
[:material-book-open-variant: Guia de estudo da Aula 3](../../tutoriais/estudo-aula03-visao.md){ .md-button }
[:material-clipboard-text: TP1 — enunciado, checklist e gates desta turma](../../recursos/tp1.md){ .md-button }
[:material-code-tags: Exemplo `aula03-visao`](../../exemplos/aula03-visao/index.md){ .md-button }

## Cenas dos últimos episódios

A Aula 2 mostrou os três tijolos — publisher, subscriber, serviço — rodando de ponta a ponta, e a [tarefa da Aula 2](../../tutoriais/tarefa-aula02-primeiros-nos.md) deixou, até ontem, o **seu** pacote com quatro nós e o `/contagem` respondendo na `dev`. No Infnet.Online você declarou o candidato a projeto.

Hoje tudo isso continua valendo. O que muda é o **tipo da mensagem**: o tópico deixa de carregar texto e passa a carregar **imagem** — e, com ela, um conjunto de preocupações novas (taxa, latência, perda de quadro, política de entrega). É a diferença entre uma conversa e um fluxo. O serviço da Aula 2 vira o `/vision/status` do TP1; o subscriber vira o segmentador.

## Como a aula de 1h30 funciona

A aula ao vivo **apresenta**; o [guia de estudo](../../tutoriais/estudo-aula03-visao.md) **ensina**. Em 90 minutos: conferência (10 min), **a leitura do TP1** com as datas desta turma (15 min), o conteúdo em linhas gerais com duas demonstrações diretas (25 min), o exemplo da aula de ponta a ponta no repositório do professor (22 min), a tarefa em duas partes e o desafio (10 min) e o fechamento (8 min). Ninguém instala nem compila durante a aula — quem tem ambiente replica junto; quem não tem acompanha pela tela e faz tudo pelo guia, que tem a saída esperada de cada comando.

## Conferência (10 min, antes de qualquer conteúdo)

Ponto de controle no chat, nesta ordem: (1) `git log --oneline -3` na sua `dev` (a tarefa da Aula 2 está lá?); (2) a família do seu projeto (1–7, ou **P** de proposta própria) e, se já souber, o **objeto** que a câmera vai procurar. Quem ainda está sem ambiente ou sem repositório escreve o sintoma no chat e segue pelas tarefas anteriores esta semana — a [da semana 1](../../tutoriais/tarefa-semana01-ambiente-e-repositorio.md) e a [da Aula 2](../../tutoriais/tarefa-aula02-primeiros-nos.md) continuam valendo e vêm **antes** da de hoje.

## Parte 1 — O TP1, lido (15 min)

O enunciado oficial está no Moodle; a página **[TP1 — enunciado, checklist e gates desta turma](../../recursos/tp1.md)** é a versão lida em aula: o que se pede (quatro tarefas), o que se entrega em **sexta, 13/11** (PDF do relatório, ZIP do código, link do repositório com a tag `tp1`, vídeo de até 5 min), um **checklist de verificação** por subcompetência para você conferir a entrega antes de enviar, e os **sete gates com as datas desta turma**:

| Gate | O que tem de estar verdadeiro | Vence |
|---|---|---|
| G1.0 | ambiente operante — `check-ambiente.sh` em "Tudo pronto!" | dom 01/11 |
| G1.1 | projeto **declarado** no `PROJETO.md`: domínio, usuário, **duas classes**, trilha, plano B | **dom 01/11** |
| G1.2 | imagem no grafo com taxa medida (`ros2 topic hz`) nas duas pontas | dom 01/11 |
| G1.3 | segmentação e contagem sobre **o seu objeto**, duas classes | sex 06/11 |
| G1.4 | `/vision/status` com informação do seu domínio + `rqt_graph` salvo | dom 08/11 |
| G1.5 | relatório fechado: decisões, oclusão discutida, limitações, IA declarada | qua 11/11 |
| G1.6 | tag `tp1` + entrega no Moodle | **sex 13/11** |

Repare no calendário: **02/11 é feriado** (não há aula), e a Aula 4 (09/11) é **clínica do TP1** — você chega lá com G1.3 e G1.4 fechados e sai com o relatório encaminhado. O gate mais urgente é o **G1.1**: sem domínio e sem as duas classes, o G1.3 não tem o que detectar, e você gasta a semana afinando HSV de um círculo vermelho que não vai para lugar nenhum.

Sobre a trilha (**S**imulada, **H**íbrida, **R**eal): a [régua é assimétrica de propósito](../../recursos/simulado-vs-hardware.md). Quem simula tem tudo sob controle, então se cobra mais escopo e mais eficácia; quem põe hardware no circuito gasta parte do esforço em problemas que a simulação não tem, e isso é reconhecido. Nesta turma, **projetos com montagem em hardware são bem-vindos**, com a simulação sempre viva como plano B. A webcam já conta como "um elemento real".

## Parte 2 — Imagem no grafo e cor na imagem (25 min, em linhas gerais)

**`sensor_msgs/Image` não tem mágica**: é a matriz do OpenCV serializada (`data`, bytes contíguos) mais os metadados de quem vai interpretá-la — `height`, `width`, `step` (bytes de uma linha), `encoding` (`bgr8`, `rgb8`, `mono8`) e o cabeçalho com `stamp` e `frame_id`. Rode `ros2 interface show sensor_msgs/msg/Image`: é mais curto do que parece.

**A QoS padrão está errada para câmera.** O padrão do ROS 2 é `RELIABLE` com fila de 10: se um quadro se perde, retransmite. Para sensor isso é a escolha errada — quando o quadro retransmitido chega, já está velho, e a fila só aumenta a latência. O perfil de sensor é `BEST_EFFORT`, `KEEP_LAST`, profundidade 1: sempre o quadro mais recente, nunca uma fila de quadros vencidos. A consequência que morde: publisher e subscriber precisam de perfis **compatíveis**; `BEST_EFFORT` de um lado e `RELIABLE` do outro simplesmente não se conectam, **sem mensagem de erro** — o tópico aparece no `topic list`, os nós aparecem no `node info`, e o `echo` fica mudo. *Demonstração direta 1:* um subscriber `RELIABLE` apontado para o publicador `BEST_EFFORT` fica mudo, e `ros2 topic info /camera/image_raw --verbose` mostra os dois perfis lado a lado. (O `ros2 topic echo` do Humble descobre a QoS do publicador sozinho — o **seu nó**, com o `10` padrão, não.)

**`cv_bridge` é a ponte canônica** entre `Image` e `numpy.ndarray`, e o exemplo da aula tem um plano B (`ponte.py`) que monta a mensagem à mão se o pacote faltar ou quebrar. Os dois modos estão certos; a linha de log do publicador diz qual está valendo. O detalhe do `KeyError: 16` (OpenCV ou NumPy de `pip` por baixo do `cv_bridge` do `apt`) está no guia de estudo — leia antes de instalar qualquer coisa com `pip`.

**HSV e não BGR**, porque em BGR brilho e cor estão misturados: vermelho no sol e vermelho na sombra têm valores diferentes nos três canais. HSV separa matiz (H), saturação (S) e valor (V); "é vermelho" vira uma faixa estreita em H, e a variação de luz vira uma tolerância frouxa em V. A primeira armadilha de visão: no OpenCV **H vai de 0 a 179**, e o vermelho mora **nas duas pontas** — segmentar vermelho exige duas máscaras somadas (0–10 e 170–179). Azul, verde e amarelo vivem no meio e precisam de uma só.

**O pipeline em cinco passos**: `cvtColor` (BGR→HSV) → `inRange` (máscara) → `morphologyEx` `OPEN` depois `CLOSE` (tira ruído, fecha buracos) → `findContours` em `RETR_EXTERNAL` → **filtro de área**, o parâmetro mais útil e mais subestimado. *Demonstração direta 2:* `python3 teste_offline.py` rodando a mesma segmentação **sem ROS 2** sobre a cena sintética e sobre uma foto.

**Oclusão é conteúdo, não defeito.** Quando os dois círculos do exemplo se sobrepõem, a contagem cai de 2 para 1. Ninguém saiu de cena; o sistema é que perdeu a capacidade de distinguir. Reproduza, registre com print e discuta no relatório do TP1 (área máxima, razão de aspecto, memória entre quadros, `watershed`): um parágrafo honesto vale mais do que um pipeline que finge que o problema não existe.

## Parte 3 — Exemplo da aula de ponta a ponta (22 min)

No repositório do professor (`pb-live-dacioms`), na ordem: copiar o pacote → `colcon build` → `launch` → `topic hz` nas **duas pontas** → `rqt_image_view` em `/vision/segmented` → trocar a cor por **parâmetro**, com o sistema no ar → a contagem caindo na oclusão → `service call /vision/status` → `amostrar_hsv` sobre uma foto, saindo com o YAML pronto. **Ponto de controle (quem replicou):** cole no chat a resposta do `ros2 service call /vision/status …` ou uma linha do `ros2 topic hz /vision/contagem`.

## Baixar o material desta aula

Os exemplos vivem no repositório da disciplina. Você **não** trabalha dentro dele: copia o pacote para dentro do **seu** projeto e compila lá. A primeira linha é a única que muda de pessoa para pessoa.

```bash
# ── uma vez por terminal ──────────────────────────────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"

# 1) baixar o material (pode repetir sempre — a linha do rm evita o erro de pasta já existente)
rm -rf /tmp/PBRoboticos_live_prof_dacio
cd /tmp && git clone --depth 1 https://github.com/Prof-Dacio-INFNET/PBRoboticos_live_prof_dacio.git

# 2) copiar o pacote desta aula para dentro do SEU projeto
cp -r /tmp/PBRoboticos_live_prof_dacio/exemplos/aula03-visao/aula03_visao \
      "$PB_WS/src/"

# 3) compilar no SEU workspace
cd "$PB_WS"
colcon build --packages-select aula03_visao --symlink-install
source install/setup.bash
ros2 launch aula03_visao visao.launch.py          # fonte sintética: não precisa de webcam
```

Em outro terminal (com `source install/setup.bash`):

```bash
ros2 topic hz /vision/contagem                    # a régua leve — ≈ 15 Hz; se vier 2–4 Hz, leia o aviso abaixo
ros2 service call /vision/status std_srvs/srv/Trigger "{}"
ros2 param set /segmentador_hsv h_min 100
ros2 param set /segmentador_hsv h_max 130         # agora ele caça azul — nada recompilado
```

!!! tip "Rode antes de modificar"
    Compile e rode o exemplo **como ele veio**, antes da sua primeira alteração. Parece perda de tempo e é o contrário: quando algo quebrar depois, você sabe que o problema é seu e não do exemplo.

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

## Esta semana e a próxima: estudo guiado, tarefa em duas partes, desafio

- [Guia de estudo da Aula 3](../../tutoriais/estudo-aula03-visao.md) — 3h a 4h em três sessões: leituras com minutos, o exemplo reproduzido com as saídas esperadas, anatomia dos cinco arquivos, autoavaliação. **Comece por ele.**
- [Tarefa da Aula 3 — pipeline de visão do seu projeto](../../tutoriais/tarefa-aula03-visao.md) — obrigatória, em **duas partes**: **Parte A até domingo 01/11** (pacote seu compilando, taxa medida, `PROJETO.md` com o G1.1 declarado); **Parte B até domingo 08/11** (duas classes do seu domínio, parâmetros em YAML, `/vision/status` com domínio, evidências). A Parte B é a **tarefa guiada da semana de 02/11**, que não tem aula.
- [Desafio 2 — visão robusta](../../recursos/desafios/desafio-02-visao.md) — opcional, sem nota: métrica em 20 quadros, iluminação quebrada de propósito, oclusão, custo em Hz. É o caminho para um relatório com números em vez de adjetivos.
- [TP1 — enunciado, checklist e gates](../../recursos/tp1.md) — releia uma vez com calma; copie o bloco de gates para o seu `PROJETO.md` e use o checklist antes de entregar.

## Os erros que mais vão aparecer

**"O tópico existe e não chega nada"** é QoS: `ros2 topic info /camera/image_raw --verbose` mostra os dois perfis; no seu nó, assine com o perfil de sensor (o `QOS_SENSOR` do exemplo). **`A message was lost!!!` / contagem a 2–8 Hz** é fragmentação UDP numa máquina só: `ROS_LOCALHOST_ONLY=1` + buffers do kernel (aviso acima). **`KeyError: 16`** na conversão é OpenCV ou NumPy de `pip` por baixo do `cv_bridge` — o exemplo não trava (cai no modo manual); a cura está no guia, seção 7, e **não passa pelo venv**. **Vermelho detectado pela metade** é a segunda faixa (170–179) esquecida. **Contagem oscilando** é `area_min` baixo ou falta de `OPEN`; se os objetos se tocam, é oclusão — registre, não "conserte". **Janela do `rqt_image_view` não abre** no WSL2 é WSLg (`wsl --update`); no VirtualBox é aceleração 3D ligada ou Guest Additions ausente. **Webcam não abre**: WSL2 precisa do [usbipd](../../tutoriais/camera-wsl2-usbipd.md); VirtualBox usa o Extension Pack; e enquanto isso `fonte:=sintetico` **vale para a tarefa inteira**.

Quem replicou durante a aula: `git add . && git commit -m "Aula 3: pipeline de visão compilando" && git push` antes de sair. Quem não, o push vem com a Parte A — até domingo 01/11.

## Próximo encontro: Aula 4, segunda 09/11

Não há aula em 02/11 (feriado): a semana é a Parte B da tarefa, com plantão de dúvidas no Infnet.Online. Em 09/11 a Aula 4 traz interfaces próprias (o `.srv` que vai substituir o `std_srvs/Trigger`) e a **clínica do TP1**: chegue com G1.3 e G1.4 fechados e com uma pergunta específica sobre o seu projeto. A entrega é na sexta, 13/11.
