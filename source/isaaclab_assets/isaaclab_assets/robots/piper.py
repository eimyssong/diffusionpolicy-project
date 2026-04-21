
import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg
from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR, ISAACLAB_NUCLEUS_DIR

# <SCANNING>

##
# Piper Configuration
##

PIPER_CFG = ArticulationCfg(
    # --- 1. 스폰(Spawn) 설정 ---
    spawn=sim_utils.UsdFileCfg(
        usd_path="/workspace/isaaclab/piper_isaac_sim/USD/piper_description.usd", 
        
        # 물리 속성은 Franka 예시와 유사하게 설정할 수 있습니다.
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=True,
            max_depenetration_velocity=5.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=True, solver_position_iteration_count=8, solver_velocity_iteration_count=0
        ),
    ),
    
    # TODO: 초기 상태 치아 위로 / 중복 초기화인지 확인
    # --- 2. 초기 상태(Initial State) 설정 ---
    init_state=ArticulationCfg.InitialStateCfg(
        joint_pos={
            "joint1": 0.0,
            "joint2": 0.0,
            "joint3": 0.0,
            "joint4": 0.0,
            "joint5": 0.0,
            "joint6": 0.0,
            "joint7": 0.0,  # Prismatic joint, 열린 상태 (upper limit)
            "joint8": 0.0,    # Prismatic joint, 열린 상태 (upper limit)
        },
    ),

    actuators={
        "piper_arm": ImplicitActuatorCfg(
            joint_names_expr=["joint1", "joint2", "joint3", "joint4", "joint5", "joint6"],
            stiffness=800.0,
            damping=120.0,
        ),
        # 그리퍼 관절 (2개)을 별도 그룹으로 묶습니다.
        "piper_gripper": ImplicitActuatorCfg(
            # joint7과 joint8을 선택합니다.
            joint_names_expr=["joint7", "joint8"],
            # 그리퍼는 보통 더 강한 힘이 필요하므로 높은 stiffness를 가집니다.
            stiffness=800.0,
            damping=100.0,
        ),
    },
)


"""Configuration for the Piper robot arm."""