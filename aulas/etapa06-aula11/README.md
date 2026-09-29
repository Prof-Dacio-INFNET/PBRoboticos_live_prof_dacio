# Aula 11 — O mundo, a deriva e o mapa que corrige

**Terça, 29/09/2026 · sala SJ205 · Etapa 6 (28/09–10/10)**

[:material-file-pdf-box: Slides da Aula 11 (PDF)](apresentacao-aula11.pdf){ .md-button .md-button--primary }
[:material-code-tags: Exemplo `aula11-mundo`](../../exemplos/aula11-mundo/index.md){ .md-button }
[:material-code-tags: Exemplo `aula10-bringup`](../../exemplos/aula10-bringup/index.md){ .md-button }

!!! danger "O G3.0 vence amanhã, 30/09"
    O bloco de launch não coube na Aula 10 — estava previsto que ele cederia se o tempo apertasse, e cedeu. Ele abre esta aula, e o **G3.0** (`bringup.launch.py` subindo o sistema inteiro) vence no dia seguinte.

    Logo atrás vêm o **G3.1** (mundo de simulação, 06/10) e o **G3.2** (árvore de TF completa, 10/10) — que é o gate de verdade do TP3.

## A ideia da aula em uma frase

**A odometria não erra por ruído; erra por viés.** Ruído se cancela: medir mais vezes ajuda, a média converge. Viés não se cancela — ele entra na conta sempre com o mesmo sinal, e **cresce com a distância percorrida**.

Por isso nenhum filtro sobre `/odom` conserta um robô perdido, e por isso existe o SLAM: para medir o erro acumulado contra uma referência que não se mexe — as paredes — e publicar a correção. Essa correção tem nome, e é uma aresta da sua árvore de TF: `map → odom`.

## Por que a aula está nesta ordem

Ordenada por **custo de perda**, como a anterior. O que vence antes vem primeiro; o que tem folga vem por último, e fica declarado de antemão.

| Bloco | Serve a | Vence | Se faltar tempo |
|---|---|---|---|
| 1. Launch do sistema inteiro | G3.0 | **amanhã** | não pode cair |
| 2. O mundo é um produtor de dados | G3.1 | 06/10 | não pode cair |
| 3. `map → odom` e a deriva | G3.2 | 10/10 | não pode cair |
| 4. O que o Nav2 acrescenta | TP4 | 30/10 | **volta na Aula 12** |

## Objetivos

Ao final da aula você deve conseguir subir o seu projeto inteiro com um `ros2 launch` e provar que ele subiu; explicar quem publica cada aresta da árvore `map → odom → base_link → sensores`; demonstrar a deriva da odometria com um número, e justificar por que ela não se resolve com mais medições; e dizer o que o Nav2 acrescenta a um robô que apenas reage.

## Baixar o material desta aula

```bash
# 1) baixar o material (pode repetir sempre — a linha do rm evita o erro de pasta já existente)
rm -rf /tmp/PBRoboticos_prof_dacio
cd /tmp && git clone --depth 1 https://github.com/Prof-Dacio-INFNET/PBRoboticos_prof_dacio.git

# 2) o mundo mínimo desta aula
cp -r /tmp/PBRoboticos_prof_dacio/exemplos/aula11-mundo/aula11_mundo \
      ~/projeto-pb-SEU-USUARIO/ros2_ws/src/

# 3) o bringup da Aula 10, se você ainda não tem
cp -r /tmp/PBRoboticos_prof_dacio/exemplos/aula10-bringup/aula10_bringup \
      ~/projeto-pb-SEU-USUARIO/ros2_ws/src/

cd ~/projeto-pb-SEU-USUARIO/ros2_ws
colcon build --packages-select aula11_mundo aula10_bringup
source install/setup.bash
```

Sem compilar e sem ROS 2, o mundo roda e se testa sozinho:

```bash
cd /tmp/PBRoboticos_prof_dacio/exemplos/aula11-mundo
python3 testar.py
python3 simular.py --segundos 90
```

## Parte 1 — Um comando sobe o sistema inteiro

Este é o bloco que faltou na semana passada, e o **G3.0 vence amanhã**.

```bash
ros2 launch aula10_bringup bringup.launch.py
```

O [`aula10-bringup`](../../exemplos/aula10-bringup/index.md) demonstra os três mecanismos que o seu `bringup.launch.py` vai precisar: **compor** com `IncludeLaunchDescription`, **parametrizar** com um YAML que vem de fora, e **condicionar** com `IfCondition`.

### Um launch que sobe sem erro não é um launch que funciona

Subir é o que o launch faz. Funcionar é outra afirmação, e ela precisa de prova:

```bash
ros2 launch aula10_bringup bringup.launch.py --show-args   # o que dá para configurar
ros2 node list                                             # quem realmente subiu
ros2 param dump /percepcao/detector                        # com que valores
```

A terceira é a que quase ninguém faz, e é a que pega o erro abaixo.

### O YAML que ninguém lê

```bash
ros2 launch aula10_bringup bringup.launch.py \
  params:=$(ros2 pkg prefix aula10_bringup)/share/aula10_bringup/config/sistema-armadilha.yaml
ros2 param get /percepcao/detector taxa_hz     # 2.0 — o padrão do código, não o 9.0 do arquivo
```

O arquivo pedia `taxa_hz: 9.0`. O nó subiu com `2.0`. **Nenhum erro foi impresso em lugar nenhum.**

A causa é a chave do YAML: `detector:` significa o nó `/detector`, na raiz, mas o launch empurrou o nó para `/percepcao/detector`. Os nomes não casam, e a regra do ROS 2 é ignorar o que não casa — sem avisar. As curas são `/percepcao/detector:` ou o curinga `/**:`; **prefira o curinga**, que sobrevive à mudança de namespace.

O `conferir-params.py` pega isso sem ROS 2 instalado:

```bash
ros2 node list | python3 conferir-params.py config/sistema.yaml -
```

### Nada espera nada

Repare na subida: o `supervisor` quase sempre nasce antes do `detector`, avisa que não recebeu dado, e se recupera sozinho. Isso é **correto**.

Em ROS 2 o grafo é descoberto, não montado em ordem. Um nó que só funciona se subir depois de outro vai quebrar no dia em que a máquina estiver mais lenta, e esse dia costuma ser o da apresentação. A regra é o nó **tolerar a ausência do outro**.

## Parte 2 — O mundo é um produtor de dados, não uma janela

O TP3 pede um cenário de simulação. A pergunta que importa é: **do que o seu sistema realmente depende?**

Não do Gazebo. Ele depende de um tópico `/scan`, de um tópico `/odom`, e de uma árvore de TF que ligue os dois ao robô. Qualquer coisa que produza esses três serve — e é por isso que este exemplo existe.

```bash
ros2 launch aula11_mundo mundo.launch.py
ros2 topic hz /scan
ros2 topic echo /odom --once
```

O [`aula11-mundo`](../../exemplos/aula11-mundo/index.md) tem 12 × 8 metros, duas salas ligadas por uma porta e três obstáculos — o "cenário não trivial" que o TP3 pede. O laser é ray-casting sobre uma grade de ocupação, em numpy. **Sem física, sem render e sem janela.**

!!! tip "Isso não é desistir do Gazebo — é chegar nele com o esqueleto pronto"
    Trocar o nó `mundo` por um Gazebo publicando nos mesmos tópicos deixa **todo o resto valendo**: o launch, os frames, o SLAM, o Nav2.

    É o mesmo movimento das Aulas 6, 9 e 10 — o contrato fica, o miolo troca. O simulador é um detalhe de implementação atrás de uma interface, e quem monta o sistema na ordem certa pode trocar de simulador numa tarde.

### Quem publica cada aresta

Saber isto é metade do G3.2:

```
map ──────────► odom ──────────► base_footprint ──► (URDF) ──► camera_link
 │               │                    │
 │               │                    └──► laser_frame
 │               │
 │               └── o nó `mundo`, integrando a odometria
 └── um static_transform_publisher — e ele é um PLACEHOLDER
```

`base_footprint → camera_link` já é conhecido: é o `robot_state_publisher` lendo o seu URDF, que foi o G2.5. O que é novo hoje são as duas arestas de cima — e a de cima de tudo está, neste momento, **mentindo**.

## Parte 3 — `map → odom`: a aresta que corrige

Suba o mundo e olhe o número crescer:

```bash
ros2 launch aula11_mundo mundo.launch.py
ros2 topic echo /deriva      # noutro terminal
```

`/deriva` é a distância entre onde o robô **está** e onde a odometria **acha** que ele está. Ela cresce. Agora desligue o viés e compare:

```bash
ros2 launch aula11_mundo mundo.launch.py deriva:=0.0
```

Offline, a mesma coisa sai em figura — linha cinza é a verdade, vermelha é a odometria:

```bash
python3 simular.py --deriva 3 --saida com-deriva.png
python3 simular.py --deriva 0 --saida sem-deriva.png
```

### Viés não é ruído, e essa é a diferença que decide tudo

O modelo aplica um erro de **escala** de 3% — o erro de quem mediu o raio da roda com régua. Não é aleatório: tem sinal constante.

Ruído você combate com repetição, porque ele se cancela; foi por isso que a Aula 9 usou mediana em vez de uma medida só. Viés não se cancela nunca. Ele entra na integral toda vez com o mesmo sinal, e o erro **cresce com a distância percorrida**. Rodar mais tempo piora.

Daí a conclusão que a aula quer: **nenhum filtro sobre `/odom` resolve.** O conserto não está em medir melhor a roda; está em medir contra outra coisa — algo que não se mexe. As paredes.

O SLAM faz exatamente isso: compara o `/scan` de agora com o mapa que vem construindo, calcula quanto a odometria já errou, e publica essa correção como `map → odom`. Enquanto essa aresta for identidade, como hoje, o robô acredita na própria odometria — e no RViz2 você vê o laser deslizar para fora das paredes.

!!! warning "É por isso que o G3.2 é o gate de verdade do TP3"
    Noventa por cento dos problemas de SLAM e de Nav2 são problemas de TF disfarçados. Se o `view_frames` mostrar árvore quebrada ou dois `odom`, **pare tudo** e conserte antes de tocar no G3.3 — insistir no SLAM com TF errada é queimar uma semana.

## Parte 4 — O que o Nav2 acrescenta

O `piloto.py` é o navegador mais burro que funciona: anda reto e gira quando fecha na frente. Trinta linhas, e ele explora o mundo inteiro.

Repare no que ele **não** tem — e é essa lista, e não outra coisa, que o Nav2 é:

| O piloto não sabe | O Nav2 acrescenta |
|---|---|
| onde está | localização (AMCL) contra o mapa |
| para onde vai | um objetivo, enviado como **action** |
| o que há além do que o laser vê agora | custos global e local, construídos do mapa |
| o que fazer quando trava | comportamentos de recuperação |

A segunda linha é a que fecha o semestre até aqui: **o objetivo do Nav2 é uma action** — com feedback periódico e cancelamento, exatamente as da Aula 8. O Nav2 não é assunto novo; é a montagem de peças que já estão no lugar.

## Tarefa da semana

**G3.0** — o seu `bringup.launch.py` subindo o sistema inteiro com um comando. Evidência: `ros2 launch <projeto> bringup.launch.py` e a saída de `ros2 node list` com todos os nós, em `docs/evidencias/tp3/`. Vence **30/09**.

**G3.1** — o seu cenário carregando com o robô e a câmera no lugar. Vence 06/10. Se o Gazebo rodar na sua máquina, use-o; se não rodar, o mundo mínimo desta aula conta — **e você documenta a escolha no relatório**, que é o que a disciplina pede em qualquer decisão de escopo.

**G3.2** — a árvore `map → odom → base_link → sensores` completa e sem warning. Evidência: `docs/evidencias/tp3/frames.pdf`. Vence 10/10.

## Socorro rápido

| Sintoma | Causa provável |
|---|---|
| `Package not found` | terminal sem `source install/setup.bash` |
| `No module named 'numpy'` | `sudo apt install python3-numpy` — nunca pip no python do sistema |
| o YAML não muda nada | a chave não casa com o nome do nó — use `/**:` |
| `package 'meu_robo_description' not found` | suba com `modelo:=false` |
| `/deriva` sempre 0 | subiu com `deriva:=0.0`, ou o robô não está andando |
| o robô não anda | `ros2 topic hz /scan` — sem laser, o piloto não decide |
| `view_frames` mostra duas árvores | falta a aresta `map → odom` |
| `view_frames` gera PDF vazio | o launch não está rodando — TF é fluxo, não arquivo |
| RViz2 vazio | o G3.2 não depende dele — `view_frames` e `tf2_echo` provam o gate |
| o laser desliza para fora das paredes | **é o ponto da aula**, não um defeito |

## Para a próxima aula (06/10)

**SLAM Toolbox: a correção publicada.** A aresta `map → odom` deixa de ser identidade e passa a ser calculada, e o mapa do G3.3 sai disso. Chegue com o G3.0 entregue e a árvore de TF do G3.2 fechada — o SLAM é construído sobre ela, e não conserta TF errada.
