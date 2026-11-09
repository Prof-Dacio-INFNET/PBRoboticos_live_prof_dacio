# Aula 4 — O seu TP1, conferido e entregue; e as interfaces do seu projeto

**Segunda, 09/11/2026 · Zoom · 1h30 · Etapa 3 (aula única) · turma live**

[:material-file-pdf-box: Slides da Aula 4 (PDF)](apresentacao-aula04.pdf){ .md-button .md-button--primary }
[:material-package-variant-closed: Checklist de entrega do TP1](../../tutoriais/checklist-entrega-tp1.md){ .md-button }
[:material-book-open-variant: Guia de estudo da Aula 4](../../tutoriais/estudo-aula04-interfaces.md){ .md-button }
[:material-code-tags: Exemplo `aula06-interfaces`](../../exemplos/aula06-interfaces/index.md){ .md-button }

## Como esta página funciona

A aula **demonstra**; a tarefa **executa**. Durante o encontro o professor roda tudo no repositório dele (`pb-live-dacioms`) e você observa e anota. Esta página guarda o que foi mostrado, na mesma ordem dos slides, e termina em [A tarefa da semana](#a-tarefa-da-semana), que é o que você roda no **seu** ambiente, passo a passo.

Sobre os blocos de comando: cada bloco diz, na primeira linha, **em qual terminal** ele roda, e pode ser **colado inteiro de uma vez**. Quando um comando ocupa o terminal (um `launch`, um `echo` sem `--once`), ele é o último do bloco, e o que vem depois vai para outro terminal. Abaixo de cada bloco, **Tem de aparecer** diz o que você deve ver.

## Cenas dos últimos episódios

**O que a Aula 3 deixou.** A imagem entrou no grafo: um nó publica `sensor_msgs/Image` em `/camera/image_raw`, com QoS de sensor. Outro nó transformou cor em contagem — HSV, máscara, contornos — e publicou um `Int32` em `/vision/contagem`. O serviço `/vision/status` respondeu a uma pergunta, no tipo pronto `std_srvs/Trigger`. A cor trocou com o sistema no ar (`ros2 param set`), sem recompilar nada. E a contagem caiu de 2 para 1 quando os objetos se encostaram: a oclusão. Na semana sem aula, a tarefa pediu as duas classes do **seu** domínio, os parâmetros em YAML e as evidências.

**As peças antigas que voltam hoje.**

| Peça | De onde vem | Onde entra hoje |
|---|---|---|
| Pacote `ament_python` | Aula 2 | ele ganha um vizinho, só de definições |
| Serviço: pergunta com resposta | Aula 2 | a resposta ganha campos com tipo |
| Todo tópico tem um **tipo** | Aula 2 | o tipo passa a ser seu |
| `source install/setup.bash` em cada terminal | Aula 2 | é ele que decide se a interface existe |
| Parâmetro fora do código | Aula 3 | o rótulo da classe entra por parâmetro |
| Oclusão | Aula 3 | ela aparece também como confiança caindo |

## A ideia em uma frase

Hoje o seu projeto **fecha uma entrega** — e para de falar a língua dos outros: a mensagem do seu sistema deixa de ser um número solto e passa a ter o vocabulário do seu domínio.

## O que você sai sabendo hoje, e o que isso vale no seu projeto

| Você sai sabendo | No seu projeto, isso vale |
|---|---|
| Conferir, com quatro comandos, se o seu TP1 mostra o que diz | você descobre hoje, e não no dia da entrega, o que falta mostrar |
| Escrever um relatório que responde a perguntas, em vez de narrar o mês | é nele que o **seu** domínio aparece — o código do exemplo é igual para todos |
| Entregar sem surpresa: `main`, `entrega-tp1`, a tag, o Moodle e a janela anônima | o que quem avalia não consegue abrir não existe |
| Dizer quando um tipo pronto basta, e quando o projeto precisa do próprio | a mensagem passa a dizer "2 tampas azuis", e não "2" |
| Criar, compilar e usar um `.msg` e um `.srv` num pacote de interfaces | é o contrato que o seu detector treinado vai reaproveitar |

## O que foi demonstrado, onde está na tarefa, e quando vence

Os gates e as datas são **referência para consulta** — estão em [TP1](../../recursos/tp1.md) e em [Gates de cada TP](../../recursos/gates-tps.md). O único prazo formal desta semana é a entrega do TP1 no Moodle.

| Demonstrado na aula | Na tarefa | Referência |
|---|---|---|
| As quatro perguntas ao sistema, e a taxa | parte 1, passo 1 | competências 1.1 e 1.2 · [TP1](../../recursos/tp1.md#checklist-de-verificacao-antes-de-entregar) |
| Caso 1: o projeto diz o que a câmera procura | parte 1, passo 2 | competência 1.1 · declaração do projeto |
| Caso 2: o `/vision/status` no vocabulário do domínio | parte 1, passo 2 | competência 1.3 |
| Caso 3: a resposta vira arquivo no repositório | parte 1, passos 1 e 2 | evidências em `docs/evidencias/tp1/` |
| A oclusão, observada e explicada | parte 1, passo 3 | competência 1.4 |
| O relatório em cinco perguntas | parte 1, passo 4 | relatório do TP1 |
| A entrega em quatro linhas, e a janela anônima | parte 1, passo 5 | **entrega: sexta, 13/11, no Moodle** |
| Os dois pacotes de interfaces, de ponta a ponta | parte 2 | começo do TP2 · push na `dev` até dom 22/11 |

## Pegar o material

```bash
# ── Terminal A · uma vez por terminal ─────────────────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"

# o material da disciplina (pode repetir sempre: a linha do rm evita o erro de pasta já existente)
rm -rf /tmp/PBRoboticos_live_prof_dacio
cd /tmp && git clone --depth 1 https://github.com/Prof-Dacio-INFNET/PBRoboticos_live_prof_dacio.git
ls /tmp/PBRoboticos_live_prof_dacio/exemplos/aula06-interfaces
```

**Tem de aparecer:** `README.md`, `aula06_percepcao` e `pb_interfaces`.

!!! warning "Se a sua taxa está em 5 Hz em vez de 15: o perfil do Fast DDS (corrige o que a página da Aula 3 dizia)"
    Numa máquina só, o ROS 2 Humble entrega as mensagens por **memória compartilhada**. Uma imagem de 640×480 pesa **0,92 MB**, e o segmento de memória padrão é pequeno para ela: quadros caem, sem mensagem de erro, e `/vision/contagem` fica em 5–7 Hz com buracos de até 0,8 s. A cura é um arquivo de perfil que aumenta esse segmento. **A cura por `sysctl` que estava na página da Aula 3 não resolve** — foi testada de novo e retirada; se você a aplicou, ela não atrapalha, só não ajuda.

    ```bash
    # ── qualquer terminal · uma vez por máquina ──────────
    mkdir -p "$HOME/.ros"
    cat > "$HOME/.ros/fastdds-imagem.xml" <<'EOF'
    <?xml version="1.0" encoding="UTF-8" ?>
    <profiles xmlns="http://www.eprosima.com/XMLSchemas/fastRTPS_Profiles">
      <transport_descriptors>
        <transport_descriptor>
          <transport_id>shm_imagem</transport_id>
          <type>SHM</type>
          <segment_size>4194304</segment_size>
        </transport_descriptor>
        <transport_descriptor>
          <transport_id>udp_padrao</transport_id>
          <type>UDPv4</type>
        </transport_descriptor>
      </transport_descriptors>
      <participant profile_name="pb_imagem" is_default_profile="true">
        <rtps>
          <userTransports>
            <transport_id>shm_imagem</transport_id>
            <transport_id>udp_padrao</transport_id>
          </userTransports>
          <useBuiltinTransports>false</useBuiltinTransports>
        </rtps>
      </participant>
    </profiles>
    EOF
    grep -q FASTRTPS_DEFAULT_PROFILES_FILE "$HOME/.bashrc" || echo 'export FASTRTPS_DEFAULT_PROFILES_FILE="$HOME/.ros/fastdds-imagem.xml"' >> "$HOME/.bashrc"
    export FASTRTPS_DEFAULT_PROFILES_FILE="$HOME/.ros/fastdds-imagem.xml"
    ```

    A variável precisa estar definida **no terminal que sobe o launch** (terminais novos já a recebem do `~/.bashrc`). Suba o launch de novo e meça: no ensaio do professor, em Ubuntu 22.04 com ROS 2 Humble, a taxa foi de 5,7 Hz para **15,0 Hz**. Se na sua máquina ela continuar baixa, **meça, registre e explique** no relatório: taxa baixa medida e explicada é uma resposta válida; taxa baixa escondida, não.

## Bloco 1 — O seu TP1, conferido e entregue

### O sistema no ar, e quatro perguntas

O que o TP1 mostra, em capacidades: o ambiente funciona, e você sabe dizer quem publica, quem assina e quem serve; a imagem circula no grafo, e a taxa está medida e explicada; um nó segmenta o **seu** objeto por cor, conta, e responde ao `/vision/status`; o OpenCV básico aparece (cores e contornos, e faces/features como demonstração); e tudo isso é sobre um projeto declarado. O detalhe de cada item está na [página do TP1](../../recursos/tp1.md).

```bash
# ── Terminal A · o sistema no ar (este comando ocupa o terminal) ──
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"
source /opt/ros/humble/setup.bash
source "$PB_WS/install/setup.bash"
ros2 launch aula03_visao visao.launch.py     # no seu projeto: o SEU pacote e o SEU launch
```

**Tem de aparecer:** `Publicando /camera/image_raw · fonte=sintetico · 640x480 @15fps` e `Segmentador no ar: /camera/image_raw -> /vision/segmented + /vision/contagem · serviço /vision/status`.

```bash
# ── Terminal B · quatro perguntas ao sistema ──────────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"
source /opt/ros/humble/setup.bash
source "$PB_WS/install/setup.bash"
ros2 node list                                               # quem está no ar
ros2 topic echo /vision/contagem --once                      # o que ele vê
ros2 service call /vision/status std_srvs/srv/Trigger "{}"   # o que ele responde
timeout 10 ros2 topic hz /vision/contagem                    # a que taxa (encerra sozinho em 10 s)
```

**Tem de aparecer:** os dois nós (`/publicador_camera` e `/segmentador_hsv`); `data: 2`; `success=True, message='2 objeto(s) no ultimo frame (NNN frames processados)'`; e `average rate:` perto de 15. Se o `echo` responder `Could not determine the type`, o sistema ainda não terminou de subir: espere dois segundos e repita.

São as quatro respostas que o relatório cita — e cada uma pode virar um arquivo no repositório (é o caso 3).

### Caso 1 — o projeto diz o que a câmera procura

Uma classe só esconde o problema: com uma classe, qualquer limiar que detecte alguma coisa parece funcionar. Quem decide as duas é o **domínio** — maduro e verde no pomar, tampa azul e tampa verde na triagem, capacete e colete na obra. A declaração fica no topo do `PROJETO.md` (o bloco para preencher está na [página do TP1](../../recursos/tp1.md#a-declaracao-do-g11-cole-no-topo-do-projetomd)):

```markdown
<!-- PB:PROJETO -->
**Domínio:** colheita em pomar de tomate, setor 3
**Usuário:** o encarregado da colheita, que decide quando colher cada fileira
**Classes percebidas no TP1:** classe A = tomate maduro · classe B = tomate verde
**Fonte de imagem no TP1:** cena sintética com as duas classes; a webcam entra depois
<!-- PB:TRILHA -->
**Trilha:** S (simulada), com a webcam como único elemento real mais adiante
**Plano B:** se a câmera falhar na semana da entrega, cena sintética e um vídeo gravado
```

Sem câmera, a cena sintética editada vale para o TP1 inteiro — dito no relatório.

### Caso 2 — o `/vision/status` no vocabulário do domínio

O serviço do exemplo responde `'2 objeto(s) no ultimo frame'`. O do seu projeto diz **de quem** é o problema e **o que** a câmera procura. São quatro linhas a mais, em `segmentador_hsv.py` (no seu pacote, o arquivo equivalente):

```python
        self.declare_parameter('dominio', 'pomar setor 3')     # de quem é o problema
        self.declare_parameter('rotulo', 'tomate maduro')      # o que a câmera procura
        ...
    def on_status(self, req, resp):
        resp.success = self.frames > 0
        dominio = self.get_parameter('dominio').value
        rotulo = self.get_parameter('rotulo').value
        resp.message = (f'{dominio}: {self.ultima_contagem} {rotulo} no ultimo frame '
                        f'({self.frames} frames processados)')
        return resp
```

O domínio e o rótulo são **parâmetros**: a mesma função serve ao pomar e ao estoque, sem editar o código. Depois de salvar, `Ctrl+C` no Terminal A e o launch de novo — com `--symlink-install` não é preciso recompilar. E a prova:

```bash
# ── Terminal B · com o Terminal A no ar ───────────────
ros2 service call /vision/status std_srvs/srv/Trigger "{}"
ros2 param set /segmentador_hsv dominio "estoque doca 2"
ros2 param set /segmentador_hsv rotulo "caixa vermelha"
ros2 service call /vision/status std_srvs/srv/Trigger "{}"
```

**Tem de aparecer:** `message='pomar setor 3: 2 tomate maduro no ultimo frame (...)'` na primeira chamada; `Set parameter successful` duas vezes; e `message='estoque doca 2: 2 caixa vermelha no ultimo frame (...)'` na segunda.

Repare no incômodo que sobra: o `2` continua **dentro de uma frase**. Quem chama precisa ler texto para achar o número. É esse incômodo que o bloco 2 resolve.

### Caso 3 — o terminal fecha, o repositório fica

O sinal `>` grava a resposta num arquivo. Evidência que ficou só no terminal não existe para quem avalia.

```bash
# ── Terminal B · com o Terminal A no ar ───────────────
: "${PB_DIR:?defina PB_USER, PB_DIR e PB_WS — o bloco está em Pegar o material}"
cd "$PB_DIR" && mkdir -p docs/evidencias/tp1
ros2 service call /vision/status std_srvs/srv/Trigger "{}" > docs/evidencias/tp1/status.txt
timeout 10 ros2 topic hz /vision/contagem > docs/evidencias/tp1/topic-hz.txt
ls docs/evidencias/tp1/
git add -A
git commit -m "TP1: evidencias do status e da taxa"
git push origin dev
```

**Tem de aparecer:** `status.txt` e `topic-hz.txt` na listagem (a medição da taxa leva dez segundos e não imprime nada na tela), o commit e o push para a `dev`. Prints (o grafo do `rqt_graph`, a imagem segmentada) vão para a mesma pasta. A regra: **um arquivo para cada afirmação do relatório**.

### A oclusão: observar, e não consertar

```bash
# ── Terminal B · com o Terminal A no ar (ocupa o terminal; saia com Ctrl+C) ──
ros2 topic echo /vision/contagem
```

**Tem de aparecer:** uma sequência de `data: 2` e, a cada poucos segundos, um trecho de `data: 1` — os dois objetos se encostando. Ninguém saiu de cena: o sistema é que perdeu a capacidade de distinguir. No relatório, um print desse momento e três linhas: o que aconteceu, por quê, e o que isso significa no **seu** domínio (dois tomates encostados virando um: a contagem da colheita erra para menos).

### O relatório responde a cinco perguntas

Quem trava no relatório quase sempre tentou narrar o mês. Não é isso: são cinco perguntas. O modelo (`docs/relatorios/relatorio-template.md`, no seu repositório) tem oito seções; a tabela diz em qual delas cada pergunta se responde.

| A pergunta | Onde se responde no modelo | Uma frase de exemplo |
|---|---|---|
| Que problema, de quem — e por que este, e não outro? | Objetivo · Projeto | "O encarregado decide a colheita no olho; o sistema conta maduros e verdes por fileira." |
| O que você escolheu, e o que **descartou**? | Desenvolvimento por tarefa · Arquitetura ROS 2 | "Fonte sintética no TP1: a webcam pelo usbipd caía a 3 quadros por segundo." |
| O que os números dizem? | Resultados e evidências | "15,0 Hz na saída, igual à entrada; a contagem cai para 1 na oclusão (`contagem.png`)." |
| O que o sistema **não** faz? | Problemas e soluções · Próximos passos | "A segmentação por cor confunde tomate maduro com um pano vermelho ao fundo." |
| O que a IA gerou, o que você revisou, o que você sabe explicar? | Referências (declaração de uso de IA) | "O esqueleto do launch foi gerado; os limiares HSV foram medidos por mim." |

A quarta é a que mais gente pula e a que mais mostra entendimento. O arquivo do relatório é `docs/relatorios/relatorio-tp1.md`; o PDF que vai ao Moodle sai dele.

### A entrega, em quatro linhas

```bash
# ── Terminal B · na pasta do projeto, com tudo commitado · UMA LINHA POR VEZ ──
: "${PB_DIR:?defina PB_USER, PB_DIR e PB_WS — o bloco está em Pegar o material}"
cd "$PB_DIR"
git checkout main && git merge dev && git push origin main                            # 1) a main recebe o trabalho
git checkout entrega-tp1 && git merge --ff-only main && git push origin entrega-tp1   # 2) entrega-tp1 = main
git tag -a tp1 -m "Entrega do TP1" && git push origin tp1                             # 3) a marca do commit avaliado
git checkout dev                                                                      # 4) de volta ao trabalho
git archive --format=zip --prefix=tp1/ -o "$HOME/tp1-codigo.zip" tp1                  # o ZIP do código
unzip -l "$HOME/tp1-codigo.zip" | tail -3
```

**Tem de aparecer:** `Fast-forward` nas duas primeiras; `* [new tag] tp1 -> tp1` na terceira; e, no fim, o total de arquivos do ZIP — sem `build/`, `install/`, `log/` nem `.git/`, porque o `git archive` só empacota o que está versionado.

A entrega **oficial** é no **Moodle**: o PDF do relatório, o ZIP do código e os links. O GitHub é **complementar e obrigatório**, e a tag marca o commit que será corrigido. A branch `entrega-tp1` já existe desde o `init-branches.sh`: é `checkout`, e não `checkout -b`. O passo a passo completo está no [checklist de entrega do TP1](../../tutoriais/checklist-entrega-tp1.md).

### Antes de enviar: quem avalia consegue abrir?

O ZIP tem o código, e não tem `build/`, `install/`, `log/` nem `.git/`. O PDF mostra as imagens (referência quebrada vira espaço em branco). O vídeo tem até 5 minutos e é público ou não listado — nunca privado. **Uma janela anônima, e um clique em cada link do relatório.** O repositório é o `pb-live-<usuario>` da organização, com o convite aceito; ele é privado, e é para ser — quem precisa abrir é o professor.

### Não vai dar tempo de tudo?

Entregue o que funciona e **declare** o que não funciona. Reduza o escopo sem abandonar o item (cena menor, fonte sintética), escreva a limitação com as suas palavras, e entregue no prazo. A [escada de recuperação](../../tutoriais/checklist-entrega-tp1.md#escada-de-recuperacao-se-algo-nao-vai-dar-tempo) tem a ordem.

## Bloco 2 — Quando a mensagem pronta acaba

### Dois. Dois o quê?

```bash
# ── Terminal B · com o Terminal A no ar ───────────────
ros2 topic echo /vision/contagem --once
ros2 interface show std_msgs/msg/Int32
```

**Tem de aparecer:** `data: 2`; e, no segundo, quatro linhas de comentário — a terceira diz *"It is recommended to create your own semantically meaningful message"* — seguidas de `int32 data`.

Dois de que classe? Com que certeza? Onde na imagem? De que instante? O segmentador conhece a posição, a área e o contorno de cada objeto — e joga tudo fora na hora de publicar, porque o tipo só tem lugar para um inteiro. Não é limite do ROS 2: é escolha de tipo, e o próprio `Int32` recomenda, no comentário, criar uma mensagem com significado.

### Tipo pronto, tipo próprio — e o atalho que cobra depois

Tipo pronto (`Int32`, `Trigger`, `Image`) está certo enquanto a pergunta é simples: para "quantos?", `Int32` continua sendo a resposta. Tipo próprio vale quando **três ou mais campos andam sempre juntos**, ou quando dois tópicos só fazem sentido lidos ao mesmo tempo. Ele custa: um pacote a mais, um build a mais, e uma dependência para quem usar o seu nó. O atalho — JSON dentro de uma `String` — funciona, e perde a conferência de tipo, a inspeção (`ros2 interface show`) e o lado C++.

Para o seu projeto, a pergunta é: **o que o seu nó sabe sobre cada objeto, e hoje não conta para ninguém?** Cada resposta é um campo da sua mensagem.

### Dois pacotes, lado a lado

```text
ros2_ws/src/
|-- pb_interfaces/            ament_cmake: SÓ definições, nenhum nó
|   |-- msg/Deteccao.msg
|   |-- msg/Deteccoes.msg
|   |-- srv/StatusVisao.srv
|   |-- CMakeLists.txt        a lista do que gerar
|   `-- package.xml           as três linhas do rosidl
`-- aula06_percepcao/         ament_python: os nós, como desde a Aula 2
    |-- aula06_percepcao/detector.py
    |-- aula06_percepcao/monitor.py
    `-- package.xml           <depend>pb_interfaces</depend>
```

Gerar interface é **gerar código**: o ROS 2 lê o `.msg` e escreve as classes em Python e em C++. Quem faz isso é o `rosidl`, que roda num pacote `ament_cmake` — o pacote Python dos seus nós não tem essa maquinaria. É assim que o `sensor_msgs` chega até você.

Três linhas do `package.xml` fazem o pacote gerar código. Sem elas ele compila, não reclama — e não gera nada:

```xml
<buildtool_depend>rosidl_default_generators</buildtool_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```

E cada arquivo novo entra na lista do `CMakeLists.txt` (no exemplo, a lista traz também uma mensagem e uma ação da próxima aula):

```cmake
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Deteccao.msg"
  "msg/Deteccoes.msg"
  "srv/StatusVisao.srv"
  DEPENDENCIES std_msgs
)
```

Criou um `.msg` e ele "não existe"? Faltou a linha aqui. O `std_msgs` aparece nos **dois** arquivos — no `package.xml` e em `DEPENDENCIES` —, por causa do `Header`.

### Uma detecção, e o quadro inteiro

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
```

Tipo, nome e comentário — e mensagens se compõem: um campo pode ser outra mensagem sua, e `[]` faz o array. O `Header` não é enfeite: sem o `stamp` não se sabe se a detecção é de agora ou de três segundos atrás. No seu projeto: troque o vocabulário, e acrescente o campo que só o seu domínio pede.

### A mesma pergunta, com vocabulário próprio

```bash
# ── Terminal B ────────────────────────────────────────
ros2 interface show std_srvs/srv/Trigger
cat /tmp/PBRoboticos_live_prof_dacio/exemplos/aula06-interfaces/pb_interfaces/srv/StatusVisao.srv
```

**Tem de aparecer:** no `Trigger`, os três traços e, abaixo, `bool success` e `string message`; no `StatusVisao`, os três traços e cinco campos — `ativo`, `classe_alvo`, `total_detectado`, `confianca_media`, `mensagem`.

Os três traços separam a pergunta da resposta. O `Trigger` diz "estou vivo". O `StatusVisao` diz **o que** está sendo visto, em campos com tipo: o `2` que estava preso na frase agora é `total_detectado`.

E onde o serviço deixa de servir: quem chama fica esperando. Para "qual o seu estado?", ótimo; para "varra a cena e me avise quando terminar", péssimo. Tarefa longa, com progresso e cancelamento, é **ação** — a próxima aula.

## Bloco 3 — Os dois pacotes, de ponta a ponta

### Copiar e compilar, na ordem

```bash
# ── Terminal B · UMA LINHA POR VEZ a partir do colcon ──
: "${PB_WS:?defina PB_USER, PB_DIR e PB_WS — o bloco está em Pegar o material}"
cp -r /tmp/PBRoboticos_live_prof_dacio/exemplos/aula06-interfaces/pb_interfaces "$PB_WS/src/"
cp -r /tmp/PBRoboticos_live_prof_dacio/exemplos/aula06-interfaces/aula06_percepcao "$PB_WS/src/"
cd "$PB_WS"
colcon build --packages-select pb_interfaces
source install/setup.bash
colcon build --packages-select aula06_percepcao --symlink-install
source install/setup.bash
```

**Tem de aparecer:** `Finished <<< pb_interfaces [10.5s]` (de dez a quinze segundos: é o CMake gerando código Python e C++ a partir dos arquivos de texto) e `Finished <<< aula06_percepcao [1.2s]`. O `source` do meio é o que faz o segundo pacote enxergar o primeiro. No dia a dia, `colcon build --symlink-install` sem selecionar nada compila tudo e acerta a ordem sozinho, porque o `package.xml` declara a dependência.

### Três mensagens, e o que cada uma pede

| A mensagem | O que aconteceu | O que fazer |
|---|---|---|
| `Check that the following packages have been built: - pb_interfaces` | os nós foram compilados **antes** das interfaces | compile `pb_interfaces`, dê `source`, compile os nós |
| `Package 'aula06_percepcao' not found ... searching: ['.../install/aula03_visao', '/opt/ros/humble']` | este terminal fez o `source` **antes** do build — a lista mostra onde ele procurou | `source "$PB_WS/install/setup.bash"` neste terminal |
| `ModuleNotFoundError: No module named 'pb_interfaces'` | o nó importa a interface, mas o terminal é antigo — ou falta `<depend>pb_interfaces</depend>` no `package.xml` dos nós | terminal novo, com os dois `source`; confira o `package.xml` |

As três têm a mesma cura em ordem diferente: interfaces compiladas, e `source` feito **depois**, neste terminal.

### O teste de fumaça

```bash
# ── Terminal B · o mesmo do build ─────────────────────
ros2 interface list | grep pb_interfaces
ros2 interface show pb_interfaces/msg/Deteccoes
```

**Tem de aparecer:** cinco linhas no primeiro (`msg/ComandoMovimento`, `msg/Deteccao`, `msg/Deteccoes`, `srv/StatusVisao` e `action/VarrerCena` — a primeira e a última são da próxima aula); e, no segundo, o `Header`, o array `Deteccao[] deteccoes` com os campos abertos logo abaixo, e `uint32 total`. Se a lista mostra, o ROS 2 enxerga a interface. Se vier vazia: faltou o `source`, ou faltam as três linhas do `package.xml`.

### Rodar, e ler a mensagem nova

```bash
# ── Terminal A · Ctrl+C no launch da Aula 3, e então (ocupa o terminal) ──
source "$PB_WS/install/setup.bash"
ros2 launch aula06_percepcao percepcao.launch.py classe:=tomate_maduro
```

**Tem de aparecer:** `detector no ar - classe='tomate_maduro'` e, em seguida, uma linha do monitor por quadro: `t=...  total=2  tomate_maduro(0.98) em (261,333) area=1450 | tomate_maduro(0.99) em (512,216) area=3524`. Cada linha é uma mensagem: a classe, a confiança, a posição e a área de cada objeto — tudo o que o `Int32` jogava fora. A classe entrou por parâmetro, no launch.

```bash
# ── Terminal B · com o Terminal A no ar ───────────────
ros2 topic echo /vision/deteccoes --once
ros2 service type /vision/status
ros2 service call /vision/status pb_interfaces/srv/StatusVisao "{}"
```

**Tem de aparecer:** o `header`, o array `deteccoes` com dois itens e `total: 2`; depois `pb_interfaces/srv/StatusVisao`; e por fim `ativo=True, classe_alvo='tomate_maduro', total_detectado=2, confianca_media=0.98..., mensagem="vendo 2 'tomate_maduro' na cena"`. O **nome** do serviço é o mesmo da primeira metade; o que mudou foi o **tipo**. Isso é uma migração, e é o coração da parte 2 da tarefa. Se o `service type` mostrar dois tipos, o launch da Aula 3 ainda está no ar em algum terminal.

### Quem consome a interface

Em `aula06_percepcao/detector.py`, a interface é um `import` como outro qualquer — e é esse `import` que falha quando falta o `source`:

```python
from pb_interfaces.msg import Deteccao, Deteccoes
from pb_interfaces.srv import StatusVisao
...
        self.pub = self.create_publisher(Deteccoes, '/vision/deteccoes', 10)
        self.srv = self.create_service(StatusVisao, '/vision/status', self.responder_status)
```

A confiança deste exemplo é a **solidez** do contorno (a área dividida pela área do fecho convexo): não é probabilidade, e o código diz isso no comentário. Quando os objetos se encostam, o monitor mostra `total=1  tomate_maduro(0.89) em (450,290) area=4965`: a contagem cai, **e a confiança cai junto**. Um detector treinado produz esse sinal de forma direta — e usa a **mesma** mensagem. Trocar o miolo sem trocar o contrato: é por isso que a interface vem antes do detector.

## A tarefa da semana

A tarefa tem duas partes, **nesta ordem**. A parte 1 é a entrega do TP1. A parte 2 começa depois dela.

### Parte 1 — a entrega do TP1, em ordem

**O que fazer:** entregar o TP1 — no Moodle (oficial) e no GitHub (complementar e obrigatório). **O que usar:** o seu repositório `pb-live-<usuario>`, os blocos desta página e o [checklist de entrega](../../tutoriais/checklist-entrega-tp1.md). **Como adequar ao seu projeto:** onde os blocos dizem `aula03_visao`, entra o **seu** pacote; onde dizem tomate, entra o **seu** objeto. **Como saber que terminou:** o bloco do passo 5 responde sem pendências, e o Moodle mostra o envio concluído.

**Passo 1 — as quatro perguntas, no SEU sistema, com as respostas guardadas.** Suba o seu launch no Terminal A (o bloco de [O sistema no ar](#o-sistema-no-ar-e-quatro-perguntas), com o seu pacote). Depois:

```bash
# ── Terminal B · com o SEU launch no ar no Terminal A ──
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"
source /opt/ros/humble/setup.bash
source "$PB_WS/install/setup.bash"
cd "$PB_DIR" && mkdir -p docs/evidencias/tp1
bash scripts/check-ambiente.sh                              > docs/evidencias/tp1/check-ambiente.txt
ros2 node list                                              > docs/evidencias/tp1/node-list.txt
ros2 service call /vision/status std_srvs/srv/Trigger "{}"  > docs/evidencias/tp1/status.txt
timeout 10 ros2 topic hz /vision/contagem                   > docs/evidencias/tp1/topic-hz.txt
tail -n 3 docs/evidencias/tp1/check-ambiente.txt docs/evidencias/tp1/status.txt docs/evidencias/tp1/topic-hz.txt
```

**Tem de aparecer:** `✅ Tudo pronto!` no fim do `check-ambiente.txt`; a resposta do serviço; e `average rate:` no `topic-hz.txt`. Os prints do grafo (`rqt_graph.png`) e da imagem segmentada (`segmentacao.png`) vão para a mesma pasta.

**Passo 2 — os três casos, conferidos no SEU repositório.**

```bash
# ── Terminal B · herda PB_USER, PB_DIR e PB_WS do passo 1 ──
: "${PB_DIR:?defina PB_USER, PB_DIR e PB_WS — o bloco está no passo 1}"
cd "$PB_DIR"
grep -n "Classes percebidas" PROJETO.md      # caso 1: duas classes, do SEU domínio
cat docs/evidencias/tp1/status.txt           # caso 2: a resposta fala do SEU domínio?
ls docs/evidencias/tp1/                      # caso 3: um arquivo para cada afirmação
```

**Tem de aparecer:** a linha das classes com **duas**; uma resposta que não seja `objeto(s)`; e os arquivos. O que faltar, você corrige agora — os blocos de cada caso estão acima.

**Passo 3 — a oclusão.** Rode o bloco de [A oclusão](#a-oclusao-observar-e-nao-consertar), tire um print no momento em que a contagem cai, salve em `docs/evidencias/tp1/oclusao.png` e escreva as três linhas no relatório.

**Passo 4 — o relatório.**

```bash
# ── Terminal B · herda PB_USER, PB_DIR e PB_WS do passo 1 ──
: "${PB_DIR:?defina PB_USER, PB_DIR e PB_WS — o bloco está no passo 1}"
cd "$PB_DIR"
[ -f docs/relatorios/relatorio-tp1.md ] || cp docs/relatorios/relatorio-template.md docs/relatorios/relatorio-tp1.md
ls -l docs/relatorios/
```

Escreva pelas [cinco perguntas](#o-relatorio-responde-a-cinco-perguntas), cite cada evidência pelo nome do arquivo, e faça commit: `git add -A && git commit -m "TP1: relatorio" && git push origin dev`.

**Passo 5 — a entrega, e a prova de que ela saiu.** Rode o bloco de [A entrega, em quatro linhas](#a-entrega-em-quatro-linhas). Depois:

```bash
# ── Terminal B · herda PB_USER, PB_DIR e PB_WS do passo 1 ──
: "${PB_DIR:?defina PB_USER, PB_DIR e PB_WS — o bloco está no passo 1}"
cd "$PB_DIR"
git status --short                    # nada: está tudo commitado
git tag --list                        # tp1
git ls-remote --tags origin           # refs/tags/tp1 e refs/tags/tp1^{}   (a tag chegou ao GitHub)
git log --oneline -1 entrega-tp1      # o mesmo commit da linha tp1^{}
```

**Tem de aparecer:** nada no primeiro; `tp1` no segundo; duas linhas no terceiro, `refs/tags/tp1` e `refs/tags/tp1^{}` (a segunda é o commit para o qual a tag aponta — o mesmo do quarto comando). No **Moodle**: o PDF, o ZIP e os links, com o envio **concluído** (não em rascunho), e cada link testado em janela anônima.

### Parte 2 — depois da entrega: as interfaces do seu projeto

[Tarefa da Aula 4 — as interfaces do seu projeto](../../tutoriais/tarefa-aula04-interfaces.md), com o [guia de estudo](../../tutoriais/estudo-aula04-interfaces.md) ao lado. **O que fazer:** o seu `<projeto>_interfaces`, com um `.msg` e um `.srv` do seu domínio. **O que usar:** o `pb_interfaces` do exemplo, copiado e renomeado em três lugares. **Como adequar:** troque o vocabulário, e acrescente o campo que só o seu domínio pede. **Como saber que terminou:** `ros2 interface list` mostra o seu pacote, e `ros2 service type /vision/status` mostra o tipo novo. Push na `dev` até domingo, 22/11.

**Antes da entrega do TP1, não mexa nisso:** nada desta parte entra nela, e migrar um tipo na semana da entrega é o jeito mais fácil de quebrar o que funciona.

### Desafio (opcional): quanto pesa informar, em vez de mostrar?

Com o launch da Aula 4 no ar, meça a banda dos dois tópicos — a imagem e as detecções:

```bash
# ── Terminal B · com o launch da Aula 4 no ar · cada linha encerra sozinha em 10 s ──
timeout 10 ros2 topic bw /vision/deteccoes
timeout 10 ros2 topic bw /camera/image_raw
```

Quantas vezes uma é maior do que a outra? E o que isso muda numa rede sem fio, entre o robô e a base? Traga o número na próxima aula. (Se o seu launch não publica `/camera/image_raw`, meça o tópico de imagem que ele publicar — `ros2 topic list` mostra.)

## Socorro rápido

| Sintoma | O que fazer |
|---|---|
| `Could not determine the type for the passed topic` | o sistema ainda está subindo: espere dois segundos e repita |
| `ros2 param set` responde `Node not found` | confira o nome com `ros2 node list`; se o nó está lá, `ros2 daemon stop` e repita |
| `/vision/contagem` a 5–7 Hz, com buracos | o perfil do Fast DDS, em [Pegar o material](#pegar-o-material); a variável tem de estar definida no terminal do launch |
| `git checkout -b entrega-tp1` diz que a branch já existe | ela existe desde o `init-branches.sh`: use `git checkout entrega-tp1` |
| `git merge --ff-only main` falha | houve commit direto na `entrega-tp1`: volte para a `dev` e leve ao Infnet.Online a saída de `git log --oneline --graph --all -8` |
| `tag 'tp1' already exists` | a tag já foi criada. Para refazer **antes do prazo**: `git tag -d tp1 && git push origin :refs/tags/tp1`, e crie de novo |
| `Check that the following packages have been built: - pb_interfaces` | compile as interfaces primeiro, dê `source`, e só então os nós |
| `Package 'aula06_percepcao' not found` | faltou o `source "$PB_WS/install/setup.bash"` **neste** terminal, depois do build |
| `ModuleNotFoundError: No module named 'pb_interfaces'` | terminal antigo, ou falta `<depend>pb_interfaces</depend>` no `package.xml` dos nós |
| o pacote compila, mas `ros2 interface list` não mostra nada | faltam as três linhas do `package.xml`, ou o arquivo não está na lista do `CMakeLists.txt` |
| o `Header` não resolve na compilação | `<depend>std_msgs</depend>` no `package.xml` **e** `DEPENDENCIES std_msgs` no `CMakeLists.txt` |
| `ros2 service type /vision/status` mostra dois tipos | os launches da Aula 3 e da Aula 4 estão no ar ao mesmo tempo: feche o antigo |

Travou, e nada aqui bate? **Infnet.Online**, com três coisas: o comando exato, a saída completa e o passo em que você está.

## Próximo encontro: Aula 5, segunda 16/11

**Ações: a tarefa que demora, avisa do progresso e pode ser cancelada** — a terceira forma de comunicação do ROS 2, e a que descreve quase tudo o que um robô faz. Ela entra no pacote de interfaces que você cria na parte 2 da tarefa. Antes disso, uma coisa só: o TP1 entregue.
