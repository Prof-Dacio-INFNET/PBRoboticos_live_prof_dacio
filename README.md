# PBRoboticos (turma LIVE) — Material da Disciplina · Prof. Dácio (INFNET 26T4/27T1)

Repositório **público de material** do Projeto de Bloco: Sistemas Robóticos, **turma live GRLEDCR3C2-N2-L1** (segundas à noite, Zoom) — consulta permanente dos alunos. Derivado do material da turma presencial 2026.2; o que foi portado está em `ORIGEM.md`. Atualizado a cada aula: consulte pelo navegador ou clone e rode `git pull` semanalmente:

```bash
gh repo clone Prof-Dacio-INFNET/PBRoboticos_live_prof_dacio
```

## Estrutura

- `aulas/` — por aula: roteiro, PDF da apresentação e arquivos usados em sala (ex.: `etapa02-aula03/`)
- `tutoriais/` — guias de ambiente (ROS 2 Humble no WSL2 **ou** no VirtualBox, workspace/colcon, câmera), processo (GitHub e entregas, uso de IA) e as tarefas semanais
- `recursos/` — o que estrutura o projeto do semestre: catálogo de projetos, derivações e aplicações, simulação × hardware real, gates de cada TP, desafios opcionais e `check-ambiente.sh`
- `exemplos/` — pacotes ROS 2 prontos para rodar, por aula (`aula02-comunicacao`, `aula03-visao`) e por TP (`tp1…tp5`), sob licença MIT
- `cheatsheets/` — consulta rápida de comandos (ROS 2, colcon, git, OpenCV, Gazebo…)

## Regras de entrega (resumo — o oficial está no Moodle)

**A entrega oficial de todo TP é no MOODLE** (ZIP de códigos + PDF + links). O repositório individual `pb-live-<usuario>` (criado pelo professor, você é convidado como colaborador) é **complementar e obrigatório**: é nele que o desenvolvimento acontece, e a tag `tpN` é o que se corrige como código. Não é opcional nem dispensável — a organização do repositório, o histórico de commits e a rastreabilidade das decisões são critérios de avaliação em todos os TPs.

Arquivos grandes e vídeos vão por **link público ou não-listado** (nunca privado). A responsabilidade de acessibilidade é do aluno: se o avaliador não consegue abrir, não existe.

**Requisitos:** Ubuntu 22.04 + ROS 2 Humble + Python 3.10 **na sua própria máquina** — WSL2 (padrão) ou Ubuntu nativo; VirtualBox para quem não consegue WSL2; Mac Apple Silicon em regime best-effort (UTM arm64). Ver `tutoriais/`.

## Licença e citação

© 2026 Dácio Moreira de Souza. Material didático sob **CC BY-NC-ND 4.0** (citação obrigatória; proibidos uso comercial e distribuição modificada) — ver `LICENSE.md`. Códigos em `exemplos/` sob **MIT** (`exemplos/LICENSE`), reutilizáveis nos projetos dos alunos com manutenção do aviso de copyright.

## Onde consultar este material

- **GitHub (fonte):** https://github.com/Prof-Dacio-INFNET/PBRoboticos_live_prof_dacio
- **Site (GitHub Pages):** https://prof-dacio-infnet.github.io/PBRoboticos_live_prof_dacio/
- **Espelho + arquivos grandes:** https://daciosouza.com.br/PB_sistRoboticos_live/
