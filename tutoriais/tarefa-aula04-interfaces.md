---
titulo: "Tarefa da Aula 4 — as interfaces do seu projeto"
aula: 4
etapa: 3
data_aula: 2026-11-09
prazo: 2026-11-22
obrigatoria: true
vira_no_tp: "TP2 — pacote de interfaces, .msg e .srv do domínio"
---

# Tarefa da Aula 4 — as interfaces do seu projeto

**Publicada em 09/11/2026 · prazo domingo 22/11, 23h59 · push na `dev`**

!!! danger "Primeiro o TP1"
    Esta é a **parte 2** da tarefa da semana; a parte 1 é a entrega do TP1, e está na [página da Aula 4](../aulas/etapa03-aula04/index.md#a-tarefa-da-semana). Volte aqui com a tag `tp1` empurrada. Trabalhe na `dev`: nada daqui entra na `entrega-tp1`.

## Cenas dos últimos episódios

Na Aula 3 o seu sistema passou a publicar um `Int32` em `/vision/contagem` e a responder ao `/vision/status` com um `Trigger`. Na Aula 4 você viu o limite disso — "dois o quê?" — e os dois pacotes do exemplo rodando: `pb_interfaces` (só definições) e `aula06_percepcao` (os nós). O [guia de estudo da Aula 4](estudo-aula04-interfaces.md) reproduz esse exemplo no seu repositório; **faça o guia antes desta tarefa**.

## As quatro perguntas

**O que fazer.** Dar ao seu projeto um vocabulário próprio: um pacote de interfaces com uma mensagem e um serviço do seu domínio, o `/vision/status` migrado para o tipo novo, e um tópico de detecções. O critério é simples: **um colega entende o que o seu robô percebe lendo só os seus `.msg`**, sem abrir o seu código.

**O que usar.** O `pb_interfaces` do exemplo, copiado e renomeado; o `detector.py` do exemplo como referência de como preencher a mensagem.

**Como adequar ao seu projeto.** Troque o vocabulário (as classes do seu domínio) e acrescente **o campo que só o seu domínio pede**.

**Como saber que terminou.** O bloco do passo 5 mostra o seu pacote no `ros2 interface list`, e o `ros2 service type /vision/status` mostra o tipo novo.

<!-- PB:TAREFA-A04 -->
- [ ] T4.1 pacote de interfaces do projeto (`ament_cmake`) compilando e visível no `ros2 interface list`
- [ ] T4.2 uma mensagem de detecção com o vocabulário do **seu** domínio (classe, confiança, posição — e o campo que o seu domínio pede)
- [ ] T4.3 `/vision/status` **migrado** do `std_srvs/Trigger` para o seu `.srv`
- [ ] T4.4 `/vision/deteccoes` publicando detecções, com o `/vision/contagem` mantido
- [ ] T4.5 evidência em `docs/evidencias/tp2/interface.txt`; commit na `dev` com push

## 1. Crie o seu pacote de interfaces

O caminho mais curto é copiar o `pb_interfaces` e renomear nos **três** lugares: a pasta, o `<name>` do `package.xml` e o `project(...)` do `CMakeLists.txt`. O bloco faz os três, e tira do pacote o que é da próxima aula.

```bash
# ── Terminal B · uma vez por terminal ─────────────────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"
export PB_IFACE=pomar_interfaces           # ← troque: o nome do SEU pacote, terminando em _interfaces
source /opt/ros/humble/setup.bash

cd "$PB_DIR" && git checkout dev
rm -rf /tmp/PBRoboticos_live_prof_dacio
git clone --depth 1 https://github.com/Prof-Dacio-INFNET/PBRoboticos_live_prof_dacio.git /tmp/PBRoboticos_live_prof_dacio
cd "$PB_WS/src"
cp -r /tmp/PBRoboticos_live_prof_dacio/exemplos/aula06-interfaces/pb_interfaces "$PB_IFACE"
rm -rf "$PB_IFACE/action" "$PB_IFACE/msg/ComandoMovimento.msg"
sed -i "s/pb_interfaces/$PB_IFACE/g" "$PB_IFACE/package.xml" "$PB_IFACE/CMakeLists.txt"
sed -i '/ComandoMovimento.msg/d; /VarrerCena.action/d' "$PB_IFACE/CMakeLists.txt"
grep -n "$PB_IFACE\|msg/\|srv/" "$PB_IFACE/package.xml" "$PB_IFACE/CMakeLists.txt"
```

**Tem de aparecer:** o nome do seu pacote em `<name>` e em `project(...)`, e três arquivos na lista: `msg/Deteccao.msg`, `msg/Deteccoes.msg` e `srv/StatusVisao.srv`. (O `action_msgs` continua declarado no pacote: não atrapalha, e volta a ser usado na Aula 5.)

O nome do pacote usa minúsculas e sublinhado, e termina em `_interfaces`: `pomar_interfaces`, `estoque_interfaces`.

## 2. Escreva uma mensagem que descreva o SEU domínio

Abra `"$PB_WS/src/$PB_IFACE/msg/Deteccao.msg"` no editor e **troque o vocabulário**. Se o seu projeto conta tampas, `classe` vale `tampa_azul` e `tampa_verde`; se inspeciona EPI, vale `capacete` e `colete`. Acrescente o campo que o **seu** domínio precisa e o exemplo não tem — e apague o que não serve.

Duas perguntas para cada campo: *quem vai ler isto?* e *o que a pessoa faz de diferente se este número mudar?* Campo que não muda a decisão de ninguém é peso morto. Mantenha o `Header` na mensagem agregada: sem `stamp`, ninguém sabe se a detecção é de agora.

```bash
# ── Terminal B · herda as variáveis do passo 1 ────────
: "${PB_IFACE:?defina PB_USER, PB_DIR, PB_WS e PB_IFACE — o bloco está no passo 1}"
cd "$PB_WS"
colcon build --packages-select "$PB_IFACE"
source install/setup.bash
ros2 interface list | grep "$PB_IFACE"
ros2 interface show "$PB_IFACE/msg/Deteccao"
```

**Tem de aparecer:** `Finished <<<` com o nome do seu pacote (de sete a quinze segundos), as três interfaces na lista, e a sua mensagem com os **seus** campos e comentários. Lista vazia? Faltou o `source`, ou o arquivo novo não entrou na lista do `CMakeLists.txt`.

## 3. Migre o `/vision/status` do `Trigger` para o seu serviço

É o coração da tarefa, porque é uma **migração**, e não uma criação: o serviço existe e funciona desde a Aula 3. No nó do seu pacote de visão, são três mudanças — o `import`, o `create_service` e o preenchimento da resposta:

```python
from pomar_interfaces.srv import StatusVisao          # o SEU pacote de interfaces
...
        self.srv = self.create_service(StatusVisao, '/vision/status', self.on_status)
...
    def on_status(self, req, resp):
        resp.ativo = self.frames > 0
        resp.classe_alvo = self.get_parameter('rotulo').value
        resp.total_detectado = self.ultima_contagem
        resp.confianca_media = 0.0                    # até o seu nó calcular uma confiança
        resp.mensagem = f'{resp.total_detectado} {resp.classe_alvo} no ultimo frame'
        return resp
```

E, no `package.xml` do pacote dos **nós**, a dependência — é ela que faz o `colcon` acertar a ordem do build sozinho:

```xml
<depend>pomar_interfaces</depend>
```

Depois, com o seu launch parado:

```bash
# ── Terminal B · herda as variáveis do passo 1 ────────
: "${PB_IFACE:?defina PB_USER, PB_DIR, PB_WS e PB_IFACE — o bloco está no passo 1}"
cd "$PB_WS"
colcon build --symlink-install
source install/setup.bash
```

**Tem de aparecer:** o pacote de interfaces compilando **antes** do pacote dos nós, e `Summary: N packages finished`.

```bash
# ── Terminal A · o SEU launch (ocupa o terminal) ──────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"
source /opt/ros/humble/setup.bash
source "$PB_WS/install/setup.bash"
ros2 launch aula03_visao visao.launch.py     # ← troque: o SEU pacote e o SEU launch
```

```bash
# ── Terminal B · com o Terminal A no ar ───────────────
: "${PB_IFACE:?defina PB_USER, PB_DIR, PB_WS e PB_IFACE — o bloco está no passo 1}"
ros2 service type /vision/status
ros2 service call /vision/status "$PB_IFACE/srv/StatusVisao" "{}"
```

**Tem de aparecer:** o tipo novo (o nome do seu pacote, `/srv/StatusVisao`) e a resposta com os campos — `ativo`, `classe_alvo`, `total_detectado`, `confianca_media`, `mensagem`. O incômodo do número dentro da frase acaba aqui: quem chama lê `total_detectado` direto. Registre a migração em `docs/decisoes.md`: o que mudou, por quê, e o que quebra para quem chamava com `Trigger`.

## 4. Publique detecções, não só a contagem

Mantenha o `/vision/contagem` — ele é a régua leve para medir taxa — e **acrescente** o tópico `/vision/deteccoes` com a sua mensagem agregada. Manter os dois é decisão, e não indecisão: um serve para medir, o outro para informar. O `detector.py` do exemplo mostra como preencher o `header.stamp`, o array e o `total`:

```python
from pomar_interfaces.msg import Deteccao, Deteccoes   # o SEU pacote de interfaces
...
        self.pub_det = self.create_publisher(Deteccoes, '/vision/deteccoes', 10)
...
        msg = Deteccoes()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'camera'
        for c in contornos:                              # os contornos que o seu nó já calcula
            d = Deteccao()
            d.classe = self.get_parameter('rotulo').value
            d.area = int(cv2.contourArea(c))
            ...                                          # x, y, confiança: veja o detector.py
            msg.deteccoes.append(d)
        msg.total = len(msg.deteccoes)
        self.pub_det.publish(msg)
```

## 5. Evidência, verificação e commit

```bash
# ── Terminal B · com o SEU launch no ar no Terminal A ──
: "${PB_IFACE:?defina PB_USER, PB_DIR, PB_WS e PB_IFACE — o bloco está no passo 1}"
cd "$PB_DIR" && mkdir -p docs/evidencias/tp2
ros2 interface list | grep "$PB_IFACE"                              >  docs/evidencias/tp2/interface.txt
ros2 interface show "$PB_IFACE/msg/Deteccao"                        >> docs/evidencias/tp2/interface.txt
ros2 service type /vision/status                                    >> docs/evidencias/tp2/interface.txt
ros2 service call /vision/status "$PB_IFACE/srv/StatusVisao" "{}"   >> docs/evidencias/tp2/interface.txt
ros2 topic echo /vision/deteccoes --once                            >> docs/evidencias/tp2/interface.txt
cat docs/evidencias/tp2/interface.txt
git add -A
git commit -m "Interfaces do projeto: pacote proprio, /vision/status migrado, /vision/deteccoes"
git push origin dev
```

**Tem de aparecer:** no arquivo, o seu pacote na lista, a sua mensagem, o tipo novo do serviço, a resposta com campos e uma mensagem de detecções; depois o commit e o push. Se isso apareceu, a tarefa terminou.

## Desafio (opcional): quanto pesa informar, em vez de mostrar?

```bash
# ── Terminal B · com o launch no ar · cada linha encerra sozinha em 10 s ──
timeout 10 ros2 topic bw /vision/deteccoes
timeout 10 ros2 topic bw /camera/image_raw
```

Quantas vezes a banda de um tópico é maior do que a do outro? O que isso muda numa rede sem fio entre o robô e a base? Anote os dois números e a sua conclusão em `docs/decisoes.md`, e traga para a próxima aula.

## O que esta tarefa adianta

O TP2 (leitura na Aula 6, 23/11) começa exatamente por aqui: o pacote de interfaces compilando, e o `.msg` e o `.srv` do domínio visíveis no ambiente. A Aula 5 (16/11) acrescenta uma ação a **este mesmo pacote** — por isso ele precisa existir. As datas do TP2 saem com o enunciado.

## Se der errado

| Sintoma | O que fazer |
|---|---|
| `Check that the following packages have been built:` seguido do nome do seu pacote de interfaces | os nós foram compilados antes das interfaces: compile as interfaces, dê `source`, e então os nós — ou `colcon build --symlink-install` de tudo, com o `<depend>` no lugar |
| `Package '...' not found ... searching: [...]` | este terminal fez o `source` antes do build: `source "$PB_WS/install/setup.bash"` |
| `ModuleNotFoundError: No module named '..._interfaces'` | terminal antigo (abra um novo, com os dois `source`), ou falta o `<depend>` no `package.xml` do pacote dos nós |
| erro de CMake num pacote onde você não escreveu CMake | o `.msg` foi parar no pacote dos nós (`ament_python`): interfaces vivem no pacote `ament_cmake` separado |
| compila, mas `ros2 interface list` não mostra nada | faltam as três linhas do `rosidl` no `package.xml`, ou o arquivo não está na lista do `CMakeLists.txt` |
| o `Header` não resolve | `std_msgs` nos **dois** lugares: `<depend>` no `package.xml` e `DEPENDENCIES` no `CMakeLists.txt` |
| editou o `.msg` e "o campo não existe" | recompile o pacote de interfaces **e** dê `source` de novo em todos os terminais abertos |
| `ros2 service type /vision/status` mostra dois tipos | há dois nós servindo o mesmo nome (o antigo e o novo): feche o launch antigo |
| `rosidl` reclama do nome de um campo | campos em minúsculas com sublinhado, sem acento; tipos válidos: `bool`, `int32`, `uint32`, `float32`, `float64`, `string` |

Travou, e nada aqui bate? **Infnet.Online**, com o comando exato, a saída completa e o passo em que você está.
