# Guia de estudo — Aula 4: as interfaces do seu projeto

**Semana de 09/11 a 22/11 · Etapa 3 · turma live.** A aula de 1h30 teve duas metades: o TP1 conferido e entregue, e as interfaces próprias. **Este guia é só sobre a segunda metade — e começa depois da entrega do TP1.** Até **13/11**, o que vale é o [checklist de entrega do TP1](checklist-entrega-tp1.md). Depois, ele é guiado pela [tarefa da Aula 4](tarefa-aula04-interfaces.md) (prazo **domingo 22/11**, push na `dev`). Tempo total: **2h a 3h**, em duas sessões.

| Sessão | O quê | Tempo | Resultado |
|---|---|---|---|
| 1 (fim de semana 14–15/11) | Seções 1 e 2 — ler, reproduzir os dois pacotes do exemplo com as saídas esperadas | 60–80 min | `pb_interfaces` e `aula06_percepcao` compilando no **seu** repositório; `interface show` funcionando |
| 2 (semana de 16/11) | Seção 3 (anatomia dos dois pacotes) + passos 1–5 da tarefa | 60–90 min | o seu `<projeto>_interfaces`; `/vision/status` migrado; `/vision/deteccoes` publicando |
| — | Seção 4 (autoavaliação) antes do push | 10 min | commit na `dev` até 22/11 |

!!! tip "Como pedir ajuda"
    No Infnet.Online, com quatro itens: o **comando exato**, a **saída completa**, `lsb_release -a` e a saída de `ros2 interface list | grep <seuprojeto>`. Antes disso, a seção 5 ("Se travar") — o primeiro sintoma dela resolve 90% dos casos.

---

## Cenas dos últimos episódios

Desde a Aula 2 os seus nós vivem num pacote `ament_python`, todo tópico tem um **tipo**, e cada terminal precisa do `source install/setup.bash`. Na Aula 3 o sistema publicou um `Int32` em `/vision/contagem` e respondeu ao `/vision/status` com um `Trigger` — e sobrou um incômodo: o número ficou preso dentro de uma frase. Na Aula 4 o professor mostrou a saída: um pacote só de definições (`pb_interfaces`) ao lado do pacote dos nós (`aula06_percepcao`). Aqui você reproduz isso no seu repositório.

Sobre os blocos de comando: cada bloco diz, na primeira linha, em qual terminal roda, e pode ser colado inteiro. Comando que ocupa o terminal é o último do bloco.

## 1. Leia antes (30 min)

| Fonte | O quê | Minutos | Depois você responde |
|---|---|---|---|
| [Página da Aula 4](../aulas/etapa03-aula04/index.md) | Blocos 2 e 3 | 10 | quando vale criar uma interface própria; por que o pacote é separado; o que o `Header` carrega |
| [README do exemplo `aula06-interfaces`](../exemplos/aula06-interfaces/index.md) | inteiro | 8 | o que cada um dos dois pacotes contém; o que é a "confiança" do exemplo |
| Docs do Humble — [Creating custom msg and srv files](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html) | até "Test the new interfaces" | 12 | o que `rosidl_generate_interfaces` faz; por que `ament_cmake`; os tipos primitivos permitidos num `.msg` |

Os dois conceitos que organizam tudo. **Interface é contrato gerado**: o `.msg` vira código C++ e Python pelo `rosidl`, dentro de um pacote `ament_cmake` separado — por isso ele é compilado antes e tem `source` antes de qualquer nó que o importe. **Tipo pronto é a resposta certa até deixar de ser**: `Int32` para "quantos?"; interface própria quando três ou mais campos andam sempre juntos; JSON dentro de `String` nunca.

## 2. Reproduza o exemplo, passo a passo (40 min)

Você trabalha **no seu repositório**, na branch `dev`, e nunca dentro do repositório do material. Com o TP1 já entregue e a tag `tp1` empurrada:

```bash
# ── Terminal B · uma vez por terminal ─────────────────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"
source /opt/ros/humble/setup.bash

cd "$PB_DIR" && git checkout dev && git pull
rm -rf /tmp/PBRoboticos_live_prof_dacio
cd /tmp && git clone --depth 1 https://github.com/Prof-Dacio-INFNET/PBRoboticos_live_prof_dacio.git
cp -r /tmp/PBRoboticos_live_prof_dacio/exemplos/aula06-interfaces/pb_interfaces \
      /tmp/PBRoboticos_live_prof_dacio/exemplos/aula06-interfaces/aula06_percepcao "$PB_WS/src/"
ls "$PB_WS/src/pb_interfaces" "$PB_WS/src/aula06_percepcao"
```

Esperado: `pb_interfaces/`: `CMakeLists.txt  action  msg  package.xml  srv` — repare que **não há código**, só definições. `aula06_percepcao/`: `aula06_percepcao  config  launch  package.xml  resource  setup.cfg  setup.py` — a mesma anatomia dos pacotes das Aulas 2 e 3.

**2.1 — Compilar na ordem certa.**

```bash
# ── Terminal B · herda as variáveis do bloco acima · UMA LINHA POR VEZ ──
: "${PB_WS:?defina PB_USER, PB_DIR e PB_WS — o bloco está no começo da seção 2}"
cd "$PB_WS"
colcon build --packages-select pb_interfaces
source install/setup.bash
colcon build --packages-select aula06_percepcao --symlink-install
source install/setup.bash
```

Esperado: `Finished <<< pb_interfaces [10.5s]` (de dez a quinze segundos, mais em máquina lenta: é o CMake gerando código, e por isso demora mais do que um pacote Python) e depois `Finished <<< aula06_percepcao [1.2s]`.

Agora conheça, de propósito, as **três mensagens** de quando a ordem sai errada — elas dizem o que falta, e vale tê-las visto uma vez:

| A mensagem | Como provocar | O que ela pede |
|---|---|---|
| `Check that the following packages have been built: - pb_interfaces` | apague `build/pb_interfaces` e `install/pb_interfaces`, abra um terminal novo e compile só o `aula06_percepcao` | interfaces primeiro, `source`, depois os nós |
| `Package 'aula06_percepcao' not found ... searching: [...]` | rode o launch num terminal que fez o `source` **antes** do build | `source "$PB_WS/install/setup.bash"` neste terminal — a lista mostra onde ele procurou |
| `ModuleNotFoundError: No module named 'pb_interfaces'` | rode o nó num terminal antigo, ou tire o `<depend>pb_interfaces</depend>` do `package.xml` dos nós | terminal novo com os dois `source`; confira o `package.xml` |

No dia a dia, `colcon build --symlink-install` sem selecionar nada compila tudo e **acerta a ordem sozinho**, porque o `package.xml` dos nós declara `<depend>pb_interfaces</depend>`.

**2.2 — O teste de fumaça.**

```bash
# ── Terminal B · o mesmo do build ─────────────────────
ros2 interface list | grep pb_interfaces
ros2 interface show pb_interfaces/msg/Deteccoes
ros2 interface show pb_interfaces/srv/StatusVisao
ros2 interface show std_srvs/srv/Trigger            # para comparar
```

Esperado no `list`: `pb_interfaces/action/VarrerCena`, `pb_interfaces/msg/ComandoMovimento`, `pb_interfaces/msg/Deteccao`, `pb_interfaces/msg/Deteccoes`, `pb_interfaces/srv/StatusVisao`. No `show` de `Deteccoes`, os comentários do `.msg` aparecem — e o `Deteccao[]` vem expandido com os campos da mensagem interna. Compare `Trigger` (`bool success` + `string message`) com `StatusVisao` (cinco campos tipados): é o mesmo lugar do grafo com outro vocabulário.

**2.3 — Rodar e ler a mensagem nova.** Antes, **derrube o launch da Aula 3** se ele estiver no ar: os dois servem o mesmo nome `/vision/status` com tipos diferentes, e com ambos rodando o `service call` fica ambíguo (é exatamente a *migração* que a tarefa pede — mesmo nome, outro tipo).

```bash
# ── Terminal A · ocupa o terminal ─────────────────────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"
source /opt/ros/humble/setup.bash
source "$PB_WS/install/setup.bash"
ros2 launch aula06_percepcao percepcao.launch.py classe:=tomate_maduro
```

Esperado: `detector no ar - classe='tomate_maduro' - publica pb_interfaces/Deteccoes em /vision/deteccoes - servico /vision/status (pb_interfaces/StatusVisao)` e, do `monitor`, uma linha por quadro:

```text
[monitor_deteccoes]: t=1794265911.67  total=2  tomate_maduro(0.98) em (261,333) area=1450 | tomate_maduro(0.99) em (512,216) area=3524
```

Deixe rodando até os dois objetos se encostarem: `total=1  tomate_maduro(0.89) em (450,290) area=4965` — a contagem cai, a área é a soma das duas, e a confiança **cai junto** (0,85 a 0,96, contra 0,98 e 0,99 dos círculos isolados). É a oclusão da Aula 3 vista pela mensagem nova — antes você via só o número mudar; agora vê o detector perdendo certeza.

**2.4 — Inspecionar.**

```bash
# ── Terminal B · com o Terminal A no ar ───────────────
ros2 topic echo /vision/deteccoes --once
ros2 service type /vision/status                              # pb_interfaces/srv/StatusVisao
ros2 service call /vision/status pb_interfaces/srv/StatusVisao "{}"
```

Esperado no `service call`: `ativo=True, classe_alvo='tomate_maduro', total_detectado=2, confianca_media=0.98…, mensagem="vendo 2 'tomate_maduro' na cena"`. Compare com a resposta do TP1: `success=True, message='2 objeto(s) no ultimo frame …'`. Quem chama o serviço novo não faz *parsing* de string nenhuma.

**2.5 — Edite um `.msg` e sinta o ciclo.** Acrescente `float32 raio` ao fim de `pb_interfaces/msg/Deteccao.msg`, recompile **só** o `pb_interfaces`, e rode `ros2 interface show pb_interfaces/msg/Deteccao` **neste** terminal e **num terminal antigo** sem `source` novo: num deles o campo existe, no outro não. Esse é o sintoma mais confuso da semana, e agora você o viu de propósito. Desfaça a edição (ou mantenha — o detector não preenche o campo e ele vai como `0.0`).

## 3. Anatomia dos dois pacotes (40 min)

**`pb_interfaces/package.xml`.** Três linhas fazem o pacote gerar código: `<buildtool_depend>rosidl_default_generators</buildtool_depend>`, `<exec_depend>rosidl_default_runtime</exec_depend>`, `<member_of_group>rosidl_interface_packages</member_of_group>`. Sem elas, compila e não gera nada — o erro silencioso. `<depend>std_msgs</depend>` existe por causa do `Header`; `<depend>action_msgs</depend>` por causa da `.action` da Aula 5. `<build_type>ament_cmake</build_type>` no `export` é o que diz ao `colcon` que este pacote é CMake, não Python.

**`pb_interfaces/CMakeLists.txt`.** `find_package` de `rosidl_default_generators`, `std_msgs` e `action_msgs`; `rosidl_generate_interfaces(${PROJECT_NAME} "msg/…" "srv/…" "action/…" DEPENDENCIES std_msgs action_msgs)` — **cada arquivo novo entra nesta lista**, e `std_msgs` aparece aqui **e** no `package.xml` (esquecer um dos dois é o erro do `Header` que não resolve); `ament_export_dependencies(rosidl_default_runtime)`. É tudo. Um pacote de interfaces não tem `src/` nem `include/`.

**`msg/Deteccao.msg` e `msg/Deteccoes.msg`.** Tipo, nome, comentário. `Deteccao`: `string classe`, `float32 confianca`, `int32 x`, `int32 y`, `int32 area`. `Deteccoes`: `std_msgs/Header header`, `Deteccao[] deteccoes`, `uint32 total` — o `total` é redundante com o tamanho do array **de propósito**: quem só quer contar não precisa desempacotar. Mensagens compõem: um campo pode ser outra mensagem sua, e `[]` é array de tamanho variável (`[8]` seria fixo).

**`srv/StatusVisao.srv`.** Requisição vazia acima do `---`; resposta com `bool ativo`, `string classe_alvo`, `uint32 total_detectado`, `float32 confianca_media`, `string mensagem`. A pergunta é sempre a mesma; a resposta carrega o vocabulário do projeto.

**`aula06_percepcao/detector.py` — o consumidor.** Localize: `from pb_interfaces.msg import Deteccao, Deteccoes` e `from pb_interfaces.srv import StatusVisao` (é isto que falha sem o `source`); `self.create_publisher(Deteccoes, '/vision/deteccoes', 10)` e `self.create_service(StatusVisao, '/vision/status', …)`; em `processar()`, para cada contorno, `d = Deteccao(); d.classe = self.classe; d.confianca = area / área do fecho convexo` — a **solidez**, não uma probabilidade, e o comentário diz isso em voz alta —; `msg.header.stamp = now`, `msg.deteccoes.append(d)`, `msg.total = len(…)`; em `responder_status()`, os campos tipados preenchidos um a um. O `package.xml` deste pacote tem `<depend>pb_interfaces</depend>` — é o que faz o `colcon` compilar na ordem certa quando você manda compilar tudo de uma vez.

**`aula06_percepcao/monitor.py`.** Assina `/vision/deteccoes` e imprime uma linha legível — é o "cliente" que mostra por que a mensagem nova vale o trabalho. **`cena.py`** desenha a cena sintética e converte `Image → numpy` sem `cv_bridge`. **`launch/percepcao.launch.py`** declara `fonte` (`sintetico | topico`) e `classe`; com `fonte:=topico` o detector assina o `/camera/image_raw` do seu publicador da Aula 3 — é assim que o pipeline do TP1 ganha a mensagem nova sem trocar a câmera.

**A ponte para a Etapa 4.** Quando os objetos se encostam, a contagem cai **e a confiança cai junto**: o detector tem um sinal interno de que algo saiu do esperado. Um detector treinado produz esse sinal de forma direta e calibrada — é a Aula 7 (30/11). O que **não** muda é a mensagem: classe, confiança e posição servem para os dois. Trocar o miolo sem trocar o contrato é a razão de esta aula vir antes daquela.

## 4. Autoavaliação (10 min)

Responda sem olhar; depois abra a resposta.

??? question "1. Você criou `msg/Alerta.msg` dentro do pacote dos seus nós (`ament_python`) e o `colcon build` reclama de CMake. O que aconteceu?"
    Gerar interface é gerar código, e isso é trabalho do `rosidl` num pacote `ament_cmake`. Um pacote `ament_python` não tem essa maquinaria. Mova o `.msg` para o seu `<projeto>_interfaces` e declare-o no `rosidl_generate_interfaces`.

??? question "2. `colcon build` passou nos dois pacotes, mas `ros2 launch` dá `ModuleNotFoundError: No module named '<projeto>_interfaces'`. Duas causas, em ordem de probabilidade?"
    (a) Faltou `source install/setup.bash` **depois** do build, neste terminal — abra um terminal novo. (b) Falta `<depend><projeto>_interfaces</depend>` no `package.xml` do pacote dos nós. Repare que ordem de build errada **não** é uma das causas: nesse caso o `colcon` para antes, com `Check that the following packages have been built`.

??? question "3. O pacote de interfaces compila sem erro e `ros2 interface list | grep <projeto>` não mostra nada. O que falta?"
    As três linhas do `package.xml` (`rosidl_default_generators`, `rosidl_default_runtime`, `member_of_group rosidl_interface_packages`) ou o arquivo não está listado em `rosidl_generate_interfaces`. O build silencioso é o pior erro: não gera nada e não reclama.

??? question "4. Por que `Deteccoes.msg` carrega um `Header`, se `Deteccao.msg` já tem x e y?"
    Porque x e y dizem **onde na imagem**; o `Header` diz **quando** (`stamp`) e **em que referencial** (`frame_id`). Sem `stamp` você não sabe se a detecção é de agora ou de três segundos atrás; sem `frame_id` não consegue combinar com outro sensor — o assunto da Etapa 4.

??? question "5. Você acrescentou um campo ao `.msg`, recompilou, e o nó continua dizendo que o campo não existe. O que é?"
    Terminal com `source` antigo: ele enxerga a versão velha da mensagem gerada. Todo build de interface pede `source` novo em **todos** os terminais abertos. Terminal novo resolve.

??? question "6. O `/vision/status` do TP1 responde `Trigger`. Vale a pena migrar para um `.srv` próprio? E para o TP1?"
    Vale para o TP2: a resposta ganha campos tipados (total, confiança média, classe) e quem chama deixa de fazer *parsing* de string. Para o TP1, **não** — mudar o tipo de um serviço a dias da entrega é uma péssima ideia; o `Trigger` atende ao que o TP1 pede.

## 5. Se travar

| Sintoma | Causa provável | Cura |
|---|---|---|
| `Check that the following packages have been built: - pb_interfaces` | os nós foram compilados antes das interfaces | interfaces primeiro, `source`, depois os nós |
| `Package '...' not found ... searching: [...]` | este terminal fez o `source` antes do build | `source "$PB_WS/install/setup.bash"` neste terminal |
| `ModuleNotFoundError: No module named 'pb_interfaces'` (ou do seu pacote) | terminal antigo, ou falta o `<depend>` no `package.xml` dos nós | terminal novo com os dois `source`; confira o `package.xml` |
| erro de CMake num pacote onde você não escreveu CMake | `msg/` dentro do pacote `ament_python` | mova para o pacote de interfaces (`ament_cmake`) |
| compila, `ros2 interface list` não mostra nada | faltam as três linhas de `rosidl` no `package.xml`, ou o arquivo não está no `rosidl_generate_interfaces` | acrescente e recompile |
| `Header` não resolve / `std_msgs` desconhecido | `std_msgs` só num dos dois lugares | `<depend>std_msgs</depend>` **e** `DEPENDENCIES std_msgs` |
| campo novo "não existe" | terminal com `source` velho | `source` em todos os terminais; ou terminal novo |
| `ros2 service call` reclama do tipo, ou `service type` mostra dois tipos | o tipo mudou — ou o launch da Aula 3 ainda está no ar servindo o mesmo `/vision/status` | `ros2 service type /vision/status`; derrube o launch antigo |
| `colcon build` do pacote de interfaces demora 10–40 s | normal: é geração de código C++ e Python | nada — só não interrompa |
| `rosidl` reclama de nome de campo | nomes em `snake_case` minúsculo, sem acento; tipos primitivos válidos (`int32`, `float32`, `string`, `bool`, `uint32`…) | corrija o `.msg` |
| nome do pacote de interfaces não bate | renomeou a pasta e esqueceu `<name>` ou `project(...)` | os **três** lugares: pasta, `package.xml`, `CMakeLists.txt`; `rm -rf build install log` |
| o nó dos seus pacotes não compila na ordem certa com `colcon build` (tudo) | falta `<depend><seuprojeto>_interfaces</depend>` no `package.xml` dos nós | acrescente; é isso que ordena o build |
| `/vision/contagem` a 5–7 Hz, com buracos | a imagem (0,92 MB) não cabe no segmento padrão de memória compartilhada do Fast DDS | o perfil do Fast DDS, na [página da Aula 4](../aulas/etapa03-aula04/index.md#pegar-o-material) |
