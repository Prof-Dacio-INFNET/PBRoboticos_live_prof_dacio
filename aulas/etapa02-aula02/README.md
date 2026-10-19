# Aula 2 — Ambiente conferido; primeiros nós: tópicos e serviços

**Segunda, 19/10/2026 · Zoom · 1h30 · Etapa 2 · turma live**

[:material-file-pdf-box: Slides da Aula 2 (PDF)](apresentacao-aula02.pdf){ .md-button .md-button--primary }
[:material-book-open-variant: Guia de estudo da Aula 2](../../tutoriais/estudo-aula02-primeiros-nos.md){ .md-button }
[:material-code-tags: Exemplo `aula02-comunicacao`](../../exemplos/aula02-comunicacao/index.md){ .md-button }

## Cenas dos últimos episódios

A Aula 1 deixou pronto o **vocabulário** — nós, tópicos, serviços, ações — e a **demonstração** de que o grafo é observável: `rqt_graph` e `ros2 topic echo` mostrando o turtlesim conversando. A semana de 12/10 (sem aula) deixou, se você fez a [tarefa da semana 1](../../tutoriais/tarefa-semana01-ambiente-e-repositorio.md), o **ambiente passando no `check-ambiente.sh`** e o **repositório `pb-live-<usuario>` clonado, com branches e a evidência commitada**.

Hoje a aula usa: **tópico** (vai virar o canal da imagem da câmera), **serviço** (vai virar o `/vision/status` do TP1) e **o seu repositório** (é nele que o pacote de hoje é compilado — não no repositório do material).

## Como a aula de 1h30 funciona

A aula ao vivo **apresenta**; o [guia de estudo](../../tutoriais/estudo-aula02-primeiros-nos.md) **ensina**. Em 90 minutos: conferência de ambiente e repositório (10 min), o conteúdo em linhas gerais com os exemplos rodando na tela (30 min), o exemplo da aula de ponta a ponta no repositório do professor (25 min), a tarefa e o desafio da semana explicados (15 min) e o fechamento (10 min). Ninguém instala nem compila durante a aula — quem já tem ambiente acompanha replicando; quem não tem, acompanha pela tela e faz tudo pelo guia, que tem a saída esperada de cada comando.

## Conferência (10 min, antes de qualquer conteúdo)

Ponto de controle no chat, nesta ordem: (1) a última linha do seu `check-ambiente.sh`; (2) a URL do seu repositório; (3) `git branch` mostrando `* dev`. Quem ficou de fora da criação de repositórios manda o usuário do GitHub no chat **agora** — o professor cria durante a aula, você aceita o convite por e-mail e clona depois. Quem travou no ambiente escreve o sintoma no chat e segue o guia de estudo esta semana; a seção "Se travar" dele e o Infnet.Online resolvem o resto.

## O que vai ser visto

Saímos do "rodar o exemplo dos outros" para o "escrever o meu". A aula mostra, em linhas gerais, um pacote `ament_python` com um **publisher**, um **subscriber** e um **serviço**, e o papel de cada arquivo: `package.xml` declara dependências, `setup.py` registra os executáveis em `entry_points`, e o `launch` sobe tudo com um comando só. O detalhe linha a linha fica para a seção 3 do guia de estudo.

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

**Ponto de controle (quem replicou):** cole no chat a resposta do `ros2 service call /contagem …`.

!!! tip "Rode antes de modificar"
    Compile e rode o exemplo **como ele veio**, antes da sua primeira alteração. Parece perda de tempo e é o contrário: quando algo quebrar depois, você sabe que o problema é seu e não do exemplo.

## Esta semana: estudo guiado, tarefa e desafio

- [Guia de estudo da Aula 2](../../tutoriais/estudo-aula02-primeiros-nos.md) — 2h30 a 3h30 em duas ou três sessões: leituras com minutos, o exemplo reproduzido com as saídas esperadas, anatomia do código, autoavaliação. **Comece por ele.**
- [Tarefa da Aula 2 — primeiros nós](../../tutoriais/tarefa-aula02-primeiros-nos.md) — obrigatória, até **domingo 25/10, 23h59**, push na `dev`; vira a estrutura de pacote e o serviço do TP1
- [Desafio 1 — comunicação](../../recursos/desafios/desafio-01-comunicacao.md) — opcional, sem nota, com uma medida para você conferir que entendeu
- **Projeto:** no Infnet.Online até 26/10, diga qual candidato você escolheu — a **leitura do TP1 é na Aula 3 (26/10)** e o enunciado pede o projeto declarado.

## Os três erros que mais aparecem

O campeão absoluto é **"package not found" depois do build**: faltou `source install/setup.bash` *naquele* terminal. Cada aba nova precisa do source, e isso não muda nunca — vale colocar no `~/.bashrc` o source do ROS, mas o do workspace é melhor manter manual, para você lembrar de qual workspace está usando.

O segundo é **editar Python e nada mudar**: sem `--symlink-install` no `colcon build`, o código instalado é uma cópia. Com a flag, é um link, e a edição vale na hora.

O terceiro é **renomear pacote pela metade**: o nome precisa bater em quatro lugares — `package.xml`, `setup.py`, `resource/<nome_do_pacote>` e `setup.cfg` —, e a edição é sempre em `src/`. O `setup.cfg` é o mais esquecido, e é ele que faz o `ros2 launch` reclamar de `libexec directory .../lib/<pacote> does not exist`. O passo a passo com a sequência de comandos está em [renomear um pacote ROS 2](../../tutoriais/renomear-pacote-ros2.md).

Quem replicou durante a aula: `git add . && git commit -m "Aula 2: pacote de comunicação compilando" && git push` antes de sair. Quem não, o push vem com a tarefa — até domingo.
