# Aula 2 — Ambiente conferido; primeiros nós: tópicos e serviços

**Segunda, 19/10/2026 · Zoom · Etapa 2 · turma live**

[:material-file-pdf-box: Slides da Aula 2 (PDF)](apresentacao-aula02.pdf){ .md-button .md-button--primary }
[:material-code-tags: Exemplo `aula02-comunicacao`](../../exemplos/aula02-comunicacao/index.md){ .md-button }

## Cenas dos últimos episódios

A Aula 1 deixou pronto o **vocabulário** — nós, tópicos, serviços, ações — e a **demonstração** de que o grafo é observável: `rqt_graph` e `ros2 topic echo` mostrando o turtlesim conversando. A semana de 12/10 (sem aula) deixou, se você fez a [tarefa da semana 1](../../tutoriais/tarefa-semana01-ambiente-e-repositorio.md), o **ambiente passando no `check-ambiente.sh`** e o **repositório `pb-live-<usuario>` clonado, com branches e a evidência commitada**.

Hoje a aula usa: **tópico** (vai virar o canal da imagem da câmera), **serviço** (vai virar o `/vision/status` do TP1) e **o seu repositório** (é nele que o pacote de hoje é compilado — não no repositório do material).

## Bloco 0 — Conferência (15 min, antes de qualquer conteúdo)

Ponto de controle no chat, nesta ordem: (1) a última linha do seu `check-ambiente.sh`; (2) a URL do seu repositório; (3) `git branch` mostrando `* dev`. Quem ficou de fora da criação de repositórios manda o usuário do GitHub no chat **agora** — o professor cria ao vivo, você aceita o convite por e-mail e clona durante o bloco 1. Quem travou no ambiente entra na fila de mentoria do bloco 3; nos blocos 1 e 2, acompanhe pela tela do professor.

## O que vai ser visto

Saímos do "rodar o exemplo dos outros" para o "escrever o meu". A aula constrói um pacote `ament_python` do zero, com um **publisher**, um **subscriber** e um **serviço**, e mostra o papel de cada arquivo: `package.xml` declara dependências, `setup.py` registra os executáveis em `entry_points`, e o `launch` sobe tudo com um comando só.

A discussão central é **quando usar tópico e quando usar serviço**. Fluxo contínuo, com muitos ouvintes possíveis e sem garantia de resposta, é tópico — é assim que a imagem da câmera vai viajar. Pergunta pontual que precisa de resposta é serviço — é assim que o `/vision/status` do TP1 vai funcionar. Tarefa longa, com progresso e cancelamento, é ação, e fica para o TP2.

## Exemplo da aula

O pacote [`aula02-comunicacao`](../../exemplos/aula02-comunicacao/index.md) tem os três nós e um launch. O serviço `/contagem` responde quantas mensagens passaram — é o embrião direto do `/vision/status`, e vale rodar `ros2 service call /contagem ...` para sentir a diferença entre perguntar e ouvir.

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
cp -r /tmp/PBRoboticos_live_prof_dacio/exemplos/aula02-comunicacao/aula02_comunicacao \
      "$PB_WS/src/"

# 3) compilar no SEU workspace
cd "$PB_WS"
colcon build --packages-select aula02_comunicacao --symlink-install
source install/setup.bash
ros2 launch aula02_comunicacao comunicacao.launch.py
```

**Ponto de controle do bloco 2:** cole no chat as duas primeiras linhas que o `ros2 launch` imprime depois de subir os nós.

!!! tip "Rode antes de modificar"
    Compile e rode o exemplo **como ele veio**, antes da sua primeira alteração. Parece perda de tempo e é o contrário: quando algo quebrar depois, você sabe que o problema é seu e não do exemplo.

## Tarefa e desafio

- [Tarefa da Aula 2 — primeiros nós](../../tutoriais/tarefa-aula02-primeiros-nos.md) — até domingo 25/10; vira a estrutura de pacote e o serviço do TP1
- [Desafio 1 — comunicação](../../recursos/desafios/desafio-01-comunicacao.md) (opcional, sem nota, aquecimento para o TP1)
- **Projeto:** na mentoria (bloco 3) ou no Infnet.Online até 26/10, diga qual candidato você escolheu — a **leitura do TP1 é na Aula 3 (26/10)** e o enunciado pede o projeto declarado.

## Os três erros que mais aparecem

O campeão absoluto é **"package not found" depois do build**: faltou `source install/setup.bash` *naquele* terminal. Cada aba nova precisa do source, e isso não muda nunca — vale colocar no `~/.bashrc` o source do ROS, mas o do workspace é melhor manter manual, para você lembrar de qual workspace está usando.

O segundo é **editar Python e nada mudar**: sem `--symlink-install` no `colcon build`, o código instalado é uma cópia. Com a flag, é um link, e a edição vale na hora.

O terceiro é **renomear pacote pela metade**: o nome precisa bater em quatro lugares — `package.xml`, `setup.py`, `resource/<nome_do_pacote>` e `setup.cfg` —, e a edição é sempre em `src/`. O `setup.cfg` é o mais esquecido, e é ele que faz o `ros2 launch` reclamar de `libexec directory .../lib/<pacote> does not exist`. O passo a passo com a sequência de comandos está em [renomear um pacote ROS 2](../../tutoriais/renomear-pacote-ros2.md).

Antes de sair da aula: `git add . && git commit -m "Aula 2: pacote de comunicação compilando" && git push`.
