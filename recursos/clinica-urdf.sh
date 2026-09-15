#!/usr/bin/env bash
# clinica-urdf.sh — diz em que ponto do G2.5 você está, e o que fazer a seguir.
# Rode DENTRO do Ubuntu, a partir da raiz do seu ros2_ws. Não altera nada.
#   cd ~/projeto-pb-SEU-USUARIO/ros2_ws && bash recursos/clinica-urdf.sh
# Sem clonar:
#   curl -sSL https://raw.githubusercontent.com/Prof-Dacio-INFNET/PBRoboticos_prof_dacio/main/recursos/clinica-urdf.sh | bash
ok(){   printf "  \033[32m✓\033[0m %s\n" "$1"; }
no(){   printf "  \033[31m✗\033[0m %s\n" "$1"; }
inf(){  printf "  · %s\n" "$1"; }
titulo(){ printf "\n\033[1m%s\033[0m\n" "$1"; }

echo "== Clínica de URDF e TF — onde você está no G2.5 =="

# ---------------------------------------------------------------- 0. rota
ROTA="nativo"
if grep -qi microsoft /proc/version 2>/dev/null || [ -n "$WSL_DISTRO_NAME" ]; then
  ROTA="wsl2"
elif [ "$(systemd-detect-virt 2>/dev/null)" = "oracle" ]; then
  ROTA="virtualbox"
fi
inf "rota: $ROTA"

# ---------------------------------------------------------------- 1. ROS
titulo "1. ROS 2"
if ! command -v ros2 >/dev/null 2>&1; then
  no "o comando 'ros2' não existe neste terminal"
  echo ""
  echo "  GRUPO A — ambiente. Faça:  source /opt/ros/humble/setup.bash"
  echo "  Se nem isso funcionar, o ROS 2 não está instalado: veja o tutorial de ambiente."
  exit 0
fi
ok "ros2 disponível"
[ -n "$AMENT_PREFIX_PATH" ] && ok "workspace com source feito" \
  || inf "nenhum overlay no PATH — se o seu pacote não for encontrado, é isto"

# ---------------------------------------------------------------- 2. ferramentas
titulo "2. Ferramentas do G2.5"
FALTA=""
command -v check_urdf >/dev/null 2>&1 && ok "check_urdf" || { no "check_urdf (liburdfdom-tools)"; FALTA="$FALTA liburdfdom-tools"; }
command -v xacro      >/dev/null 2>&1 && ok "xacro"      || { no "xacro";                     FALTA="$FALTA ros-humble-xacro"; }
ros2 pkg list 2>/dev/null | grep -qx joint_state_publisher_gui \
  && ok "joint_state_publisher_gui" || { no "joint_state_publisher_gui"; FALTA="$FALTA ros-humble-joint-state-publisher-gui"; }
ros2 pkg list 2>/dev/null | grep -qx tf2_tools \
  && ok "tf2_tools" || { no "tf2_tools"; FALTA="$FALTA ros-humble-tf2-tools"; }
ros2 pkg list 2>/dev/null | grep -qx rviz2 && ok "rviz2" || no "rviz2"

if [ -n "$FALTA" ]; then
  echo ""
  echo "  >>> GRUPO A — falta instalar. Um comando resolve:"
  echo ""
  echo "      sudo apt update && sudo apt install -y$FALTA"
  echo ""
  echo "  Rode e chame este script de novo."
  exit 0
fi

# ---------------------------------------------------------------- 3. pacote e URDF
titulo "3. O seu modelo"
PKG=$(ls -d src/*_description 2>/dev/null | head -n1)
if [ -z "$PKG" ]; then
  no "não achei nenhum pacote 'src/*_description' a partir daqui ($PWD)"
  echo ""
  echo "  >>> GRUPO B — sem modelo. Ou você não está na raiz do ros2_ws,"
  echo "      ou ainda não copiou/criou o pacote. O exemplo pronto é:"
  echo "      exemplos/aula09-urdf/meu_robo_description"
  exit 0
fi
ok "pacote encontrado: $PKG"

URDF=$(find "$PKG" -name '*.urdf' -o -name '*.urdf.xacro' 2>/dev/null | head -n1)
if [ -z "$URDF" ]; then
  no "o pacote existe mas não tem .urdf nem .urdf.xacro"
  echo ""
  echo "  >>> GRUPO B — sem modelo. O arquivo vai em $PKG/urdf/"
  exit 0
fi
inf "arquivo: $URDF"

TMP=$(mktemp -d)
ALVO="$URDF"
case "$URDF" in *.xacro) xacro "$URDF" > "$TMP/gerado.urdf" 2>"$TMP/xacro.err" \
   && { ALVO="$TMP/gerado.urdf"; ok "xacro expandiu"; } \
   || { no "o xacro não expandiu:"; sed 's/^/      /' "$TMP/xacro.err" | head -5; echo ""; \
        echo "  >>> GRUPO B — o modelo não chega a ser lido."; rm -rf "$TMP"; exit 0; };; esac

if ! check_urdf "$ALVO" > "$TMP/chk.txt" 2>&1; then
  no "check_urdf rejeitou o modelo:"
  sed 's/^/      /' "$TMP/chk.txt" | head -8
  echo ""
  echo "  >>> GRUPO B — URDF inválido. As três causas, em ordem de frequência:"
  echo "      1. um link é filho de DUAS juntas (URDF é árvore, não grafo)"
  echo "      2. junta apontando para link que não existe (erro de digitação no nome)"
  echo "      3. junta revolute sem <limit> (sem limite, use 'continuous')"
  rm -rf "$TMP"; exit 0
fi
RAIZ=$(grep -m1 'root Link' "$TMP/chk.txt" | sed 's/.*root Link: //; s/ has .*//')
NLINKS=$(grep -c 'child(' "$TMP/chk.txt")
ok "check_urdf passou — raiz: $RAIZ, $((NLINKS+1)) links"
[ "$RAIZ" = "base_footprint" ] || inf "a raiz não é 'base_footprint'. Não é erro; vira aviso do KDL se ela tiver <inertial>, e Nav2/SLAM esperam esse nome no TP3"
rm -rf "$TMP"

# ---------------------------------------------------------------- 4. grafo vivo
titulo "4. O modelo está NO AR? (precisa do launch rodando, noutra aba)"
PUBS=$(ros2 topic info /robot_description 2>/dev/null | grep -i 'publisher count' | grep -oE '[0-9]+' | head -n1)
PUBS=${PUBS:-0}
if [ "$PUBS" -eq 0 ]; then
  no "ninguém publica /robot_description"
  echo ""
  echo "  >>> GRUPO C — o modelo é válido, mas não está no ar."
  echo "      Abra OUTRA aba e deixe rodando:"
  echo ""
  echo "          ros2 launch $(basename "$PKG") ver_robo.launch.py"
  echo ""
  echo "      TF é fluxo, não arquivo: sem o robot_state_publisher no ar,"
  echo "      não existe TF para ler — e o view_frames gera um PDF VAZIO"
  echo "      sem reclamar de nada."
  exit 0
fi
ok "/robot_description publicado por $PUBS nó(s)"

NFRAMES=$(timeout 5 ros2 topic echo /tf_static --once 2>/dev/null | grep -c 'child_frame_id')
NFRAMES=${NFRAMES:-0}
if [ "$NFRAMES" -eq 0 ]; then
  no "nenhuma transformação em /tf_static"
  echo ""
  echo "  >>> GRUPO C — o modelo subiu mas a TF não saiu."
  echo "      Confira se o launch não morreu, e releia o log dele."
  exit 0
fi
ok "$NFRAMES transformação(ões) estática(s) em /tf_static"

# ---------------------------------------------------------------- 5. gráfico
titulo "5. Ambiente gráfico"
if [ -z "$DISPLAY" ] && [ -z "$WAYLAND_DISPLAY" ]; then
  no "nem DISPLAY nem WAYLAND_DISPLAY definidos — nenhuma janela vai abrir"
  [ "$ROTA" = "wsl2" ] && inf "no WSL2: 'wsl --update' no PowerShell e reabra o terminal"
else
  ok "servidor gráfico presente (DISPLAY=${DISPLAY:-}${WAYLAND_DISPLAY:+ wayland})"
  [ -n "$LIBGL_ALWAYS_SOFTWARE" ] && inf "LIBGL_ALWAYS_SOFTWARE=$LIBGL_ALWAYS_SOFTWARE (renderização por software — ok)"
fi

# ---------------------------------------------------------------- veredito
titulo "Veredito"
echo "  O terminal já prova o que o G2.5 pede:"
echo "      check_urdf .......... modelo válido        ✓"
echo "      /robot_description .. modelo no ar         ✓"
echo "      /tf_static .......... TF publicada         ✓"
echo ""
echo "  >>> GRUPO D/E — falta só a evidência. Rode, com o launch no ar:"
echo ""
echo "      ros2 run tf2_tools view_frames            # gera frames.pdf"
echo "      ros2 run tf2_ros tf2_echo $RAIZ camera_link"
echo "      ros2 param dump /<seu_no_parametrizado>"
echo ""
echo "  Se o RViz2 abrir VAZIO, isso NÃO bloqueia o gate — os três comandos"
echo "  acima são a prova. Para consertar a janela: rode 'ros2 run turtlesim"
echo "  turtlesim_node'. Tartaruga aparece e RViz não -> export"
echo "  LIBGL_ALWAYS_SOFTWARE=1. Tartaruga também some -> export QT_QPA_PLATFORM=xcb"
