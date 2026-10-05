# ⭐ Colcon — workspace e build

```bash
# ── uma vez por terminal ──────────────────────────────
export PB_USER=seu-usuario-github          # ← troque pelo seu usuário do GitHub
export PB_DIR="$HOME/pb-live-$PB_USER"
export PB_WS="$PB_DIR/ros2_ws"

cd "$PB_WS"        # sempre compile na RAIZ do workspace
colcon build                        # compila tudo
colcon build --packages-select PKG  # compila 1 pacote (mais rápido)
colcon build --symlink-install      # edita Python sem recompilar
source install/setup.bash           # SEMPRE após compilar (por terminal)
rosdep install --from-paths src --ignore-src -r -y   # instala dependências declaradas
```
Criar pacote: `ros2 pkg create --build-type ament_python meu_pacote`
Limpeza: `rm -rf build install log` e recompile. Nada de `build/ install/ log/` no git.
