# Aula 6 — O servidor da ação, por dentro; e o TP2, lido

**Segunda, 23/11/2026 · Zoom · 1h30 · Etapa 4 · turma live**

[:material-file-pdf-box: Slides da Aula 6 (PDF)](apresentacao-aula06.pdf){ .md-button .md-button--primary }
[:material-book-open-variant: Guia de estudo da Aula 6](../../tutoriais/estudo-aula06-servidor-acao.md){ .md-button }
[:material-clipboard-check: Tarefa: o servidor da sua ação](../../tutoriais/tarefa-aula06-servidor-acao.md){ .md-button }
[:material-file-document-check: TP2 — enunciado, checklist e gates](../../recursos/tp2.md){ .md-button }
[:material-code-tags: Exemplo `aula07-acoes`](../../exemplos/aula07-acoes/index.md){ .md-button }

## Como esta página funciona

A aula **demonstra**; a tarefa **executa**. Durante o encontro o professor roda tudo no repositório dele (`pb-live-dacioms`) e você observa e anota. Esta página guarda o que foi mostrado, na ordem dos slides, e termina em [A tarefa da semana](#a-tarefa-da-semana), que é o que você roda no **seu** ambiente.

Sobre os blocos de comando: cada bloco diz, na primeira linha, **em qual terminal** ele roda, e pode ser **colado inteiro de uma vez**. Quando um comando ocupa o terminal (um `launch`, o cliente, o servidor), ele é o último do bloco. Abaixo de cada bloco, **Tem de aparecer** diz o que você deve ver.

## Cenas dos últimos episódios

**O que a Aula 5 deixou.** A mensagem do projeto — um pacote só de definições (`pb_interfaces`), e o `/vision/status` respondendo com campos em vez de uma frase. As três formas de conversar: tópico (fluxo), serviço (pergunta), ação (tarefa que demora). As três partes de um `.action`: o objetivo, o resultado e o feedback. E três casos pela linha de comando: pedir e acompanhar; ser rejeitado, e parar cedo; cancelar no meio. Ficou uma pergunta sem resposta: **quem** decide aceitar, rejeitar, cancelar? Na semana passada a resposta era "o servidor". Hoje a resposta é uma linha de código.

**As peças antigas que voltam hoje.**

| Peça | De onde vem | Onde entra hoje |
|---|---|---|
| O nó como classe, com funções chamadas quando algo chega | Aula 2 | o servidor da ação tem **três** dessas funções |
| O arquivo `.action`, com três partes | Aula 5 | cada campo dele aparece numa linha do servidor |
| O pacote de interfaces do projeto | tarefa da Aula 4 | é de lá que o **seu** servidor importa a ação |
| `setup.py` e `package.xml` | Aula 2 | o servidor é mais um executável do **seu** pacote |
| `ros2 action send_goal` e o cliente do exemplo | Aula 5 | são as ferramentas de teste de hoje |
| A percepção que some (oclusão, câmera fora do ar) | Aulas 3 e 5 | hoje o servidor **reage** a isso |

## A ideia em uma frase

Hoje a ação **deixa de ser uma caixa-preta** — e o seu projeto ganha um enunciado: o servidor da ação do seu domínio é o centro do TP2.

## O que você sai sabendo hoje, e o que isso vale no seu projeto

| Você sai sabendo | No seu projeto, isso vale |
|---|---|
| Ler um servidor de ação: três decisões, três funções | são as três funções que você escreve |
| A ordem dentro do laço de execução | é ela que faz o seu robô parar **na hora** em que mandam |
| Concluir, cancelar e abortar | o seu servidor precisa dizer **como** a tarefa terminou |
| As duas linhas que fazem o servidor ouvir | sem elas ele compila, roda — e não cancela |
| Levar o exemplo para o seu pacote, e testar sem a câmera | é o passo a passo da tarefa desta semana |
| O que o TP2 pede, e quanto dele você já tem | você sabe por onde começar, e onde não gastar tempo |

## O que foi demonstrado, onde está na tarefa, e quando vence

Os gates e as datas são **referência para consulta** — estão na página [TP2 — enunciado, checklist e gates](../../recursos/tp2.md).

| Demonstrado na aula | Na tarefa | Referência |
|---|---|---|
| As três decisões do servidor | passo 3 (o que o **seu** servidor rejeita) | ação do projeto, com servidor |
| A ordem dentro do laço; os três verbos de término | passo 3 (o que faz a **sua** tarefa abortar) | — |
| Caso 1: abortar | passo 2 (a percepção de mentira, ligada e desligada) | — |
| Casos 2 e 3: o servidor surdo, e a cura | passo 4 (o cancelamento funcionando, com evidência) | cancelamento que funciona · push na `dev` até **dom 06/12** |
| O cliente, em quatro momentos | passo 4 | servidor e cliente juntos, com captura de tela |
| Copiar para o seu pacote; testar sem a câmera | passos 1 e 2 | servidor respondendo · **qua 02/12** |
| O período do laço | desafio | opcional |
| A leitura do TP2 | [página do TP2](../../recursos/tp2.md) | entrega do TP2: **sex 11/12** |

## Pegar o material

Os blocos desta página usam os três pacotes do exemplo (`pb_interfaces`, `aula06_percepcao` e `aula07_acoes`) **já compilados no seu workspace** — é a seção 2 do [guia de estudo da Aula 5](../../tutoriais/estudo-aula05-acoes.md#2-reproduza-o-exemplo-passo-a-passo-45-min). O bloco abaixo só atualiza a cópia do material.

```bash
# ── Terminal B · uma vez por terminal ─────────────────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"
source /opt/ros/humble/setup.bash
source "$PB_WS/install/setup.bash"

# o material da disciplina (pode repetir sempre: a linha do rm evita o erro de pasta já existente)
rm -rf /tmp/PBRoboticos_live_prof_dacio
git clone --depth 1 https://github.com/Prof-Dacio-INFNET/PBRoboticos_live_prof_dacio.git /tmp/PBRoboticos_live_prof_dacio
ls /tmp/PBRoboticos_live_prof_dacio/exemplos/aula07-acoes/aula07_acoes/aula07_acoes
ros2 pkg executables aula07_acoes
```

**Tem de aparecer:** `__init__.py`, `cliente_varredura.py` e `servidor_varredura.py`; e os dois executáveis, `aula07_acoes cliente_varredura` e `aula07_acoes servidor_varredura`. Se o último comando disser `Package 'aula07_acoes' not found`, o exemplo ainda não está compilado no seu workspace: faça antes a seção 2 do guia de estudo da Aula 5.

## Bloco 1 — O servidor, por dentro

### Três decisões, não uma

Um serviço tem **uma** função: chegou a pergunta, devolve a resposta. Um servidor de ação tem **três**, uma para cada decisão:

```python
# aula07_acoes/servidor_varredura.py
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from pb_interfaces.action import VarrerCena
...
        self._server = ActionServer(
            self, VarrerCena, 'varrer_cena',
            goal_callback=self.aceitar_objetivo,          # 1) aceito este pedido?
            cancel_callback=self.aceitar_cancelamento,    # 2) aceito parar?
            execute_callback=self.executar,               # 3) fazer o trabalho
            callback_group=ReentrantCallbackGroup())      #    (esta linha: mais abaixo)
```

Na Aula 5 você viu as três acontecendo **de fora**: `Goal was rejected.` é a primeira; `cancelamento pedido - aceitando` é a segunda; o feedback e o resultado saem da terceira.

```bash
# ── Terminal A · o launch ocupa o terminal ────────────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"
source /opt/ros/humble/setup.bash
source "$PB_WS/install/setup.bash"
ros2 launch aula07_acoes varredura.launch.py classe:=tomate_maduro
```

**Tem de aparecer:** `[detector]: detector no ar - classe='tomate_maduro' ...` e `[servidor_varredura]: servidor da action 'varrer_cena' no ar - teste com: ...`. Deixe rodando.

### Decisões 1 e 2: aceitar o pedido; aceitar parar

```python
    def aceitar_objetivo(self, goal_request):
        if self.ocupado:                                  # um objetivo por vez
            return GoalResponse.REJECT
        d = goal_request.duracao_s
        if not (0.0 < d <= 120.0):                        # pedido absurdo
            return GoalResponse.REJECT
        return GoalResponse.ACCEPT

    def aceitar_cancelamento(self, goal_handle):
        # um robô com o braço no meio de um movimento pode precisar recusar,
        # ou aceitar e recolher antes. Aqui observar é inofensivo: aceita.
        return CancelResponse.ACCEPT
```

A primeira roda **antes** de a tarefa começar: é nela que se recusa o pedido absurdo — e o segundo pedido, enquanto o primeiro está em curso (um robô tem um braço só). A segunda decide se o servidor aceita parar: aceitar é uma **decisão**, e não um automatismo. Para o seu projeto: o que o **seu** servidor deveria recusar? E em que momento ele **não** pode parar de repente?

### Decisão 3: executar — e a ordem dentro do laço

```python
        while True:
            decorrido = time.monotonic() - inicio
            if goal_handle.is_cancel_requested:           # 1) o cancelamento vem ANTES de tudo
                goal_handle.canceled()
                return self._resultado(..., 'cancelada em %.1fs' % decorrido)
            ...                                           # 2) amostra a percepção
            if limite and picos >= limite:                # 3) já viu o bastante: termina cedo
                goal_handle.succeed()
                return self._resultado(..., 'parou cedo ...')
            if decorrido >= pedido.duracao_s:             # 4) acabou o prazo
                goal_handle.succeed()
                return self._resultado(..., 'varredura completa ...')
            goal_handle.publish_feedback(fb)              # 5) avisa do progresso
            time.sleep(PERIODO_S)                         #    e dorme 0,2 s
```

O que se copia deste laço não é o corpo: é a **ordem**. Cancelamento primeiro, trabalho depois, feedback por último, e um sono curto. O servidor só olha o pedido de cancelamento **uma vez por volta** — por isso o sono é curto. Inverta a ordem, e o robô leva uma volta inteira para obedecer.

### Três verbos para terminar — e um resultado, sempre

| Verbo | Quem decidiu | Quando |
|---|---|---|
| `goal_handle.succeed()` | a tarefa | concluiu — no prazo, ou antes, porque o objetivo foi atingido |
| `goal_handle.canceled()` | quem pediu | o cliente desistiu, e o servidor aceitou parar |
| `goal_handle.abort()` | o **servidor** | a tarefa deixou de ser possível |

Depois do verbo vem o `return` com o resultado: ele volta **nos três casos**, com o que deu para saber. Sair do laço sem chamar um dos três deixa o cliente pendurado, esperando para sempre. E **rejeitar** não é um quarto verbo: acontece antes, na primeira função, e a tarefa nem começa.

### Caso 1 — o servidor desiste: abortar

```bash
# ── Terminal B · com o Terminal A no ar ───────────────
pkill -f "aula06_percepcao/detector"
ros2 action send_goal /varrer_cena pb_interfaces/action/VarrerCena "{duracao_s: 20.0, classe_alvo: 'tomate_maduro', minimo_para_parar: 0}"
```

**Tem de aparecer:** `Goal accepted with ID: ...` e, uns três segundos depois, o resultado com `resumo: 'abortada: percepcao muda ha mais de 3.0s'` e `Goal finished with status: ABORTED`. No Terminal A, `[ERROR] [detector-1]: process has died` e, em vermelho, `varredura ABORTADA: sem percepcao ha mais de 3.0s`.

O pedido era de vinte segundos, e ninguém cancelou. Foi o servidor que desistiu: esperou três segundos por uma percepção que não veio, e disse por quê. **Cancelar** é decisão de quem pediu; **abortar** é decisão do servidor. Varrer a cena sem imagem não é uma varredura ruim: é uma varredura que não está acontecendo. Para o seu projeto: o que torna a **sua** tarefa impossível no meio do caminho?

### Caso 2 — o servidor surdo: duas linhas a menos

O defeito mais caro de uma ação cabe em duas linhas. O bloco tira as duas do servidor que está no **seu** workspace (o caso 3 as devolve):

```bash
# ── Terminal B · herda as variáveis de "Pegar o material" ──
: "${PB_WS:?defina PB_USER, PB_DIR e PB_WS — o bloco está em Pegar o material}"
F="$PB_WS/src/aula07_acoes/aula07_acoes/servidor_varredura.py"
sed -i 's/            callback_group=ReentrantCallbackGroup())/            )   # EXPERIMENTO: sem ReentrantCallbackGroup/' "$F"
sed -i 's/        rclpy.spin(no, executor=executor)/        rclpy.spin(no)   # EXPERIMENTO: sem MultiThreadedExecutor/' "$F"
grep -n "EXPERIMENTO" "$F"
```

**Tem de aparecer:** duas linhas, a 55 e a 191, com o comentário `EXPERIMENTO`.

```bash
# ── Terminal A · Ctrl+C no launch, espere o prompt, e então (ocupa o terminal) ──
ros2 launch aula07_acoes varredura.launch.py classe:=tomate_maduro
```

Não é preciso compilar de novo: com `--symlink-install`, o que roda é o arquivo da pasta `src/`.

```bash
# ── Terminal B · o cliente ocupa o terminal; Ctrl+C UM segundo depois de "objetivo aceito" ──
ros2 run aula07_acoes cliente_varredura --ros-args -p duracao_s:=30.0 -p classe_alvo:=tomate_maduro
```

**Tem de aparecer:** `objetivo aceito - acompanhando (Ctrl+C cancela)`, depois do seu `Ctrl+C` a linha `pedindo cancelamento...` e, aos três segundos:

```text
RESULTADO: total_visto=2  confianca_media=0.99  quadros=0  |  abortada: percepcao muda ha mais de 3.0s
```

Você pediu para cancelar — e ele respondeu "abortada: percepção muda". No Terminal A **não aparece** `cancelamento pedido`: o pedido nunca foi ouvido. E a percepção estava no ar, publicando quinze vezes por segundo: `quadros=0`. O `total_visto=2` é a última mensagem que chegou **antes** de a tarefa começar — o servidor passou três segundos olhando uma foto velha. Nenhum erro, nenhum `Traceback`: o servidor compila, roda, aceita o objetivo — e fica surdo enquanto trabalha.

### Por que ele ficou surdo: uma fila, uma linha de execução

Todo nó tem uma **fila** de coisas a fazer: mensagens que chegam, pedidos, temporizadores. Por padrão, **uma** linha de execução atende a fila: uma função por vez, até ela terminar. A função `executar` entrou — e só sai quando a tarefa acaba. A fila parou atrás dela: o pedido de cancelamento está lá, as mensagens da percepção também, e ninguém as lê. É por isso que as funções dos nós da Aula 2 eram curtas; a ação é o primeiro caso em que uma função **precisa** demorar.

### As duas linhas que fazem o servidor ouvir

```python
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
...
        self._server = ActionServer(
            self, VarrerCena, 'varrer_cena', ...,
            callback_group=ReentrantCallbackGroup())      # 1) as funções deste nó podem
                                                          #    rodar ao mesmo tempo
def main():
    rclpy.init()
    no = ServidorVarredura()
    executor = MultiThreadedExecutor()                    # 2) mais de uma linha de execução
    rclpy.spin(no, executor=executor)
```

A primeira diz que as funções deste nó **podem** rodar em paralelo. A segunda dá mais de uma linha de execução para atender a fila. Precisa das **duas**: uma sem a outra não resolve. No seu servidor, elas entram no primeiro dia — o bloco da tarefa já as traz.

### Caso 3 — as duas linhas de volta: agora ele ouve

```bash
# ── Terminal B · herda as variáveis de "Pegar o material" ──
: "${PB_WS:?defina PB_USER, PB_DIR e PB_WS — o bloco está em Pegar o material}"
cp /tmp/PBRoboticos_live_prof_dacio/exemplos/aula07-acoes/aula07_acoes/aula07_acoes/servidor_varredura.py "$PB_WS/src/aula07_acoes/aula07_acoes/servidor_varredura.py"
grep -c "EXPERIMENTO" "$PB_WS/src/aula07_acoes/aula07_acoes/servidor_varredura.py"
```

**Tem de aparecer:** `0`.

```bash
# ── Terminal A · Ctrl+C no launch, espere o prompt, e então (ocupa o terminal) ──
ros2 launch aula07_acoes varredura.launch.py classe:=tomate_maduro
```

```bash
# ── Terminal B · o mesmo cliente; Ctrl+C uns três segundos depois de "objetivo aceito" ──
ros2 run aula07_acoes cliente_varredura --ros-args -p duracao_s:=30.0 -p classe_alvo:=tomate_maduro
```

**Tem de aparecer:** `pedindo cancelamento...` e `RESULTADO: total_visto=2  confianca_media=0.98  quadros=54  |  cancelada em 3.6s` (os números mudam com o instante do `Ctrl+C`). No Terminal A, as duas linhas que faltavam: `cancelamento pedido - aceitando` e `varredura CANCELADA em 3.6s`.

O mesmo cliente, o mesmo `Ctrl+C` — e agora o servidor ouve, aceita e para. A diferença entre os dois casos são duas linhas. É por isso que a evidência do TP2 é o cancelamento **funcionando**, e não o código existir.

### O cliente, em quatro momentos

```python
# aula07_acoes/cliente_varredura.py
        self.cliente = ActionClient(self, VarrerCena, 'varrer_cena')
        ...
        fut = self.cliente.send_goal_async(objetivo, feedback_callback=self.ao_feedback)   # 1
        fut.add_done_callback(self.ao_responder)

    def ao_responder(self, fut):
        gh = fut.result()
        if not gh.accepted: ...                               # 2) REJEITADO não é FALHOU
        gh.get_result_async().add_done_callback(self.ao_terminar)                          # 3

    def cancelar(self):
        self.goal_handle.cancel_goal_async()                  # 4) PEDE o cancelamento
```

Enviar **não bloqueia**: o cliente segue vivo, e as respostas chegam em funções suas. Um: envia, e diz onde quer o feedback. Dois: foi aceito? Três: pede o resultado. Quatro: **pede** o cancelamento — quem decide é o servidor. O TP2 quer os dois lados: o cliente mostra cada feedback e registra o resultado.

## Bloco 2 — Do exemplo ao SEU servidor

Este bloco é o caminho da [tarefa da semana](../../tutoriais/tarefa-aula06-servidor-acao.md); aqui fica o resumo do que foi mostrado.

**Copiar, e trocar quatro nomes.** Você não começa de uma página em branco: começa do servidor que acabou de ver, já com as duas linhas e com a ordem certa no laço. Quatro variáveis — o pacote dos seus nós, o seu pacote de interfaces, o nome da sua ação e o nome dela no grafo — e o bloco do passo 1 da tarefa copia o servidor e o cliente para o **seu** pacote, troca os nomes, registra os dois executáveis no `setup.py` e a dependência no `package.xml`. O servidor da ação é mais um executável do seu pacote, e não um pacote novo.

**Onde o servidor usa cada campo da sua ação.** Se a sua ação tem outros campos — e deveria ter —, são estas as linhas que mudam:

| Parte da ação | Linhas do `servidor_acao.py` | O que elas fazem |
|---|---|---|
| objetivo | 84 a 87 | o limite que o servidor rejeita |
| objetivo | 111 e 112 | o que procurar, e a parada antecipada |
| objetivo | 160 | o prazo |
| feedback | 168 a 170 | o que volta durante |
| resultado | 177 a 180 | o que volta no fim |

O resto do arquivo — as três decisões, a ordem do laço, as duas linhas — fica como está.

**Testar sem a câmera.** `ros2 topic pub` publica o que você escrever, na taxa que você pedir; o servidor não sabe que é de mentira. É a vantagem de ter uma mensagem com tipo: dá para testar cada peça sozinha. O passo 2 da tarefa traz os três terminais: o seu servidor, a percepção de mentira e o pedido.

## Bloco 3 — O TP2, lido

O enunciado oficial é o do Moodle. A página [TP2 — enunciado, checklist e gates](../../recursos/tp2.md) é a versão lida em aula: o que se pede, onde cada coisa aparece nas aulas, o que se entrega, o checklist de verificação e o calendário desta turma.

**O TP2 pede quatro coisas.**

| O que o TP2 pede | Onde você aprende, e faz |
|---|---|
| 1. As interfaces do projeto: uma mensagem do seu domínio, um serviço de controle e uma ação | [tarefa da Aula 4](../../tutoriais/tarefa-aula04-interfaces.md) e [tarefa da Aula 5](../../tutoriais/tarefa-aula05-acoes.md) |
| 2. A ação central do projeto: o servidor, com feedback e cancelamento — e o cliente | hoje, e a [tarefa da Aula 6](../../tutoriais/tarefa-aula06-servidor-acao.md) |
| 3. Rastreamento em vídeo: YOLO, um filtro que suaviza a trajetória, a trilha e a caixa no quadro | Aula 7 |
| 4. Parâmetros num arquivo YAML, trocados com o sistema no ar — e o URDF do robô | Aula 3 (o YAML) e Aula 8 (o URDF) |

Quem está em dia com as tarefas chega à entrega com metade do TP2 pronta. Quem não está: a ordem é a da tabela, de cima para baixo.

**O que conferir.** As interfaces são do **seu** domínio (renomear o `pb_interfaces` não é adaptar). A ação é a tarefa **principal** do projeto: a que demora, e faz sentido interromper. O servidor dá feedback, pode ser cancelado, e rejeita algum pedido de propósito; o cliente mostra cada feedback e registra o resultado; e a prova pedida é **servidor e cliente rodando ao mesmo tempo, com captura de tela**. O detector roda sobre o **seu** objeto, a trajetória é suavizada por um filtro que você sabe nomear, e o rastreamento publica a sua mensagem em vez de viver isolado num script. Três parâmetros no YAML, e um deles trocado com o sistema no ar. O URDF, coerente e sem enfeite.

**O que se entrega.** No Moodle, a entrega **oficial**: o PDF do relatório, o ZIP do código e os links. No GitHub, complementar e **obrigatório**: `main`, a branch de entrega e a tag, como no TP1. As evidências numa pasta só, `docs/evidencias/tp2/`. A partir deste TP, uma entrega só no repositório, sem o Moodle, não é aceita.

**Onde gastar o tempo — e onde não.** Gaste numa ação que cancela de verdade, e num rastreamento que conversa com o resto do sistema. Não gaste treinando um modelo do zero, num URDF detalhado ou na estética do relatório. Não vai dar tempo de tudo? A regra é a do TP1: entregue o que funciona, e **declare** o que não funciona.

## A tarefa da semana

[Tarefa da Aula 6 — o servidor da sua ação](../../tutoriais/tarefa-aula06-servidor-acao.md), com o [guia de estudo da Aula 6](../../tutoriais/estudo-aula06-servidor-acao.md) antes dela.

**O que fazer.** O servidor e o cliente da ação do seu projeto — respondendo, e cancelando.

**O que usar.** O servidor e o cliente do exemplo `aula07-acoes`, copiados para o **seu** pacote pelo bloco do passo 1; e o seu pacote de interfaces, com a sua ação.

**Como adequar ao seu projeto.** Os campos da **sua** ação; o que o seu servidor rejeita; e o que faz a sua tarefa abortar.

**Como saber que terminou.** O seu cliente cancela, e o log do seu servidor mostra `cancelamento pedido - aceitando` — guardado em `docs/evidencias/tp2/acao-servidor.txt`, com a captura de tela de servidor e cliente juntos.

Antes dela vêm as duas partes da semana passada — o [pacote de interfaces](../../tutoriais/tarefa-aula04-interfaces.md) e o [arquivo da ação](../../tutoriais/tarefa-aula05-acoes.md): sem eles, não há servidor. Push na `dev` até domingo, 06/12.

### Desafio (opcional): o período do laço é uma decisão

O servidor do exemplo dorme 0,2 s por volta. Mude a constante `PERIODO_S` para `1.0`, e depois para `0.05`, e meça duas coisas em cada caso: a taxa do feedback (`ros2 topic hz /varrer_cena/_action/feedback`) e o maior atraso do cancelamento (no log do servidor, o horário da linha `cancelamento pedido` contra o da linha `CANCELADA`). Qual valor você escolheria para um robô que se move? E para um que só observa? Os comandos estão na [tarefa](../../tutoriais/tarefa-aula06-servidor-acao.md#desafio-opcional-o-periodo-do-laco-e-uma-decisao); traga os números, e a escolha para o **seu** projeto em uma frase.

## Socorro rápido

| Sintoma | O que fazer |
|---|---|
| `Package 'aula07_acoes' not found` | o exemplo não está compilado neste workspace, ou faltou o `source "$PB_WS/install/setup.bash"` **neste** terminal |
| o `grep -n "EXPERIMENTO"` mostra uma linha só, ou nenhuma | o arquivo já estava alterado: faça o `cp` do caso 3 e repita os dois `sed` |
| no caso 2, o resultado veio `cancelada em ...` | o servidor antigo ainda estava rodando: `Ctrl+C` no Terminal A, e o launch de novo |
| no caso 2, o resultado `abortada` veio antes do seu `Ctrl+C` | você esperou mais de três segundos; o defeito é o mesmo (`quadros=0`): o servidor ficou surdo até para a câmera |
| no caso 3, o `cp` diz `No such file or directory` | o `/tmp` foi limpo: refaça o [Pegar o material](#pegar-o-material) |
| depois da aula, o cancelamento parou de funcionar no exemplo | o arquivo ficou com as duas linhas trocadas: faça o `cp` do caso 3 |
| `Goal was rejected.` num pedido válido | já existe uma varredura em curso: espere a anterior terminar |
| `Goal finished with status: ABORTED`, sem você ter derrubado nada | o detector do caso 1 continua morto: `Ctrl+C` no Terminal A, e o launch de novo |
| `The passed action type is invalid` no `send_goal` | é o terminal: `source "$PB_WS/install/setup.bash"` |

Travou, e nada aqui bate? **Infnet.Online**, com três coisas: o comando exato, a saída completa e o passo em que você está.

## Próximo encontro: Aula 7, segunda 30/11

**O detector treinado — e o número que diz se ele presta.** O miolo da percepção troca: sai a segmentação por cor, entra um detector treinado, com rastreamento. A mensagem continua a mesma — foi para isso que ela veio antes. E aparece a pergunta que o TP2 faz a todo detector: quanto ele acerta, e quanto ele custa?
