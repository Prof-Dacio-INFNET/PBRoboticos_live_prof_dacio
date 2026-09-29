# Exemplo — `aula09-metrica`

**Aula 9 · Etapa 5.** Um banco de provas para detectores: vídeo fixo com rótulo conhecido, três detectores, uma régua só. Cobre o gate **G2.4** do TP2.

```
aula09-metrica/
├── gerar_video.py    # cria cena.avi + rotulos.csv (rótulo perfeito, de graça)
├── detectores.py     # três detectores com a MESMA assinatura
└── avaliar.py        # roda, mede, imprime — e, com --video, anota a saída
```

## Rodar

```bash
# ── uma vez por terminal ──────────────────────────────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/projeto-pb-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"

# 1) baixar o material (pode repetir sempre -- o rm evita o erro de pasta ja existente)
rm -rf /tmp/PBRoboticos_prof_dacio
cd /tmp && git clone --depth 1 https://github.com/Prof-Dacio-INFNET/PBRoboticos_prof_dacio.git

# 2) copiar para dentro do SEU projeto
cp -r /tmp/PBRoboticos_prof_dacio/exemplos/aula09-metrica \
      "$PB_DIR/"

# 3) gerar a cena e medir
cd "$PB_DIR/aula09-metrica"
python3 gerar_video.py
python3 avaliar.py
```

Não precisa de ROS 2, não precisa de câmera, não precisa de rede. É Python e OpenCV do apt.

## O resultado, e o que ele conta

```
detector            mantido    falso positivo    custo relativo
hsv_ingenuo          65,7%          43,3%        linha de base
hsv_com_area         94,3%           6,7%        igual
hsv_adaptativo      100,0%          10,0%        ~40% mais caro
```

As duas primeiras colunas são **determinísticas** — rodando de novo, saem idênticas. A de tempo não é, e o `avaliar.py` toma três cuidados por causa disso: **aquece** antes de cronometrar (senão o primeiro detector medido paga sozinho o custo de aquecer cache e aparece mais lento do que é), reporta **mediana** em vez de média (um quadro lento isolado não diz nada sobre o detector) e mostra o **p90** ao lado. Ainda assim, o valor absoluto é da máquina; o que viaja é a razão.

Quatro leituras, e a terceira é a que vale a aula.

**A média esconde onde falhou.** O `hsv_ingenuo` marca 65,7%, o que soa como "funciona na maior parte do tempo". O detalhamento por trecho conta outra história:

```
    normal               100.0% mantido
    oclusao              alvo ausente; 13 falso(s) positivo(s) em 30
    distrator vermelho     0.0% mantido      <---
    luz caindo            86.7% mantido
```

Não é um detector que erra um pouco em todo lugar: é um detector que **funciona perfeitamente até encontrar uma mancha vermelha maior, e então erra 100% do tempo**. Média é um resumo; modo de falha é o que você precisa saber.

**Cada ideia compra uma quantidade mensurável.** Trocar "a maior mancha" por "a mancha do tamanho esperado" é uma linha de código conceitualmente diferente e levou 65,7% para 94,3%, sem custo de tempo. Adaptar o limiar de brilho ao brilho da cena levou para 100%, e custou ~40% mais CPU.

**Não existe almoço grátis.** Repare que o `hsv_adaptativo` acha o alvo sempre **e inventa mais**: o falso positivo subiu de 6,7% para 10,0%. Um detector mais sensível enxerga mais coisa — inclusive coisa que não existe. Esse par sobe junto, e escolher onde ficar no par é decisão de projeto, não de programação.

Para um robô que **freia** ao ver obstáculo, falso positivo é freada fantasma e talvez seja pior que perder o alvo. Para um robô que **conta** frutos, perder o alvo é subcontagem e falso positivo é superestimativa. **O mesmo número significa coisas opostas em domínios diferentes** — e é por isso que a métrica tem que ser declarada junto com o domínio.

## Ver o que o detector viu

```bash
python3 avaliar.py --video                    # gera saida_<detector>.avi
python3 avaliar.py hsv_ingenuo --video        # um só
```

Cada quadro sai anotado com a **caixa da verdade** em âmbar, a **caixa detectada** em verde (quando valeu) ou vermelho (quando não), o IoU do quadro, o trecho da cena, o veredito — `ACERTO`, `PERDA`, `FALSO POSITIVO`, `ausente (ok)` — e a métrica **acumulada até aquele quadro** na faixa de baixo.

É a forma mais rápida de responder à pergunta que o número agregado não responde: *em que ele estava olhando quando errou?* Abra o vídeo do `hsv_ingenuo` e vá até o quadro 90: dá para ver o instante exato em que ele troca o alvo pelo distrator maior e não volta mais.

### Por que isso é um parâmetro, e não o comportamento padrão

Porque desenhar custa — e custa mais do que se imagina. Medido nesta máquina:

| | por quadro |
|---|---|
| a detecção (`hsv_com_area`) | 1,65 ms |
| desenhar o OSD | **2,07 ms** |
| se os dois entrassem na mesma conta | 3,72 ms |

**O custo de observar é maior que o custo do que se observa.** Se o desenho estivesse dentro da janela cronometrada, 56% do número reportado seria o OSD, e a comparação entre detectores mediria principalmente quem desenha mais rápido.

Por isso o `avaliar.py` faz duas coisas: põe o vídeo atrás de um parâmetro **e** desenha fora da janela cronometrada. O efeito é verificável — ligar o `--video` mexe no tempo reportado em ~0,07 ms, dentro do ruído entre execuções, contra os 56% que mexeria se estivesse dentro.

```python
# ---------- JANELA CRONOMETRADA: so o detector ----------
t0 = time.perf_counter()
caixa = fn(img)
tempos.append((time.perf_counter() - t0) * 1000.0)
# ---------- fim da janela. Nada abaixo entra na conta. ----------
```

!!! tip "A regra geral, que vale para o seu nó ROS 2"
    **O que você mede não pode incluir o custo de observar.** Vale para o OSD, para o `print` de depuração dentro do laço, para o log em nível DEBUG e para qualquer visualização que você acrescente. Instrumentação que entra na medição transforma o instrumento em parte do experimento.

    É o mesmo erro do aquecimento: medir a coisa errada com precisão.

## O que a cena tem, de propósito

| Quadros | O que acontece | O que quebra |
|---|---|---|
| 0–59 | normal, alvo + distrator azul | nada; é a linha de base |
| 60–89 | **oclusão**: o alvo passa atrás de uma barra | rótulo vira *ausente*; quem detecta aqui produz falso positivo |
| 90–149 | entra um distrator **vermelho maior** que o alvo | "a maior mancha vermelha" aponta para o lugar errado |
| 150–239 | a luz cai até ~22% | limiar fixo de brilho para de enxergar o alvo |

## Por que o vídeo é gerado, e não filmado

Para medir um detector você precisa saber a resposta certa **em cada quadro**. Rotular vídeo real é caro e chato; gerar um cenário onde você mesmo desenhou o alvo dá rótulo perfeito de graça.

Isso **não substitui dado real** — substitui a falta dele no dia em que você precisa validar o seu *método de medição*. Um medidor que erra no cenário sintético vai errar mais no real, e você descobre agora, não na entrega.

## Trocar o detector por um treinado

O `avaliar.py` não sabe nada sobre como o detector funciona: ele chama uma função que recebe a imagem e devolve `(x, y, w, h)` ou `None`. Plugar um modelo treinado é acrescentar uma função com essa assinatura e registrá-la no dicionário `DETECTORES`.

```python
# detectores.py — esboço; você precisa baixar os arquivos do modelo
_rede = None

def dnn(img):
    global _rede
    if _rede is None:
        _rede = cv2.dnn.readNet('modelo.onnx')        # ou readNetFromDarknet(...)
    blob = cv2.dnn.blobFromImage(img, 1/255.0, (416, 416), swapRB=True, crop=False)
    _rede.setInput(blob)
    saidas = _rede.forward()
    # ... converter a saída do SEU modelo para (x, y, w, h) ou None
```

**A régua é a mesma, e é isso que permite comparar.** Um detector treinado que marque 92% não é melhor que o `hsv_adaptativo` de 100% — nesta cena. Em cena real, com iluminação variável e objetos que não são círculos perfeitos, a conclusão costuma se inverter. Dizer isso é honestidade; medir é o que transforma a opinião em afirmação.

!!! note "`cv2.dnn` vem do apt e não quebra a regra da disciplina"
    O módulo `dnn` do OpenCV roda modelos ONNX e Darknet **sem** instalar `torch` nem `ultralytics`. Se você quiser o ecossistema completo do YOLO, ele vai num **venv** (`uv venv --system-site-packages`), como script solto — nunca no python do sistema, e nunca dentro de um nó ROS 2.

## Licença

MIT, como todo o diretório `exemplos/`.
