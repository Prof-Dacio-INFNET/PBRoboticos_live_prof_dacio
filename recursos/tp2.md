---
titulo: "TP2 — enunciado, checklist de verificação e gates (turma live)"
tp: 2
etapas: "3–5"
leitura_em_aula: 2026-11-23
entrega: 2026-12-11
---

# TP2 — Interfaces customizadas, ação assíncrona, rastreamento e URDF

**Entrega: sexta, 11/12/2026, no Moodle · Etapas 3–5 · Competência 2 · lido em aula em 23/11 (Aula 6)**

O enunciado **oficial** é o do Moodle; esta página é a versão lida em aula, com as datas desta turma, o que cada tarefa já tem de pronto no seu repositório, um checklist de verificação para usar antes de entregar, e os gates. Os conceitos são lançados no Moodle, pelo professor, a partir da entrega completa — nada aqui antecipa conceito. Se algo aqui parecer diferente do Moodle, vale o Moodle — e avise no Infnet.Online.

## Cenas dos últimos episódios

O TP1 deixou o seu projeto com um ambiente que funciona, uma imagem circulando no grafo, um nó que segmenta o **seu** objeto por cor, um serviço `/vision/status` e um relatório. Desde então, três aulas construíram o que o TP2 pede: a Aula 4 mostrou o limite do tipo pronto (o número preso dentro de uma frase), a Aula 5 trouxe as interfaces próprias e a ação pelo lado de quem usa, e a Aula 6 abriu o servidor da ação. **Boa parte do TP2 já está nas tarefas dessas semanas** — a tabela da próxima seção diz qual parte.

## O contexto, nas palavras do enunciado

Depois de configurar a comunicação básica em ROS 2 e o pipeline inicial de visão no TP1, este TP avança para a **camada de comunicação avançada** e para a **percepção visual inteligente** do seu sistema: as interfaces de dados do projeto (mensagens e serviços do seu domínio), as ações ROS 2 para tarefas de longa duração com feedback em tempo real, e a evolução do módulo de visão — rastreamento de objetos, detecção com YOLO e as primeiras redes neurais treinadas. Ao final, você entrega o pacote ROS 2 com as interfaces customizadas, os nós de rastreamento e detecção em operação, o modelo URDF do robô e o relatório atualizado, com evidências de todos os módulos.

## O que se pede (as quatro tarefas do enunciado), e o que você já tem

| # | A tarefa do enunciado | Onde ela está nesta turma |
|---|---|---|
| **1** | **Criar as interfaces customizadas do projeto.** Ao menos uma mensagem (`.msg`) relevante ao seu domínio — o enunciado dá como exemplo `DeteccaoObj.msg`, com `string classe`, `float32 confianca`, `int32 x`, `int32 y`, `int32 w`, `int32 h` —, um serviço (`.srv`) de controle e uma ação (`.action`) com goal, feedback de progresso e result com métricas. Compilar com o Colcon e verificar com `ros2 interface list`. | [Tarefa da Aula 4](../tutoriais/tarefa-aula04-interfaces.md) (o pacote, o `.msg` e o `.srv`) e [tarefa da Aula 5](../tutoriais/tarefa-aula05-acoes.md) (o `.action`). Quem fez as duas tem esta tarefa quase pronta. |
| **2** | **Implementar a ação assíncrona central do projeto.** O Action Server executa a tarefa principal do seu projeto, com feedback e suporte a cancelamento. O Action Client envia goals, exibe cada feedback recebido e registra o result final. Demonstrar a operação simultânea de servidor e cliente, com captura de tela. | [Aula 6](../aulas/etapa04-aula06/index.md) e a [tarefa da Aula 6](../tutoriais/tarefa-aula06-servidor-acao.md): o servidor e o cliente da **sua** ação, com a evidência do cancelamento. |
| **3** | **Implementar rastreamento de objetos em vídeo.** Usar YOLO para detectar os objetos relevantes ao projeto, aplicar um filtro para suavizar a trajetória rastreada, e exibir a trilha de rastreamento e a bounding box no frame de saída. | Aula 7 (30/11): detecção treinada e métrica declarada. A mensagem de detecção que você criou na tarefa 1 é a que este nó publica. |
| **4** | **Parametrizar o sistema e elaborar o URDF.** Todos os parâmetros do projeto (limiar de confiança, frequência de publicação, modelo YOLO) em arquivo YAML; carregar no nó, e demonstrar a alteração dinâmica em tempo de execução com `ros2 param`. Elaborar o URDF do robô, com links, joints, câmera e sensores simulados. | Os parâmetros em YAML você usa desde a Aula 3; a Aula 8 (07/12) junta tudo num launch e traz o URDF. Tutorial de apoio: [URDF, TF e RViz2](../tutoriais/urdf-tf-rviz2.md). |

Duas observações de leitura. **A mensagem do exemplo tem largura e altura** (`w`, `h`): a `Deteccao.msg` da aula tem `x`, `y` e `area`; quando o seu nó passar a publicar caixas (tarefa 3), acrescente `w` e `h` — é uma linha no `.msg` e um build. **"Ação central" quer dizer a tarefa principal do seu projeto**, a que leva mais de um segundo e faz sentido interromper: a que você escolheu na tarefa da Aula 5.

## O que se entrega em 11/12

No **Moodle** (entrega oficial, que gera registro acadêmico): o **PDF do relatório** (a partir de `docs/relatorios/relatorio-template.md`, como `relatorio-tp2.md`), o **ZIP do código** (`git archive` a partir da tag, como no TP1), o **link do repositório** `pb-live-<usuario>` e o **link do vídeo** (YouTube público ou não listado, até 5 min: a ação sendo pedida, acompanhada e cancelada; o rastreamento com a trilha; um parâmetro trocado com o sistema no ar; o URDF no RViz2).

No **GitHub** (complementar e obrigatório — critério de avaliação): `main` atualizada, branch `entrega-tp2`, **tag `tp2`** empurrada, e as evidências em `docs/evidencias/tp2/`. O caminho é o mesmo do TP1, trocando `tp1` por `tp2`: [checklist de entrega](../tutoriais/checklist-entrega-tp1.md). A partir deste TP, uma entrega **só** no repositório, sem o Moodle, não é aceita.

## Checklist de verificação antes de entregar

A competência 2 do plano de ensino tem quatro subcompetências. Para cada linha, pergunte "onde, na minha entrega, isso está demonstrado?" — se a resposta for "no meu terminal" ou "na minha cabeça", ainda falta commitar ou escrever.

| Subcompetência | O que conferir | Onde fica na sua entrega |
|---|---|---|
| **2.1** interfaces customizadas (`.msg`, `.srv`, `.action`) | o pacote de interfaces é **separado** e compila; os campos falam do **seu** domínio (e não do exemplo); a ação tem goal, feedback e result com sentido; o servidor dá feedback **e** pode ser cancelado; o cliente mostra o feedback e registra o resultado | `interface.txt`, `acao-projeto.txt`, `acao-servidor.txt`, a captura de servidor e cliente juntos |
| **2.2** parâmetros dinâmicos e URDF | os parâmetros estão num YAML, e não no código; um deles é trocado com o sistema no ar, e a troca tem efeito visível; o URDF carrega no RViz2 com links, joints e a câmera, e a árvore de TF é coerente | `config/*.yaml`, saída do `ros2 param`, `urdf/`, print do RViz2 |
| **2.3** detecção e rastreamento | o detector roda sobre o **seu** objeto; a trajetória é suavizada por um filtro, e você sabe dizer qual e por quê; a trilha e a caixa aparecem no frame de saída; o nó publica a **sua** mensagem — o rastreamento está no grafo do ROS 2, e não isolado num script | o nó de rastreamento, um print ou GIF com a trilha, `ros2 topic echo` da sua mensagem |
| **2.4** redes neurais em tempo real | o modelo usado está nomeado (qual, de onde veio, com que classes); há uma **medida** do que ele acerta e do que ele custa em taxa; as limitações estão ditas | `metrica-tracking.md`, o relatório |

Tópicos que valem revisão com calma, porque são os que mais costumam faltar: as interfaces são **suas** (renomear o `pb_interfaces` não é adaptar); o servidor da ação **cancela de verdade**, e há evidência disso; a ação rejeita algum pedido de propósito; o rastreamento conversa com o resto do sistema por tópico; a taxa com o detector ligado está medida e interpretada; os parâmetros estão fora do código; o histórico de commits conta o processo; e nada que a entrega afirma fica sem evidência commitada. O uso de IA é permitido e **declarado** ([orientação](../tutoriais/orientacao-uso-ia.md)).

## Os sete gates, com as datas desta turma

Um gate ou é verdade ou não é, e se prova com um comando. As datas são **referência para você se localizar**, com folga; o único prazo formal é 11/12. Copie o bloco para o seu `PROJETO.md` e marque o que já tem evidência.

```markdown
<!-- PB:GATES-TP2 -->
- [ ] G2.0 pacote de interfaces separado, compilando · `docs/evidencias/tp2/interface.txt` · dom 22/11
- [ ] G2.1 .msg e .srv do MEU domínio, visíveis no ambiente; /vision/status migrado · `interface.txt` · dom 22/11
- [ ] G2.2 ação definida, e servidor respondendo do objetivo ao resultado · `acao-projeto.txt` + `acao-servidor.txt` · qua 02/12
- [ ] G2.3 ação com feedback periódico e cancelamento que funciona · `acao-servidor.txt` + captura de servidor e cliente · dom 06/12
- [ ] G2.4 detecção e rastreamento sobre o MEU objeto, com filtro, trilha e uma métrica declarada · `metrica-tracking.md` · dom 06/12
- [ ] G2.5 parâmetros em YAML com troca ao vivo + URDF no RViz2 com TF coerente · `config/`, `urdf/`, print · qua 09/12
- [ ] G2.6 entrega: main atualizada, branch entrega-tp2, tag tp2, PDF+ZIP+links no Moodle · sex 11/12
```

Marque `[x]` quando passou com evidência commitada, e `[!]` quando não fechou — com um parágrafo dizendo o que faltou e por quê. A tabela completa (como provar cada gate) está em [gates de cada TP](gates-tps.md#tp2-interfaces-proprias-acoes-e-parametrizacao).

## O calendário do TP2 nesta turma

| Quando | O quê |
|---|---|
| seg 16/11 | Aula 5: interfaces próprias; ações pelo lado de quem usa |
| dom 22/11 | tarefa da Aula 4 na `dev`: o pacote de interfaces, o `.msg` e o `.srv` do domínio |
| seg 23/11 | Aula 6: o servidor da ação por dentro; **leitura do TP2** |
| dom 29/11 | tarefa da Aula 5: os três casos do exemplo, e o `.action` do projeto |
| seg 30/11 | Aula 7: detecção treinada e métrica declarada |
| dom 06/12 | tarefa da Aula 6: o servidor e o cliente da ação do projeto, com o cancelamento |
| seg 07/12 | Aula 8: aterrissagem do TP2 — parâmetros, launch e URDF |
| **sex 11/12** | **entrega no Moodle** + tag `tp2` |

## Onde gastar o tempo (e onde não)

Gaste em: interfaces que descrevem o **seu** domínio; uma ação que é a tarefa principal do projeto, com feedback que informa e cancelamento que funciona; um rastreamento que está no grafo, publicando a sua mensagem; uma medida do que o detector acerta e do que ele custa; parâmetros fora do código. Não gaste em: treinar um modelo do zero quando um pré-treinado resolve o seu objeto (diga qual usou e por quê); um URDF detalhado além de links, joints, câmera e sensores; estética do relatório. Confira antes de enviar, porque inviabiliza a avaliação: link que não abre em janela anônima, ZIP com `build/`, e uma ação que não pode ser interrompida — um servidor que não cancela é um serviço lento com mais código.

**Não vai dar tempo de tudo?** A regra é a do TP1: entregue o que funciona e **declare** o que não funciona. Fonte sintética ou vídeo gravado valem para o rastreamento, ditos no relatório.
