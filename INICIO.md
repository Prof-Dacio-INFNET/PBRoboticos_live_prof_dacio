---
hide:
  - navigation
---

# PB Sistemas Robóticos — INFNET · Turma Live 26T4/27T1

Material da disciplina **Projeto de Bloco: Sistemas Robóticos**, turma **GRLEDCR3C2-N2-L1** (live).
Aulas às **segundas-feiras à noite, pelo Zoom** (1h30, gravadas) · Prof. Dácio Moreira de Souza · comunicação pelo **Infnet.Online** · entregas e conceitos no **Moodle**.

<div class="pb-hero" markdown>
**Ao longo de dois trimestres você vai construir um sistema robótico seu, do zero até a demonstração.** Não são cinco trabalhos avulsos: são cinco cortes do *mesmo* projeto, que cresce de um nó publicando imagem (TP1) até um robô que percebe, mapeia, navega, manipula e aprende (TP5). Escolher bem o projeto na primeira semana é a decisão mais barata e mais valiosa do bloco.
</div>

## Comece por aqui

<div class="grid cards" markdown>

-   :material-console:{ .lg .middle } **1. Monte o ambiente — na sua máquina**

    ---

    Ubuntu 22.04 + ROS 2 Humble + Python 3.10. Nesta turma **não há laboratório**: o seu computador é o único ambiente. **Escolha uma rota:** WSL2 (padrão, Windows 10/11), Ubuntu 22.04 nativo, ou VirtualBox (quem não consegue WSL2). Mac com chip Apple: rota *best-effort* (UTM arm64) — avise no formulário. Os tutoriais validam cada pré-requisito antes de instalar.

    [:octicons-arrow-right-24: Setup ROS 2 Humble no WSL2](tutoriais/setup-ros2-humble-wsl2.md)

    [:octicons-arrow-right-24: Rota alternativa: VirtualBox](tutoriais/setup-ros2-humble-virtualbox.md)

-   :material-github:{ .lg .middle } **2. Receba e prepare o seu repositório**

    ---

    Preencha o **formulário de cadastro** com o seu usuário do GitHub; o professor cria o seu `pb-live-<usuario>` e te convida. **Aceite o convite por e-mail**, clone **dentro do Linux** (na home do Ubuntu — nunca numa pasta do Windows) e rode `init-branches.sh`. O repositório é parte da entrega, não um anexo dela.

    [:octicons-arrow-right-24: Manual do aluno: GitHub e entregas](tutoriais/manual-do-aluno-github.md)

-   :material-lightbulb-on:{ .lg .middle } **3. Escolha o seu projeto**

    ---

    Sete famílias no catálogo, dezenas de derivações possíveis. Escolha o domínio que te interessa — o esqueleto técnico é o mesmo. **Projetos com montagem em hardware são bem-vindos e recomendados** — leia antes *simulação × hardware real*: as mesmas reflexões valem para esta turma.

    [:octicons-arrow-right-24: Catálogo de projetos](recursos/catalogo-projetos.md)

    [:octicons-arrow-right-24: Simulação × hardware real](recursos/simulado-vs-hardware.md)

-   :material-flag-checkered:{ .lg .middle } **4. Marque os seus gates**

    ---

    Cada TP tem checkpoints verificáveis por comando, com data. Copie o checklist para o seu `PROJETO.md` e faça um commit por gate. A versão com as datas desta turma sai com cada enunciado.

    [:octicons-arrow-right-24: Gates de cada TP](recursos/gates-tps.md)

</div>

## Aula mais recente

**Aula 3 — segunda, 26/10/2026 — O TP1, lido; e a imagem no grafo** <span class="pb-tag next">atual</span>

**A aula ao vivo tem 1h30: ela mostra, o guia de estudo ensina.** A Aula 3 leu o **TP1** com as datas desta turma (entrega **sexta 13/11**; os sete gates estão na [página do TP1](recursos/tp1.md)) e mostrou o pipeline `câmera → segmentação → contagem → serviço` rodando de ponta a ponta no repositório do professor. O aprendizado acontece no **guia de estudo** (3h a 4h em três sessões), guiado pela tarefa em duas partes — e a semana de 02/11, sem aula, existe para a Parte B.

[Conteúdo e slides da aula](aulas/etapa02-aula03/index.md){ .md-button .md-button--primary }
[Guia de estudo da Aula 3](tutoriais/estudo-aula03-visao.md){ .md-button }
[Tarefa da Aula 3](tutoriais/tarefa-aula03-visao.md){ .md-button }
[TP1 — enunciado, checklist e gates](recursos/tp1.md){ .md-button }

!!! warning "Até domingo 01/11 (Parte A) e domingo 08/11 (Parte B): o pipeline de visão do seu projeto"
    Nesta ordem: **[guia de estudo](tutoriais/estudo-aula03-visao.md)** (comece por ele) → **[tarefa, Parte A](tutoriais/tarefa-aula03-visao.md)** até **01/11, 23h59**: pacote seu compilando, taxa medida nas duas pontas, `PROJETO.md` com o **G1.1** declarado (domínio, usuário, duas classes, trilha, plano B) → **Parte B** até **08/11, 23h59**: duas classes do seu domínio, parâmetros em YAML, `/vision/status` com domínio, oclusão registrada, evidências. [Desafio 2](recursos/desafios/desafio-02-visao.md) é opcional. **Não há aula em 02/11** (feriado); a Aula 4 (09/11) é a clínica do TP1.

!!! note "Atrasado na Aula 2 ou ainda sem ambiente?"
    A [tarefa da Aula 2](tutoriais/tarefa-aula02-primeiros-nos.md) e a [tarefa da semana 1](tutoriais/tarefa-semana01-ambiente-e-repositorio.md) continuam valendo — e vêm **antes** da desta semana. Sem repositório ainda? **[Formulário de cadastro](https://forms.gle/6Lbq37mhYQWJKGxX7)** (o convite chega por e-mail).

## Calendário de entregas

Todas as entregas são no **Moodle**, na sexta-feira indicada, com o repositório atualizado e a tag correspondente empurrada.

| Entrega | Data | Tema |
|---|---|---|
| **TP1** | sexta, 13/11/2026 | ambiente, comunicação básica e pipeline inicial de visão |
| **TP2** | sexta, 11/12/2026 | interfaces próprias, ações e parametrização |
| **TP3** | sexta, 12/02/2027 | integração, mapeamento (SLAM) e percepção avançada |
| **TP4** | sexta, 12/03/2027 | navegação autônoma, registro e percepção veicular |
| **TP5** | sexta, 19/03/2027 | manipulação, aprendizado e validação |
| **Entrega final** | sexta, 26/03/2027 ⚠️ | sistema integrado, vídeo e relatório |
| Apresentações | segundas, 29/03 e 05/04/2027 | banca e arguição (remotas) |

Prazo que cai em feriado passa para **meio-dia do dia seguinte** — regra da disciplina. ⚠️ 26/03/2027 é Sexta-feira Santa: a regra aplicada à entrega final será confirmada no enunciado.

## Como as entregas funcionam

A entrega **oficial e formal** de todo TP é no **Moodle**: ZIP dos códigos, PDF do relatório e os links. É o que gera registro acadêmico, e sem ela não há nota.

O **GitHub é complementar e obrigatório**, e também é critério de avaliação. O repositório é onde o processo fica visível: histórico de commits, branches `dev` → `main` → `entrega-tpN`, a tag `tpN` que congela o código corrigido, e as evidências commitadas. Um TP entregue só no Moodle, com repositório vazio ou com um único commit "projeto final", perde pontos — porque a disciplina avalia como você chegou lá, não apenas onde chegou.

Arquivos grandes (vídeos, datasets, bags, pesos de modelo) **não** vão para o Git. Publique em link acessível — YouTube **público ou não-listado**, nunca privado — e coloque o link no relatório e no README. A regra é dura de propósito: **se o avaliador não consegue abrir, não existe**. Teste cada link em uma janela anônima antes de entregar.

## Onde encontrar cada coisa

O material está organizado por uso, não por data. Em **[Aulas](aulas/index.md)** ficam o roteiro e os slides de cada encontro — e o calendário completo da turma. Em **[Tutoriais](tutoriais/index.md)** ficam os guias que você segue passo a passo, de setup a tarefa da semana. Em **[Projeto](recursos/index.md)** ficam as decisões estruturais: catálogo, derivações, simulação × hardware e os gates. Em **[Exemplos](exemplos/index.md)** ficam os pacotes ROS 2 prontos para rodar e adaptar (licença MIT — pode copiar). E em **[Consulta rápida](cheatsheets/index.md)** ficam as referências de comando para o dia a dia.

!!! info "Este material nasceu da turma presencial 2026.2"
    As páginas marcadas como *herdadas* ainda trazem datas e referências daquela turma; cada uma é adaptada antes da aula correspondente. O conteúdo técnico vale desde já.

!!! tip "Este site é atualizado a cada aula"
    Se preferir trabalhar offline, clone o repositório e rode `git pull` toda semana:
    ```bash
    gh repo clone Prof-Dacio-INFNET/PBRoboticos_live_prof_dacio
    ```
    Espelho e arquivos grandes: [daciosouza.com.br/PB_sistRoboticos_live](https://daciosouza.com.br/PB_sistRoboticos_live/).

## Uso de IA

Ferramentas de IA são **permitidas e incentivadas** — com declaração. O que se avalia é o seu entendimento, e a arguição final vai testar exatamente isso: você precisa saber explicar cada linha que entregou. As regras estão em [orientação sobre uso de IA](tutoriais/orientacao-uso-ia.md).

---

© 2026 Dácio Moreira de Souza. Material didático sob **CC BY-NC-ND 4.0**; códigos em `exemplos/` sob **MIT** e livremente reutilizáveis nos projetos, mantendo o aviso de copyright. Detalhes em [licença](licenca.md).
