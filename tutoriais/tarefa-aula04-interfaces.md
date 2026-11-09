---
titulo: "Tarefa da Aula 4 — as interfaces do seu projeto"
aula: 4
etapa: 3
data_aula: 2026-11-09
prazo: 2026-11-22
obrigatoria: true
vira_no_tp: "TP2 — pacote de interfaces, .msg e .srv do domínio (gates G2.0 e G2.1)"
---

# Tarefa da Aula 4 — as interfaces do seu projeto

**Publicada em 09/11/2026 · prazo domingo 22/11, 23h59 · push na `dev`**

!!! danger "Antes de sexta, 13/11, existe uma coisa só: entregar o TP1"
    Esta tarefa é do TP2. Se o seu TP1 ainda não está fechado, o [checklist de entrega](checklist-entrega-tp1.md) vem primeiro — sem discussão. Volte aqui no fim de semana, com a tag `tp1` empurrada. Trabalhe na `dev`: nada daqui entra na `entrega-tp1`.

O objetivo é dar ao seu projeto um vocabulário próprio, e o critério de pronto é simples: **um colega consegue entender o que o seu robô percebe lendo só os seus `.msg`**, sem abrir o seu código. Tempo: ~2h, **depois** de estudar — o [guia de estudo da Aula 4](estudo-aula04-interfaces.md) explica os dois pacotes e cada arquivo que você vai mexer; comece por ele.

<!-- PB:TAREFA-A04 -->
- [ ] T4.1 pacote `<seuprojeto>_interfaces` (`ament_cmake`) compilando; `ros2 interface list | grep <seuprojeto>` mostra as suas interfaces
- [ ] T4.2 uma mensagem de detecção com o vocabulário do **seu** domínio (classe, confiança, posição — e o campo que o seu domínio pede)
- [ ] T4.3 `/vision/status` **migrado** do `std_srvs/Trigger` para o seu `.srv`, respondendo com informação do domínio
- [ ] T4.4 `/vision/deteccoes` publicando detecções, com o `/vision/contagem` mantido
- [ ] T4.5 nenhum rótulo `objeto_alvo` sobrando; evidência em `docs/evidencias/tp2/interface.txt`; commit na `dev` com push

## 1. Crie o seu pacote de interfaces

```bash
# ── uma vez por terminal ──────────────────────────────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"

cd "$PB_DIR" && git checkout dev
cd "$PB_WS/src"
ros2 pkg create --build-type ament_cmake <seuprojeto>_interfaces
mkdir -p <seuprojeto>_interfaces/msg <seuprojeto>_interfaces/srv
```

Ajuste o `package.xml` e o `CMakeLists.txt` como no [exemplo da aula](../exemplos/aula06-interfaces/index.md) (`pb_interfaces`): as três linhas que fazem o pacote gerar código são `rosidl_default_generators`, `rosidl_default_runtime` e `member_of_group rosidl_interface_packages`; `std_msgs` entra **nos dois lugares** (`<depend>` no `package.xml` e `DEPENDENCIES` no `rosidl_generate_interfaces`) por causa do `Header`. O caminho mais curto é copiar o `pb_interfaces` do exemplo e renomear nos **três** lugares — pasta, `<name>` no `package.xml` e `project(...)` no `CMakeLists.txt` — apagando o `.action` e o `ComandoMovimento.msg`, que são da Aula 5.

## 2. Escreva uma mensagem que descreva o SEU domínio

Comece pela `Deteccao.msg` do exemplo e **troque o vocabulário**. Se o seu projeto conta tampas, `classe` vale `tampa_azul` e `tampa_verde`; se inspeciona EPI, vale `capacete` e `colete`. Acrescente o campo que o **seu** domínio precisa e o exemplo não tem — e apague o que não serve.

Duas perguntas para cada campo: *quem vai ler isto?* e *o que a pessoa faz de diferente se este número mudar?* Campo que não muda decisão de ninguém é peso morto. Mantenha o `Header` na mensagem agregada: sem `stamp`, ninguém sabe se a detecção é de agora.

```bash
cd "$PB_WS"
colcon build --packages-select <seuprojeto>_interfaces
source install/setup.bash                                   # em TODOS os terminais abertos
ros2 interface show <seuprojeto>_interfaces/msg/<SuaMensagem>
```

## 3. Migre o `/vision/status` do `Trigger` para o seu serviço

Este é o coração da tarefa, porque é uma **migração**, não uma criação: o serviço já existe e já funciona desde a Aula 3. Você troca o tipo (`from <seuprojeto>_interfaces.srv import <SeuServico>` e o `create_service`), preenche os campos tipados em vez de montar uma string, e confere que o grafo continua de pé.

```bash
ros2 service type /vision/status          # antes: std_srvs/srv/Trigger
                                          # depois: <seuprojeto>_interfaces/srv/<SeuServico>
ros2 service call /vision/status <seuprojeto>_interfaces/srv/<SeuServico> "{}"
```

O incômodo que você guardou na Aula 3 — números dentro de uma string — acaba aqui: `total_detectado` é `uint32`, `confianca_media` é `float32`, e quem chama não precisa fazer *parsing* de nada.

## 4. Publique detecções, não só a contagem

Mantenha o `/vision/contagem` funcionando — ele é a régua leve que você usa para medir taxa — e **acrescente** o tópico `/vision/deteccoes` com a sua mensagem agregada. Manter os dois é uma decisão consciente, não indecisão: um serve para medir, o outro para informar. O `detector.py` do exemplo mostra como preencher `header.stamp`, o array e o `total`.

## 5. Evidência e commit

```bash
mkdir -p docs/evidencias/tp2
ros2 interface show <seuprojeto>_interfaces/msg/<SuaMensagem>              >  docs/evidencias/tp2/interface.txt
ros2 topic echo /vision/deteccoes --once                                   >> docs/evidencias/tp2/interface.txt
ros2 service call /vision/status <seuprojeto>_interfaces/srv/<SeuServico> "{}" >> docs/evidencias/tp2/interface.txt
cd "$PB_DIR" && git add -A && git commit -m "Interfaces proprias: <seuprojeto>_interfaces, /vision/status migrado, /vision/deteccoes" && git push origin dev
```

## O que esta tarefa adianta

No TP2 (leitura na Aula 6, 23/11; entrega 11/12) os dois primeiros gates são exatamente isto: o pacote de interfaces compilando e o `.msg`/`.srv` do domínio visíveis no ambiente. As datas desta turma saem com o enunciado. A Aula 5 (16/11) acrescenta um `.action` a **este mesmo pacote** — por isso ele precisa existir até 22/11.

## Se der errado

| Sintoma | O que verificar |
|---|---|
| `ModuleNotFoundError: No module named '<seuprojeto>_interfaces'` | faltou `source install/setup.bash` **depois** do build, em **todos** os terminais — é quase sempre isto; abra um terminal novo |
| erro de CMake num pacote onde você não escreveu CMake | você pôs `msg/` no pacote dos nós (`ament_python`); interfaces vivem em pacote `ament_cmake` separado |
| compila, mas `ros2 interface list` não mostra nada | faltam as três linhas de `rosidl` no `package.xml` |
| `Header` não resolve | `std_msgs` nos **dois** lugares: `<depend>` no `package.xml` e `DEPENDENCIES` no CMake |
| editou o `.msg` e "o campo não existe" | recompile o pacote de interfaces **e** dê `source` de novo em todos os terminais |
| `ros2 pkg create` criou `src/` e `include/` que você não usa | pode apagar; um pacote de interfaces só tem `msg/`, `srv/`, `package.xml` e `CMakeLists.txt` |
| o nó Python não acha o pacote nem depois do `source` | falta `<depend><seuprojeto>_interfaces</depend>` no `package.xml` do pacote dos nós; e a ordem de build: interfaces primeiro |
