---
titulo: "Tarefa da Aula 6 — o servidor da sua ação: responde, e cancela"
aula: 6
etapa: 4
data_aula: 2026-11-23
prazo: 2026-12-06
obrigatoria: true
vira_no_tp: "TP2 — a ação central do projeto, com servidor e cliente"
---

# Tarefa da Aula 6 — o servidor da sua ação: responde, e cancela

**Publicada em 23/11/2026 · prazo domingo 06/12, 23h59 · push na `dev`**

!!! danger "Primeiro as duas partes da semana passada"
    O servidor importa a **sua** ação do **seu** pacote de interfaces. Sem a [tarefa da Aula 4](tarefa-aula04-interfaces.md) (o pacote, com a mensagem e o serviço) e a [tarefa da Aula 5](tarefa-aula05-acoes.md) (o arquivo `.action`), não há o que servir. Faça as duas antes, nessa ordem.

## Cenas dos últimos episódios

Na Aula 5 você usou uma ação pronta (`VarrerCena`) e definiu a do seu projeto. Na Aula 6 o professor abriu o servidor: as **três decisões** (aceitar o pedido, aceitar parar, executar), a **ordem** dentro do laço (cancelamento primeiro, trabalho depois, feedback por último), os **três verbos** de término (`succeed`, `canceled`, `abort`) e as **duas linhas** sem as quais o servidor compila, roda — e não cancela. O [guia de estudo da Aula 6](estudo-aula06-servidor-acao.md) reproduz os três casos da aula no seu repositório; **faça o guia antes desta tarefa**.

## As quatro perguntas

**O que fazer.** O servidor e o cliente da ação do seu projeto: o servidor aceita um pedido, dá feedback, conclui, rejeita um pedido absurdo, aborta quando a tarefa fica impossível — e **cancela** quando o cliente pede.

**O que usar.** O `servidor_varredura.py` e o `cliente_varredura.py` do exemplo `aula07-acoes`, copiados para o **seu** pacote pelo bloco do passo 1; e o seu pacote de interfaces, com a sua ação.

**Como adequar ao seu projeto.** Três coisas: os **campos** da sua ação (passo 3); o que o seu servidor **rejeita**; e o que faz a sua tarefa **abortar**.

**Como saber que terminou.** O seu cliente cancela, e `docs/evidencias/tp2/acao-servidor.txt` tem a linha `cancelamento pedido - aceitando`; há uma captura de tela com o servidor e o cliente juntos; e está tudo commitado na `dev`.

<!-- PB:TAREFA-A06 -->
- [ ] T6.1 `servidor_acao` e `cliente_acao` no **seu** pacote, compilando e listados em `ros2 pkg executables`
- [ ] T6.2 a sua ação visível em `ros2 action list -t`, com o tipo do **seu** pacote de interfaces
- [ ] T6.3 o servidor adaptado: os campos da sua ação, um pedido que ele rejeita, e a condição que o faz abortar — as duas decisões escritas no `PROJETO.md`
- [ ] T6.4 pedido concluído, pedido rejeitado e pedido cancelado, com `docs/evidencias/tp2/acao-servidor.txt` e `acao-cliente.txt`
- [ ] T6.5 captura de tela com servidor e cliente juntos em `docs/evidencias/tp2/`; commit na `dev` com push

## 1. Copie o servidor e o cliente para o seu pacote

Quatro nomes, no primeiro bloco: o pacote dos **seus** nós, o seu pacote de interfaces, a sua ação e o nome dela no grafo (minúsculas com sublinhado: `contar_fileira`, `inspecionar_lote`). O bloco copia os dois arquivos do exemplo para o seu pacote com os nomes trocados, registra os dois executáveis no `setup.py` e a dependência no `package.xml`. Ele pode ser repetido: não sobrescreve o que você já editou.

```bash
# ── Terminal B · uma vez por terminal ─────────────────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"
export PB_PKG=visao_pomar                  # ← troque: o pacote dos SEUS nós
export PB_IFACE=pomar_interfaces           # ← troque: o SEU pacote de interfaces
export PB_ACAO=ContarFileira               # ← troque: o nome da SUA ação
export PB_ACAO_NOME=contar_fileira         # ← troque: o nome dela no grafo
source /opt/ros/humble/setup.bash

cd "$PB_DIR" && git checkout dev
rm -rf /tmp/PBRoboticos_live_prof_dacio
git clone --depth 1 https://github.com/Prof-Dacio-INFNET/PBRoboticos_live_prof_dacio.git /tmp/PBRoboticos_live_prof_dacio
E=/tmp/PBRoboticos_live_prof_dacio/exemplos/aula07-acoes/aula07_acoes/aula07_acoes
ls "$PB_WS/src/$PB_IFACE/action/$PB_ACAO.action" "$PB_WS/src/$PB_PKG/setup.py"
cd "$PB_WS/src/$PB_PKG"
[ -e "$PB_PKG/servidor_acao.py" ] || sed "s/pb_interfaces/$PB_IFACE/g; s/VarrerCena/$PB_ACAO/g; s/varrer_cena/$PB_ACAO_NOME/g; s/servidor_varredura/servidor_acao/g; s/ServidorVarredura/ServidorAcao/g" "$E/servidor_varredura.py" > "$PB_PKG/servidor_acao.py"
[ -e "$PB_PKG/cliente_acao.py" ] || sed "s/pb_interfaces/$PB_IFACE/g; s/VarrerCena/$PB_ACAO/g; s/varrer_cena/$PB_ACAO_NOME/g; s/cliente_varredura/cliente_acao/g; s/ClienteVarredura/ClienteAcao/g; s/aula07_acoes/$PB_PKG/g" "$E/cliente_varredura.py" > "$PB_PKG/cliente_acao.py"
grep -q "servidor_acao = " setup.py || sed -i "s|'console_scripts': \[|'console_scripts': [\n        'servidor_acao = $PB_PKG.servidor_acao:main',\n        'cliente_acao = $PB_PKG.cliente_acao:main',|" setup.py
grep -q "<depend>$PB_IFACE</depend>" package.xml || sed -i "s|  <export>|  <depend>$PB_IFACE</depend>\n  <export>|" package.xml
grep -n "servidor_acao\|cliente_acao" setup.py
grep -n "<depend>$PB_IFACE" package.xml
grep -n "^from $PB_IFACE\|'$PB_ACAO_NOME'" "$PB_PKG/servidor_acao.py"
```

**Tem de aparecer:** os dois caminhos do `ls` (o arquivo da sua ação e o `setup.py` do seu pacote — se der `No such file`, um dos quatro nomes está errado, ou falta uma das tarefas anteriores); duas linhas no `setup.py`, com `servidor_acao` e `cliente_acao`; a linha `<depend>` com o seu pacote de interfaces; e, no servidor, os dois `import` (`from <o seu pacote>.action import <SuaAcao>` e `from <o seu pacote>.msg import Deteccoes`) e a linha do `ActionServer` com o nome da ação.

Se um dos dois primeiros `grep` não mostrar nada, o seu `setup.py` ou o seu `package.xml` têm um formato diferente do padrão: acrescente à mão as duas linhas em `console_scripts` e a linha `<depend>` antes de `<export>`.

## 2. Compile, e veja o servidor no ar

```bash
# ── Terminal B · herda as variáveis do passo 1 ────────
: "${PB_ACAO_NOME:?defina PB_USER, PB_DIR, PB_WS, PB_PKG, PB_IFACE, PB_ACAO e PB_ACAO_NOME — o bloco está no passo 1}"
cd "$PB_WS"
colcon build --packages-up-to "$PB_PKG" --symlink-install
source install/setup.bash
ros2 pkg executables "$PB_PKG" | grep acao
```

**Tem de aparecer:** o pacote de interfaces compilando **antes** do pacote dos nós, `Summary: 2 packages finished` (uns quinze segundos), e as duas linhas novas: `cliente_acao` e `servidor_acao`.

Pare qualquer launch do exemplo que esteja no ar: ele publica `/vision/deteccoes` com o tipo do `pb_interfaces`, e o seu servidor espera o tipo do **seu** pacote — um tópico não pode ter dois tipos.

```bash
# ── Terminal A · o SEU servidor (ocupa o terminal) ────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"
export PB_PKG=visao_pomar                  # ← troque: o pacote dos SEUS nós
source /opt/ros/humble/setup.bash
source "$PB_WS/install/setup.bash"
ros2 run "$PB_PKG" servidor_acao
```

```bash
# ── Terminal B · com o Terminal A no ar ───────────────
: "${PB_ACAO_NOME:?defina as variáveis — o bloco está no passo 1}"
ros2 action list -t
ros2 action info "/$PB_ACAO_NOME"
```

**Tem de aparecer:** no Terminal A, `[servidor_acao]: servidor da action '<a sua ação>' no ar - teste com: ...`; no Terminal B, o nome da sua ação com o tipo do seu pacote entre colchetes, e `Action servers: 1`.

## 3. Adapte: os campos da sua ação, e as duas decisões do seu domínio

**Se o seu `.action` manteve os campos do exemplo** (`duracao_s`, `classe_alvo`, `minimo_para_parar` etc.), o servidor já funciona: vá ao passo 4 e volte aqui depois — mas volte, porque a ação do TP2 fala do **seu** domínio.

**Se você trocou os campos** (era o pedido da tarefa da Aula 5), o servidor sobe, mas quebra com `AttributeError` quando o primeiro pedido chega. São estas as linhas que mudam — abra `"$PB_WS/src/$PB_PKG/$PB_PKG/servidor_acao.py"` no editor:

| Linhas do `servidor_acao.py` | Usa | Troque por |
|---|---|---|
| 84 a 89 | `goal_request.duracao_s`, `goal_request.classe_alvo` | os campos do **seu** objetivo; o limite que o **seu** servidor rejeita |
| 111 e 112 | `pedido.classe_alvo`, `pedido.minimo_para_parar` | o que procurar, e a sua condição de parada antecipada |
| 145 e 148 | `d.classe`, `d.confianca` (da mensagem de detecção) | os campos da **sua** mensagem, se você os renomeou |
| 160 | `pedido.duracao_s` | o seu prazo (ou a sua condição de fim) |
| 168 a 170 | `fb.decorrido_s`, `fb.vistos_ate_agora`, `fb.progresso` | os campos do **seu** feedback |
| 177 a 180 | `r.total_visto`, `r.confianca_media`, `r.quadros_analisados`, `r.resumo` | os campos do **seu** resultado |

E, no `cliente_acao.py`: as linhas 24 a 26 (os parâmetros), 40 a 45 (o preenchimento do objetivo), 52 e 53 (o que ele mostra de cada feedback) e 69 e 70 (o que ele registra do resultado).

Troque **um grupo por vez**, e teste a cada troca (o passo 4). Com `--symlink-install` não é preciso compilar de novo depois de editar um `.py`: basta parar o servidor (`Ctrl+C`) e subir de novo. O que **não** muda: as três funções, a ordem dentro do laço, os três verbos e as duas linhas (`ReentrantCallbackGroup` e `MultiThreadedExecutor`).

**As duas decisões do seu domínio.** Escreva as duas no `PROJETO.md`, na seção "Ação do projeto", uma linha cada:

- **O que o servidor rejeita** (a função `aceitar_objetivo`). Um limite do **seu** domínio: uma fileira que não existe, um lote vazio, uma duração fora de faixa.
- **O que faz a tarefa abortar** (o trecho `1b` do laço). No exemplo é a percepção muda por três segundos. No seu projeto pode ser a mesma coisa — diga por quê — ou outra: a esteira parou, o robô saiu da área.

## 4. Teste sem a câmera: concluir, rejeitar, abortar

`ros2 topic pub` publica o que você escrever, na taxa que você pedir: o servidor não sabe que é de mentira. Com o seu servidor no ar no Terminal A:

```bash
# ── Terminal B · a percepção de mentira (ocupa o terminal) ──
: "${PB_IFACE:?defina as variáveis — o bloco está no passo 1}"
ros2 topic pub -r 15 /vision/deteccoes "$PB_IFACE/msg/Deteccoes" "{deteccoes: [{classe: 'tomate_maduro', confianca: 0.9, x: 100, y: 100, area: 1500}], total: 1}"
```

```bash
# ── Terminal C · os pedidos ───────────────────────────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"
export PB_IFACE=pomar_interfaces           # ← troque: o SEU pacote de interfaces
export PB_ACAO=ContarFileira               # ← troque: o nome da SUA ação
export PB_ACAO_NOME=contar_fileira         # ← troque: o nome dela no grafo
source /opt/ros/humble/setup.bash
source "$PB_WS/install/setup.bash"
ros2 action send_goal "/$PB_ACAO_NOME" "$PB_IFACE/action/$PB_ACAO" "{duracao_s: 3.0, classe_alvo: 'tomate_maduro', minimo_para_parar: 0}" --feedback
ros2 action send_goal "/$PB_ACAO_NOME" "$PB_IFACE/action/$PB_ACAO" "{duracao_s: 999.0, classe_alvo: 'tomate_maduro', minimo_para_parar: 0}"
```

**Tem de aparecer:** no primeiro pedido, o feedback cinco vezes por segundo e o resultado — `total_visto: 1`, `quadros_analisados: 45` (perto disso), `resumo: varredura completa de 3.0s` e `Goal finished with status: SUCCEEDED`; no segundo, `Goal was rejected.` (e, no Terminal A, `objetivo REJEITADO: ...`).

Os campos entre chaves — na mensagem do Terminal B e no objetivo do Terminal C — são os do **exemplo**. Se você trocou os seus, escreva os seus: `ros2 interface show "$PB_IFACE/action/$PB_ACAO"` mostra os nomes.

Agora o abortar: `Ctrl+C` no Terminal B (a percepção some), e:

```bash
# ── Terminal C · com a percepção de mentira PARADA ────
ros2 action send_goal "/$PB_ACAO_NOME" "$PB_IFACE/action/$PB_ACAO" "{duracao_s: 10.0, classe_alvo: 'tomate_maduro', minimo_para_parar: 0}"
```

**Tem de aparecer:** uns três segundos depois, `resumo: 'abortada: percepcao muda ha mais de 3.0s'` e `Goal finished with status: ABORTED`.

## 5. Cancele com o cliente — e guarde a evidência

É o centro da tarefa: o cancelamento **funcionando**, com o servidor e o cliente no ar ao mesmo tempo. O `tee -i` grava em arquivo o que aparece na tela, e não morre com o `Ctrl+C`.

```bash
# ── Terminal A · Ctrl+C no servidor, e então, gravando o log (ocupa o terminal) ──
: "${PB_PKG:?defina as variáveis — o bloco do Terminal A está no passo 2}"
cd "$PB_DIR" && mkdir -p docs/evidencias/tp2
ros2 run "$PB_PKG" servidor_acao 2>&1 | tee -i docs/evidencias/tp2/acao-servidor.txt
```

```bash
# ── Terminal B · a percepção de mentira de novo (seta para cima; ocupa o terminal) ──
: "${PB_IFACE:?defina as variáveis — o bloco está no passo 1}"
ros2 topic pub -r 15 /vision/deteccoes "$PB_IFACE/msg/Deteccoes" "{deteccoes: [{classe: 'tomate_maduro', confianca: 0.9, x: 100, y: 100, area: 1500}], total: 1}"
```

```bash
# ── Terminal C · o SEU cliente; depois de uns quatro segundos, Ctrl+C UMA vez ──
: "${PB_DIR:?defina PB_USER, PB_DIR e PB_WS — o bloco do Terminal C está no passo 4}"
export PB_PKG=visao_pomar                  # ← troque: o pacote dos SEUS nós
cd "$PB_DIR" && mkdir -p docs/evidencias/tp2
ros2 run "$PB_PKG" cliente_acao --ros-args -p duracao_s:=30.0 -p classe_alvo:=tomate_maduro 2>&1 | tee -i docs/evidencias/tp2/acao-cliente.txt
```

**Tem de aparecer:** no Terminal C, `objetivo aceito - acompanhando (Ctrl+C cancela)`, uma linha de feedback a cada 0,2 s, e, depois do seu `Ctrl+C`, `pedindo cancelamento...` e `RESULTADO: ... | cancelada em 4.0s`. No Terminal A, `cancelamento pedido - aceitando` e `varredura CANCELADA em 4.0s`.

**A captura de tela.** Com os Terminais A e C lado a lado, e as linhas acima visíveis nos dois, tire a captura (no Windows: `Win`+`Shift`+`S`) e salve em `docs/evidencias/tp2/acao-servidor-cliente.png`. É a "operação simultânea" que o enunciado do TP2 pede.

Depois: `Ctrl+C` no Terminal A e no Terminal B.

## 6. Verificação e commit

```bash
# ── Terminal C · com os três terminais já parados ─────
: "${PB_DIR:?defina PB_USER, PB_DIR e PB_WS — o bloco do Terminal C está no passo 4}"
cd "$PB_DIR"
grep -c "cancelamento pedido" docs/evidencias/tp2/acao-servidor.txt
grep "RESULTADO" docs/evidencias/tp2/acao-cliente.txt
ls docs/evidencias/tp2/
git add -A
git commit -m "Acao do projeto: servidor e cliente, com feedback, rejeicao, aborto e cancelamento"
git push origin dev
```

**Tem de aparecer:** `1` (ou mais) no primeiro `grep`; a linha `RESULTADO: ... cancelada em ...` no segundo; na pasta, `acao-servidor.txt`, `acao-cliente.txt` e a captura, ao lado dos arquivos das tarefas anteriores; o commit e o push. Se isso apareceu, a tarefa terminou.

Se você trocou o texto das mensagens de log do servidor (faz sentido: "varredura" pode virar "contagem"), ajuste o `grep` — o que importa é a linha em que o servidor registra que **recebeu e aceitou** o pedido de cancelamento.

## Desafio (opcional): o período do laço é uma decisão

O servidor só olha o pedido de cancelamento **uma vez por volta**, e publica um feedback por volta. O tamanho da volta é a constante `PERIODO_S`. O desafio usa o servidor do **exemplo**, com o launch da varredura (pare antes o seu servidor e a percepção de mentira):

```bash
# ── Terminal B · muda o período do exemplo para 1,0 s ──
: "${PB_WS:?defina PB_USER, PB_DIR e PB_WS — o bloco está no passo 1}"
F="$PB_WS/src/aula07_acoes/aula07_acoes/servidor_varredura.py"
sed -i 's/^PERIODO_S = [0-9.]* /PERIODO_S = 1.0 /' "$F"
grep -n "^PERIODO_S" "$F"
```

```bash
# ── Terminal A · o launch do exemplo (ocupa o terminal) ──
: "${PB_WS:?defina as variáveis — o bloco do Terminal A está no passo 2}"
ros2 launch aula07_acoes varredura.launch.py classe:=tomate_maduro
```

```bash
# ── Terminal B · o cliente do exemplo; Ctrl+C depois de uns dez segundos ──
ros2 run aula07_acoes cliente_varredura --ros-args -p duracao_s:=30.0 -p classe_alvo:=tomate_maduro
```

```bash
# ── Terminal C · enquanto o cliente roda (encerra sozinho em 8 s) ──
timeout 8 ros2 topic hz /varrer_cena/_action/feedback
```

Anote a taxa do feedback; e, no log do Terminal A, a diferença entre o horário (entre colchetes) da linha `cancelamento pedido` e o da linha `CANCELADA`. Cancele três vezes e fique com o **maior** atraso. Depois repita tudo com `0.05` no lugar de `1.0` (troque o número no `sed`, e suba o launch de novo).

Três perguntas: **(1)** qual a taxa do feedback e o maior atraso do cancelamento em cada caso — `1.0`, `0.2` (o original, medido na tarefa da Aula 5) e `0.05`? **(2)** Qual valor você escolheria para um robô que se move? E para um que só observa? **(3)** O que se paga por um período muito curto? Anote os números e a escolha para o **seu** projeto em `docs/decisoes.md`.

No fim, devolva o arquivo original:

```bash
# ── Terminal B · o servidor do exemplo de volta ───────
: "${PB_WS:?defina PB_USER, PB_DIR e PB_WS — o bloco está no passo 1}"
cp /tmp/PBRoboticos_live_prof_dacio/exemplos/aula07-acoes/aula07_acoes/aula07_acoes/servidor_varredura.py "$PB_WS/src/aula07_acoes/aula07_acoes/servidor_varredura.py"
grep -n "^PERIODO_S" "$PB_WS/src/aula07_acoes/aula07_acoes/servidor_varredura.py"
```

## O que esta tarefa adianta

Com as tarefas das Aulas 4, 5 e 6 feitas, as duas primeiras das quatro tarefas do [TP2](../recursos/tp2.md) estão prontas: as interfaces do projeto, e a ação central com servidor e cliente. Falta o rastreamento (Aula 7) e a parametrização com o URDF (Aula 8).

## Se der errado

| Sintoma | O que fazer |
|---|---|
| `No such file` no `ls` do passo 1 | um dos quatro nomes está errado, ou falta a tarefa da Aula 4 (o pacote) ou a da Aula 5 (o `.action`) |
| `ModuleNotFoundError: No module named '<o seu pacote de interfaces>'` | faltou o `source "$PB_WS/install/setup.bash"` neste terminal, depois do build |
| `No executable found` no `ros2 run` | o `setup.py` não tem as duas linhas (`grep -n acao setup.py`), ou faltou compilar e dar `source` |
| `AttributeError: ... object has no attribute 'duracao_s'` (ou outro campo) | o seu `.action` tem outros campos: é o passo 3 |
| `Failed to populate message fields` no `send_goal` ou no `topic pub` | o nome de um campo entre chaves não existe na **sua** interface: confira com `ros2 interface show` |
| `ABORTED` com `percepcao muda`, sem você querer | a percepção de mentira não está no ar, ou publica com o tipo de outro pacote |
| o `ros2 topic pub` reclama de tipos incompatíveis no `/vision/deteccoes` | há um launch do exemplo no ar, publicando com o tipo do `pb_interfaces`: pare-o |
| o cliente cancela, e o resultado vem `abortada`, com `quadros=0` | faltam as duas linhas (`ReentrantCallbackGroup` e `MultiThreadedExecutor`): compare o seu `servidor_acao.py` com o do exemplo |
| o arquivo de evidência ficou vazio | faltou o `2>&1` antes do `| tee -i` |
| `Goal was rejected.` num pedido válido | já existe um pedido em curso: espere terminar |

Travou, e nada aqui bate? **Infnet.Online**, com três coisas: o comando exato, a saída completa e o passo em que você está.
