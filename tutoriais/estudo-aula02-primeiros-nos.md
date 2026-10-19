# Guia de estudo — Aula 2: primeiros nós (tópicos e serviços)

**Semana de 19/10 a 25/10 · Etapa 2 · turma live.** A aula de 1h30 mostrou os três tijolos de comunicação do ROS 2 rodando; **este guia é onde você aprende a usá-los**. Ele é guiado pela [tarefa da Aula 2](tarefa-aula02-primeiros-nos.md) (obrigatória, prazo **domingo 25/10, 23h59**, push na `dev`) e pelo [Desafio 1](../recursos/desafios/desafio-01-comunicacao.md) (opcional). Tempo total: **2h30 a 3h30**, em duas ou três sessões — não tente fazer de uma vez só.

| Sessão | O quê | Tempo | Resultado |
|---|---|---|---|
| 1 | Seções 1 e 2 — ler, reproduzir o exemplo, entender cada arquivo | 60–80 min | o launch sobe os 3 nós no **seu** repositório |
| 2 | Seção 3 (anatomia do código) + passos 4–6 da tarefa | 60–90 min | pacote renomeado, publisher seu, 2º subscriber |
| 3 | Seções 4 e 5 — autoavaliação, desafio, push e evidência | 30–60 min | commit na `dev`, `rqt_graph` em `docs/evidencias/aula02/` |

!!! tip "Como pedir ajuda"
    No Infnet.Online, com três itens: o **comando exato** que rodou, a **saída completa** e `lsb_release -a`. Antes disso, leia a seção 6 ("Se travar") — 80% dos problemas desta semana estão lá.

---

## 1. Leia antes (30 min)

Leia na ordem; cada item diz o que você deve ser capaz de responder depois.

| Fonte | O quê | Minutos | Depois você responde |
|---|---|---|---|
| [Cheatsheet ROS 2](../cheatsheets/ros2-cheatsheet.md) | seções *nós*, *tópicos*, *serviços* | 8 | o que faz `ros2 topic echo`, `ros2 topic info`, `ros2 service call` |
| Docs do Humble — [Understanding nodes](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes.html) | só a página | 5 | o que é um nó e o que `ros2 node list` mostra |
| Docs do Humble — [Understanding topics](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html) | até "ros2 topic hz" | 10 | por que o publisher não sabe quem escuta; o que é o **tipo** da mensagem |
| Docs do Humble — [Understanding services](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html) | só a página | 5 | a diferença entre chamar um serviço e assinar um tópico |
| [Workspace e colcon](workspace-colcon.md) | seções 1–3 | 7 | por que `source install/setup.bash` em **cada** terminal; o que `--symlink-install` muda |

A regra de bolso que organiza tudo: **fluxo contínuo → tópico** (imagem da câmera, `/cmd_vel`); **pergunta pontual com resposta → serviço** (`/vision/status`); **tarefa longa com progresso e cancelamento → ação** (chega no TP2).

## 2. Reproduza o exemplo, passo a passo (40 min)

Você trabalha **no seu repositório**, na branch `dev`, e nunca dentro do repositório do material. O exemplo é copiado para o seu workspace e compilado lá.

```bash
# ── uma vez por terminal ──────────────────────────────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"

cd "$PB_DIR" && git checkout dev
git branch --show-current                   # esperado: dev
```

```bash
# herda as variáveis do bloco anterior
rm -rf /tmp/PBRoboticos_live_prof_dacio
cd /tmp && git clone --depth 1 https://github.com/Prof-Dacio-INFNET/PBRoboticos_live_prof_dacio.git
mkdir -p "$PB_WS/src"
cp -r /tmp/PBRoboticos_live_prof_dacio/exemplos/aula02-comunicacao/aula02_comunicacao "$PB_WS/src/"
ls "$PB_WS/src/aula02_comunicacao"
```

Esperado no `ls`: `aula02_comunicacao  launch  package.xml  resource  setup.cfg  setup.py`. Cada um tem um papel — e você vai mexer em todos eles no passo 4 da tarefa:

| Arquivo | Papel | Onde o nome do pacote aparece |
|---|---|---|
| `package.xml` | declara o pacote e as **dependências** (`rclpy`, `std_msgs`, `std_srvs`) | `<name>` |
| `setup.py` | registra os **executáveis** em `entry_points` (é o que faz `ros2 run PKG publicador` existir) e instala o launch | `package_name` |
| `setup.cfg` | diz ao `colcon` em que pasta instalar os executáveis | `lib/<nome>` (duas vezes) |
| `resource/<nome>` | arquivo vazio que registra o pacote no índice do ROS | o nome do arquivo |
| `aula02_comunicacao/` | o código Python: um arquivo por nó | o nome da pasta |
| `launch/comunicacao.launch.py` | sobe os três nós com um comando | `package='…'` em cada `Node(...)` |

```bash
# herda as variáveis
cd "$PB_WS"
colcon build --packages-select aula02_comunicacao --symlink-install
source install/setup.bash
ros2 launch aula02_comunicacao comunicacao.launch.py
```

Esperado (as linhas podem vir em ordem diferente):

```
[publicador-1] [INFO] [...] [publicador]: Publicando em /camera/status
[servico_contagem-3] [INFO] [...] [servico_contagem]: Serviço /contagem pronto (chame com ros2 service call)
[assinante-2] [INFO] [...] [assinante]: [1] recebi: "frame 0: 0 objeto(s) detectado(s)"
[assinante-2] [INFO] [...] [assinante]: [2] recebi: "frame 1: 0 objeto(s) detectado(s)"
```

Deixe rodando e abra um **segundo terminal** (repita o bloco "uma vez por terminal" e o `source`):

```bash
# herda as variáveis
cd "$PB_WS" && source install/setup.bash
ros2 node list                 # esperado: /assinante  /publicador  /servico_contagem
ros2 topic list                # esperado inclui: /camera/status
ros2 topic info /camera/status # esperado: Type: std_msgs/msg/String · 1 publisher · 2 subscriptions
ros2 topic echo /camera/status --once
ros2 service call /contagem std_srvs/srv/Trigger "{}"
```

A resposta do serviço é a frase que importa esta semana: `message='N mensagens em /camera/status até agora'`. Repare em **2 subscriptions** no `topic info`: o `assinante` e o `servico_contagem` escutam o mesmo tópico sem que o `publicador` saiba de nenhum dos dois — isso é o desacoplamento do pub/sub. Agora `rqt_graph`: o desenho tem que mostrar `publicador → /camera/status → assinante` e `→ servico_contagem`. Feche o `rqt_graph` depois de olhar.

!!! tip "Rode antes de modificar"
    Só comece a mexer no código depois que o exemplo rodou **como veio**. Quando algo quebrar depois, você sabe que o problema é seu, e não do exemplo.

## 3. Anatomia do código: o que cada linha faz (30 min)

Abra `aula02_comunicacao/publicador.py`. São 20 linhas e todas importam:

```python
class Publicador(Node):                                   # todo nó é uma classe que herda de Node
    def __init__(self):
        super().__init__('publicador')                     # o NOME do nó (aparece no ros2 node list)
        self.pub = self.create_publisher(String, '/camera/status', 10)   # tipo, tópico, fila
        self.n = 0
        self.create_timer(1.0, self.tick)                  # chama tick() a cada 1,0 s
        self.get_logger().info('Publicando em /camera/status')

    def tick(self):
        msg = String()
        msg.data = f'frame {self.n}: 0 objeto(s) detectado(s)'   # ← o conteúdo: é aqui que o TP1 entra
        self.pub.publish(msg)
        self.n += 1
```

Três coisas para fixar. O nó **não tem loop**: `rclpy.spin(no)` no `main()` fica girando e chama o timer — você escreve callbacks, não `while True`. O `10` é o tamanho da **fila** (QoS mais simples): se o subscriber atrasar, as 10 últimas ficam guardadas. E `msg.data` é um `str` porque o tipo é `std_msgs/String`; no TP1 o tipo vira `sensor_msgs/Image` e o conteúdo vira o frame da câmera — o resto do arquivo quase não muda.

Em `assinante.py`, a linha que importa é `self.create_subscription(String, '/camera/status', self.ao_receber, 10)`: **mesmo tipo e mesmo nome de tópico** do publisher, e um callback que recebe cada mensagem. Se o tipo ou o nome divergirem em uma letra, nada chega e nada avisa — é o erro silencioso nº 1 do pub/sub (a seção 6 mostra como diagnosticar).

Em `servico_contagem.py` há **dois** mecanismos no mesmo nó: uma subscription (para contar) e `self.create_service(Trigger, '/contagem', self._responder)`. O callback do serviço recebe `request` e `response`, preenche `response.message` e **retorna** `response`. `std_srvs/Trigger` é o serviço mais simples que existe (pedido vazio, resposta com `success` e `message`); no TP1 o `/vision/status` segue exatamente essa forma.

No `setup.py`, a linha `'publicador = aula02_comunicacao.publicador:main'` lê-se "o executável `publicador` é a função `main` do módulo `aula02_comunicacao/publicador.py`". Sem essa linha, `ros2 run` e o launch não encontram o nó — e é por isso que, ao criar um nó novo no passo 6 da tarefa, o `setup.py` tem que ser editado.

**QoS, numa pincelada.** Publisher e subscriber precisam de configurações de qualidade compatíveis; com o `10` dos dois lados, são. Guarde só o sintoma: "publiquei, mas não chega" pode ser QoS, nome de tópico errado, tipo errado — ou o `source` que faltou. `ros2 topic info /camera/status -v` mostra o QoS de cada lado.

## 4. Tarefa da semana (obrigatória)

**O que fazer:** o pacote do exemplo, **com o seu nome**, publicando um status do seu domínio em `/camera/status`, com um **segundo subscriber** que reage só quando há objeto, o serviço `/contagem` respondendo, tudo subindo pelo launch — commitado na `dev` e com um `rqt_graph` em `docs/evidencias/aula02/`.

**O que usar:** `exemplos/aula02-comunicacao/aula02_comunicacao` (copiado para o seu `ros2_ws/src/`); [renomear um pacote ROS 2](renomear-pacote-ros2.md) para o passo 4; o código do `assinante_alerta` está no passo 6 da [tarefa](tarefa-aula02-primeiros-nos.md).

**Como adequar ao seu projeto:** o nome do pacote vem do seu projeto (`percepcao_entregador`, `visao_sentinela`…); o texto publicado descreve o que o **seu** robô vai perceber ("2 caixa(s) na prateleira", "porta aberta"); a regra do alerta é a regra que faria sentido para o seu robô.

**Como saber que terminou:** no seu repositório, `ros2 launch <seu_pacote> comunicacao.launch.py` sobe **4 nós** (`ros2 node list`), `ros2 service call /contagem std_srvs/srv/Trigger "{}"` responde com um número que cresce, o `assinante_alerta` só loga quando o número de objetos é maior que zero, e `git log --oneline -1` na `dev` mostra o seu commit — já no GitHub.

Passo a passo com as saídas esperadas: [tarefa da Aula 2](tarefa-aula02-primeiros-nos.md).

## 5. Desafio 1 (opcional, mede o que você aprendeu)

[Desafio 1 — comunicação](../recursos/desafios/desafio-01-comunicacao.md): segundo publisher em outra frequência, filtro no callback, parâmetro `frequencia_hz` alterado com `ros2 param set`, conferência do `/contagem` contra o `topic echo`. A medida: com dois publishers (1 Hz e 2 Hz) rodando por 20 s, quantas mensagens o `/contagem` reporta? Se a sua resposta bate com `ros2 topic hz /camera/status`, você entendeu pub/sub de verdade. Comente no Infnet.Online com o link do commit.

## 6. Autoavaliação (10 min)

Responda sem olhar; depois abra a resposta.

??? question "1. A imagem da câmera do TP1 vai viajar por tópico ou por serviço? Por quê?"
    Tópico. É um fluxo contínuo (30 frames por segundo), com possivelmente vários consumidores, e ninguém "responde" a um frame. Serviço é para uma pergunta pontual com resposta — o `/vision/status`.

??? question "2. Você editou `publicador.py`, rodou o launch de novo e o texto antigo continua aparecendo. Duas causas prováveis?"
    (a) O build foi feito **sem** `--symlink-install`, então o que roda é uma cópia antiga em `install/` — recompile (ou passe a usar a flag). (b) Você editou o arquivo dentro de `install/` ou `build/`, não em `src/` — a edição é sempre em `src/`.

??? question "3. `ros2 topic info /camera/status` mostra 1 publisher e 0 subscriptions, mas o seu `assinante` está rodando. O que conferir?"
    O nome do tópico e o **tipo** no `create_subscription` (uma letra diferente e o ROS trata como outro tópico), e se o `assinante` foi iniciado num terminal com `source install/setup.bash` do mesmo workspace. `ros2 node list` diz se o nó existe; `ros2 node info /assinante` diz o que ele assina.

??? question "4. O que acontece se você criar `assinante_alerta.py` e esquecer o `setup.py`?"
    `ros2 run` responde `No executable found` e o launch falha ao subir esse nó. O `entry_points` do `setup.py` é o registro dos executáveis — arquivo novo, linha nova, e `colcon build` de novo (o symlink não cria entradas novas).

??? question "5. Por que o `servico_contagem` tem uma subscription, se ele é um serviço?"
    Porque para **responder** quantas mensagens passaram ele precisa **ouvir** o tópico. Um nó pode combinar vários mecanismos — é o normal: no TP1, o nó de visão assina a imagem, publica detecções e serve o `/vision/status`.

## 7. Se travar

| Sintoma | Causa provável | Cura |
|---|---|---|
| `Package 'aula02_comunicacao' not found` | faltou `source install/setup.bash` **neste** terminal | `cd "$PB_WS" && source install/setup.bash` |
| editou Python, nada mudou | build sem `--symlink-install`, ou editou fora de `src/` | `colcon build --symlink-install`; edite só em `src/` |
| `libexec directory .../lib/<pacote> does not exist` | renomeou o pacote e esqueceu o `setup.cfg` | [renomear um pacote ROS 2](renomear-pacote-ros2.md); `rm -rf build install log` e recompile |
| `No executable found` | nó novo sem linha no `entry_points` do `setup.py` | adicione a linha e `colcon build` |
| `topic info` mostra 0 subscriptions | nome ou tipo diferente no subscriber; ou workspace sem `source` | confira as duas strings; `ros2 node info /assinante` |
| dois alunos vendo os nós um do outro | mesmo `ROS_DOMAIN_ID` na mesma rede | cada um com o seu número de 1 a 100 |
| `colcon build` falha com `Permission denied` ou é lentíssimo | repositório em `/mnt/c` (ou `/media/sf_*`) | clone de novo em `~` |
| `rclpy._rclpy_pybind11 ... undefined symbol` ou `ModuleNotFoundError: rclpy` | venv ativo sem `--system-site-packages`, ou Python errado | `deactivate`; rode o ROS fora do venv (ou recrie com `uv venv --system-site-packages`) |
| `rcl_shutdown already called` ao sair com Ctrl+C | ruído de encerramento | ignore, ou `if rclpy.ok(): rclpy.shutdown()` |

Nada disso resolveu? Infnet.Online, com o comando, a saída completa e `lsb_release -a`.
