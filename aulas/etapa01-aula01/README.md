# Aula 1 — Abertura, ROS 2 e o projeto do semestre

**Segunda, 05/10/2026 · Zoom · Etapa 1 · turma live**

[:material-file-pdf-box: Slides da Aula 1 (PDF)](apresentacao-aula01.pdf){ .md-button .md-button--primary }
[:material-clipboard-check: Tarefa da semana 1](../../tutoriais/tarefa-semana01-ambiente-e-repositorio.md){ .md-button }

!!! warning "12/10 é feriado — a próxima aula ao vivo é 19/10"
    A Etapa 1 tem uma única aula ao vivo. Conferir o ambiente e inicializar o repositório — o que normalmente ocupa uma segunda aula — você faz **sozinho, guiado**, ao longo da semana de 12/10, com o canal da turma no Infnet.Online para dúvidas. Tudo está na [tarefa da semana 1](../../tutoriais/tarefa-semana01-ambiente-e-repositorio.md).

## Como esta turma funciona

Quatro lugares, cada um com uma função — e vale o semestre inteiro. O **Zoom** é a aula: segundas à noite, gravada, com o chat aberto o tempo todo (ponto de controle a cada bloco e fila de mentoria por tela compartilhada no terceiro bloco). O **Infnet.Online** é o feed de avisos e o chat da turma: toda dúvida técnica vai com três itens — o comando que rodou, a saída completa e o resultado de `lsb_release -a`. O **Moodle** recebe só os TPs e o projeto final (ZIP + PDF + links): não há atividade semanal lá; o acompanhamento da semana é feito lendo o seu repositório. O **GitHub** é a oficina: o repositório `pb-live-<usuario>` é criado pelo professor a partir do formulário de cadastro, e `git push` ao fim de toda aula e de toda tarefa é o que mostra que a semana aconteceu.

## Baixar o material desta aula

A Aula 1 não tem pacote para compilar — o material que importa é o script que confere o seu ambiente. Quando o Ubuntu estiver instalado, baixe e rode:

```bash
# baixar o material (pode repetir sempre)
rm -rf /tmp/PBRoboticos_live_prof_dacio
cd /tmp && git clone --depth 1 https://github.com/Prof-Dacio-INFNET/PBRoboticos_live_prof_dacio.git

bash /tmp/PBRoboticos_live_prof_dacio/recursos/check-ambiente.sh
```

Ele detecta a sua rota (WSL2, VirtualBox ou nativo), confere Ubuntu, ROS 2, `colcon`, `git`, `gh`, `uv`, o `ROS_DOMAIN_ID` e a procedência do OpenCV e do NumPy. **Rode antes de pedir ajuda:** a saída dele é metade do diagnóstico — e é ela que você entrega como evidência da semana 1.

## O que foi visto

A aula abriu o bloco apresentando o que é um sistema robótico do ponto de vista de software: um conjunto de processos independentes que trocam informação por uma rede, e não um programa monolítico. A partir daí veio o vocabulário do ROS 2 — nós, tópicos, serviços, ações e parâmetros — com a analogia da mensageria: o tópico é um canal em que qualquer um publica e qualquer um assina, o serviço é uma pergunta com resposta, e a ação é uma tarefa longa que informa progresso e pode ser cancelada.

Na parte prática o professor rodou, com a tela compartilhada, `talker`/`listener`, o `turtlesim` com teleoperação, `rqt_graph` e `ros2 topic echo` — para **ver** o grafo existindo enquanto a tartaruga se move. O efeito é proposital: o grafo deixa de ser diagrama de slide e passa a ser algo observável com comando de terminal. Quem já tinha o ambiente pronto reproduziu em paralelo; quem não tinha, reproduz esta semana — é o passo 3 da tarefa. Nesta turma ninguém instala nada durante a aula: a sua máquina é o laboratório, e o tutorial foi escrito para ser seguido sozinho, com a saída esperada de cada passo.

O ciclo que organiza tudo é **sentir → pensar → agir**, rodando dezenas de vezes por segundo, com o ROS 2 levando as mensagens de um lado ao outro. Na mensageria: o **nó** é um programa que faz uma coisa bem; o **tópico** é o correio contínuo (publica quem quer, escuta quem precisa); o **serviço** é pergunta → resposta; a **ação** é a tarefa longa com progresso e cancelamento — ela chega no TP2.

A aula terminou apresentando a estrutura dos dois trimestres — cinco TPs que são cinco cortes do mesmo projeto (13/11, 11/12, 12/02, 12/03, 19/03; projeto final 26/03; apresentações 29/03 e 05/04) — e o catálogo de projetos, com o teste decisivo: o projeto precisa ter **o que perceber** (câmera) e **onde navegar** (ambiente/mapa), senão quebra no meio do caminho.

## Para fazer até domingo, 18/10

Em ordem, e cada passo é pré-requisito do seguinte. O passo a passo com as saídas esperadas está na [tarefa da semana 1](../../tutoriais/tarefa-semana01-ambiente-e-repositorio.md).

1. **Formulário de cadastro** ([forms.gle/6Lbq37mhYQWJKGxX7](https://forms.gle/6Lbq37mhYQWJKGxX7) — também fixado no Infnet.Online) — usuário do GitHub, rota de ambiente e hardware da sua máquina. **Hoje**: é dele que sai o seu repositório.
2. **Conta no GitHub** com nome profissional e 2FA — [manual do aluno, Parte A](../../tutoriais/manual-do-aluno-github.md).
3. **Ambiente**: Ubuntu 22.04 (jammy) + ROS 2 Humble + git + `gh` + `uv`, numa rota só. [WSL2](../../tutoriais/setup-ros2-humble-wsl2.md) é a padrão; Ubuntu nativo vale; [VirtualBox](../../tutoriais/setup-ros2-humble-virtualbox.md) para quem não consegue WSL2. Se `lsb_release -a` não disser 22.04, pare e corrija antes de qualquer outra coisa.
4. **Repositório**: aceitar o convite por e-mail, clonar dentro do Linux, rodar `init-branches.sh`, preencher o front-matter do README e commitar a evidência do `check-ambiente.sh` — [manual do aluno, Partes B e C](../../tutoriais/manual-do-aluno-github.md).
5. **Projeto**: leia o [catálogo](../../recursos/catalogo-projetos.md) e venha para a Aula 2 com um ou dois candidatos. **Projetos com montagem em hardware são recomendados** — Raspberry Pi, chassi com motores, câmera — e as reflexões de [simulação × hardware real](../../recursos/simulado-vs-hardware.md) valem integralmente: a simulação continua obrigatória como rede de segurança, e hardware falha perto do prazo.

## Duas regras que valem o semestre inteiro

O **`ROS_DOMAIN_ID` é um número de 1 a 100 só seu**, anotado no README do repositório. Nesta turma ninguém divide a rede de um laboratório, mas a regra continua: na sua casa pode haver outra máquina com ROS 2 (um colega de república, o Raspberry Pi do projeto), e com o mesmo domain ID vocês enxergam os nós um do outro — é assim que o ROS 2 foi desenhado (descoberta automática via DDS). Fixe o seu número agora e nunca mais pense nisso.

O repositório mora **dentro do Linux**, na home (`~`) — nunca numa pasta que é do Windows por baixo: `/mnt/c/...` no WSL2, `/media/sf_<nome>` no VirtualBox. Clonar lá funciona e é lento a ponto de atrapalhar, além de gerar problemas de permissão e de fim de linha que aparecem só no `colcon build`.
