---
titulo: "Checklist de entrega do TP1"
tipo: entrega
etapa: 2
prazo: "sexta, 13/11/2026"
---

# Checklist de entrega do TP1

**Prazo: sexta, 13/11/2026.** A entrega **oficial e formal** é no **Moodle** — o PDF do relatório, o ZIP do código e os links. É ela que gera registro acadêmico, e sem ela não há nota. O **GitHub é complementar e obrigatório**, e é critério de avaliação: é onde o processo fica visível, e a tag `tp1` marca o commit que será corrigido.

Faça este checklist **de cima para baixo, num dia em que ainda dá tempo de consertar**. Cada item tem um comando que responde sim ou não. Todos os blocos rodam num **único terminal**, na ordem em que aparecem, e cada bloco pode ser colado inteiro — exceto o da seção 4, que é para colar **uma linha por vez**.

## 1. O repositório está no estado certo

```bash
# ── Terminal B · uma vez por terminal ─────────────────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"

cd "$PB_DIR"
git checkout dev
git status --short               # tem de vir vazio
git log --oneline -10            # commits pequenos, com mensagens que dizem o que mudou
```

**Tem de aparecer:** nada no `git status --short`. Se aparecer arquivo, decida: entra na entrega (`git add -A && git commit -m "..."`) ou não entra. Arquivo não commitado **não existe** para quem avalia.

## 2. As evidências estão commitadas

```bash
# ── Terminal B · herda PB_USER, PB_DIR e PB_WS da seção 1 ──
: "${PB_DIR:?defina PB_USER, PB_DIR e PB_WS — o bloco está na seção 1}"
cd "$PB_DIR"
ls docs/evidencias/tp1/
ls docs/relatorios/
```

**Tem de aparecer:** `check-ambiente.txt` (o ambiente), `topic-hz.txt` (a taxa medida), `status.txt` (a resposta do serviço), `segmentacao.png` (a imagem segmentada), `rqt_graph.png` (o grafo) — e `relatorio-tp1.md` em `docs/relatorios/`. Como gerar cada um está na [página da Aula 4](../aulas/etapa03-aula04/index.md#a-tarefa-da-semana). Evidência que ficou só no terminal não conta: o terminal fecha.

## 3. O `PROJETO.md` reflete a verdade

A declaração do projeto está no topo (domínio, usuário, **duas** classes, trilha, plano B), e a lista de gates do TP1 está marcada: `[x]` para o que tem evidência commitada, `[!]` para o que não fechou — com um parágrafo dizendo o que faltou e por quê. Um `[!]` declarado custa pouco; um `[x]` sem evidência é o contrário, e é fácil de verificar. A lista e as datas de referência estão na [página do TP1](../recursos/tp1.md#os-sete-gates-com-as-datas-desta-turma).

## 4. A entrega no Git: `main`, `entrega-tp1` e a tag

A branch `entrega-tp1` **já existe** desde o `init-branches.sh`: é `git checkout entrega-tp1`, e **não** `git checkout -b`.

```bash
# ── Terminal B · herda as variáveis da seção 1 · UMA LINHA POR VEZ ──
: "${PB_DIR:?defina PB_USER, PB_DIR e PB_WS — o bloco está na seção 1}"
cd "$PB_DIR"
git checkout main && git merge dev && git push origin main                            # 1) a main recebe o trabalho
git checkout entrega-tp1 && git merge --ff-only main && git push origin entrega-tp1   # 2) entrega-tp1 = main
git tag -a tp1 -m "Entrega do TP1" && git push origin tp1                             # 3) a marca do commit avaliado
git checkout dev                                                                      # 4) de volta ao trabalho
```

**Tem de aparecer:** `Fast-forward` (ou `Already up to date`) nas duas primeiras linhas, e `* [new tag] tp1 -> tp1` na terceira.

A tag **marca** o commit avaliado. Commit depois da tag não é considerado, e é isso que protege você: o que veio depois não conta contra. Errou a tag, **antes do prazo**? `git tag -d tp1 && git push origin :refs/tags/tp1`, corrija e crie de novo.

## 5. O ZIP e o PDF

O ZIP é do **código versionado**: sem `build/`, sem `install/`, sem `log/`, sem `.git/`. O `git archive` faz isso sozinho, a partir da tag.

```bash
# ── Terminal B · herda as variáveis da seção 1 ────────
: "${PB_DIR:?defina PB_USER, PB_DIR e PB_WS — o bloco está na seção 1}"
cd "$PB_DIR"
git archive --format=zip --prefix=tp1/ -o "$HOME/tp1-$PB_USER.zip" tp1
unzip -l "$HOME/tp1-$PB_USER.zip" | tail -3
```

**Tem de aparecer:** o total de arquivos e o tamanho — dezenas ou poucas centenas de arquivos, e poucos megabytes. Se vier com centenas de megabytes, algum arquivo grande foi commitado por engano (veja a seção 6). No Windows, o arquivo está em `\\wsl$\Ubuntu-22.04\home\<seu-usuario-linux>\` — ou copie para a área do Windows com `cp "$HOME/tp1-$PB_USER.zip" /mnt/c/Users/Public/`.

O PDF é o `docs/relatorios/relatorio-tp1.md` exportado. Confira que as imagens apareceram no PDF: referência quebrada no Markdown vira espaço em branco, e quem avalia não vê o que você viu.

## 6. Arquivos grandes vão por link, nunca no Git

Vídeo, dataset, bag e peso de modelo **não** entram no repositório. Publique em link acessível — YouTube **público ou não listado, nunca privado** — e ponha o link no relatório e no README.

## 7. A conferência que separa entrega boa de entrega perdida

Abra uma **janela anônima** e teste, um por um: cada link do relatório, o vídeo, e o ZIP e o PDF baixados do Moodle depois do envio.

**Se quem avalia não consegue abrir, não existe.** Link do Drive restrito e vídeo privado no YouTube não dão erro na sua máquina, porque você está logado. O repositório `pb-live-<usuario>` é diferente: ele é **privado, e é para ser** — na janela anônima ele responde 404, e está certo. Quem precisa abri-lo é o professor, e para isso basta ele estar na organização `Prof-Dacio-INFNET`, com o seu convite aceito.

## 8. A prova de que a entrega saiu, e o Moodle

```bash
# ── Terminal B · herda as variáveis da seção 1 ────────
: "${PB_DIR:?defina PB_USER, PB_DIR e PB_WS — o bloco está na seção 1}"
cd "$PB_DIR"
git status --short                    # nada: está tudo commitado
git tag --list                        # tp1
git ls-remote --tags origin           # refs/tags/tp1 e refs/tags/tp1^{}   (a tag chegou ao GitHub)
git log --oneline -1 entrega-tp1      # o mesmo commit da linha tp1^{}
```

**Tem de aparecer:** nada no primeiro; `tp1` no segundo; e duas linhas no terceiro — `refs/tags/tp1` e `refs/tags/tp1^{}`, sendo a segunda o commit para o qual a tag aponta, o mesmo que o quarto comando mostra.

No **Moodle**: o PDF, o ZIP, o link do repositório e o link do vídeo, se houver. Confira que o envio foi **concluído** e não ficou em rascunho.

---

## Escada de recuperação, se algo não vai dar tempo

Não entregar nada é sempre a pior opção, e não é a única. Nesta ordem:

1. **Entregue o que funciona e declare o que não funciona.** Uma limitação escrita por você vale muito mais do que a mesma falha descoberta por quem avalia.
2. **Substitua o item pelo plano B declarado no `PROJETO.md`.** É para isso que o plano B existe, e usá-lo não é derrota — é o comportamento que o projeto previu.
3. **Reduza o escopo sem abandonar o item** — cena menor, fonte sintética, uma classe a menos — e diga, em um parágrafo, o que faltou e por quê.

O que não funciona é entregar em silêncio, esperando que ninguém rode o comando. Alguém roda.

## Se algo der errado

| Sintoma | O que fazer |
|---|---|
| `fatal: a branch named 'entrega-tp1' already exists` | ela existe desde o `init-branches.sh`: use `git checkout entrega-tp1`, sem o `-b` |
| `fatal: Not possible to fast-forward` | houve commit direto na `entrega-tp1`. Volte para a `dev` e leve ao Infnet.Online a saída de `git log --oneline --graph --all -8` |
| `fatal: tag 'tp1' already exists` | a tag já foi criada. Para refazer antes do prazo: `git tag -d tp1 && git push origin :refs/tags/tp1` |
| `error: pathspec 'entrega-tp1' did not match` | o `init-branches.sh` não foi rodado neste repositório: `bash scripts/init-branches.sh`, e repita |
| `rejected ... fetch first` no push | você editou em outra máquina sem `pull`: `git pull`, resolva, e `git push` de novo |
| o ZIP tem centenas de megabytes | um vídeo, bag ou dataset foi commitado: tire do Git (seção 6) antes de criar a tag |

Travou, e nada aqui bate? **Infnet.Online**, com o comando exato, a saída completa e a seção em que você está.
