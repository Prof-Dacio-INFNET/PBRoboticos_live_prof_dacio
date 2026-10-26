---
titulo: "TP1 — enunciado, checklist de verificação e gates (turma live)"
tp: 1
etapas: "1–2"
leitura_em_aula: 2026-10-26
entrega: 2026-11-13
---

# TP1 — Ambiente, comunicação básica e pipeline inicial de visão

**Entrega: sexta, 13/11/2026, no Moodle · Etapas 1–2 · Competência 1 · lido em aula em 26/10 (Aula 3)**

O enunciado **oficial** é o do Moodle; esta página é a versão lida em aula, com as datas desta turma, um checklist de verificação para você usar antes de entregar e os gates. Os conceitos são lançados no Moodle, pelo professor, a partir da entrega completa — nada aqui antecipa conceito. Se algo aqui parecer diferente do Moodle, vale o Moodle — e avise no Infnet.Online.

## O que se pede (as quatro tarefas do enunciado)

1. **Escolher o projeto e planejar os TPs.** Um robô de inspeção visual, um rastreador de objetos com ROS 2, um robô perceptivo com câmera/sensores, ou uma proposta própria aprovada pelo professor — com fundamentação técnica. Na prática: o `PROJETO.md` do seu repositório preenchido (domínio, usuário, funcionalidades, sensores, arquitetura prevista, **plano por TP**, riscos e plano B). Use o [catálogo](catalogo-projetos.md) e as [derivações](derivacoes-projetos.md); hardware real é bem-vindo, com a simulação viva como plano B ([simulação × hardware](simulado-vs-hardware.md)).
2. **Configurar o ambiente.** Ubuntu 22.04 + ROS 2 Humble, workspace colcon, OpenCV + Python, validação com `ros2 doctor` — documentado com capturas. Você já fez isso na [tarefa da semana 1](../tutoriais/tarefa-semana01-ambiente-e-repositorio.md); a evidência é o `check-ambiente.txt`.
3. **Comunicação básica.** Um publisher de câmera em `/camera/image_raw`; um subscriber que converte para HSV e segmenta por cor; um serviço `/vision/status` que responde o número de objetos segmentados. É o exemplo `aula03-visao` adaptado ao **seu** objeto — a [tarefa da Aula 3](../tutoriais/tarefa-aula03-visao.md) é exatamente isto.
4. **Pipeline de visão.** Detecção de faces e extração de *features* (OpenCV), o grafo de comunicação (`rqt_graph`) e o diagrama de nós/tópicos no relatório. A parte de faces/features entra como **demonstração** (um nó ou script com o detector Haar do OpenCV e um extrator como ORB ou Shi-Tomasi sobre a sua cena); o centro do TP é o pipeline do item 3.

## O que se entrega em 13/11

No **Moodle** (entrega oficial, que gera registro acadêmico): o **PDF do relatório** (modelo em `docs/relatorios/relatorio-template.md` do seu repositório), o **ZIP do código** (sem `build/`, `install/`, `log/` e `.git/`), o **link do repositório** `pb-live-<usuario>` e o **link do vídeo** (YouTube público ou não-listado, até 5 min: o sistema rodando, a troca de parâmetro ao vivo, a oclusão).

No **GitHub** (complementar e obrigatório — critério de avaliação): `main` atualizada, branch `entrega-tp1`, **tag `tp1`** empurrada, evidências em `docs/evidencias/tp1/`, `PROJETO.md` com os gates marcados. O passo a passo está no [checklist de entrega do TP1](../tutoriais/checklist-entrega-tp1.md). Um TP entregue só no Moodle com repositório vazio perde pontos; a partir do TP2, um TP entregue **só** no repositório não é aceito.

## Checklist de verificação antes de entregar

A competência 1 do plano de ensino tem quatro subcompetências. Use a tabela como roteiro de conferência: para cada linha, pergunte "onde, na minha entrega, isso está demonstrado?" — se a resposta for "no meu terminal" ou "na minha cabeça", ainda falta commitar ou escrever.

| Subcompetência | O que conferir | Onde fica na sua entrega |
|---|---|---|
| **1.1** ambiente e arquitetura ROS 2 | ambiente funcional e integrado; workspace que compila do zero; você sabe explicar quem publica, quem assina e quem serve | `check-ambiente.txt`, estrutura do pacote, relatório |
| **1.2** sensores, atuadores e tópicos padrão | imagem no grafo; QoS de sensor escolhida e justificada; taxa medida nas duas pontas **e interpretada** | `topic-hz.txt`, publisher da câmera, relatório |
| **1.3** tópicos e serviços | subscriber + segmentação + contagem; `/vision/status` com informação do domínio; grafo completo | código, `rqt_graph.png`, saída do serviço |
| **1.4** OpenCV básico (cores, faces, features) | HSV e contornos sobre o seu objeto, duas classes, limiares medidos; faces/features demonstrados | `segmentacao.png`, nó/script de faces, relatório |

Tópicos que valem revisão com calma, porque são os que mais costumam faltar: o código é **seu** e roda sobre o **seu** objeto (renomear o exemplo não é adaptar); a taxa está medida e interpretada, não só colada; o experimento de oclusão está reproduzido e discutido; um caso difícil (iluminação, fundo, objeto parecido) está registrado com números; as limitações estão nomeadas; os parâmetros estão fora do código; o histórico de commits conta o processo; e nada que a entrega afirma fica sem evidência commitada. Quem quiser ir além da tarefa tem no [Desafio 2](desafios/desafio-02-visao.md) um caminho medido (duas classes com métrica de acerto, iluminação quebrada, oclusão, custo em Hz) — e um relatório com números em vez de adjetivos.

Faces/features (item 4): entra como demonstração; o centro do TP é o pipeline do item 3, e o que diferencia é a integração ao pipeline e a discussão. O uso de IA é permitido e **declarado** ([orientação](../tutoriais/orientacao-uso-ia.md)); a arguição final cobra que você explique cada linha entregue.

## Os sete gates, com as datas desta turma

Um gate ou é verdade ou não é, e se prova com um comando. Copie o bloco abaixo para o seu `PROJETO.md` e faça **um commit por gate**, com a mensagem começando pelo código (`G1.3: segmentação sobre tampas azuis e verdes`). As datas são recomendações com folga; o único prazo formal é 13/11.

```markdown
<!-- PB:GATES-TP1 -->
- [ ] G1.0 ambiente operante — `check-ambiente.sh` em "Tudo pronto!" · evidência `docs/evidencias/tp1/check-ambiente.txt` · dom 01/11
- [ ] G1.1 projeto declarado: domínio, usuário, duas classes, trilha S/H/R, plano B · `PROJETO.md` · dom 01/11
- [ ] G1.2 imagem no grafo, taxa medida nas duas pontas · `docs/evidencias/tp1/topic-hz.txt` · dom 01/11
- [ ] G1.3 segmentação e contagem sobre o MEU objeto, duas classes · `docs/evidencias/tp1/segmentacao.png` · sex 06/11
- [ ] G1.4 /vision/status com informação do domínio + rqt_graph · `docs/evidencias/tp1/rqt_graph.png` + saída do serviço · dom 08/11
- [ ] G1.5 relatório fechado (decisões, oclusão, limitações, IA declarada) · `docs/relatorios/relatorio-tp1.md` · qua 11/11
- [ ] G1.6 entrega: main atualizada, branch entrega-tp1, tag tp1, PDF+ZIP+links no Moodle · sex 13/11
```

Marque `[x]` quando passou com evidência commitada, `[ ]` enquanto não chegou a data, e `[!]` quando **venceu sem passar** — um `[!]` declarado é informação e custa pouco; um `[x]` sem evidência é o contrário, e é fácil de verificar. A tabela completa (como provar cada gate) está em [gates de cada TP](gates-tps.md).

### A declaração do G1.1 (cole no topo do `PROJETO.md`)

```markdown
<!-- PB:PROJETO -->
**Domínio:** (ex.: triagem de recicláveis numa esteira)
**Usuário:** (quem usaria o sistema e para quê)
**Classes percebidas no TP1:** classe A = … · classe B = … (duas, distinguíveis por cor)
**Fonte de imagem no TP1:** sintética / webcam / vídeo gravado — e por quê
<!-- PB:TRILHA -->
**Trilha:** S (simulada) · H (híbrida) · R (hardware real) — e o que é "real" nela
**Plano B:** o que acontece se o hardware/câmera falhar na semana da entrega
```

## O calendário do TP1 nesta turma

| Quando | O quê |
|---|---|
| seg 26/10 | Aula 3: leitura do TP1; imagem no grafo e segmentação; exemplo de ponta a ponta |
| dom 01/11 | **Parte A da tarefa da Aula 3** na `dev`: pacote seu compilando, taxa medida, G1.1 declarado |
| seg 02/11 | feriado — sem aula; a semana é a **Parte B** (tarefa guiada) com plantão no Infnet.Online |
| dom 08/11 | **Parte B**: duas classes, YAML, `/vision/status` com domínio, evidências (G1.3 e G1.4) |
| seg 09/11 | Aula 4: interfaces próprias + **clínica do TP1** (traga uma pergunta específica) |
| qua 11/11 | relatório fechado (G1.5) |
| **sex 13/11** | **entrega no Moodle** + tag `tp1` (G1.6) |

Prazo que cai em feriado passa para meio-dia do dia seguinte — regra da disciplina; não se aplica ao TP1.

## Onde gastar o tempo (e onde não)

Gaste em: código **seu** rodando sobre o **seu** objeto; taxa medida nas duas pontas e **interpretada**; `/vision/status` que fala a língua do domínio; parâmetros fora do código; a oclusão reproduzida e discutida; histórico de commits que conta o processo. Não gaste em: estética do relatório, quantidade de páginas, vídeo editado. Confira antes de enviar, porque inviabiliza a avaliação: link que não abre em janela anônima, ZIP com `build/`, repositório com um único commit "entrega final".
