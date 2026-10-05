# Aula 10 — Aterrissagem do TP2: o sistema sobe com um comando

!!! info "Página herdada da turma presencial — será adaptada antes da aula correspondente da turma live"
    O conteúdo técnico, os exemplos e as tarefas valem. As **datas, os nomes de sala e as referências a laboratório** são da turma presencial 2026.2; o calendário da turma live está em [Aulas](../index.md). Quando esta página for adaptada, este aviso some.


**Terça, 22/09/2026 · sala SJ205 · Etapa 5 (14/09–26/09)**

[:material-file-pdf-box: Slides da Aula 10 (PDF)](apresentacao-aula10.pdf){ .md-button .md-button--primary }
[:material-code-tags: Exemplo `aula10-bringup`](../../exemplos/aula10-bringup/index.md){ .md-button }
[:material-cube-outline: Tutorial de URDF e TF](../../tutoriais/urdf-tf-rviz2.md){ .md-button }

!!! danger "O TP2 vence sexta, 25/09 — três dias depois desta aula"
    O **G2.5** (YAML + URDF no RViz2 com TF coerente) vence **hoje**. A primeira metade da aula é a clínica que fecha esse gate, e a evidência sai da própria clínica.

    Esta é a **última aula antes da entrega**. O que não for resolvido aqui será resolvido sozinho, em casa, na quinta à noite.

## A ideia da aula em uma frase

**Um projeto que só você consegue subir não está entregue.** Até aqui cada nó foi rodado à mão, num terminal próprio, na ordem que você decorou. Hoje isso vira um comando — e a diferença não é conforto, é a diferença entre um trabalho que o avaliador consegue reproduzir e um que ele não consegue.

É o mesmo princípio do repositório: se o avaliador não consegue abrir, não existe. Se ele não consegue subir, também não.

## Por que a aula está nesta ordem

Esta aula está ordenada por **custo de perda**, e não por sequência lógica. O que vence antes vem primeiro; o que tem folga vem por último.

| Bloco | Serve a | Vence | Se faltar tempo |
|---|---|---|---|
| 1. Clínica de URDF e TF | G2.5 | **hoje** | não pode cair |
| 2. Aterrissagem | entrega do TP2 | 25/09 | não pode cair |
| 3. Contrato do detector | relatório do TP2 | 25/09 | não pode cair |
| 4. Launch | G3.0 do TP3 | 30/09 | **volta na Aula 11** |

Declarar antes o que será cortado é a mesma disciplina da Aula 9, aplicada ao tempo em vez de ao detector: a régua vem antes da medição, e o corte vem antes do aperto. O bloco 4 é o único com folga, então é ele que cede — por decisão, não por acidente.

## Objetivos

Ao final da aula você deve conseguir provar que o seu URDF carrega com TF coerente sem depender de janela gráfica; subir o seu sistema inteiro com um `ros2 launch`; explicar por que um launch não garante ordem de subida e o que fazer a respeito; descobrir sozinho quando um arquivo de parâmetros está sendo ignorado em silêncio; e fechar a entrega do TP2 com branch, tag e relatório.

## Baixar o material desta aula

```bash
# ── uma vez por terminal ──────────────────────────────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"

# 1) baixar o material (pode repetir sempre — a linha do rm evita o erro de pasta já existente)
rm -rf /tmp/PBRoboticos_live_prof_dacio
cd /tmp && git clone --depth 1 https://github.com/Prof-Dacio-INFNET/PBRoboticos_live_prof_dacio.git

# 2) o pacote de bringup, para a segunda metade
cp -r /tmp/PBRoboticos_live_prof_dacio/exemplos/aula10-bringup/aula10_bringup \
      "$PB_WS/src/"

cd "$PB_WS"
colcon build --packages-select aula10_bringup
source install/setup.bash
```

O conferidor de parâmetros roda solto, sem compilar e sem ROS 2:

```bash
python3 /tmp/PBRoboticos_live_prof_dacio/exemplos/aula10-bringup/conferir-params.py
```

## Parte 1 — Clínica de URDF e TF

Bancada aberta sobre o [tutorial de URDF, TF e RViz2](../../tutoriais/urdf-tf-rviz2.md), que cobre o **G2.5**. Ele está publicado desde 08/09; quem chegar sem ter lido vai gastar a clínica instalando pacote.

**Comece rodando o diagnóstico**, na raiz do seu `ros2_ws`. Ele percorre a cadeia inteira do gate, para no primeiro ponto que falhou e diz qual é o próximo comando:

```bash
bash recursos/clinica-urdf.sh
```

Depois rode o que ele mandar, e traga para a bancada o que travou:

```bash
check_urdf src/<seuprojeto>_description/urdf/<seu_robo>.urdf
ros2 launch <seuprojeto>_description ver_robo.launch.py
# noutro terminal, com o launch RODANDO:
ros2 run tf2_tools view_frames
ros2 run tf2_ros tf2_echo base_footprint camera_link
```

Os três tropeços conhecidos, todos documentados no tutorial: **TF exige o launch rodando** — sem ele o `view_frames` gera um PDF vazio sem reclamar; **janelas vazias no WSL2** se resolvem por bisseção com o `turtlesim`; e o **`<origin>` do joint confundido com o do visual** deixa o RViz2 parecendo certo com a TF errada.

!!! tip "O G2.5 não depende da janela gráfica"
    `check_urdf`, `view_frames` e `tf2_echo` rodam no terminal e provam exatamente o que o gate pede. Se o RViz2 não abre na sua máquina, você ainda entrega o G2.5 hoje — e resolve o RViz2 depois, com calma, porque ele volta no TP3.

## Parte 2 — Aterrissagem: o que significa entregar

O **G2.6** não é "mandar o trabalho". São quatro coisas verificáveis, e a correção olha para as quatro:

```bash
git checkout -b entrega-tp2          # 1. a branch da entrega
git tag tp2                          # 2. a tag, que congela o ponto exato
git push origin entrega-tp2 --tags   # 3. os dois no GitHub
```

E a quarta: **a postagem no Moodle**, que é a entrega oficial. O GitHub é complementar e obrigatório — ele é critério de avaliação, não repositório de conveniência —, mas o que marca a data é o Moodle.

O relatório precisa responder, no mínimo, ao que cada gate pediu. Para o TP2 isso significa as interfaces do seu domínio e por que elas existem (G2.0, G2.1), a action com feedback e cancelamento demonstrados (G2.2, G2.3), a métrica declarada com os números das duas versões e **onde cada uma falha** (G2.4), e a parametrização com o URDF e a TF (G2.5).

!!! warning "A armadilha clássica do TP2"
    Implementar a action como "um publisher com nome bonito". Se o seu servidor não pode ser cancelado no meio, o **G2.3 não passou** — e o G2.3 é o gate que a correção efetivamente testa. Se isso ainda está aberto, este é o momento de dizer, não quinta à noite.

## Parte 3 — Trocar o detector sem trocar a régua

Este é o bloco que ficou faltando na Aula 9, e ele ainda vale para a entrega de sexta.

O `avaliar.py` não sabe nada sobre como o detector funciona. Ele chama uma função que recebe a imagem e devolve `(x, y, w, h)` ou `None`. **Plugar um modelo treinado é escrever outra função com essa assinatura** — nada mais.

Essa separação é o ponto arquitetural, e é o mesmo princípio das interfaces da Aula 6: **o contrato fica, o miolo troca**. A régua sobrevive à troca do detector, e é exatamente por isso que os números continuam comparáveis. É também o mesmo princípio do launch, daqui a pouco: o `bringup.launch.py` não sabe o que cada nó faz; ele conhece só o nome e os parâmetros.

!!! note "Sobre YOLO, `torch` e a regra da disciplina"
    O gate diz *"YOLO ou equivalente"*, e o equivalente importa. O módulo `cv2.dnn` roda modelos ONNX e Darknet **sem** instalar `torch` nem `ultralytics` — é o OpenCV do apt que vocês já têm.

    Se quiser o ecossistema completo do YOLO, ele vai num **venv** (`uv venv --system-site-packages`), como script solto. Nunca no python do sistema, e nunca dentro de um nó ROS 2 — pelas mesmas razões do `KeyError: 16` da Aula 3.

    E o mais importante: **o que se avalia é a métrica e a justificativa, não o modelo.** Um HSV medido honestamente vale mais que um YOLO sem régua. A três dias da entrega, trocar um HSV medido por um YOLO não medido é piorar a nota.

## Parte 4 — Launch: um comando sobe o sistema inteiro

!!! warning "Não trabalhada em 22/09 — recuperada na Aula 11"
    Este era o bloco de folga declarado no começo da aula, e foi ele que cedeu quando o tempo apertou — como combinado. Ele abre a [Aula 11, de 29/09](../etapa06-aula11/index.md), a tempo do G3.0, que vence em 30/09. O texto continua aqui para quem quiser chegar lá com ele lido.

Launch vocês usam desde a Aula 2. O que muda agora é a escala: sair de "um launch por exemplo" para **um launch que sobe o projeto todo**, que é o que o G3.0 do TP3 vai cobrar em 30/09.

```bash
ros2 launch aula10_bringup bringup.launch.py
ros2 launch aula10_bringup bringup.launch.py modelo:=false   # sem o pacote da Aula 9
```

O [`aula10-bringup`](../../exemplos/aula10-bringup/index.md) compõe um sistema pequeno e completo: um subsistema de percepção incluído de outro arquivo, o modelo do robô da Aula 9 ligado por condição, e um YAML de parâmetros que vem de fora. Três mecanismos, e todos os três reaparecem no seu `bringup.launch.py`.

### Um launch que sobe sem erro não é um launch que funciona

Subir é o que o launch faz. Funcionar é outra afirmação, e ela precisa de prova:

```bash
ros2 launch aula10_bringup bringup.launch.py --show-args   # o que dá para configurar
ros2 node list                                             # quem realmente subiu
ros2 param dump /percepcao/detector                        # com que valores
```

A terceira é a que quase ninguém faz, e é a que pega o erro abaixo.

### O YAML que ninguém lê

Suba o sistema com o arquivo defeituoso que vem no pacote:

```bash
ros2 launch aula10_bringup bringup.launch.py \
  params:=$(ros2 pkg prefix aula10_bringup)/share/aula10_bringup/config/sistema-armadilha.yaml
ros2 param get /percepcao/detector taxa_hz     # 2.0 — o padrão do código, não o 9.0 do arquivo
```

O arquivo pedia `taxa_hz: 9.0`. O nó subiu com `2.0`. **Nenhum erro foi impresso em lugar nenhum**: o launch subiu, os nós subiram, o arquivo foi lido e os valores foram descartados em silêncio.

A causa é a chave do YAML. `detector:` significa o nó `/detector`, na raiz — mas o launch empurrou o nó para `/percepcao/detector`. Os nomes não casam, e a regra do ROS 2 é ignorar o que não casa, sem avisar.

Isso pertence à mesma família de falhas que vocês já encontraram: o `view_frames` que gera PDF vazio, a saturação que vira ruído quando o valor é quase zero, o `ros2 action list` que funciona sem `source`. **São erros que não se apresentam como erro** — e a defesa contra todos eles é a mesma: verificar a afirmação em vez de assumir que o silêncio é aprovação.

Para não descobrir isso no meio do TP3, o pacote traz um conferidor que roda sem ROS 2:

```bash
ros2 node list | python3 conferir-params.py config/sistema.yaml -
```

As duas curas são trocar a chave por `/percepcao/detector:` ou usar o curinga `/**:`. **Prefira o curinga**: ele sobrevive à mudança de namespace, e mudar namespace é exatamente o que você vai fazer quando o sistema crescer.

### Nada espera nada

Repare na subida: o `supervisor` quase sempre nasce antes do `detector`, avisa que não recebeu dado, e se recupera sozinho. Isso é o comportamento **correto**.

Em ROS 2 o grafo é descoberto, não montado em ordem — o launch dispara todos os processos e segue em frente. Um nó que só funciona se subir depois de outro vai quebrar no dia em que a máquina estiver mais lenta, e esse dia sempre chega: costuma ser o da apresentação.

A regra prática é que **o nó tolera a ausência do outro**. Se você acha que precisa de ordem de subida, quase sempre precisa é de um nó mais tolerante.

## Tarefa da semana

**Fechar o TP2 e entregar até sexta, 25/09.** Não há tarefa nova: o que existe é a entrega.

Antes de postar, confira o que a correção vai conferir — branch `entrega-tp2` no GitHub, tag `tp2` visível em `git tag --list`, relatório respondendo aos seis gates, evidências em `docs/evidencias/tp2/`, e a postagem no Moodle.

Se algum gate não fechou, **diga no relatório o que não fechou e por quê**. Um gate aberto e documentado custa muito menos que um gate aberto e escondido — e é a mesma honestidade que a Aula 9 pediu na hora de relatar onde o detector falha.

## Socorro rápido

| Sintoma | Causa provável |
|---|---|
| `view_frames` gera PDF vazio | o launch não está rodando — TF é fluxo, não arquivo |
| janelas do RViz2 vazias no WSL2 | bisseção com `turtlesim`; depois `LIBGL_ALWAYS_SOFTWARE=1` |
| o YAML não muda nada | a chave não casa com o nome do nó — rode o `conferir-params.py` |
| `ros2 param get` diz `Node not found` | use o nome que o `ros2 node list` imprime, com namespace |
| `Package 'aula10_bringup' not found` | terminal sem `source install/setup.bash` |
| `package 'meu_robo_description' not found` | suba com `modelo:=false` |
| `libexec directory ... does not exist` | `setup.cfg` com o nome antigo do pacote |
| `git tag --list` não mostra `tp2` | faltou o `--tags` no push |

## Para a próxima aula (29/09)

**[O mundo, a deriva e o mapa que corrige](../etapa06-aula11/index.md)**, abrindo a Etapa 6. A aula começa pelo bloco de launch acima, a tempo do G3.0, e segue para as duas arestas novas da árvore de TF — `map → odom` e `odom → base_link` — que são o que o G3.2 cobra.

A navegação autônoma entra como introdução: o Nav2 é construído sobre ações, da Aula 8, e TF coerente, do G2.5. Não é assunto novo — é a montagem do que já está no lugar, e ela faz sentido depois que existir mapa.

E é por isso que a clínica de hoje importa além do TP2: o **G3.2** do TP3 pede a árvore de TF completa e sem warning, e noventa por cento dos problemas de SLAM e de Nav2 são problemas de TF disfarçados.
