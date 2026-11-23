# Guia de estudo — Aula 6: o servidor da ação, por dentro

**Semana de 23/11 a 06/12 · Etapa 4 · turma live.** A aula de 1h30 teve três blocos: o servidor da ação por dentro, o caminho até o servidor do seu projeto, e a leitura do TP2. Aqui você reproduz o primeiro bloco no seu repositório, lê o servidor com perguntas na mão, e chega pronto à [tarefa da Aula 6](tarefa-aula06-servidor-acao.md). Tempo total: **1h15 a 1h30**, numa sessão.

| O quê | Tempo | Resultado |
|---|---|---|
| Seção 1 — ler | 15 min | você sabe dizer as três decisões de um servidor, e os três jeitos de terminar |
| Seção 2 — reproduzir os três casos, e um que a aula não mostrou | 35 min | abortar, o servidor surdo e a cura, rodados no **seu** repositório |
| Seção 3 — anatomia: o servidor, linha a linha | 20 min | você sabe onde mexer quando a ação for a sua |
| Seção 4 — autoavaliação | 10 min | seis perguntas, com resposta |

!!! tip "Como pedir ajuda"
    No Infnet.Online, com três itens: o **comando exato**, a **saída completa** e o **passo** em que você está. Antes disso, a seção 5 ("Se travar").

---

## Cenas dos últimos episódios

Na Aula 2 você escreveu nós como classes, com funções chamadas quando algo chega. Na Aula 5 você usou uma ação pronta pela linha de comando — pediu, acompanhou, foi rejeitado, cancelou — e definiu o `.action` do seu projeto. Na Aula 6 o professor abriu o servidor dessa ação: três funções, um laço com uma ordem, três verbos de término, e duas linhas que decidem se ele ouve ou fica surdo. Aqui você repete os três casos, e acrescenta um.

## 1. Leia antes (15 min)

Releia, na [página da Aula 6](../aulas/etapa04-aula06/index.md), o bloco 1 inteiro — só o texto e os trechos de código, sem rodar nada. Depois abra o arquivo do exemplo e leia o comentário do começo (as primeiras 17 linhas):

```bash
# ── Terminal B · uma vez por terminal ─────────────────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"
source /opt/ros/humble/setup.bash
source "$PB_WS/install/setup.bash"
sed -n '1,17p' "$PB_WS/src/aula07_acoes/aula07_acoes/servidor_varredura.py"
```

**Tem de aparecer:** o comentário que começa com `Servidor da action VarrerCena` e termina falando das duas linhas. Se der `No such file`, o exemplo ainda não está no seu workspace: faça antes a seção 2 do [guia de estudo da Aula 5](estudo-aula05-acoes.md#2-reproduza-o-exemplo-passo-a-passo-45-min).

Três perguntas para responder de cabeça antes de seguir: quantas funções o servidor entrega ao `ActionServer`? Qual delas roda antes de a tarefa começar? E quais são os três jeitos de uma tarefa aceita terminar?

## 2. Reproduza os três casos — e um a mais (35 min)

Os blocos estão na página da aula, na ordem; cada um diz em que terminal roda e o que tem de aparecer. Faça nesta sequência:

1. [Pegar o material](../aulas/etapa04-aula06/index.md#pegar-o-material) — atualiza a cópia em `/tmp`.
2. O launch da varredura no Terminal A — o bloco está em [Três decisões, não uma](../aulas/etapa04-aula06/index.md#tres-decisoes-nao-uma).
3. [Caso 1 — abortar](../aulas/etapa04-aula06/index.md#caso-1-o-servidor-desiste-abortar). Anote o `resumo` e o `status`.
4. [Caso 2 — o servidor surdo](../aulas/etapa04-aula06/index.md#caso-2-o-servidor-surdo-duas-linhas-a-menos). Anote a linha `RESULTADO` — e procure, no Terminal A, a linha `cancelamento pedido`. Ela **não** está lá.

**O caso que a aula não mostrou.** Com o servidor ainda surdo (antes do caso 3), o que acontece se ele não abortar? Dê a ele sessenta segundos de paciência com a percepção, e peça oito segundos:

```bash
# ── Terminal B · com o servidor SURDO no ar no Terminal A ──
ros2 param set /servidor_varredura timeout_percepcao_s 60.0
ros2 run aula07_acoes cliente_varredura --ros-args -p duracao_s:=8.0 -p classe_alvo:=tomate_maduro
```

Aperte `Ctrl+C` dois segundos depois de `objetivo aceito`. **Tem de aparecer:** `Set parameter successful`; depois do seu `Ctrl+C`, `pedindo cancelamento...`; e, só aos oito segundos, `RESULTADO: ... quadros=0  |  varredura completa de 8.0s`. O pedido de cancelamento foi **ignorado**, e a tarefa foi até o fim. Num robô que se move, são seis segundos andando depois de mandarem parar.

Por fim, o [Caso 3 — as duas linhas de volta](../aulas/etapa04-aula06/index.md#caso-3-as-duas-linhas-de-volta-agora-ele-ouve). **Não pule**: sem ele, o exemplo do seu workspace fica com o defeito.

## 3. Anatomia: o servidor, linha a linha (20 min)

Com o arquivo original de volta, leia cada trecho com a pergunta ao lado. O `sed -n 'A,Bp'` mostra as linhas de A a B.

```bash
# ── Terminal B · herda as variáveis da seção 1 ────────
: "${PB_WS:?defina PB_USER, PB_DIR e PB_WS — o bloco está na seção 1}"
F="$PB_WS/src/aula07_acoes/aula07_acoes/servidor_varredura.py"
sed -n '50,55p' "$F"
sed -n '68,99p' "$F"
sed -n '120,173p' "$F"
sed -n '175,191p' "$F"
```

| Linhas | O que é | A pergunta |
|---|---|---|
| 50 a 55 | o `ActionServer` | qual função responde a cada uma das três decisões? |
| 68 a 90 | `aceitar_objetivo` | quais são os dois motivos de recusa? O que os comentários das linhas 77 a 82 admitem? |
| 92 a 99 | `aceitar_cancelamento` | em que situação um servidor deveria **recusar** um cancelamento? |
| 120 a 129 | o começo do laço | por que o cancelamento é a primeira coisa? |
| 131 a 142 | abortar | qual a diferença entre a `carencia` e o `timeout`? |
| 144 a 164 | o trabalho, e os dois sucessos | o que faz a tarefa terminar **antes** do prazo? |
| 166 a 173 | o feedback, e o sono | quantos feedbacks por segundo, e de onde vem esse número? |
| 175 a 181 | `_resultado` | por que o resultado é montado numa função só? |
| 184 a 191 | `main` | qual linha, se trocada, deixa o servidor surdo? |

## 4. Autoavaliação (10 min)

??? question "1. Um serviço tem uma função. Um servidor de ação tem quantas, e o que cada uma decide?"
    Três. `goal_callback`: aceito este pedido? `cancel_callback`: aceito parar? `execute_callback`: faz o trabalho, publica o feedback e devolve o resultado.

??? question "2. Qual a diferença entre rejeitar, cancelar e abortar?"
    Rejeitar acontece **antes**: o servidor olha o pedido e diz não; a tarefa nem começa. Cancelar é decisão de **quem pediu**, no meio da tarefa, e o servidor precisa aceitar. Abortar é decisão do **servidor**: a tarefa deixou de ser possível.

??? question "3. Por que o teste do cancelamento é a primeira coisa do laço?"
    Porque é a única coisa que vem de fora e tem pressa. Depois do trabalho, o robô faria mais uma volta inteira antes de obedecer.

??? question "4. No caso 2, o cliente pediu cancelamento e o resultado veio 'abortada: percepcao muda', com quadros=0. Por quê?"
    Sem as duas linhas, o nó tem uma linha de execução só, e ela está presa dentro de `executar`. O pedido de cancelamento e as mensagens da percepção ficam na fila, sem ninguém para ler. Sem mensagens novas, o próprio servidor conclui, aos três segundos, que a percepção está muda — e aborta.

??? question "5. Quais são as duas linhas, e por que precisa das duas?"
    `callback_group=ReentrantCallbackGroup()` no `ActionServer` (as funções deste nó **podem** rodar ao mesmo tempo) e `MultiThreadedExecutor()` no `main` (há **mais de uma** linha de execução para atender a fila). Permitir sem ter quem atenda não resolve; ter quem atenda sem permitir, também não.

??? question "6. Por que 'o código existe' não serve de evidência do cancelamento?"
    Porque o servidor sem as duas linhas tem **o mesmo** código de cancelamento, compila, roda e aceita objetivos — e não cancela. Só o comportamento prova: o cliente pede, e o log do servidor mostra `cancelamento pedido - aceitando`.

## 5. Se travar

A tabela [Socorro rápido](../aulas/etapa04-aula06/index.md#socorro-rapido) da página da aula cobre os sintomas destes casos. O mais comum depois do estudo: o cancelamento do exemplo "parou de funcionar" — o arquivo ficou com as duas linhas trocadas; faça o `cp` do caso 3.
