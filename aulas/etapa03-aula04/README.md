# Aula 4 — Clínica do TP1; e as interfaces do seu projeto

**Segunda, 09/11/2026 · Zoom · 1h30 · Etapa 3 (aula única) · turma live**

[:material-file-pdf-box: Slides da Aula 4 (PDF)](apresentacao-aula04.pdf){ .md-button .md-button--primary }
[:material-package-variant-closed: Checklist de entrega do TP1](../../tutoriais/checklist-entrega-tp1.md){ .md-button }
[:material-book-open-variant: Guia de estudo da Aula 4](../../tutoriais/estudo-aula04-interfaces.md){ .md-button }
[:material-code-tags: Exemplo `aula06-interfaces`](../../exemplos/aula06-interfaces/index.md){ .md-button }

!!! danger "O TP1 vence nesta sexta, 13/11"
    Esta é a **única aula da Etapa 3** e a **última antes da entrega**. A primeira metade de hoje é clínica: medir onde o seu TP1 está, fechar o que falta, escrever o relatório e **ensaiar a entrega inteira**. O conteúdo novo vem depois — e ele é do TP2, não do TP1. Se tiver que escolher onde prestar atenção hoje, escolha a primeira metade.

## Cenas dos últimos episódios

A Aula 3 leu o TP1 e mostrou o pipeline `câmera → segmentação → contagem → serviço`. A Parte A da tarefa (dom 01/11) deixou o pacote **seu** compilando, a taxa medida e o `PROJETO.md` com o G1.1 declarado; a Parte B (dom 08/11, a semana sem aula) deixou as **duas classes** do seu domínio, os parâmetros em YAML, o `/vision/status` com domínio, a oclusão registrada e as evidências em `docs/evidencias/aula03/`. Hoje tudo isso vira entrega — e, na segunda metade, ganha um vocabulário próprio.

## Como a aula de 1h30 funciona

Hoje tem duas aulas dentro de uma. **Clínica do TP1** (até o minuto 40): censo de gates pelo chat, os três bloqueios mais comuns resolvidos na tela do professor, o relatório em cinco perguntas, o ensaio da entrega e duas telas compartilhadas. **Interfaces próprias** (do minuto 40 ao 80): o conteúdo em linhas gerais, com o exemplo rodando de ponta a ponta no repositório do professor. Fechamento (10 min): o que acontece até sexta, e depois dela. Ninguém instala nem compila durante a aula; o [guia de estudo](../../tutoriais/estudo-aula04-interfaces.md) tem a saída esperada de cada comando.

## Conferência (8 min) — onde o seu TP1 está

Ponto de controle no chat, nesta ordem, rodado no **seu** repositório:

```bash
# ── uma vez por terminal ──────────────────────────────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"

cd "$PB_DIR"
grep -c "PB:PROJETO\|PB:TRILHA" PROJETO.md            # G1.1 — espera-se 2
grep -o "\[x\] G1\.[0-6]" PROJETO.md | tr '\n' ' '   # quais gates você já marcou
ls docs/evidencias/aula03/ docs/evidencias/tp1/ 2>&1  # a prova de tudo isso
```

Cole as três saídas. Quem está sem ambiente ou sem repositório escreve o sintoma — e, hoje, a resposta é a **escada de recuperação** do [checklist de entrega](../../tutoriais/checklist-entrega-tp1.md#escada-de-recuperacao-se-algo-nao-vai-dar-tempo): entregue o que funciona e **declare** o que não funciona.

## Parte 1 — Clínica do TP1 (até o minuto 40)

### Os três bloqueios que mais aparecem — e a cura de cada um

**Projeto com uma classe só (G1.1).** É o mais grave e o mais rápido de resolver: quinze minutos de conversa fecham. Uma classe esconde o problema interessante; o domínio define as duas (tampa azul × verde, maduro × verde, capacete × colete). Sem câmera, a cena sintética editada vale para o TP1 inteiro — e você diz isso no relatório.

**`/vision/status` genérico (G1.4).** O serviço do exemplo responde `"2 objeto(s) no ultimo frame"`. O seu precisa falar a língua do domínio: `"pomar setor 3: 2 maduros, 5 verdes, taxa 12.4 Hz"`. É uma função de dez linhas, e o [gabarito está no guia da Aula 3](../../tutoriais/estudo-aula03-visao.md#3-anatomia-do-codigo-os-cinco-arquivos-40-min).

**Evidência que ficou no terminal.** O mais comum e o mais barato: rode o comando de novo e redirecione para arquivo. **O terminal fecha; o repositório fica.**

```bash
# ── herda PB_USER, PB_DIR e PB_WS do bloco acima ──
: "${PB_WS:?defina PB_USER, PB_DIR e PB_WS — o bloco está no topo desta página}"
cd "$PB_DIR" && mkdir -p docs/evidencias/tp1
bash scripts/check-ambiente.sh                        > docs/evidencias/tp1/check-ambiente.txt   # G1.0
cp docs/evidencias/aula03/taxas.md                      docs/evidencias/tp1/topic-hz.txt          # G1.2
cp docs/evidencias/aula03/pipeline.png                  docs/evidencias/tp1/segmentacao.png       # G1.3
cp docs/evidencias/aula03/grafo.png                     docs/evidencias/tp1/rqt_graph.png         # G1.4
ros2 service call /vision/status std_srvs/srv/Trigger "{}" > docs/evidencias/tp1/status.txt       # G1.4 (pipeline no ar)
git add -A && git commit -m "G1.4: evidencias do TP1 em docs/evidencias/tp1" && git push origin dev
```

### A oclusão, se você ainda não registrou

É o único item do TP1 que produz uma **observação** em vez de um funcionamento. Com o pipeline no ar e `ros2 topic echo /vision/contagem` rodando, espere (ou provoque) os dois objetos se encostarem: a contagem cai e volta. O que se escreve no relatório é a interpretação — em que ponto o detector deixou de separar os objetos, por que a área combinada não é a soma das áreas, e o que isso significa **no seu domínio**: se dois tomates encostados viram um, a contagem de colheita erra para menos, e isso é uma limitação conhecida, não um bug escondido.

### O relatório é um documento de decisões, não um diário

Quem trava no `docs/relatorios/relatorio-tp1.md` quase sempre tentou narrar o mês. Não é isso. São cinco perguntas, uma seção para cada:

| Seção | A pergunta que ela responde |
|---|---|
| Domínio e derivação | que problema, de quem, e por que este e não outro |
| Decisões técnicas | o que você escolheu e **o que descartou** — fonte de imagem, faixas HSV, `area_min`, QoS |
| Experimento de oclusão | o que aconteceu, e o que isso implica no seu domínio |
| Limitações conhecidas | o que o sistema **não** faz, dito por você antes de ser dito por outro |
| Uso de IA | o que foi gerado, o que foi revisado, o que você sabe explicar |

A seção de limitações é a que mais gente pula e a que mais revela entendimento. Declarar "a segmentação por cor confunde tomate maduro com um pano vermelho ao fundo" mostra que você conhece o seu sistema. Omitir e deixar o avaliador descobrir mostra o contrário. O [checklist de verificação do TP1](../../recursos/tp1.md#checklist-de-verificacao-antes-de-entregar) é o roteiro de releitura.

### Ensaie a entrega hoje, não na sexta

O passo a passo está no [checklist de entrega do TP1](../../tutoriais/checklist-entrega-tp1.md). O resumo: `main` atualizada, branch `entrega-tp1`, tag `tp1` empurrada, ZIP (sem `build/`, `install/`, `log/`, `.git/`) e PDF no Moodle, vídeo de até 5 min público ou não-listado, e **todos os links testados em janela anônima** — você está logado em tudo, na sua máquina tudo abre. A regra é dura de propósito: se o avaliador não consegue abrir, não existe.

**Ponto de controle 2 (chat):** "até sexta me falta: G1.x, G1.y" — ou "nada". É a sua lista, não a minha.

## Parte 2 — Quando a mensagem pronta acaba (minutos 40–65, em linhas gerais)

Olhe o que o seu TP1 publica hoje: `ros2 topic echo /vision/contagem --once` → `data: 2`. Dois. Dois o quê? Com que confiança? Onde na imagem? De que instante? A informação **existe** dentro do seu nó — o segmentador conhece a área, a posição e o contorno de cada objeto — e é **jogada fora** na hora de publicar, porque o tipo escolhido não tem onde guardá-la. Não é limitação do ROS; é escolha de tipo. O tipo pronto serviu enquanto a pergunta era "quantos?"; deixa de servir quando a pergunta vira "quantos, de que classe, com que certeza, e onde?".

!!! tip "A regra prática, para não cair no extremo oposto"
    Interface própria custa: um pacote a mais, um `colcon build` a mais, e uma dependência que todo colaborador precisa compilar antes de rodar o seu nó. Vale a pena quando **três ou mais campos** andam sempre juntos, ou quando você se pega publicando dois tópicos que só fazem sentido lidos ao mesmo tempo. Para um número solto, `Int32` continua sendo a resposta certa. O erro oposto — JSON dentro de `String` — perde checagem de tipo, introspecção (`ros2 interface show`) e compatibilidade com C++: contrato vira convenção que só existe na sua cabeça.

**Por que o pacote de interfaces é separado.** Gerar interface é **gerar código**: o ROS 2 lê o seu `.msg` e produz código C++, Python e headers, e quem faz isso é o `rosidl`, que roda num pacote `ament_cmake`. Um pacote `ament_python` — o tipo dos seus nós desde a Aula 2 — **não tem** essa maquinaria. Daí a arquitetura padrão, sempre a mesma: `<projeto>_interfaces` (`ament_cmake`, só `.msg`/`.srv`/`.action`) ao lado do pacote dos nós (`ament_python`), que depende dele. É exatamente assim que o `sensor_msgs` chega até você. Três linhas do `package.xml` fazem o pacote gerar código — sem elas ele compila e não gera nada, o pior tipo de erro, o silencioso:

```xml
<buildtool_depend>rosidl_default_generators</buildtool_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```

**Anatomia.** Um `.msg` é uma lista de campos — tipo, nome, comentário — e mensagens **compõem**: um campo pode ser outra mensagem sua, e `[]` faz array de tamanho variável. `Deteccao.msg` (classe, confiança, x, y, área) dentro de `Deteccoes.msg` (`Header` + `Deteccao[]` + total). O `Header` não é enfeite: `stamp` diz se a detecção é de agora ou de três segundos atrás — a diferença entre um robô que reage e um que alucina — e `frame_id` é o que permite combinar com outro sensor na Etapa 4. O `.srv` é a mesma ideia com `---` separando pergunta de resposta: `StatusVisao.srv` responde `ativo`, `classe_alvo`, `total_detectado`, `confianca_media`, `mensagem` — o mesmo serviço, no mesmo lugar do grafo, com um vocabulário que pertence ao seu projeto. *Demonstração direta:* `ros2 interface show std_srvs/srv/Trigger` ao lado de `ros2 interface show pb_interfaces/srv/StatusVisao`.

**Onde o serviço deixa de servir.** Quem chama fica bloqueado esperando. Bom para "qual o seu status?"; péssimo para "vá até a bancada e me avise quando chegar". Para tarefa longa, com progresso e cancelamento, existe a **ação** — a Aula 5 (16/11) é inteira sobre ela, e ela é o coração do TP2.

## Parte 3 — Exemplo de ponta a ponta (minutos 65–80)

No repositório do professor (`pb-live-dacioms`), na ordem: copiar os **dois** pacotes → compilar `pb_interfaces` → `source` → compilar `aula06_percepcao` → `ros2 interface show` (o teste de fumaça) → `launch` com `classe:=tomate_maduro` → o `monitor` imprimindo classe, confiança e posição → `echo /vision/deteccoes --once` → `service call` no tipo novo → a oclusão vista pela mensagem nova: a contagem cai **e a confiança cai junto**. **Ponto de controle 3 (quem replicou):** cole a linha do `monitor` ou a resposta do `service call`.

## Baixar o material desta aula

```bash
# ── uma vez por terminal ──────────────────────────────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"

# 1) baixar o material (pode repetir sempre — a linha do rm evita o erro de pasta já existente)
rm -rf /tmp/PBRoboticos_live_prof_dacio
cd /tmp && git clone --depth 1 https://github.com/Prof-Dacio-INFNET/PBRoboticos_live_prof_dacio.git

# 2) copiar os DOIS pacotes desta aula para dentro do SEU projeto
cp -r /tmp/PBRoboticos_live_prof_dacio/exemplos/aula06-interfaces/pb_interfaces \
      /tmp/PBRoboticos_live_prof_dacio/exemplos/aula06-interfaces/aula06_percepcao \
      "$PB_WS/src/"

# 3) compilar no SEU workspace — a ORDEM importa
cd "$PB_WS"
colcon build --packages-select pb_interfaces
source install/setup.bash                     # sem isto o próximo passo falha
colcon build --packages-select aula06_percepcao --symlink-install
source install/setup.bash
ros2 interface show pb_interfaces/msg/Deteccoes             # o teste de fumaça
ros2 launch aula06_percepcao percepcao.launch.py classe:=tomate_maduro   # com o launch da Aula 3 DESLIGADO (mesmo /vision/status)
```

São **dois** pacotes, e a ordem de compilação não é opcional: o pacote de interfaces precisa estar compilado **e** com `source` feito antes de qualquer nó que o importe. Inverter a ordem produz um `ModuleNotFoundError` que não menciona nada disso.

!!! tip "Rode antes de modificar"
    Compile e rode o exemplo **como ele veio**, antes da sua primeira alteração. Quando algo quebrar depois, você sabe que o problema é seu e não do exemplo.

## Até sexta, e depois dela

- **Até sexta 13/11 existe uma coisa só: entregar o TP1.** [Checklist de entrega](../../tutoriais/checklist-entrega-tp1.md) de cima para baixo, num dia em que ainda dá tempo de consertar; relatório fechado até **quarta 11/11** (G1.5).
- [Guia de estudo da Aula 4](../../tutoriais/estudo-aula04-interfaces.md) — **depois** da entrega: 2h a 3h em duas sessões; leituras, o exemplo reproduzido com as saídas esperadas, anatomia dos dois pacotes, autoavaliação.
- [Tarefa da Aula 4 — as interfaces do seu projeto](../../tutoriais/tarefa-aula04-interfaces.md) — **não mexa nela antes de sexta.** Prazo **domingo 22/11, 23h59**, push na `dev`: o seu `<projeto>_interfaces`, o `/vision/status` migrado para um serviço próprio, detecções com classe e confiança. É o começo do TP2 (leitura na Aula 6, 23/11).

## Socorro rápido

| Sintoma | Causa provável |
|---|---|
| `ModuleNotFoundError: No module named 'pb_interfaces'` | faltou compilar o pacote de interfaces, ou faltou `source install/setup.bash` **depois** de compilar — em **todos** os terminais |
| erro de CMake num pacote onde você não escreveu CMake | você tentou gerar interface num pacote `ament_python`. Interfaces vivem em pacote `ament_cmake` separado |
| o pacote compila mas `ros2 interface list` não mostra nada | faltam as três linhas do `package.xml` (`rosidl_default_generators`, `rosidl_default_runtime`, `member_of_group`) |
| `Header` não resolve na compilação | faltou `<depend>std_msgs</depend>` no `package.xml` **e** `DEPENDENCIES std_msgs` no `rosidl_generate_interfaces` |
| campo novo "não existe" num terminal e existe noutro | terminal antigo com `source` velho. Abra um terminal novo — é sempre isto |
| `ros2 service call` reclama do tipo | o tipo agora é `pb_interfaces/srv/StatusVisao`, não `std_srvs/srv/Trigger` — e o launch da Aula 3 não pode estar no ar ao mesmo tempo (mesmo nome, outro tipo). Confira com `ros2 service type /vision/status` |
| a contagem cai quando os objetos se encostam | é o experimento de oclusão. Registre no relatório em vez de "consertar" |
| `/vision/contagem` a 2–8 Hz, `A message was lost!!!` | fragmentação UDP numa máquina só: `ROS_LOCALHOST_ONLY=1` + buffers do kernel ([guia da Aula 3, §2.4](../../tutoriais/estudo-aula03-visao.md#2-reproduza-o-exemplo-passo-a-passo-45-min)) |

Quem replicou durante a aula: `git add . && git commit -m "Aula 4: pacote de interfaces compilando" && git push` antes de sair — na `dev`, sem misturar com a entrega do TP1.

## Próximo encontro: Aula 5, segunda 16/11

**Ações: tarefas longas, feedback e cancelamento** — a terceira forma de comunicação do ROS 2, e a única que serve para o que um robô faz na maior parte do tempo. Abre a Etapa 4 e é o alicerce do TP2 (e do Nav2). Chegue com o TP1 entregue; o pacote de interfaces próprio pode esperar até 22/11.
