# Tutorial do Aluno — GitHub e o Repositório do Projeto de Bloco

**Disciplina:** Projeto de Bloco: Sistemas Robóticos · **Prof.:** Dácio Moreira de Souza

> ## ⚠️ Antes de tudo: onde a entrega vale
>
> **A entrega oficial de TODO TP — e do projeto final — é feita no MOODLE**, obrigatoriamente com: **ZIP com os códigos**, **PDF do relatório**, **link do repositório**, **link do vídeo** e tudo mais que o enunciado pedir, **registrado por lá**. O Moodle é a fonte da verdade da entrega: **o que não está no Moodle não foi entregue**, mesmo que esteja no GitHub.
>
> O GitHub é **complementar e obrigatório** (não é apoio dispensável): é onde você desenvolve, versiona, sincroniza entre máquinas e onde o professor **corrige o seu código** (no estado da sua branch/tag de entrega) — e a **qualidade do repositório é critério de avaliação** em todos os TPs. Moodle **e** GitHub, sempre os dois.

## Parte A — Semana 1: prepare sua conta

### A1. Conta no GitHub (5 min)

1. Se ainda não tem: crie em [github.com/signup](https://github.com/signup) com um **nome de usuário profissional** — ele aparecerá no seu repositório e, um dia, no seu currículo. O professor é `dacioms`, por exemplo. Já `capitao-gambiarra`, por mais que descreva com precisão certos momentos da robótica, talvez não seja a melhor escolha (ele será nosso aluno-exemplo fictício neste tutorial).
2. Use um e-mail que você **acessa de verdade** (você vai precisar dele na Parte B) e ative a **autenticação em dois fatores** (Settings → Password and authentication).
3. (Recomendado) Solicite o [Student Developer Pack](https://education.github.com/pack) com o e-mail institucional — Copilot e outros benefícios grátis.

### A2. Git e GitHub CLI (5 min — na sua máquina)

No terminal do Ubuntu — do WSL2, nativo ou da VM, tanto faz (ver o tutorial da sua rota de ambiente):

```bash
sudo apt update && sudo apt install -y git gh
git config --global user.name "Seu Nome"
git config --global user.email "seu-email@exemplo.com"
gh auth login    # GitHub.com → HTTPS → Login with a web browser
```

Repita em **cada máquina** que usar (notebook e PC, por exemplo).

## Parte B — Receber o seu repositório (sem Classroom)

Nesta turma **não existe link de assignment**: o professor cria o seu repositório e te convida.

1. **Preencha o formulário de cadastro da turma** ([forms.gle/6Lbq37mhYQWJKGxX7](https://forms.gle/6Lbq37mhYQWJKGxX7) — também fixado no Infnet.Online) com o seu **usuário do GitHub exatamente como está no seu perfil** (ex.: `capitao-gambiarra`, não o e-mail). É esse dado que vira o nome do seu repositório.
2. O professor roda o script que cria **`pb-live-<seu-usuario>`** na organização `Prof-Dacio-INFNET` (privado, só você e ele) e te **convida como colaborador**. Rodadas de criação: **quarta 07/10**, **sábado 10/10** e, para quem ficou de fora, **ao vivo na Aula 2 (19/10)**.
3. **📧 Aceite o convite.** Chega por e-mail ("*dacioms invited you to collaborate on Prof-Dacio-INFNET/pb-live-…*") e também em [github.com/notifications](https://github.com/notifications). Abrir a URL do repositório logado também mostra o botão de aceitar. **Sem aceitar, o repositório dá erro 404.** Confira o spam.
4. Confirme: abra `https://github.com/Prof-Dacio-INFNET/pb-live-SEU-USUARIO` — se a página carrega, está pronto para a Parte C.

## Parte C — Clonar e conhecer o repositório

```bash
cd ~
gh repo clone Prof-Dacio-INFNET/pb-live-SEU-USUARIO   # ex.: pb-live-dacioms
cd pb-live-SEU-USUARIO
```

| Pasta/arquivo | O que vai aí |
|---|---|
| `README.md` | Identificação, como executar, status dos TPs — **preencha já no 1º dia** |
| `PROJETO.md` | Proposta e planejamento do seu projeto (TP1; evolui depois) |
| `ARTEFATOS.md` | **Links dos vídeos (por TP) e artefatos grandes** + como cada um é gerado |
| `scripts/` | `setup.sh` e `reproduzir.sh` — o professor corrige executando-os! |
| `ros2_ws/src/` | Seus pacotes ROS 2 |
| `docs/relatorios/` · `docs/evidencias/` | Relatórios entregues e capturas por TP |
| `docs/decisoes.md` | **Registro do que mudou no projeto, onde e por quê** (ver Parte E) |
| `docs/diario.md` | Diário de desenvolvimento (recomendado) |
| `media/` | Vídeos curtos/GIFs leves (longos → YouTube) |
| `consulta/` | Cheatsheets de git, ROS 2 e regras de entrega — não editar |
| `exemplos/` | Código-base de referência: **copie para `ros2_ws/src` e adapte** ao seu projeto |

**O que você pode e não pode mudar:** pode **adicionar** qualquer estrutura útil ao seu desenvolvimento; **não pode alterar nem remover** as estruturas de referência de entrega (README, PROJETO, ARTEFATOS, scripts/, docs/, consulta/, .github/). Um verificador automático acusa (X vermelho no commit) se algo protegido sumir. Os `exemplos/` são seus: adapte à vontade.

## Parte D — Commits, push e as branches

**O repositório é a sua mochila** — nada fica só no seu disco:

```bash
git pull          # AO COMEÇAR (indispensável se você usa mais de uma máquina)
git add . && git commit -m "Implementa publisher de câmera em /camera/image_raw"
git push          # AO TERMINAR (e no fim de cada aula ao vivo!)
```

Commits **pequenos e frequentes**, mensagens que dizem o que a mudança faz. O histórico é critério de avaliação — um commit gigante na véspera conta contra você. Trabalho perdido por falta de push (disco que falha, WSL reinstalado) é responsabilidade sua.

**Branches:** use à vontade para desenvolver com segurança (`git checkout -b feat/deteccao-faixas`), **mas a correção e as entregas olham exclusivamente a `main`**: antes da tag do TP, faça merge de tudo que conta (`git checkout main && git merge feat/deteccao-faixas && git push`). Branch não mergeada = trabalho invisível para a correção. Mantenha a `main` sempre compilável.

## Parte E — Reprodutibilidade e evolução documentada

O professor corrige **clonando e executando**:

```bash
./scripts/setup.sh        # dependências além do padrão da disciplina
./scripts/reproduzir.sh   # compila, obtém/gera artefatos, roda a demo
```

Reproduziu de primeira? **Destaque na avaliação.** Precisou adivinhar comandos? Perde pontos de organização. Regras:

- **Todo artefato derivado tem fonte:** o script que gera o modelo/dataset/mapa fica versionado. Treino demorado? O `reproduzir.sh` **baixa** do seu link público e o comando de treino fica documentado ao lado.
- **Arquivo grande não entra no git:** Google Drive/OneDrive com **link público**, registrado em `ARTEFATOS.md`.
- **Seu projeto vai mudar — e tudo bem.** Escopo, sensores e arquitetura podem ser refinados ao longo dos TPs. O que a disciplina espera é o que se espera de um engenheiro: **rastreabilidade**. Cada mudança relevante ganha uma entrada no `docs/decisoes.md` (data, o que mudou, onde, por quê, impacto) e o `PROJETO.md` reflete o plano atual. Refatorar com registro é sinal de maturidade; mudar silenciosamente parece improviso.

## Parte F — Como entregar cada TP

**1) Entrega oficial — MOODLE (obrigatória, é o que vale).** O Moodle aceita **até 4 arquivos de 20 MB cada**. O desejável: **1 PDF** com o relatório completo e detalhado + **ZIPs pertinentes** com os códigos (+ os links de repo e vídeo registrados no envio).

*E se não couber?* Priorize nos ZIPs: código-fonte, launch/config e evidências-chave. O que exceder (datasets, modelos treinados, vídeos) fica no GitHub/links públicos, referenciado no `ARTEFATOS.md` e citado no relatório — **use essa divisão apenas quando realmente necessário**; o padrão é caber no Moodle.

**Confira duas vezes:** arquivo errado, corrompido ou incompleto enviado é responsabilidade sua. Depois do upload, **baixe e abra** o próprio ZIP/PDF para conferir o que de fato subiu.

**Uma dica de quem já corrigiu muito TP:** commits no GitHub e envios no Moodle têm carimbo de data e hora — eles contam a sua linha do tempo por você. Links "vivos" de drive não registram quando o arquivo ficou disponível. Prefira deixar o que é da entrega commitado ou anexado até o prazo: isso **protege você** de qualquer dúvida sobre datas, sem depender da memória de ninguém.

**2) Fotografia no repositório — branch + tag (complementar, obrigatória p/ correção do código):**

No 1º dia, rode uma vez `./scripts/init-branches.sh` (cria `dev` e as branches `entrega-*`). Você trabalha na **`dev`**; a **`main`** guarda o estado estável. Na entrega:

```bash
git checkout main && git merge dev && git push              # 1) main completa
git checkout entrega-tpN && git merge --ff-only main && git push   # 2) branch = main
git tag tpN && git push origin tpN                          # 3) tag imutável
git checkout dev                                            # 4) volte a trabalhar
```

| TP | Branch / Tag | Prazo (sexta, 23h59) — turma live |
|---|---|---|
| TP1 | `entrega-tp1` / `tp1` | **13/11** |
| TP2 | `entrega-tp2` / `tp2` | **11/12** |
| TP3 | `entrega-tp3` / `tp3` | **12/02** (2027) |
| TP4 | `entrega-tp4` / `tp4` | **12/03** (2027) |
| TP5 | `entrega-tp5` / `tp5` | **19/03** (2027) |
| Final | `entrega-final` / `final` | **26/03** (2027) ⚠️ Sexta-feira Santa — regra do prazo será confirmada no enunciado |

> ⚠️ **Depois de entregar, NÃO altere a branch `entrega-tpN` nem a tag `tpN`** — elas são a fotografia da entrega e **vale a data da última alteração**. Continue evoluindo o projeto na `dev`/`main`.

**Checklist antes de fechar:** dev→main mergeado → entrega-tpN == main + tag → front-matter do README atualizado (entregue/branch/tag/video/data) → `ARTEFATOS.md` com vídeo e artefatos (links testados em aba anônima) → `reproduzir.sh` roda num clone limpo → `docs/decisoes.md` atualizado → **Moodle enviado e conferido**.

> Errou a tag? `git tag -d tp1 && git push origin :refs/tags/tp1`, corrija e recrie (antes do prazo).

## Problemas comuns

| Sintoma | Causa/solução |
|---|---|
| **O repositório dá 404** | **Convite pendente** (Parte B, passo 3): aceite pelo e-mail ou em `github.com/notifications`; confira o spam. Se não há convite, o seu usuário no formulário pode estar errado — avise no Infnet.Online |
| Não preenchi o formulário / mudei de usuário | Preencha ou avise no Infnet.Online com o usuário correto; o repositório sai na rodada seguinte |
| `Permission denied` no clone/push | `gh auth login` nesta máquina; confirme que é o **seu** `pb-live-…` |
| `rejected: fetch first` no push | Você editou em outra máquina sem pull. `git pull`, resolva, `git push` |
| "Meu trabalho não apareceu na correção" | Estava numa branch não mergeada na `main` — merge antes da tag |
| Trabalho de uma máquina não está na outra | Faltou `git push` numa e `git pull` na outra. Crie o hábito da Parte D |
| X vermelho no commit (estrutura) | Você alterou/removeu algo protegido — restaure (Parte C) |
| Professor disse que meu link/vídeo "não existe" | Estava privado/restrito. Teste em aba anônima; corrija o compartilhamento |
| Não acho meu repositório | A barra lateral esquerda do github.com lista os repositórios em que você colabora; ou vá direto em `github.com/Prof-Dacio-INFNET/pb-live-SEU-USUARIO` |

## Regras importantes

- **Moodle é a entrega oficial** — sem exceção. GitHub sem Moodle = não entregue.
- **Vídeos: YouTube "público" OU "não listado" — nunca "privado".** Drives: "qualquer pessoa com o link". **Links são responsabilidade sua: inacessível = inexistente.**
- Correção e entrega olham a **`main`**; estruturas protegidas do repositório não se alteram nem removem.
- O repositório é **privado**: não torne público nem copie de colegas — commits têm autor, data e hora.
- Uso de IA generativa: siga a orientação da disciplina (declaração de uso no relatório; a arguição valida a autoria).
- Dúvidas de git **não são vergonha**: quase todo caso comum está resolvido neste manual e no [cheatsheet de git](../cheatsheets/git-cheatsheet.md).
