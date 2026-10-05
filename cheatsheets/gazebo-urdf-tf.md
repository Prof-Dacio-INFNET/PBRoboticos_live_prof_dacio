# Gazebo · RViz2 · URDF · TF — referência (TP2–TP3)

## URDF (modelo do robô)
Estrutura: `<link>` (corpos) + `<joint>` (articulações, type: fixed/continuous/revolute) + `<visual>/<collision>/<inertial>`. Sensores via `<gazebo>`/plugins. Verificar: `check_urdf robo.urdf`; visualizar: `ros2 launch urdf_tutorial display.launch.py model:=robo.urdf`.

## TF (transformadas)
```bash
ros2 run tf2_tools view_frames        # gera frames.pdf da árvore (map→odom→base_link→sensores)
ros2 run tf2_ros tf2_echo base_link laser   # transformada entre 2 frames
```
`robot_state_publisher` publica as TFs a partir do URDF + estados das juntas.

## Gazebo (Fortress, que é o par do Humble) + RViz2

**Humble pareia com Fortress, não com Harmonic.** No Fortress o binário ainda é `ign gazebo` e os tipos são `ignition.msgs.X`; `gz sim` e `gz.msgs.X` são de versões mais novas e não valem aqui. Instalação, ponte e critério de desistência: [Gazebo para o TP3](../tutoriais/gazebo-para-o-tp3.md).

```bash
sudo apt install ros-humble-ros-gz                 # traz simulador, ponte e utilitários
ign gazebo shapes.sdf                              # teste de dois minutos
ros2 run ros_gz_bridge parameter_bridge \
  /scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan
rviz2 -d config.rviz                               # o -d não é detalhe: sem ele, só aparece o Grid
```
Direção na ponte: `[` Gazebo→ROS (sensores), `]` ROS→Gazebo (comandos), `@` ambos.

Orquestre tudo num `bringup.launch.py` (Gazebo + ponte + RSP + RViz2 + seus nós), parâmetros via YAML.
