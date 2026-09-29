# Gazebo para o TP3 — instalar, conferir e desistir na hora certa

Este tutorial existe porque o TP3 pede um cenário de simulação, e o caminho mais
óbvio é o Gazebo. Ele é uma ferramenta excelente e **também** é a peça mais
provável de consumir a sua semana sem entregar gate nenhum.

Então ele começa pela pergunta que a maioria dos tutoriais não faz.

## 1. Você precisa mesmo do Gazebo?

O seu sistema não depende do Gazebo. Ele depende de três coisas: um tópico
`/scan`, um tópico `/odom`, e uma árvore de TF que ligue os dois ao robô. O
[mundo mínimo da Aula 11](../exemplos/aula11-mundo/index.md) produz as três sem
física, sem render e sem janela.

O que o Gazebo acrescenta, de verdade:

| Acrescenta | Vale para você? |
|---|---|
| Física: colisão, atrito, inércia, o robô tombando | sim, se o seu projeto depende de dinâmica |
| Câmera simulada publicando imagem | sim, se o seu domínio é visão e você não tem webcam |
| Sensores 3D (profundidade, IMU) | sim, se o seu projeto os usa |
| Mundos 3D prontos e editor visual | conveniência, não requisito |
| Fidelidade para a defesa do trabalho | **nenhuma** — a régua é a métrica, não a ferramenta |

Se nenhuma das três primeiras linhas é o seu caso, **o Gazebo é opcional para o
seu TP3**, e o mundo mínimo fecha G3.0, G3.1 e G3.2. Documente a escolha no
relatório e siga. Decisão de escopo documentada é decisão; escondida é buraco.

!!! tip "A ordem que economiza a semana"
    Monte o sistema com o mundo mínimo **primeiro** — launch, frames, SLAM. Só
    então troque o produtor de dados. Se o Gazebo não subir, você perdeu uma
    tarde em vez da semana, e o TP3 continua de pé.

## 2. Qual Gazebo — e a armadilha da versão

**Esta seção é a que mais economiza tempo.** Gazebo e ROS 2 têm pareamentos
oficiais, e usar o par errado quebra de formas confusas.

| ROS 2 | Gazebo oficial |
|---|---|
| **Humble** (o nosso) | **Fortress** |
| Jazzy | Harmonic |
| Kilted | Ionic |

Nós usamos **Humble**, então o par é o **Fortress**.

!!! danger "Não instale o Harmonic no Humble"
    Harmonic é o par do Jazzy. Existe um pacote não oficial
    (`ros-humble-ros-gzharmonic`, do `packages.osrfoundation.org`) que **conflita
    com os pacotes `ros-humble-ros-gz*`** — o apt vai querer remover um para
    instalar o outro, e você termina com meia instalação dos dois.

    Se você já instalou o Harmonic por engano, desinstale antes de seguir.

Uma pista para reconhecer em que mundo você está: o Fortress ainda usa o nome
antigo, **Ignition**. O binário é `ign gazebo` e os tipos de mensagem são
`ignition.msgs.X`. Do Garden em diante virou `gz sim` e `gz.msgs.X`. Tutorial da
internet que usa `gz sim` **não é para a nossa versão** — e essa é a origem da
maior parte dos erros que parecem inexplicáveis.

## 3. Instalar

```bash
sudo apt update
sudo apt install -y ros-humble-ros-gz
```

Esse metapacote traz o simulador, a ponte (`ros_gz_bridge`) e os utilitários
(`ros_gz_sim`). Não precisa de PPA extra: vem do repositório do ROS 2 que você
já configurou na Etapa 1.

Confira que os três chegaram:

```bash
ign gazebo --versions
ros2 pkg list | grep ros_gz
```

## 4. Conferir que abre — e o teste de dois minutos

```bash
ign gazebo shapes.sdf
```

Deve abrir uma janela com três formas geométricas. Se abriu, pule para a seção 5.

### Se a janela abrir preta (WSL2, quase sempre)

O Gazebo desenha em 3D acelerado. No WSL2 isso passa pelo WSLg, e o Fortress com
renderização por software (`llvmpipe`) é uma combinação **conhecidamente
problemática** — é bug registrado no projeto, não erro seu.

Tente, nesta ordem, um por vez:

```bash
export LIBGL_ALWAYS_SOFTWARE=1
ign gazebo shapes.sdf

# se continuar preto, force a engine antiga de renderização
ign gazebo --render-engine ogre shapes.sdf

# se continuar preto, rode sem interface e veja se o SIMULADOR vive
ign gazebo -s -r shapes.sdf          # -s = server only, -r = rodando
```

O terceiro comando é o que importa. **Se o servidor roda sem a interface, o
Gazebo está funcionando** — o que quebrou foi só o desenho. Você ainda pode
publicar `/scan` e `/odom` pela ponte e fechar os gates, visualizando no RViz2,
que é muito mais leve.

!!! warning "Critério de desistência: trinta minutos"
    Marque no relógio. Se em **trinta minutos** você não tiver nem a janela nem o
    servidor rodando, pare e volte ao mundo mínimo.

    Isso não é desânimo, é gestão de risco — a mesma coisa que o material pede
    quando a webcam não abre. O TP3 tem sete gates, e nenhum deles é "instalou o
    Gazebo".

## 5. A ponte: o Gazebo fala outra língua

O Gazebo não publica em tópicos ROS 2. Ele tem o próprio transporte, e a
`ros_gz_bridge` traduz. É isto que faz o simulador virar um produtor de dados
como qualquer outro.

```bash
ros2 run ros_gz_bridge parameter_bridge \
  /scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan \
  /odom@nav_msgs/msg/Odometry[ignition.msgs.Odometry \
  /cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist
```

A sintaxe é `/topico@TipoROS<direção>TipoGazebo`, e a direção está no caractere:

| Caractere | Direção | Use em |
|---|---|---|
| `[` | Gazebo **→** ROS | sensores: `/scan`, `/odom`, imagem |
| `]` | ROS **→** Gazebo | comandos: `/cmd_vel` |
| `@` | os dois lados | quando precisar mesmo dos dois |

**Errar a direção é o erro mais comum**, e ele falha em silêncio: o tópico
aparece em `ros2 topic list`, mas `ros2 topic hz` nunca imprime nada. Se um
tópico existe e não tem taxa, olhe o caractere antes de olhar qualquer outra
coisa.

Lembre do prefixo: no Fortress é `ignition.msgs.`, não `gz.msgs.`.

## 6. Trocar o mundo mínimo pelo Gazebo sem mexer no resto

Esta é a razão de ter começado pelo mundo mínimo. O seu `bringup.launch.py`
sobe o nó `mundo`; agora ele sobe o Gazebo mais a ponte. **Tudo o mais continua
igual** — os nomes dos tópicos, os frames, o SLAM, o Nav2, os seus nós.

```python
# antes
Node(package='aula11_mundo', executable='mundo', name='mundo', parameters=[params]),

# depois
ExecuteProcess(cmd=['ign', 'gazebo', '-r', mundo_sdf], output='screen'),
Node(package='ros_gz_bridge', executable='parameter_bridge',
     arguments=['/scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan',
                '/odom@nav_msgs/msg/Odometry[ignition.msgs.Odometry',
                '/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist'],
     output='screen'),
```

Uma linha trocada por duas, e o resto do sistema não percebe. É o mesmo
princípio do contrato do detector e das interfaces da Aula 6: **o contrato fica,
o miolo troca**.

Uma diferença que você precisa tratar: o Gazebo publica o seu próprio
`odom → base_link`, então **tire o nó `mundo` do launch** para não ter dois
publicadores da mesma aresta. Dois publicadores de uma transformada é o defeito
que o `view_frames` mostra como árvore estranha, e que trava o SLAM.

## 7. Um mundo e um robô, no mínimo

O mundo é um arquivo `.sdf`. O menor útil tem chão, luz e uma parede:

```xml
<?xml version="1.0"?>
<sdf version="1.8">
  <world name="meu_mundo">
    <plugin filename="ignition-gazebo-physics-system"
            name="ignition::gazebo::systems::Physics"/>
    <plugin filename="ignition-gazebo-sensors-system"
            name="ignition::gazebo::systems::Sensors">
      <render_engine>ogre2</render_engine>
    </plugin>
    <include>
      <uri>https://fuel.openrobotics.org/1.0/OpenRobotics/models/Ground Plane</uri>
    </include>
    <light type="directional" name="sol">
      <direction>-0.5 0.1 -0.9</direction>
    </light>
  </world>
</sdf>
```

Guarde em `worlds/meu_mundo.sdf` no seu projeto — o gate pede exatamente essa
pasta. E coloque o seu robô dentro a partir do URDF que você já validou no G2.5:

```bash
ros2 run ros_gz_sim create -topic robot_description -name meu_robo
```

Para o laser aparecer, o URDF precisa de um bloco `<gazebo>` declarando o
sensor. Esse é o ponto em que o URDF do G2.5 deixa de ser só geometria — e é
também onde vale ir devagar, um sensor por vez, conferindo com
`ign topic -l` se ele começou a publicar antes de adicionar o próximo.

!!! tip "Confira o nome antes de decorar"
    Nomes de executáveis e launch files mudaram entre versões do Gazebo. Antes de
    copiar comando de tutorial da internet, veja o que a **sua** instalação tem:

    ```bash
    ls $(ros2 pkg prefix ros_gz_sim)/share/ros_gz_sim/launch/
    ros2 run ros_gz_sim create --help
    ign topic -l
    ```

    É o mesmo hábito que a Aula 10 pediu com `ros2 param dump`: verificar a
    afirmação em vez de assumir.

## 8. Socorro rápido

| Sintoma | Causa provável |
|---|---|
| `ign: command not found` | faltou `ros-humble-ros-gz`, ou o terminal sem `source /opt/ros/humble/setup.bash` |
| apt quer remover `ros-humble-ros-gz*` | você está instalando o Harmonic no Humble — não instale |
| janela preta no WSL2 | `LIBGL_ALWAYS_SOFTWARE=1`, depois `--render-engine ogre`, depois `-s` sem interface |
| tópico existe mas `topic hz` não imprime | direção errada na ponte: `[` e `]` estão trocados |
| `gz sim: command not found` | tutorial de outra versão; no Fortress é `ign gazebo` |
| tipo de mensagem não reconhecido | usou `gz.msgs.X`; no Fortress é `ignition.msgs.X` |
| árvore de TF estranha, dois `odom` | o nó `mundo` e o Gazebo publicando a mesma aresta — tire um |
| o robô aparece e afunda no chão | falta `<collision>` no URDF, ou inércia irreal |
| laser não publica | falta o bloco `<gazebo>` com o sensor no URDF; confira com `ign topic -l` |
| simulação lenta demais | mundo menor, menos feixes no laser, e `-s` sem interface enquanto depura |

## 9. Se você desistir

Não é derrota, e não custa nota. Escreva no relatório o que tentou, em que ponto
parou e com qual hardware — isso é uma seção de limitações honesta, que o
material pede em todos os TPs.

E volte para o [mundo mínimo](../exemplos/aula11-mundo/index.md): ele fecha
G3.0, G3.1 e G3.2, e alimenta o SLAM do G3.3 com `/scan` de verdade.
