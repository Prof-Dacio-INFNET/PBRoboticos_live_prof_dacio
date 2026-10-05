---
title: "Tarefa da semana 1 — ambiente pronto e repositório no ar"
prazo: "domingo, 18/10/2026, 23h59"
---

# Tarefa da semana 1 — ambiente pronto e repositório no ar

**Prazo: domingo, 18/10/2026, 23h59** (a Aula 2 é na segunda, 19/10, e começa assumindo que isto foi feito).

A segunda-feira 12/10 é feriado, então a Etapa 1 tem uma aula ao vivo só. Esta tarefa substitui o encontro: ela faz, guiado e com saídas esperadas, o que a turma presencial fez em sala — e entrega o **G1.0 do TP1** (ambiente operante e repositório inicializado). Tempo total: 2 a 4 horas, dependendo do download do ROS 2. Faça na ordem: cada passo é pré-requisito do seguinte.

!!! tip "Travou? Peça ajuda do jeito certo"
    Poste no canal da turma no **Infnet.Online** três coisas: o comando exato que rodou, a saída completa e o resultado de `lsb_release -a`. Com isso a resposta vem em uma mensagem; sem isso, vem em cinco. Se houver um plantão no Zoom na semana de 12/10, o aviso sai no mesmo canal.

---

## Passo 0 — Formulário de cadastro (5 min, hoje)

Preencha o [formulário da turma](https://forms.gle/6Lbq37mhYQWJKGxX7) (link também fixado no Infnet.Online). Ele pede o seu **usuário do GitHub exatamente como aparece no seu perfil** (ex.: `capitao-gambiarra`), a rota de ambiente que você vai usar e os dados da sua máquina (sistema, RAM, disco livre, GPU). É desse formulário que sai o seu repositório: usuário errado = repositório para a pessoa errada.

**Sem conta no GitHub ainda?** Crie primeiro (Passo 1) e depois preencha.

## Passo 1 — Conta no GitHub (5 min)

Siga a [Parte A do manual do aluno](manual-do-aluno-github.md): nome profissional, e-mail que você acessa, **2FA ativado**. Student Developer Pack é recomendado, não obrigatório.

## Passo 2 — Ambiente: Ubuntu 22.04 + ROS 2 Humble (1 a 3 h)

Escolha **uma** rota e siga o tutorial dela do início ao fim:

| Rota | Quando | Tutorial |
|---|---|---|
| **WSL2** (padrão) | Windows 10/11 | [Setup ROS 2 Humble no WSL2](setup-ros2-humble-wsl2.md), Passos 1 a 6 |
| **Ubuntu 22.04 nativo** | já tem Ubuntu instalado ou dual boot | o mesmo tutorial, a partir da instalação do ROS 2 |
| VirtualBox | Windows Home sem WSL2, política corporativa, Mac Intel | [Rota alternativa: VirtualBox](setup-ros2-humble-virtualbox.md) |
| Mac com chip Apple | best-effort: UTM + Ubuntu 22.04 **arm64** | o tutorial WSL2 a partir da instalação do ROS 2; avise no formulário |

**O erro número 1** da disciplina é instalar o Ubuntu errado: `wsl --install` sem argumento instala uma versão mais nova, e o `ros-humble-desktop` **não existe** fora do 22.04 (jammy). Confira antes de instalar qualquer coisa:

```bash
lsb_release -a
```

Saída esperada (a linha que importa): `Codename: jammy`. Qualquer outra coisa: pare e volte ao Passo 1 do tutorial.

No fim do tutorial, o teste é o turtlesim: `ros2 run turtlesim turtlesim_node` abre a janela com a tartaruga. Se abriu, o ROS 2 está instalado e a parte gráfica funciona.

## Passo 3 — Confira o ambiente com o script (2 min)

No terminal do Ubuntu:

```bash
curl -sSL https://raw.githubusercontent.com/Prof-Dacio-INFNET/PBRoboticos_live_prof_dacio/main/recursos/check-ambiente.sh | bash
```

A primeira linha diz qual rota ele detectou (WSL2, VirtualBox ou nativo) — se estiver errada, você está no terminal errado. A última linha precisa ser:

```
✅ Tudo pronto!
```

Se for `⚠️ Há itens pendentes acima`, cada item diz o que falta e em qual tutorial está. Resolva, rode de novo. **Não siga para o Passo 4 com pendência** — o repositório não vai compilar nada enquanto o ambiente não estiver inteiro.

## Passo 4 — Receba o seu repositório (depende do professor)

Depois do formulário, o professor cria **`pb-live-<seu-usuario>`** na organização `Prof-Dacio-INFNET` e te convida como colaborador. Rodadas: **quarta 07/10** e **sábado 10/10**. Detalhes na [Parte B do manual](manual-do-aluno-github.md).

1. Abra o **e-mail** da conta GitHub (ou [github.com/notifications](https://github.com/notifications)) e **aceite o convite**. Sem aceitar, o repositório dá 404.
2. Confirme no navegador: `https://github.com/Prof-Dacio-INFNET/pb-live-SEU-USUARIO` carrega.

Preencheu o formulário depois de sábado 10/10? O seu repositório sai **ao vivo na Aula 2**. Faça os Passos 1–3 mesmo assim.

## Passo 5 — Clone, branches e identificação (10 min)

Tudo no terminal do Ubuntu, dentro do Linux (na home — nunca em `/mnt/c`):

```bash
sudo apt update && sudo apt install -y git gh
git config --global user.name "Seu Nome"
git config --global user.email "seu-email@exemplo.com"
gh auth login          # GitHub.com → HTTPS → Login with a web browser
```

```bash
# ── uma vez por terminal ──────────────────────────────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"

cd ~
gh repo clone "Prof-Dacio-INFNET/pb-live-$PB_USER"
cd "$PB_DIR"
./scripts/init-branches.sh
```

Saída esperada do `init-branches.sh`: uma linha `(criada)` para `dev` e para cada `entrega-*`, e no fim **"Você está na branch 'dev' — trabalhe aqui."** Confira com `git branch`: o asterisco está em `dev`.

Agora **preencha o bloco YAML no topo do `README.md`** (`aluno`, `github`, `projeto` pode ficar "a definir") e o nome na linha `<!-- PB:ALUNO -->`. Esse bloco é lido por script na correção — mantenha-o YAML válido (aspas, dois-pontos, indentação).

## Passo 6 — Evidência da semana 1: commit e push (10 min)

```bash
cd "$PB_DIR"
bash scripts/check-ambiente.sh > docs/evidencias/semana01-ambiente.txt
tail -n 1 docs/evidencias/semana01-ambiente.txt     # tem que mostrar: ✅ Tudo pronto!
git add README.md docs/evidencias/semana01-ambiente.txt
git commit -m "Semana 1: ambiente conferido e identificação preenchida"
git push
```

Saída esperada do `git push`: termina com `dev -> dev` sem a palavra `rejected`. Confirme no navegador: o arquivo `docs/evidencias/semana01-ambiente.txt` aparece na branch `dev` do seu repositório.

**Não há envio no Moodle nesta semana** — o Moodle fica só para os TPs. A evidência é o próprio push: o professor lê os repositórios `pb-live-*` na quarta e no sábado e, na segunda 19/10, começa a Aula 2 pela lista de quem está sem ambiente ou sem repositório. Esse arquivo é o **G1.0** do TP1. Se o check não terminar em `✅ Tudo pronto!`, commite a saída mesmo assim e poste o trecho que falhou no Infnet.Online.

## Passo 7 — Pense no seu projeto (30 min)

Leia o [catálogo de projetos](../recursos/catalogo-projetos.md) e as [derivações](../recursos/derivacoes-projetos.md). Venha para a Aula 2 com **um ou dois candidatos** e uma frase para cada: o que o robô percebe, onde ele navega, o que ele faz de longo (a futura *action*). Projetos com **montagem em hardware** (Raspberry Pi, chassi, câmera) são recomendados — e, exatamente por isso, leia [simulação × hardware real](../recursos/simulado-vs-hardware.md) antes de se apaixonar por um kit: a simulação continua sendo a rede de segurança obrigatória.

---

## Checklist de fechamento

- [ ] Formulário enviado com o usuário do GitHub correto
- [ ] `lsb_release -a` → `jammy`; turtlesim abre
- [ ] `check-ambiente.sh` termina em `✅ Tudo pronto!`
- [ ] Convite aceito; `github.com/Prof-Dacio-INFNET/pb-live-SEU-USUARIO` carrega
- [ ] Clone dentro do Linux; `git branch` mostra `* dev` e as `entrega-*`
- [ ] README com o YAML preenchido; `docs/evidencias/semana01-ambiente.txt` commitado e no GitHub
- [ ] Um ou dois candidatos a projeto anotados

## Se travar

| Sintoma | Veja |
|---|---|
| `Unable to locate package ros-humble-desktop` | Ubuntu não é 22.04 — Passo 1.5 do tutorial WSL2 |
| WSL não instala / virtualização desativada | rota VirtualBox, ou pergunte no Infnet.Online |
| Repositório dá 404 | convite não aceito (Passo 4) ou usuário errado no formulário — avise no Infnet.Online |
| `Permission denied` no clone | `gh auth login` nesta máquina |
| `check-ambiente.sh` reclama do `ROS_DOMAIN_ID` | `echo "export ROS_DOMAIN_ID=SEU_NUMERO" >> ~/.bashrc && source ~/.bashrc` (um número de 1 a 100 que só você usa) |
| Turtlesim não abre a janela no WSL2 | Windows 11 com WSLg: `wsl --update` no PowerShell e reabra; Windows 10: ver o tutorial, seção de interface gráfica |
