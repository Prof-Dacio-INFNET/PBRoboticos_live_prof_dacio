# Exemplo — `aula07-acoes`

**Turma live: Aula 5 (usar a ação) e Aula 6 (o servidor por dentro) · Etapa 4.** Uma ação completa: objetivo aceito ou rejeitado, feedback durante a execução, sucesso antecipado, aborto quando a tarefa deixa de ser possível, e **cancelamento que funciona de verdade**. (O nome da pasta segue a numeração da turma presencial, de onde o exemplo veio.)

```text
aula07-acoes/
`-- aula07_acoes/                  ament_python
    |-- servidor_varredura.py      o servidor: aceita, executa, publica feedback, cancela, aborta
    `-- cliente_varredura.py       o cliente: envia, acompanha, e sabe pedir cancelamento
```

A ação em si — `VarrerCena.action` — mora no **mesmo** `pb_interfaces` do exemplo `aula06-interfaces`. Interface não ganha pacote novo a cada aula: o pacote de interfaces do projeto cresce.

## Baixar, copiar e compilar

```bash
# ── Terminal B · uma vez por terminal · UMA LINHA POR VEZ a partir do colcon ──
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"
source /opt/ros/humble/setup.bash

rm -rf /tmp/PBRoboticos_live_prof_dacio
git clone --depth 1 https://github.com/Prof-Dacio-INFNET/PBRoboticos_live_prof_dacio.git /tmp/PBRoboticos_live_prof_dacio
M=/tmp/PBRoboticos_live_prof_dacio/exemplos
cp -r "$M/aula06-interfaces/pb_interfaces" "$M/aula06-interfaces/aula06_percepcao" "$M/aula07-acoes/aula07_acoes" "$PB_WS/src/"
cd "$PB_WS"
colcon build --packages-select pb_interfaces
source install/setup.bash
colcon build --packages-select aula06_percepcao aula07_acoes --symlink-install
source install/setup.bash
```

**Tem de aparecer:** `Finished <<< pb_interfaces` (de dez a quinze segundos) e `Summary: 2 packages finished`. Interfaces primeiro, sempre.

## Rodar

```bash
# ── Terminal A · o launch ocupa o terminal ────────────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"
source /opt/ros/humble/setup.bash
source "$PB_WS/install/setup.bash"
ros2 launch aula07_acoes varredura.launch.py classe:=tomate_maduro
```

**Tem de aparecer:** `servidor da action 'varrer_cena' no ar` e `detector no ar - classe='tomate_maduro'`: o launch sobe a percepção e o servidor.

Noutro terminal, pela linha de comando — sem escrever cliente nenhum:

```bash
# ── Terminal B · espere uns cinco segundos depois do launch ──
ros2 action list -t
ros2 action info /varrer_cena -t
ros2 action send_goal /varrer_cena pb_interfaces/action/VarrerCena \
  "{duracao_s: 6.0, classe_alvo: 'tomate_maduro', minimo_para_parar: 0}" --feedback
```

**Tem de aparecer:** `/varrer_cena [pb_interfaces/action/VarrerCena]`; `Action servers: 1`; e, no `send_goal`, `Goal accepted`, uns trinta blocos `Feedback:`, o `Result:` com `resumo: varredura completa de 6.0s` e `Goal finished with status: SUCCEEDED`. O `--feedback` é o que mostra a diferença: sem ele, a ação parece um serviço lento.

!!! warning "Se o `send_goal` disser `The passed action type is invalid`"
    É o terminal, e não a ação. `ros2 action list` e `ros2 action info` continuam funcionando porque perguntam ao **grafo**; o `send_goal` precisa **importar o tipo**. Resolva com `source "$PB_WS/install/setup.bash"` **neste** terminal.

## Os experimentos

**1. A rejeição.** Peça algo absurdo e veja o servidor recusar antes de começar:

```bash
# ── Terminal B · com o Terminal A no ar ───────────────
ros2 action send_goal /varrer_cena pb_interfaces/action/VarrerCena \
  "{duracao_s: 999.0, classe_alvo: 'tomate_maduro', minimo_para_parar: 0}"
```

**Tem de aparecer:** `Goal was rejected.` — e, no Terminal A, `objetivo REJEITADO: duracao_s=999.0 fora de (0, 120]`. Rejeitado é diferente de falhou: o servidor olhou o pedido e disse não. O servidor também rejeita um segundo objetivo enquanto o primeiro está em curso (`ja existe uma varredura em curso`).

**2. O sucesso antecipado.**

```bash
# ── Terminal B · com o Terminal A no ar ───────────────
ros2 action send_goal /varrer_cena pb_interfaces/action/VarrerCena \
  "{duracao_s: 30.0, classe_alvo: 'tomate_maduro', minimo_para_parar: 2}"
```

**Tem de aparecer:** `resumo: 'parou cedo: viu 2 (minimo 2) em 0.0s'` e `SUCCEEDED`, quase na hora. Tarefa longa não é tarefa de duração fixa.

**3. O cancelamento.**

```bash
# ── Terminal B · o cliente ocupa o terminal; depois de uns cinco segundos, Ctrl+C UMA vez ──
ros2 run aula07_acoes cliente_varredura --ros-args -p duracao_s:=30.0 -p classe_alvo:=tomate_maduro
```

**Tem de aparecer**, depois do `Ctrl+C`: `pedindo cancelamento...` e `RESULTADO: ... | cancelada em N.Ns`; no Terminal A, `cancelamento pedido - aceitando` e `varredura CANCELADA em N.Ns`. O `Ctrl+C` no cliente **pede** o cancelamento; o servidor decide aceitar, e devolve o resultado parcial.

O `Ctrl+C` no `ros2 action send_goal` também pede o cancelamento (`Canceling goal...`), mas a ferramenta do Humble tem uma corrida: de vez em quando ele não cancela, e a tarefa segue até o prazo. Para demonstrar cancelamento, use o cliente.

**4. O aborto.** `Ctrl+C` no launch, e suba **só** o servidor, sem a percepção:

```bash
# ── Terminal A · só o servidor (ocupa o terminal) ─────
ros2 run aula07_acoes servidor_varredura
```

```bash
# ── Terminal B · com o servidor sozinho no ar ─────────
ros2 action send_goal /varrer_cena pb_interfaces/action/VarrerCena \
  "{duracao_s: 20.0, classe_alvo: 'tomate_maduro', minimo_para_parar: 0}"
```

**Tem de aparecer**, depois de uns três segundos: `resumo: 'abortada: percepcao muda ha mais de 3.0s'` e `Goal finished with status: ABORTED`. Cancelar é decisão de quem pediu; abortar é decisão do servidor, quando a tarefa deixou de ser possível.

**5. O servidor surdo (assunto da Aula 6).** Duas linhas do `servidor_varredura.py` decidem se ele ouve alguma coisa enquanto trabalha: o `ReentrantCallbackGroup` no `ActionServer` e o `MultiThreadedExecutor` no `main()`. O bloco tira as duas — no **seu** workspace, e não no material:

```bash
# ── Terminal B · com o launch PARADO no Terminal A ────
: "${PB_WS:?defina PB_USER, PB_DIR e PB_WS — o bloco está em Baixar, copiar e compilar}"
F="$PB_WS/src/aula07_acoes/aula07_acoes/servidor_varredura.py"
sed -i 's/            callback_group=ReentrantCallbackGroup())/            )   # EXPERIMENTO: sem ReentrantCallbackGroup/' "$F"
sed -i 's/        rclpy.spin(no, executor=executor)/        rclpy.spin(no)   # EXPERIMENTO: sem MultiThreadedExecutor/' "$F"
grep -n "EXPERIMENTO" "$F"
```

**Tem de aparecer:** duas linhas marcadas com `EXPERIMENTO`. Suba o launch de novo no Terminal A (com `--symlink-install` não é preciso recompilar), envie um objetivo de dez segundos com `--feedback` no Terminal B, e dê `Ctrl+C` depois de um ou dois segundos.

O que acontece: o servidor **não registra** nenhum `cancelamento pedido` (a ferramenta pode responder `Failed to cancel goal`); e, aos três segundos, ele aborta com `varredura ABORTADA: sem percepcao ha mais de 3.0s` — **com a percepção no ar**. Não há erro de programação à vista: a função que executa a tarefa ocupou a única linha de execução do nó, e ele ficou surdo para tudo — para o cancelamento **e** para a própria percepção. É um defeito que não aparece como erro: aparece como uma funcionalidade que simplesmente não acontece.

Para voltar ao normal:

```bash
# ── Terminal B · com o launch PARADO no Terminal A ────
: "${PB_WS:?defina PB_USER, PB_DIR e PB_WS — o bloco está em Baixar, copiar e compilar}"
cp /tmp/PBRoboticos_live_prof_dacio/exemplos/aula07-acoes/aula07_acoes/aula07_acoes/servidor_varredura.py "$PB_WS/src/aula07_acoes/aula07_acoes/servidor_varredura.py"
grep -c "EXPERIMENTO" "$PB_WS/src/aula07_acoes/aula07_acoes/servidor_varredura.py"
```

**Tem de aparecer:** `0`.

## O que copiar para o seu projeto

A forma do `VarrerCena.action` serve para quase qualquer tarefa longa de percepção: um prazo, um alvo, uma condição de parada antecipada, e um feedback com progresso. Troque o vocabulário e mantenha a estrutura de três partes.

Do servidor, o que se copia não é o corpo do laço — é a **ordem** dentro dele: checar o cancelamento primeiro, trabalhar depois, publicar o feedback por último, e dormir um pouco. Do cliente, o tratamento do `Ctrl+C`: o `SignalHandlerOptions.NO` no `rclpy.init`, para que o nó continue vivo depois do `Ctrl+C` e consiga acompanhar o cancelamento até o resultado.

## Licença

MIT, como todo o diretório `exemplos/`.
