# Guia de estudo — Aula 5: ações, pelo lado de quem usa

**Semana de 16/11 a 29/11 · Etapa 4 · turma live.** A aula de 1h30 teve dois blocos: as interfaces próprias e as ações. As interfaces têm o seu próprio guia — o [guia de estudo da Aula 4](estudo-aula04-interfaces.md) — e ele vem **antes** deste. Aqui você reproduz o bloco das ações no seu repositório, e chega pronto à [tarefa da Aula 5](tarefa-aula05-acoes.md). Tempo total: **1h30 a 2h**, numa sessão.

| O quê | Tempo | Resultado |
|---|---|---|
| Seção 1 — ler | 25 min | você sabe dizer quando uma tarefa é tópico, serviço ou ação |
| Seção 2 — reproduzir o exemplo, com as saídas esperadas | 45 min | os três casos da aula rodando no **seu** repositório, mais dois que a aula não mostrou |
| Seção 3 — anatomia: o `.action`, o cliente | 20 min | você sabe ler o arquivo da ação e os quatro momentos do cliente |
| Seção 4 — autoavaliação | 10 min | seis perguntas, com resposta |

!!! tip "Como pedir ajuda"
    No Infnet.Online, com três itens: o **comando exato**, a **saída completa** e o **passo** em que você está. Antes disso, a seção 5 ("Se travar").

---

## Cenas dos últimos episódios

Na Aula 2 você conheceu o tópico (um fluxo) e o serviço (pergunta e resposta), e aprendeu que cada terminal precisa do `source install/setup.bash`. Na Aula 3 o `/vision/status` respondeu com um `Trigger`. Na Aula 5 o professor mostrou as interfaces próprias — o `pb_interfaces`, com `.msg` e `.srv` — e, no mesmo pacote, um terceiro tipo de arquivo: o `.action`, para a tarefa que demora. A ação foi usada em três casos: pedir e acompanhar, ser rejeitado e parar cedo, cancelar no meio. Aqui você repete os três, e acrescenta dois.

Sobre os blocos de comando: cada bloco diz, na primeira linha, em qual terminal roda, e pode ser colado inteiro. Comando que ocupa o terminal é o último do bloco.

## 1. Leia antes (25 min)

| Fonte | O quê | Minutos | Depois você responde |
|---|---|---|---|
| [Página da Aula 5](../aulas/etapa04-aula05/index.md) | Bloco 2 | 10 | onde o serviço quebra; as três partes de uma ação; os quatro fins |
| Docs do Humble — [Understanding actions](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html) | inteiro (é com o `turtlesim`; leia sem rodar) | 10 | o que `ros2 action list`, `info` e `send_goal` fazem |
| [README do exemplo `aula07-acoes`](../exemplos/aula07-acoes/index.md) | até "Os experimentos" | 5 | o que o servidor do exemplo aceita, recusa e devolve |

A ideia que organiza tudo: **uma ação é um objetivo com vida própria.** Ele é aceito ou rejeitado, avisa do progresso enquanto acontece, termina com um resultado e um estado — e pode ser cancelado no meio. Serviço lento não faz nenhuma dessas coisas.

## 2. Reproduza o exemplo, passo a passo (45 min)

Você trabalha **no seu repositório**, na branch `dev`.

**2.1 — Baixar, copiar e compilar.** Se você já fez o guia da Aula 4, o `pb_interfaces` e o `aula06_percepcao` já estão no seu workspace; o bloco copia de novo sem problema, e traz o terceiro pacote.

```bash
# ── Terminal B · uma vez por terminal · UMA LINHA POR VEZ a partir do colcon ──
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"
source /opt/ros/humble/setup.bash

cd "$PB_DIR" && git checkout dev && git pull
rm -rf /tmp/PBRoboticos_live_prof_dacio
git clone --depth 1 https://github.com/Prof-Dacio-INFNET/PBRoboticos_live_prof_dacio.git /tmp/PBRoboticos_live_prof_dacio
M=/tmp/PBRoboticos_live_prof_dacio/exemplos
cp -r "$M/aula06-interfaces/pb_interfaces" "$M/aula06-interfaces/aula06_percepcao" "$M/aula07-acoes/aula07_acoes" "$PB_WS/src/"
cd "$PB_WS"
colcon build --packages-select pb_interfaces
source install/setup.bash
colcon build --packages-select aula06_percepcao aula07_acoes --symlink-install
source install/setup.bash
ros2 interface list | grep pb_interfaces
```

Esperado: `Finished <<< pb_interfaces [14.9s]` (de dez a quinze segundos), `Summary: 2 packages finished`, e cinco interfaces na lista — a última é `pb_interfaces/action/VarrerCena`.

**2.2 — Subir o servidor, e conhecer a ação sem escrever cliente.**

```bash
# ── Terminal A · o launch ocupa o terminal ────────────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"
source /opt/ros/humble/setup.bash
source "$PB_WS/install/setup.bash"
ros2 launch aula07_acoes varredura.launch.py classe:=tomate_maduro
```

Esperado: `servidor da action 'varrer_cena' no ar` e `detector no ar - classe='tomate_maduro'`. O launch sobe **dois** nós: a percepção e o servidor da ação.

```bash
# ── Terminal B · espere uns cinco segundos depois do launch ──
ros2 action list -t
ros2 action info /varrer_cena -t
ros2 interface show pb_interfaces/action/VarrerCena
```

Esperado: `/varrer_cena [pb_interfaces/action/VarrerCena]`; `Action clients: 0` e `Action servers: 1`, com `/servidor_varredura`; e o arquivo da ação, com as três partes separadas por `---`. Se vier `Action servers: 0`, foi cedo demais: repita.

**2.3 — Caso 1: pedir, e acompanhar.**

```bash
# ── Terminal B · com o Terminal A no ar ───────────────
ros2 action send_goal /varrer_cena pb_interfaces/action/VarrerCena \
  "{duracao_s: 6.0, classe_alvo: 'tomate_maduro', minimo_para_parar: 0}" --feedback
```

Esperado: `Goal accepted with ID: ...`; uns trinta blocos `Feedback:`; `Result:` com `total_visto: 2`, `quadros_analisados: 90`, `resumo: varredura completa de 6.0s`; e `Goal finished with status: SUCCEEDED`. Repita **sem** o `--feedback`: seis segundos de silêncio e a mesma resposta — é assim que uma ação parece um serviço lento.

**2.4 — Caso 2: o servidor diz não; e termina cedo.**

```bash
# ── Terminal B · com o Terminal A no ar ───────────────
ros2 action send_goal /varrer_cena pb_interfaces/action/VarrerCena \
  "{duracao_s: 999.0, classe_alvo: 'tomate_maduro', minimo_para_parar: 0}"
ros2 action send_goal /varrer_cena pb_interfaces/action/VarrerCena \
  "{duracao_s: 30.0, classe_alvo: 'tomate_maduro', minimo_para_parar: 2}"
```

Esperado: `Goal was rejected.` (e, no Terminal A, `objetivo REJEITADO: duracao_s=999.0 fora de (0, 120]`); depois `resumo: 'parou cedo: viu 2 (minimo 2) em 0.0s'` e `SUCCEEDED`, quase na hora.

**2.5 — Caso 3: cancelar no meio.**

```bash
# ── Terminal B · o cliente ocupa o terminal; depois de uns cinco segundos, Ctrl+C UMA vez ──
ros2 run aula07_acoes cliente_varredura --ros-args -p duracao_s:=30.0 -p classe_alvo:=tomate_maduro
```

Esperado: `objetivo aceito - acompanhando (Ctrl+C cancela)`, o feedback a cada 0,2 s e, depois do `Ctrl+C`, `pedindo cancelamento...` e `RESULTADO: total_visto=2 ... | cancelada em N.Ns`. No Terminal A: `cancelamento pedido - aceitando` e `varredura CANCELADA em N.Ns`. O resultado parcial voltou: o servidor parou porque **aceitou** parar.

**2.6 — O que a aula não mostrou: dois objetivos ao mesmo tempo.**

```bash
# ── Terminal B · o cliente ocupa o terminal por vinte segundos ──
ros2 run aula07_acoes cliente_varredura --ros-args -p duracao_s:=20.0 -p classe_alvo:=tomate_maduro
```

```bash
# ── Terminal C · enquanto o cliente do Terminal B ainda roda ──
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"
source /opt/ros/humble/setup.bash
source "$PB_WS/install/setup.bash"
ros2 action info /varrer_cena
ros2 action send_goal /varrer_cena pb_interfaces/action/VarrerCena "{duracao_s: 3.0, classe_alvo: 'tomate_maduro', minimo_para_parar: 0}"
```

Esperado: `Action clients: 1`, com `/cliente_varredura`; e `Goal was rejected.` — no Terminal A, `objetivo REJEITADO: ja existe uma varredura em curso`. O servidor do exemplo aceita **um objetivo por vez**: um robô tem um braço só, e descobrir isso na hora é melhor do que descobrir por comportamento estranho.

**2.7 — O que a aula não mostrou: o servidor desiste sozinho.**

```bash
# ── Terminal A · Ctrl+C no launch, e então só o servidor, SEM a percepção (ocupa o terminal) ──
ros2 run aula07_acoes servidor_varredura
```

```bash
# ── Terminal B · com o servidor sozinho no ar ─────────
ros2 action send_goal /varrer_cena pb_interfaces/action/VarrerCena "{duracao_s: 20.0, classe_alvo: 'tomate_maduro', minimo_para_parar: 0}"
```

Esperado, depois de uns três segundos: `resumo: 'abortada: percepcao muda ha mais de 3.0s'` e `Goal finished with status: ABORTED` — no Terminal A, em vermelho, `varredura ABORTADA: sem percepcao ha mais de 3.0s`. **Cancelar** é decisão de quem pediu; **abortar** é decisão do servidor, quando a tarefa deixou de ser possível. Varrer a cena sem imagem não é uma varredura ruim: é uma varredura que não está acontecendo.

**2.8 — O erro do terminal, de propósito.** Abra um terminal novo e faça **só** `source /opt/ros/humble/setup.bash` (sem o do workspace). `ros2 action list -t` funciona — ele pergunta ao grafo. Mas o `send_goal` responde `The passed action type is invalid`: ele precisa **importar** o tipo, e este terminal não sabe onde ele está. A cura é o `source "$PB_WS/install/setup.bash"`.

## 3. Anatomia (20 min)

**`pb_interfaces/action/VarrerCena.action`.** Três partes, dois separadores. **Objetivo** (`duracao_s`, `classe_alvo`, `minimo_para_parar`): o que se pede — e o pedido já traz a condição para parar cedo. **Resultado** (`total_visto`, `confianca_media`, `quadros_analisados`, `resumo`): o que ficou sabendo; repare que ele volta **também** quando a ação é cancelada ou abortada, com o que deu para saber. **Feedback** (`decorrido_s`, `vistos_ate_agora`, `progresso`): o que muda durante.

**O que muda no pacote de interfaces.** O arquivo entra na lista do `rosidl_generate_interfaces`, e o `action_msgs` entra em três linhas: `find_package(action_msgs REQUIRED)` e `DEPENDENCIES ... action_msgs` no `CMakeLists.txt`, e `<depend>action_msgs</depend>` no `package.xml`. Nada de pacote novo: o pacote de interfaces do projeto **cresce**.

**`aula07_acoes/cliente_varredura.py` — o cliente, em quatro momentos.** Localize no arquivo: `ActionClient(self, VarrerCena, 'varrer_cena')` e o `wait_for_server` (ele espera dez segundos e desiste com uma mensagem útil); `send_goal_async(objetivo, feedback_callback=self.ao_feedback)` — enviar não bloqueia, e o feedback chega numa função sua; em `ao_responder`, o `gh.accepted` (**rejeitado** é diferente de **falhou**) e o `get_result_async()`; em `ao_terminar`, o resultado; e em `cancelar`, o `cancel_goal_async()`. No `main`, repare no `SignalHandlerOptions.NO`: por padrão o `rclpy` desliga tudo ao receber `Ctrl+C`, e um cliente desligado não consegue acompanhar o cancelamento — por isso este cliente trata o `Ctrl+C` por conta própria.

**`aula07_acoes/servidor_varredura.py` — só o mapa, por enquanto.** O servidor tem três funções, uma para cada decisão: aceitar ou rejeitar o objetivo, aceitar ou recusar o cancelamento, e executar. É o assunto da próxima aula; abra o arquivo, ache as três, e leia os comentários.

**Por dentro: dois tópicos e três serviços.**

```bash
# ── Terminal B · com o launch da varredura no ar ──────
ros2 topic list --include-hidden-topics | grep varrer
ros2 service list --include-hidden-services | grep varrer
```

Esperado: `/varrer_cena/_action/feedback` e `/varrer_cena/_action/status`; e `.../cancel_goal`, `.../get_result` e `.../send_goal`. Uma ação é a Aula 2 organizada para a tarefa que demora — e é daí que sai o desafio da tarefa.

## 4. Autoavaliação (10 min)

Responda sem olhar; depois abra a resposta.

??? question "1. \"Qual a temperatura do motor agora?\", \"a temperatura do motor, dez vezes por segundo\" e \"aqueça o motor até 60 °C\": tópico, serviço ou ação?"
    Serviço (pergunta com resposta imediata), tópico (um fluxo, sem pergunta) e ação (demora, tem progresso, e faz sentido interromper).

??? question "2. Você rodou `ros2 action send_goal` sem `--feedback` e a tarefa de 20 s terminou certo. O que você deixou de ver, e por que isso importa?"
    O feedback: o progresso chegando durante a execução. Sem ele a ação parece um serviço lento — e quem chamou fica 20 s sem saber se a tarefa anda ou travou.

??? question "3. `Goal was rejected.` e `Goal finished with status: ABORTED` são a mesma coisa?"
    Não. **Rejeitado**: o servidor olhou o pedido e recusou **antes de começar** (pedido sem sentido, ou servidor ocupado). **Abortado**: o servidor começou e **desistiu no meio**, porque a tarefa deixou de ser possível (aqui, ficou sem percepção).

??? question "4. Você deu `Ctrl+C` no cliente e o servidor continuou trabalhando por mais uma fração de segundo. É defeito?"
    Não: cancelar é um **pedido**. O servidor o vê na próxima volta do laço, decide aceitar, e devolve o resultado parcial. O atraso é limitado pelo período do laço — é o item (2) do desafio.

??? question "5. `ros2 action list` mostra `/varrer_cena`, mas `ros2 action send_goal` responde `The passed action type is invalid`. O que falta?"
    O `source "$PB_WS/install/setup.bash"` **neste** terminal. O `list` pergunta ao grafo; o `send_goal` precisa importar o tipo.

??? question "6. No seu projeto, você pensou numa ação \"tirar uma foto e dizer quantos objetos há\". É uma boa ação?"
    Provavelmente não: é instantânea, e não há o que interromper nem progresso a relatar — é um serviço. Uma boa ação leva mais de um segundo e faz sentido cancelar: "observe por 30 s", "percorra a fileira", "inspecione o lote até achar 5 refugos".

## 5. Se travar

| Sintoma | Causa provável | Cura |
|---|---|---|
| `Package 'aula07_acoes' not found ... searching: [...]` | este terminal fez o `source` antes do build | `source "$PB_WS/install/setup.bash"` neste terminal |
| `Check that the following packages have been built: - pb_interfaces` | os nós foram compilados antes das interfaces | interfaces primeiro, `source`, depois os nós |
| `The passed action type is invalid` | terminal sem o `source` do workspace | `source "$PB_WS/install/setup.bash"` |
| `Waiting for an action server to become available...`, e nada | o servidor não está no ar | confira o Terminal A; `ros2 action list` |
| `Action servers: 0` | o `info` foi rodado cedo demais | espere cinco segundos e repita |
| `Goal was rejected.` num pedido válido | já existe uma varredura em curso | espere a anterior terminar |
| `Failed to populate message fields` | nome de campo errado no objetivo | `ros2 interface show pb_interfaces/action/VarrerCena` |
| `status: ABORTED`, `percepcao muda` | o servidor está sem `/vision/deteccoes` | suba pelo `varredura.launch.py`, que traz o detector |
| o `Ctrl+C` no `ros2 action send_goal` não cancelou | corrida da ferramenta no Humble (acontece de vez em quando) | a tarefa segue até o prazo; para cancelar, use o cliente do exemplo |
| o cliente mostra um `Traceback` no `Ctrl+C` | exemplo antigo no seu workspace | baixe o material de novo e copie `aula07_acoes` outra vez |
| `/vision/contagem` ou as detecções com taxa baixa | o perfil do Fast DDS não está no terminal do launch | [página da Aula 4](../aulas/etapa03-aula04/index.md#pegar-o-material) |
