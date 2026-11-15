---
titulo: "Tarefa da Aula 5 — a ação do seu projeto: usada, e depois definida"
aula: 5
etapa: 4
data_aula: 2026-11-16
prazo: 2026-11-29
obrigatoria: true
vira_no_tp: "TP2 — a ação do domínio"
---

# Tarefa da Aula 5 — a ação do seu projeto: usada, e depois definida

**Publicada em 16/11/2026 · prazo domingo 29/11, 23h59 · push na `dev`**

!!! danger "Primeiro a parte 1"
    Esta é a **parte 2** da tarefa da semana. A parte 1 é a [tarefa da Aula 4 — as interfaces do seu projeto](tarefa-aula04-interfaces.md): a sua ação mora no pacote de interfaces que você cria lá. O passo 1 daqui pode ser feito antes; o passo 2, só depois.

## Cenas dos últimos episódios

Na Aula 5 você viu duas coisas. Primeiro, as interfaces próprias: um pacote só de definições (`pb_interfaces`) ao lado do pacote dos nós, e o `/vision/status` respondendo com campos em vez de uma frase. Depois, a ação: `VarrerCena`, com três partes (o objetivo, o resultado e o feedback), usada pela linha de comando em três casos — pedir e acompanhar, ser rejeitado e parar cedo, cancelar no meio. O [guia de estudo da Aula 5](estudo-aula05-acoes.md) reproduz tudo isso no seu repositório; **faça o guia antes desta tarefa**.

## As quatro perguntas

**O que fazer.** Duas coisas: rodar os três casos da aula no seu ambiente, guardando a saída; e escrever o `.action` do **seu** projeto, no seu pacote de interfaces, compilando.

**O que usar.** O exemplo `aula07-acoes` (com o `pb_interfaces` e o `aula06_percepcao`), e o pacote de interfaces que você criou na parte 1.

**Como adequar ao seu projeto.** A ação descreve uma tarefa do **seu** domínio que leva mais de um segundo e faz sentido interromper. As três partes ganham o seu vocabulário: um objetivo com condição de parada antecipada, um resultado que informa, e um feedback com uma medida do seu domínio.

**Como saber que terminou.** `ros2 interface show` mostra a sua ação, com as três partes e os dois separadores; e `docs/evidencias/tp2/` tem `acao-exemplo.txt` e `acao-projeto.txt`, commitados.

O **servidor** da sua ação não é desta tarefa: ele vem depois da próxima aula.

<!-- PB:TAREFA-A05 -->
- [ ] T5.1 os três casos do exemplo rodados no seu ambiente, com a saída em `docs/evidencias/tp2/acao-exemplo.txt`
- [ ] T5.2 a tarefa demorada do seu projeto escolhida, e escrita em uma linha no `PROJETO.md`
- [ ] T5.3 o `.action` do seu projeto no seu pacote de interfaces, compilando e visível no `ros2 interface list`
- [ ] T5.4 evidência em `docs/evidencias/tp2/acao-projeto.txt`; commit na `dev` com push

## 1. Rode os três casos no seu ambiente

Com os três pacotes do exemplo já compilados no seu workspace (é a seção 2 do [guia de estudo](estudo-aula05-acoes.md#2-reproduza-o-exemplo-passo-a-passo-45-min)):

```bash
# ── Terminal A · o launch ocupa o terminal ────────────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"
source /opt/ros/humble/setup.bash
source "$PB_WS/install/setup.bash"
ros2 launch aula07_acoes varredura.launch.py classe:=tomate_maduro
```

**Tem de aparecer:** `servidor da action 'varrer_cena' no ar` e `detector no ar - classe='tomate_maduro'`.

```bash
# ── Terminal B · casos 1 e 2, com a saída guardada (leva uns dez segundos) ──
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"
source /opt/ros/humble/setup.bash
source "$PB_WS/install/setup.bash"
cd "$PB_DIR" && git checkout dev && mkdir -p docs/evidencias/tp2
ros2 action list -t > docs/evidencias/tp2/acao-exemplo.txt
ros2 action send_goal /varrer_cena pb_interfaces/action/VarrerCena "{duracao_s: 6.0, classe_alvo: 'tomate_maduro', minimo_para_parar: 0}" --feedback >> docs/evidencias/tp2/acao-exemplo.txt
ros2 action send_goal /varrer_cena pb_interfaces/action/VarrerCena "{duracao_s: 999.0, classe_alvo: 'tomate_maduro', minimo_para_parar: 0}" >> docs/evidencias/tp2/acao-exemplo.txt
ros2 action send_goal /varrer_cena pb_interfaces/action/VarrerCena "{duracao_s: 30.0, classe_alvo: 'tomate_maduro', minimo_para_parar: 2}" >> docs/evidencias/tp2/acao-exemplo.txt
grep -c "Feedback" docs/evidencias/tp2/acao-exemplo.txt
grep "varrer_cena\|status\|rejected\|resumo" docs/evidencias/tp2/acao-exemplo.txt
```

**Tem de aparecer:** um número perto de `30` (os feedbacks do caso 1); a linha `/varrer_cena [pb_interfaces/action/VarrerCena]`; `resumo: varredura completa de 6.0s` e `Goal finished with status: SUCCEEDED`; `Goal was rejected.`; e `resumo: 'parou cedo: viu 2 (minimo 2) em ...'` com outro `SUCCEEDED`.

```bash
# ── Terminal B · caso 3: o cliente ocupa o terminal; depois de uns cinco segundos, Ctrl+C UMA vez ──
ros2 run aula07_acoes cliente_varredura --ros-args -p duracao_s:=30.0 -p classe_alvo:=tomate_maduro 2>&1 | tee -ia docs/evidencias/tp2/acao-exemplo.txt
```

**Tem de aparecer**, depois do `Ctrl+C`: `pedindo cancelamento...` e `RESULTADO: ... cancelada em N.Ns`; e, no Terminal A, `cancelamento pedido - aceitando` e `varredura CANCELADA em N.Ns`. O `tee -ia` grava no arquivo o que passa na tela, sem morrer com o `Ctrl+C`.

## 2. Defina a ação do seu projeto

**Escolha a tarefa.** Responda antes de escrever qualquer coisa: *qual tarefa do meu projeto leva mais de um segundo, e faz sentido interromper?*

| Domínio | Uma ação plausível |
|---|---|
| inspeção de peças | inspecionar um lote até achar N refugos, ou esgotar a esteira |
| estacionamento | varrer o pátio e mapear as vagas livres |
| agricultura | percorrer a fileira contando frutos maduros |
| segurança | monitorar a área por N minutos e relatar intrusões |
| logística | seguir uma rota de coleta e reportar o progresso |

Escreva a sua em uma linha no `PROJETO.md`, numa seção "Ação do projeto": o que se pede, o que volta durante, o que volta no fim. Se a tarefa **não** tem como ser interrompida de forma útil, ela provavelmente é um serviço — diga isso, e escolha outra.

**Crie o arquivo.** O bloco copia a ação do exemplo para o **seu** pacote de interfaces, com o nome que você escolher, e a põe na lista do `CMakeLists.txt`. O nome da ação começa por maiúscula e não tem espaço nem sublinhado: `ContarFileira`, `InspecionarLote`, `VarrerPatio`.

```bash
# ── Terminal B · uma vez por terminal ─────────────────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"
export PB_IFACE=pomar_interfaces           # ← troque: o nome do SEU pacote de interfaces (o da parte 1)
export PB_ACAO=ContarFileira               # ← troque: o nome da SUA ação
source /opt/ros/humble/setup.bash

ls "$PB_WS/src/$PB_IFACE/CMakeLists.txt"
cd "$PB_WS/src/$PB_IFACE" && mkdir -p action
cp /tmp/PBRoboticos_live_prof_dacio/exemplos/aula06-interfaces/pb_interfaces/action/VarrerCena.action "action/$PB_ACAO.action"
grep -q "action/$PB_ACAO.action" CMakeLists.txt || sed -i "s|^  DEPENDENCIES|  \"action/$PB_ACAO.action\"\n  DEPENDENCIES|" CMakeLists.txt
grep -n "action" CMakeLists.txt package.xml
```

**Tem de aparecer:** o caminho do `CMakeLists.txt` do seu pacote (se der `No such file`, o pacote da parte 1 ainda não existe, ou `PB_IFACE` está com o nome errado); e, no `grep`, quatro coisas: `find_package(action_msgs REQUIRED)`, a linha `"action/<SuaAcao>.action"` dentro da lista, `DEPENDENCIES std_msgs action_msgs`, e `<depend>action_msgs</depend>` no `package.xml`. Se o `/tmp/PBRoboticos_live_prof_dacio` não existir mais, refaça o [Pegar o material](../aulas/etapa04-aula05/index.md#pegar-o-material).

**Escreva as três partes com o seu vocabulário.** Abra `"$PB_WS/src/$PB_IFACE/action/$PB_ACAO.action"` no editor e troque os campos — mantendo os **dois** separadores `---`:

- **Objetivo** — o que se pede, incluindo um critério de **parada antecipada** (quantos bastam? até onde ir?).
- **Resultado** — o que ficou sabendo, e não só "deu certo".
- **Feedback** — algo que muda **durante**. Progresso sozinho é pobre: acrescente uma medida do seu domínio (quantos já contou, qual vaga está olhando, quantos refugos até agora).

Um exemplo, para um pomar:

```text
# ContarFileira.action -- percorre uma fileira contando frutos maduros
# ---------- Goal ----------
uint32  fileira             # qual fileira percorrer
uint32  bastam              # 0 = a fileira inteira; N = para ao contar N maduros
float32 duracao_maxima_s    # desiste depois disso
---
# ---------- Result ----------
uint32  maduros
uint32  verdes
float32 confianca_media
string  resumo
---
# ---------- Feedback ----------
float32 progresso           # 0.0 a 1.0 da fileira
uint32  maduros_ate_agora
```

Campos em minúsculas com sublinhado, sem acento; tipos válidos: `bool`, `int32`, `uint32`, `float32`, `float64`, `string`, e as suas próprias mensagens.

```bash
# ── Terminal B · herda as variáveis do bloco acima ────
: "${PB_ACAO:?defina PB_USER, PB_DIR, PB_WS, PB_IFACE e PB_ACAO — o bloco está logo acima}"
cd "$PB_WS"
colcon build --packages-select "$PB_IFACE"
source install/setup.bash
ros2 interface list | grep "$PB_IFACE"
ros2 interface show "$PB_IFACE/action/$PB_ACAO"
```

**Tem de aparecer:** `Finished <<<` com o nome do seu pacote (uns dez segundos); a sua ação na lista, ao lado do `.msg` e do `.srv` da parte 1; e as três partes, com os **seus** campos e comentários.

## 3. Evidência, verificação e commit

```bash
# ── Terminal B · herda as variáveis do passo 2 ────────
: "${PB_ACAO:?defina PB_USER, PB_DIR, PB_WS, PB_IFACE e PB_ACAO — o bloco está no passo 2}"
cd "$PB_DIR" && mkdir -p docs/evidencias/tp2
ros2 interface list | grep "$PB_IFACE"            >  docs/evidencias/tp2/acao-projeto.txt
ros2 interface show "$PB_IFACE/action/$PB_ACAO"   >> docs/evidencias/tp2/acao-projeto.txt
cat docs/evidencias/tp2/acao-projeto.txt
ls docs/evidencias/tp2/
git add -A
git commit -m "Acao do projeto: definicao no pacote de interfaces; tres casos do exemplo rodados"
git push origin dev
```

**Tem de aparecer:** a lista com a sua ação, o arquivo dela, os dois arquivos de evidência (`acao-exemplo.txt` e `acao-projeto.txt`), o commit e o push. Se isso apareceu, a tarefa terminou.

## Desafio (opcional): a ação por dentro, medida

Por dentro, uma ação é feita de dois tópicos e três serviços (`ros2 topic list --include-hidden-topics | grep varrer`). Se o feedback é um tópico, dá para medir a taxa dele. Com o launch da varredura no ar no Terminal A:

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

**(1)** Quantos feedbacks por segundo o servidor publica — e de qual linha do `servidor_varredura.py` vem esse número? **(2)** Cancele três objetivos (o caso 3, três vezes) e compare, no log do Terminal A, o horário entre colchetes da linha `cancelamento pedido` com o da linha `CANCELADA`: qual foi o maior atraso, e por que ele nunca passa de um certo valor? Anote os números e a sua conclusão em `docs/decisoes.md`, e traga para a próxima aula.

## O que esta tarefa adianta

O TP2 (leitura na Aula 6, 23/11) pede a mensagem, o serviço e a **ação** do seu domínio. Com esta tarefa, a ação já está definida e compilando; depois da próxima aula você escreve o servidor dela — com feedback, e com um cancelamento que funciona de verdade.

## Se der errado

| Sintoma | O que fazer |
|---|---|
| `The passed action type is invalid` | é o terminal: `source "$PB_WS/install/setup.bash"` neste terminal, depois do build |
| `Waiting for an action server to become available...`, e nada | o servidor não está no ar: confira o Terminal A e `ros2 action list` |
| `Goal was rejected.` num pedido válido | já existe uma varredura em curso: espere a anterior terminar |
| `Failed to populate message fields` | o nome de um campo do objetivo está errado: `ros2 interface show pb_interfaces/action/VarrerCena` |
| `Goal finished with status: ABORTED` | o servidor ficou sem percepção: suba pelo launch `varredura.launch.py`, que traz o detector junto |
| o `Ctrl+C` no `ros2 action send_goal` não cancelou | é uma corrida da ferramenta no Humble; a tarefa segue até o prazo. Para cancelar, use o cliente do exemplo |
| o cliente mostra um `Traceback` no `Ctrl+C` | exemplo antigo: baixe o material de novo e copie `aula07_acoes` outra vez |
| o `colcon build` do seu pacote reclama do `.action` | nome do arquivo com minúscula inicial, espaço ou sublinhado; campo com maiúscula ou acento; ou um dos dois `---` foi apagado |
| compila, mas `ros2 interface list` não mostra a ação | o arquivo não entrou na lista do `CMakeLists.txt` (o `grep` do passo 2 mostra), ou faltou o `source` depois do build |
| `rosidl` reclama de `action_msgs` | `find_package(action_msgs REQUIRED)` e `DEPENDENCIES ... action_msgs` no `CMakeLists.txt`; `<depend>action_msgs</depend>` no `package.xml` |

Travou, e nada aqui bate? **Infnet.Online**, com o comando exato, a saída completa e o passo em que você está.
