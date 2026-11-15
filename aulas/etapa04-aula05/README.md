# Aula 5 — A mensagem do seu projeto; e a tarefa que demora, avisa e pode ser cancelada

**Segunda, 16/11/2026 · Zoom · 1h30 · Etapa 4 · turma live**

[:material-file-pdf-box: Slides da Aula 5 (PDF)](apresentacao-aula05.pdf){ .md-button .md-button--primary }
[:material-book-open-variant: Guia de estudo da Aula 5](../../tutoriais/estudo-aula05-acoes.md){ .md-button }
[:material-clipboard-check: Tarefa: interfaces](../../tutoriais/tarefa-aula04-interfaces.md){ .md-button }
[:material-clipboard-check: Tarefa: ações](../../tutoriais/tarefa-aula05-acoes.md){ .md-button }
[:material-code-tags: Exemplo `aula07-acoes`](../../exemplos/aula07-acoes/index.md){ .md-button }

## Como esta página funciona

A aula **demonstra**; a tarefa **executa**. Durante o encontro o professor roda tudo no repositório dele (`pb-live-dacioms`) e você observa e anota. Esta página guarda o que foi mostrado, na ordem dos slides, e termina em [A tarefa da semana](#a-tarefa-da-semana), que é o que você roda no **seu** ambiente.

Sobre os blocos de comando: cada bloco diz, na primeira linha, **em qual terminal** ele roda, e pode ser **colado inteiro de uma vez**. Quando um comando ocupa o terminal (um `launch`, o cliente da ação), ele é o último do bloco. Abaixo de cada bloco, **Tem de aparecer** diz o que você deve ver.

## Cenas dos últimos episódios

**O que a Aula 4 deixou.** O TP1 conferido com quatro perguntas ao sistema (quem está no ar, o que ele vê, o que responde, a que taxa); três casos resolvidos — o projeto com domínio declarado, o `/vision/status` no vocabulário do domínio, a resposta gravada em arquivo —; a taxa corrigida de 5 Hz para 15 Hz com o perfil do Fast DDS; e a entrega em quatro linhas (`main`, `entrega-tp1`, a tag e o Moodle). Sobrou um incômodo: o `2` continua preso **dentro de uma frase**. A solução dele — as interfaces próprias — **não coube na Aula 4**, e por isso é o primeiro bloco de hoje.

**As peças antigas que voltam hoje.**

| Peça | De onde vem | Onde entra hoje |
|---|---|---|
| Pacote `ament_python` | Aula 2 | ele ganha um vizinho, só de definições |
| Todo tópico tem um **tipo** | Aula 2 | o tipo passa a ser seu |
| Serviço: pergunta com resposta | Aula 2 | hoje se vê onde ele deixa de servir |
| `source install/setup.bash` em cada terminal | Aula 2 | é ele que decide se a interface existe |
| Parâmetro fora do código | Aula 3 | a classe procurada entra pelo launch |
| Oclusão | Aula 3 | ela aparece também como confiança caindo |

## A ideia em uma frase

Hoje o seu sistema **ganha vocabulário próprio** — e aprende a fazer uma coisa que demora: avisando do progresso, e aceitando ser interrompido.

## O que você sai sabendo hoje, e o que isso vale no seu projeto

| Você sai sabendo | No seu projeto, isso vale |
|---|---|
| Dizer quando um tipo pronto basta, e quando o projeto precisa do próprio | a mensagem passa a dizer "2 tampas azuis", e não "2" |
| Ler os arquivos de um pacote de interfaces (`.msg`, `.srv`, `.action`) | é o contrato que o seu detector treinado vai reaproveitar |
| Compilar na ordem, e ler os três erros de quem erra a ordem | uma semana sem ficar travado no `source` |
| Escolher entre tópico, serviço e ação | cada tarefa do seu robô cai numa das três |
| Pedir, acompanhar e cancelar uma ação pela linha de comando | é assim que se manda um robô fazer algo que demora — e que se testa a ação do seu projeto |

## O que foi demonstrado, onde está na tarefa, e quando vence

Os gates e as datas são **referência para consulta** — estão em [Gates de cada TP](../../recursos/gates-tps.md); as datas do TP2 desta turma saem com o enunciado, na próxima aula.

| Demonstrado na aula | Na tarefa | Referência |
|---|---|---|
| "Dois o quê?": o limite do tipo pronto | parte 1, passo 2 | competência 1.3 |
| Os dois pacotes; as três linhas do `package.xml`; a lista do `CMakeLists.txt` | parte 1, passo 1 | pacote de interfaces do projeto |
| Compilar na ordem; as três mensagens de erro | guia de estudo da Aula 4, seção 2 | — |
| O `/vision/status` com tipo próprio (a migração) | parte 1, passo 3 | `.msg` e `.srv` do domínio · push na `dev` até **dom 22/11** |
| A ação em três partes (`.action`) | parte 2, passo 2 | ação do projeto, definida |
| Três casos: pedir e acompanhar; rejeitar e parar cedo; cancelar | parte 2, passo 1 | push na `dev` até **dom 29/11** |
| Por dentro: dois tópicos e três serviços | desafio | opcional |

## Pegar o material

```bash
# ── Terminal B · uma vez por terminal ─────────────────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"
source /opt/ros/humble/setup.bash

# o material da disciplina (pode repetir sempre: a linha do rm evita o erro de pasta já existente)
rm -rf /tmp/PBRoboticos_live_prof_dacio
git clone --depth 1 https://github.com/Prof-Dacio-INFNET/PBRoboticos_live_prof_dacio.git /tmp/PBRoboticos_live_prof_dacio
ls /tmp/PBRoboticos_live_prof_dacio/exemplos/aula06-interfaces /tmp/PBRoboticos_live_prof_dacio/exemplos/aula07-acoes
```

**Tem de aparecer:** `README.md`, `aula06_percepcao` e `pb_interfaces` na primeira pasta; `README.md` e `aula07_acoes` na segunda. Os nomes das pastas seguem a numeração da turma presencial, de onde os exemplos vieram: `aula06-interfaces` é o exemplo desta turma para interfaces, e `aula07-acoes`, para ações.

## Bloco 1 — A mensagem do seu projeto

### Dois. Dois o quê?

```bash
# ── Terminal B · com o sistema da Aula 3 no ar no Terminal A ──
ros2 topic echo /vision/contagem --once
ros2 interface show std_msgs/msg/Int32
```

**Tem de aparecer:** `data: 2` (ou `data: 1`, se cair no instante em que os dois objetos se encostam: repita); e quatro linhas de comentário — a terceira diz *"It is recommended to create your own semantically meaningful message"* — seguidas de `int32 data`.

Dois de que classe? Com que certeza? Onde na imagem? De que instante? O segmentador conhece a posição, a área e o contorno de cada objeto — e joga tudo fora na hora de publicar, porque o tipo só tem lugar para um inteiro. Não é limite do ROS 2: é escolha de tipo.

**Tipo pronto, tipo próprio — e o atalho que cobra depois.** Tipo pronto (`Int32`, `Trigger`, `Image`) está certo enquanto a pergunta é simples. Tipo próprio vale quando **três ou mais campos andam sempre juntos**; ele custa um pacote a mais, um build a mais, e uma dependência para quem usar o seu nó. O atalho — JSON dentro de uma `String` — funciona, e perde a conferência de tipo, a inspeção (`ros2 interface show`) e o lado C++. Para o seu projeto, a pergunta é: **o que o seu nó sabe sobre cada objeto, e hoje não conta para ninguém?**

### Dois pacotes, lado a lado

```text
ros2_ws/src/
|-- pb_interfaces/                   ament_cmake: SÓ definições, nenhum nó
|   |-- msg/Deteccao.msg
|   |-- msg/Deteccoes.msg
|   |-- srv/StatusVisao.srv
|   |-- action/VarrerCena.action     o assunto do bloco 2
|   |-- CMakeLists.txt               a lista do que gerar
|   `-- package.xml                  as três linhas do rosidl
`-- aula06_percepcao/                ament_python: os nós, como desde a Aula 2
    |-- aula06_percepcao/detector.py
    |-- aula06_percepcao/monitor.py
    `-- package.xml                  <depend>pb_interfaces</depend>
```

Gerar interface é **gerar código**: o ROS 2 lê o arquivo de texto e escreve as classes em Python e em C++. Quem faz isso é o `rosidl`, que roda num pacote `ament_cmake` — o pacote Python dos seus nós não tem essa maquinaria. É assim que o `sensor_msgs` chega até você.

Três linhas do `package.xml` fazem o pacote gerar código (sem elas ele compila, não reclama, e não gera nada), e cada arquivo novo ganha uma linha na lista do `CMakeLists.txt`:

```xml
<buildtool_depend>rosidl_default_generators</buildtool_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```

```cmake
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Deteccao.msg"
  "msg/Deteccoes.msg"
  "srv/StatusVisao.srv"
  "action/VarrerCena.action"
  DEPENDENCIES std_msgs action_msgs
)
```

### Uma detecção, o quadro inteiro, e a mesma pergunta com vocabulário próprio

```text
# msg/Deteccao.msg -- uma detecção individual
string  classe       # rótulo do SEU domínio: "tomate_maduro", "vaga_livre", "peca_ok"
float32 confianca    # 0.0 a 1.0 -- quanto o detector acredita nisso
int32   x            # centro do objeto, em pixels da imagem
int32   y
int32   area         # área em pixels: separa objeto de respingo

# msg/Deteccoes.msg -- o que a percepção viu em UM quadro
std_msgs/Header header        # stamp: QUANDO · frame_id: em que referencial
Deteccao[]      deteccoes     # array de tamanho variável de outra mensagem SUA
uint32          total

# srv/StatusVisao.srv -- acima dos três traços, a pergunta (vazia); abaixo, a resposta
---
bool    ativo
string  classe_alvo
uint32  total_detectado
float32 confianca_media
string  mensagem
```

Tipo, nome e comentário — e mensagens se compõem: um campo pode ser outra mensagem sua, e `[]` faz o array. O `Header` não é enfeite: sem o `stamp` não se sabe se a detecção é de agora ou de três segundos atrás. No serviço, os três traços separam a pergunta da resposta: o `Trigger` do TP1 dizia "estou vivo"; o `StatusVisao` diz **o que** está sendo visto — e o `2` que estava preso na frase agora é `total_detectado`.

### Copiar e compilar, na ordem

```bash
# ── Terminal B · herda as variáveis de "Pegar o material" · UMA LINHA POR VEZ a partir do colcon ──
: "${PB_WS:?defina PB_USER, PB_DIR e PB_WS — o bloco está em Pegar o material}"
M=/tmp/PBRoboticos_live_prof_dacio/exemplos
cp -r "$M/aula06-interfaces/pb_interfaces" "$M/aula06-interfaces/aula06_percepcao" "$M/aula07-acoes/aula07_acoes" "$PB_WS/src/"
cd "$PB_WS"
colcon build --packages-select pb_interfaces
source install/setup.bash
colcon build --packages-select aula06_percepcao aula07_acoes --symlink-install
source install/setup.bash
ros2 interface list | grep pb_interfaces
```

**Tem de aparecer:** `Finished <<< pb_interfaces [14.9s]` (de dez a quinze segundos: é o CMake escrevendo código Python e C++); `Summary: 2 packages finished`; e cinco linhas na lista — `msg/ComandoMovimento`, `msg/Deteccao`, `msg/Deteccoes`, `srv/StatusVisao` e `action/VarrerCena`. O `source` do meio é o que faz os outros pacotes enxergarem o primeiro. São três pacotes: o terceiro (`aula07_acoes`) é o servidor da ação do bloco 2.

**Três mensagens, e o que cada uma pede:**

| A mensagem | O que aconteceu | O que fazer |
|---|---|---|
| `Check that the following packages have been built: - pb_interfaces` | os nós foram compilados **antes** das interfaces | compile `pb_interfaces`, dê `source`, compile os nós |
| `Package 'aula06_percepcao' not found ... searching: ['.../install/aula03_visao', '/opt/ros/humble']` | este terminal fez o `source` **antes** do build — a lista mostra onde ele procurou | `source "$PB_WS/install/setup.bash"` neste terminal |
| `ModuleNotFoundError: No module named 'pb_interfaces'` | o nó importa a interface, mas o terminal é antigo — ou falta `<depend>pb_interfaces</depend>` no `package.xml` dos nós | terminal novo, com os dois `source`; confira o `package.xml` |

### Rodar, e ler a mensagem nova

```bash
# ── Terminal A · o launch ocupa o terminal ────────────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"
source /opt/ros/humble/setup.bash
source "$PB_WS/install/setup.bash"
ros2 launch aula06_percepcao percepcao.launch.py classe:=tomate_maduro
```

**Tem de aparecer:** `detector no ar - classe='tomate_maduro'` e, em seguida, uma linha do monitor por quadro: `t=...  total=2  tomate_maduro(0.98) em (261,333) area=1450 | tomate_maduro(0.99) em (512,216) area=3524`. Cada linha é uma mensagem: a classe, a confiança, a posição e a área de cada objeto — tudo o que o `Int32` jogava fora.

```bash
# ── Terminal B · com o Terminal A no ar ───────────────
ros2 topic echo /vision/deteccoes --once
ros2 service type /vision/status
ros2 service call /vision/status pb_interfaces/srv/StatusVisao "{}"
```

**Tem de aparecer:** o `header`, o array `deteccoes` com dois itens e `total: 2`; depois `pb_interfaces/srv/StatusVisao`; e por fim `ativo=True, classe_alvo='tomate_maduro', total_detectado=2, confianca_media=0.98..., mensagem="vendo 2 'tomate_maduro' na cena"`. O **nome** do serviço é o mesmo do TP1; o que mudou foi o **tipo**. Isso é uma migração, e é o coração da parte 1 da tarefa.

Quando os dois objetos vermelhos se encostam, o monitor mostra `total=1  tomate_maduro(0.89) em (450,290) area=4965`: a contagem cai e a área é a soma das duas; a confiança costuma cair (fica entre 0,85 e 0,98, conforme o quanto eles se sobrepõem). Há uma segunda oclusão na cena, que o `Int32` **não mostrava**: quando o objeto azul passa na frente de um vermelho, a contagem continua `total=2`, mas a linha vira `tomate_maduro(0.75) ... area=2167` — a área encolhe e a confiança cai, e quem recebe a mensagem sabe que um objeto está encoberto. A confiança deste exemplo é a solidez do contorno (a área dividida pela área do fecho convexo), e não uma probabilidade. Um detector treinado usa a **mesma** mensagem: trocar o miolo sem trocar o contrato é a razão de a interface vir antes do detector.

## Bloco 2 — Quando a resposta demora: ações

### Três formas de conversar, e onde cada uma quebra

| Forma | O que é | Serve para | Onde quebra |
|---|---|---|---|
| **Tópico** | um fluxo; quem publica não sabe quem ouve | "o que você está vendo agora?" | quando alguém precisa de uma resposta |
| **Serviço** | pergunta e resposta; quem chama fica **esperando** | "qual o seu estado?" | quando a resposta demora: quem chamou fica no escuro, e não pode desistir |
| **Ação** | um objetivo, o progresso **durante**, um resultado no fim — e pode ser cancelada | "varra a cena por 30 segundos", "vá até a doca 3" | quando a tarefa é instantânea: vira cerimônia |

A regra prática: respondeu em menos de um segundo, é serviço. Demora, e faz sentido interromper, é ação. É a forma que descreve quase tudo o que um robô faz.

### Uma ação tem três partes

```text
# pb_interfaces/action/VarrerCena.action
# ---------- Goal: o que se pede ----------
float32 duracao_s          # por quanto tempo observar
string  classe_alvo        # o que procurar
uint32  minimo_para_parar  # 0 = observa a duração inteira; N = termina cedo ao ver N
---
# ---------- Result: o que volta no fim ----------
uint32  total_visto
float32 confianca_media
uint32  quadros_analisados
string  resumo
---
# ---------- Feedback: o que volta DURANTE ----------
float32 decorrido_s
uint32  vistos_ate_agora
float32 progresso          # 0.0 a 1.0
```

O serviço tinha um separador; a ação tem dois. O objetivo diz o que se pede — e já traz uma condição para parar cedo. O resultado diz o que ficou sabendo, e não só "deu certo". O feedback é o que muda durante.

A ação **não ganha pacote novo**: o pacote de interfaces do projeto cresce. O arquivo entra na mesma lista do `CMakeLists.txt`, e o `action_msgs` entra nos dois lugares (`find_package` e `DEPENDENCIES` no `CMakeLists.txt`; `<depend>` no `package.xml`), como o `std_msgs` entrou por causa do `Header`.

### O servidor no ar — e a ação, sem escrever cliente nenhum

```bash
# ── Terminal A · Ctrl+C no launch anterior, e então (ocupa o terminal) ──
: "${PB_WS:?defina PB_USER, PB_DIR e PB_WS — o bloco está em Rodar, e ler a mensagem nova}"
source "$PB_WS/install/setup.bash"
ros2 launch aula07_acoes varredura.launch.py classe:=tomate_maduro
```

**Tem de aparecer:** `servidor da action 'varrer_cena' no ar` e `detector no ar - classe='tomate_maduro'`. Este launch sobe a percepção **e** o servidor da ação.

```bash
# ── Terminal B · espere uns cinco segundos depois do launch ──
ros2 action list -t
ros2 action info /varrer_cena -t
ros2 interface show pb_interfaces/action/VarrerCena
```

**Tem de aparecer:** `/varrer_cena [pb_interfaces/action/VarrerCena]`; `Action clients: 0` e `Action servers: 1`, com `/servidor_varredura` embaixo; e o arquivo da ação, com as três partes. Se vier `Action servers: 0`, foi cedo demais: repita. O `ros2 action` é primo do `ros2 topic` e do `ros2 service` — e é com ele que você vai testar a ação do seu projeto, antes de escrever uma linha de cliente.

### Caso 1 — pedir, e acompanhar enquanto acontece

```bash
# ── Terminal B · com o Terminal A no ar ───────────────
ros2 action send_goal /varrer_cena pb_interfaces/action/VarrerCena \
  "{duracao_s: 6.0, classe_alvo: 'tomate_maduro', minimo_para_parar: 0}" --feedback
```

**Tem de aparecer**, nesta ordem: `Goal accepted with ID: ...`; uns trinta blocos `Feedback:` (cinco por segundo), com `decorrido_s` e `progresso` subindo; e, no fim, `Result:` com `total_visto: 2`, `quadros_analisados: 90` e `resumo: varredura completa de 6.0s`, seguido de `Goal finished with status: SUCCEEDED`.

Três momentos que só a ação tem: o objetivo **aceito**, o feedback chegando **durante**, e o resultado no fim, com um estado. Sem o `--feedback`, a mesma chamada parece um serviço lento: seis segundos de silêncio e uma resposta.

### Caso 2 — o servidor diz não; e termina cedo quando já viu o bastante

```bash
# ── Terminal B · com o Terminal A no ar ───────────────
ros2 action send_goal /varrer_cena pb_interfaces/action/VarrerCena \
  "{duracao_s: 999.0, classe_alvo: 'tomate_maduro', minimo_para_parar: 0}"
ros2 action send_goal /varrer_cena pb_interfaces/action/VarrerCena \
  "{duracao_s: 30.0, classe_alvo: 'tomate_maduro', minimo_para_parar: 2}"
```

**Tem de aparecer:** no primeiro, `Goal was rejected.` — e, no Terminal A, `objetivo REJEITADO: duracao_s=999.0 fora de (0, 120]`. No segundo, quase na hora, `resumo: 'parou cedo: viu 2 (minimo 2) em 0.0s'` e `Goal finished with status: SUCCEEDED`.

Rejeitado é diferente de falhou: o servidor olhou o pedido e disse não, antes de gastar um segundo. E tarefa longa não é tarefa de duração fixa: ela termina quando o objetivo foi atingido. No seu projeto: o que o seu servidor deveria recusar? E quando ele já pode parar?

### Caso 3 — cancelar no meio, e receber o resultado parcial

```bash
# ── Terminal B · o cliente ocupa o terminal; depois de uns cinco segundos, Ctrl+C UMA vez ──
ros2 run aula07_acoes cliente_varredura --ros-args -p duracao_s:=30.0 -p classe_alvo:=tomate_maduro
```

**Tem de aparecer:** `objetivo aceito - acompanhando (Ctrl+C cancela)` e uma linha de feedback a cada 0,2 s (`... 4.6s  progresso=15%  vistos=2`). Depois do `Ctrl+C`: `pedindo cancelamento...` e `RESULTADO: total_visto=2  confianca_media=0.98  quadros=72  |  cancelada em 4.8s`. No Terminal A: `cancelamento pedido - aceitando` e `varredura CANCELADA em 4.8s`.

O `Ctrl+C` no cliente não mata a tarefa: ele **pede** o cancelamento, o servidor decide aceitar, para, e devolve o que já sabia. Um robô com o braço no meio de um movimento pode precisar recolher antes de parar — por isso cancelar é um pedido, e não um corte de energia. **Um servidor que não consegue ser interrompido não é uma ação: é um serviço lento com mais código.**

!!! note "E o `Ctrl+C` no `ros2 action send_goal`?"
    Ele também pede o cancelamento (`Canceling goal...` e, depois, `Goal finished with status: CANCELED`). Mas, no Humble, a ferramenta tem uma corrida: de vez em quando — no ensaio, em 3 de 14 tentativas — o `Ctrl+C` não cancela, e a tarefa segue até o prazo. Para demonstrar cancelamento, use o cliente do exemplo.

### Por dentro, uma ação é feita de peças que você já conhece

```bash
# ── Terminal B · com o Terminal A no ar ───────────────
ros2 topic list --include-hidden-topics | grep varrer
ros2 service list --include-hidden-services | grep varrer
```

**Tem de aparecer:** dois tópicos (`/varrer_cena/_action/feedback` e `/varrer_cena/_action/status`) e três serviços (`.../cancel_goal`, `.../get_result` e `.../send_goal`).

Enviar o objetivo, pedir o resultado e cancelar são serviços; o feedback e o estado são tópicos. A ação não é mágica nova: é a Aula 2 organizada para a tarefa que demora.

### Quatro fins possíveis — e a pergunta para o seu projeto

| Fim | O que significa | Onde apareceu |
|---|---|---|
| `SUCCEEDED` | concluiu — no prazo, ou antes, porque o objetivo foi atingido | casos 1 e 2 |
| `CANCELED` | quem pediu desistiu, e o servidor aceitou parar | caso 3 |
| `ABORTED` | o **servidor** desistiu — aqui, quando fica sem percepção por três segundos | guia de estudo, seção 2 |
| rejeitado | nem começou: o pedido não fazia sentido, ou já havia uma varredura em curso | caso 2 |

**No seu projeto: qual tarefa leva mais de um segundo, e faz sentido interromper?**

| Domínio | Uma ação plausível |
|---|---|
| inspeção de peças | inspecionar um lote até achar N refugos, ou esgotar a esteira |
| estacionamento | varrer o pátio e mapear as vagas livres |
| agricultura | percorrer a fileira contando frutos maduros |
| segurança | monitorar a área por N minutos e relatar intrusões |
| logística | seguir uma rota de coleta e reportar o progresso |

Se a sua tarefa **não** tem como ser interrompida de forma útil, ela provavelmente é um serviço — diga isso no relatório, e escolha outra para a ação.

## A tarefa da semana

A tarefa tem duas partes, **nesta ordem**: a ação do seu projeto mora no pacote de interfaces que você cria na parte 1.

### Parte 1 — as interfaces do seu projeto

[Tarefa da Aula 4 — as interfaces do seu projeto](../../tutoriais/tarefa-aula04-interfaces.md), com o [guia de estudo da Aula 4](../../tutoriais/estudo-aula04-interfaces.md) antes dela. **O que fazer:** o seu pacote de interfaces, com um `.msg` e um `.srv` do seu domínio, e o `/vision/status` migrado para o tipo novo. **O que usar:** o `pb_interfaces` do exemplo, copiado e renomeado (o bloco da tarefa faz os três lugares). **Como adequar:** troque o vocabulário, e acrescente o campo que só o seu domínio pede. **Como saber que terminou:** `ros2 interface list` mostra o seu pacote, e `ros2 service type /vision/status` mostra o tipo novo. Push na `dev` até domingo, 22/11.

### Parte 2 — a ação do seu projeto: usada, e depois definida

[Tarefa da Aula 5 — a ação do seu projeto](../../tutoriais/tarefa-aula05-acoes.md), com o [guia de estudo da Aula 5](../../tutoriais/estudo-aula05-acoes.md) antes dela. **O que fazer:** rodar os três casos de hoje no seu ambiente, e escrever o `.action` do **seu** projeto. **O que usar:** o exemplo `aula07-acoes`, e o pacote de interfaces da parte 1. **Como adequar:** objetivo com parada antecipada, resultado que informa, feedback com uma medida do seu domínio. **Como saber que terminou:** `ros2 interface show` mostra a sua ação, com as três partes. Push na `dev` até domingo, 29/11 — e vale chegar à próxima aula com os três casos já rodados.

O **servidor** da sua ação fica para depois da próxima aula: esta semana é usar a do exemplo e **definir** a sua.

### Desafio (opcional): a ação por dentro, medida

Se o feedback é um tópico, dá para medir a taxa dele. Com o launch da varredura no ar no Terminal A:

```bash
# ── Terminal B · o cliente ocupa o terminal por vinte segundos ──
ros2 run aula07_acoes cliente_varredura --ros-args -p duracao_s:=20.0 -p classe_alvo:=tomate_maduro
```

```bash
# ── Terminal C · enquanto o cliente roda (encerra sozinho em 8 s) ──
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"
source /opt/ros/humble/setup.bash
source "$PB_WS/install/setup.bash"
timeout 8 ros2 topic hz /varrer_cena/_action/feedback
```

Duas perguntas, as duas respondidas medindo: **(1)** quantos feedbacks por segundo o servidor publica, e de qual linha do `servidor_varredura.py` vem esse número? **(2)** Cancele três objetivos e compare, no log do Terminal A, o horário da linha `cancelamento pedido` com o da linha `CANCELADA`: qual foi o maior atraso, e por que ele nunca passa de um certo valor? Traga os dois números na próxima aula.

## Socorro rápido

| Sintoma | O que fazer |
|---|---|
| `Check that the following packages have been built: - pb_interfaces` | compile as interfaces primeiro, dê `source`, e só então os nós |
| `Package 'aula07_acoes' not found` (ou `aula06_percepcao`) | faltou o `source "$PB_WS/install/setup.bash"` **neste** terminal, depois do build |
| `The passed action type is invalid` no `send_goal` | é o terminal, e não a ação: `ros2 action list` funciona porque pergunta ao grafo, mas o `send_goal` precisa importar o tipo. `source "$PB_WS/install/setup.bash"` neste terminal |
| `Waiting for an action server to become available...`, e nada | o servidor não está no ar: confira o Terminal A e `ros2 action list` |
| `Action servers: 0` no `ros2 action info` | foi cedo demais depois do launch: espere cinco segundos e repita |
| `Goal was rejected.` num pedido válido | já existe uma varredura em curso (o servidor aceita uma por vez): espere a anterior terminar |
| `Failed to populate message fields` | o nome de um campo do objetivo está errado: confira com `ros2 interface show pb_interfaces/action/VarrerCena` |
| `Goal finished with status: ABORTED`, com `percepcao muda` no resumo | o servidor está sem `/vision/deteccoes`: suba pelo launch `varredura.launch.py`, que traz a percepção junto |
| o `Ctrl+C` no `ros2 action send_goal` não cancelou | é a corrida da ferramenta no Humble: a tarefa segue até o prazo. Para cancelar, use o cliente do exemplo |
| o cliente mostra um `Traceback` no `Ctrl+C` | você está com a versão antiga do exemplo: refaça o [Pegar o material](#pegar-o-material) e copie `aula07_acoes` de novo |
| `ros2 service type /vision/status` mostra dois tipos | o launch da Aula 3 e o da Aula 5 estão no ar ao mesmo tempo: feche o antigo |

Travou, e nada aqui bate? **Infnet.Online**, com três coisas: o comando exato, a saída completa e o passo em que você está.

## Próximo encontro: Aula 6, segunda 23/11

**Ações a fundo, e a leitura do TP2.** O servidor por dentro — como ele aceita, recusa, publica o progresso e obedece ao cancelamento, e por que duas linhas decidem se ele ouve ou fica surdo — e o enunciado do TP2, que junta a mensagem, o serviço e a ação do seu projeto.
