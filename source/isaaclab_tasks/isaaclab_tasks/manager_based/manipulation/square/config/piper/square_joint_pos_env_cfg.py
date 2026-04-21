# Copyright (c) 2022-2026, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from isaaclab.assets import RigidObjectCfg
from isaaclab.managers import EventTermCfg as EventTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.sensors import FrameTransformerCfg
from isaaclab.sensors.frame_transformer.frame_transformer_cfg import OffsetCfg
from isaaclab.sim.schemas.schemas_cfg import RigidBodyPropertiesCfg
from isaaclab.sim.spawners.from_files.from_files_cfg import UsdFileCfg
from isaaclab.utils import configclass
from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR


from isaaclab.utils.assets import ISAACLAB_NUCLEUS_DIR
ASSET_DIR = f"{ISAACLAB_NUCLEUS_DIR}/Factory"

# from isaaclab_tasks.manager_based.manipulation.stack import mdp
# from isaaclab_tasks.manager_based.manipulation.stack.mdp import franka_stack_events
# from isaaclab_tasks.manager_based.manipulation.stack.mdp import piper_stack_events
# from isaaclab_tasks.manager_based.manipulation.stack.stack_env_cfg import StackEnvCfg


from isaaclab_tasks.manager_based.manipulation.square import mdp
from isaaclab_tasks.manager_based.manipulation.square.mdp import piper_square_events
from isaaclab_tasks.manager_based.manipulation.square.square_env_cfg import SquareEnvCfg


##
# Pre-defined configs
##
from isaaclab.markers.config import FRAME_MARKER_CFG  # isort: skip
from isaaclab_assets.robots.franka import FRANKA_PANDA_CFG  # isort: skip
from isaaclab_assets.robots.piper import PIPER_CFG  # isort: skip


from isaaclab.sim.schemas import ArticulationRootPropertiesCfg



@configclass
class PiperSEventCfg:
    """Configuration for events."""

    init_piper_arm_pose = EventTerm(
        func=piper_square_events.set_default_joint_pose,
        mode="reset",
        params={
            # "default_pose": [0.0444, -0.1894, -0.1107, -2.5148, 0.0044, 2.3775, 0.0400, 0.0400],
            # "default_pose": [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
            "default_pose": [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0400, -0.0400],
        },
    )

    randomize_piper_joint_state = EventTerm(
        func=piper_square_events.randomize_joint_by_gaussian_offset,
        mode="reset",
        params={
            "mean": 0.0,
            "std": 0.02,
            "asset_cfg": SceneEntityCfg("robot"),
        },
    )

    randomize_square_positions = EventTerm(
        func=piper_square_events.randomize_object_pose,
        mode="reset",
        params={
            "pose_range": {"x": (0.4, 0.6), "y": (-0.10, 0.10), "z": (0.0203, 0.0203), "yaw": (-1.0, 1, 0)},
            # "min_separation": 0.1,
            "min_separation": 0.6,
            "asset_cfgs": [SceneEntityCfg("square"), SceneEntityCfg("square_hole")],
        },
    )


@configclass
class PiperSquareEnvCfg(SquareEnvCfg):

    def __post_init__(self):
        # post init of parent
        super().__post_init__()

        # Set events
        self.events = PiperSEventCfg()

        # Set Franka as robot
        # self.scene.robot = FRANKA_PANDA_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")

        # set piper as robot
        self.scene.robot = PIPER_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")


        self.scene.robot.spawn.semantic_tags = [("class", "robot")]

        # Add semantics to table
        self.scene.table.spawn.semantic_tags = [("class", "table")]

        # Add semantics to ground
        self.scene.plane.semantic_tags = [("class", "ground")]

        # Set actions for the specific robot type (franka)
        self.actions.arm_action = mdp.JointPositionActionCfg(
            asset_name="robot", joint_names=["joint[1-6]"], scale=0.5, use_default_offset=False
            # asset_name="robot", joint_names=["panda_joint.*"], scale=0.5, use_default_offset=True
        )
        self.actions.gripper_action = mdp.BinaryJointPositionActionCfg(
            asset_name="robot",
            joint_names=["joint7", "joint8"],
            open_command_expr={"joint7": 0.04, "joint8": -0.04},
            close_command_expr={"joint7": 0.0, "joint8": 0.0},
            # joint_names=["panda_finger.*"],
            # open_command_expr={"panda_finger_.*": 0.04},
            # close_command_expr={"panda_finger_.*": 0.0},
        )
        # utilities for gripper status check
        self.gripper_joint_names = ["joint7", "joint8"]
        # self.gripper_joint_names = ["panda_finger_.*"]        
        self.gripper_open_val = 0.04
        self.gripper_threshold = 0.005

        # Rigid body properties of each cube
        square_properties = RigidBodyPropertiesCfg(
            solver_position_iteration_count=16,
            solver_velocity_iteration_count=1,
            max_angular_velocity=1000.0,
            max_linear_velocity=1000.0,
            max_depenetration_velocity=5.0,
            disable_gravity=False,
        )

        square_hole_properties = RigidBodyPropertiesCfg(
            solver_position_iteration_count=16,
            solver_velocity_iteration_count=1,
            max_angular_velocity=1000.0,
            max_linear_velocity=1000.0,
            max_depenetration_velocity=5.0,
            disable_gravity=False,
        )

        # Set each stacking cube deterministically
        self.scene.square = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/Square",
            init_state=RigidObjectCfg.InitialStateCfg(pos=[0.4, 0.0, 0.05], rot=[1, 0, 0, 0]),
            # spawn=UsdFileCfg(
            #     usd_path=f"{ISAAC_NUCLEUS_DIR}/Props/Nuts/nut.usd",
            #     scale=(1.0, 1.0, 1.0),
            #     rigid_props=square_properties,
            #     semantic_tags=[("class", "square")],
            # ),
            spawn=UsdFileCfg(
                usd_path=f"{ASSET_DIR}/factory_bolt_m16.usd",
                scale=(3.0, 3.0, 3.0),
                rigid_props=square_properties,
                articulation_props=ArticulationRootPropertiesCfg(
                    articulation_enabled=False
                ),
                semantic_tags=[("class", "square")],
            ),
        )
        self.scene.square_hole = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/Square_hole",
            init_state=RigidObjectCfg.InitialStateCfg(pos=[0.55, 0.05, 0.05], rot=[1, 0, 0, 0]),
            # spawn=UsdFileCfg(
            #     usd_path=f"{ISAAC_NUCLEUS_DIR}/Props/Pegs/peg.usd",
            #     scale=(1.0, 1.0, 1.0),
            #     rigid_props=square_hole_properties,
            #     semantic_tags=[("class", "square_hole")],
            # ),
            spawn=UsdFileCfg(
                usd_path=f"{ASSET_DIR}/factory_nut_m16.usd",
                scale=(3.0, 3.0, 3.0),
                rigid_props=square_hole_properties,
                articulation_props=ArticulationRootPropertiesCfg(
                    articulation_enabled=False
                ),
                semantic_tags=[("class", "square_hole")],
            ),
        )



        # fixed_asset: ArticulationCfg = ArticulationCfg(
        #     prim_path="/World/envs/env_.*/FixedAsset",
        #     spawn=sim_utils.UsdFileCfg(
        #         usd_path=fixed_asset_cfg.usd_path,
        #         activate_contact_sensors=True,
        #         rigid_props=sim_utils.RigidBodyPropertiesCfg(
        #             disable_gravity=False,
        #             max_depenetration_velocity=5.0,
        #             linear_damping=0.0,
        #             angular_damping=0.0,
        #             max_linear_velocity=1000.0,
        #             max_angular_velocity=3666.0,
        #             enable_gyroscopic_forces=True,
        #             solver_position_iteration_count=192,
        #             solver_velocity_iteration_count=1,
        #             max_contact_impulse=1e32,
        #         ),
        #         mass_props=sim_utils.MassPropertiesCfg(mass=fixed_asset_cfg.mass),
        #         collision_props=sim_utils.CollisionPropertiesCfg(contact_offset=0.005, rest_offset=0.0),
        #     ),
        #     init_state=ArticulationCfg.InitialStateCfg(
        #         pos=(0.6, 0.0, 0.05), rot=(1.0, 0.0, 0.0, 0.0), joint_pos={}, joint_vel={}
        #     ),
        #     actuators={},
        # )
        # held_asset: ArticulationCfg = ArticulationCfg(
        #     prim_path="/World/envs/env_.*/HeldAsset",
        #     spawn=sim_utils.UsdFileCfg(
        #         usd_path=held_asset_cfg.usd_path,
        #         activate_contact_sensors=True,
        #         rigid_props=sim_utils.RigidBodyPropertiesCfg(
        #             disable_gravity=True,
        #             max_depenetration_velocity=5.0,
        #             linear_damping=0.0,
        #             angular_damping=0.0,
        #             max_linear_velocity=1000.0,
        #             max_angular_velocity=3666.0,
        #             enable_gyroscopic_forces=True,
        #             solver_position_iteration_count=192,
        #             solver_velocity_iteration_count=1,
        #             max_contact_impulse=1e32,
        #         ),
        #         mass_props=sim_utils.MassPropertiesCfg(mass=held_asset_cfg.mass),
        #         collision_props=sim_utils.CollisionPropertiesCfg(contact_offset=0.005, rest_offset=0.0),
        #     ),
        #     init_state=ArticulationCfg.InitialStateCfg(
        #         pos=(0.0, 0.4, 0.1), rot=(1.0, 0.0, 0.0, 0.0), joint_pos={}, joint_vel={}
        #     ),
        #     actuators={},
        # )



        # @configclass
        # class NutM16(HeldAssetCfg):
        #     usd_path = f"{ASSET_DIR}/factory_nut_m16.usd"
        #     diameter = 0.024
        #     height = 0.01
        #     mass = 0.03
        #     friction = 0.01  # Additive with the nut means friction is (-0.25 + 0.75)/2 = 0.25


        # @configclass
        # class BoltM16(FixedAssetCfg):
        #     usd_path = f"{ASSET_DIR}/factory_bolt_m16.usd"
        #     diameter = 0.024
        #     height = 0.025
        #     base_height = 0.01
        #     thread_pitch = 0.002



        # self.scene.square = BoltM16()
        # self.scene.square_hole = NutM16()


        # Listens to the required transforms
        marker_cfg = FRAME_MARKER_CFG.copy()
        marker_cfg.markers["frame"].scale = (0.1, 0.1, 0.1)
        marker_cfg.prim_path = "/Visuals/FrameTransformer"
        self.scene.ee_frame = FrameTransformerCfg(
            # prim_path="{ENV_REGEX_NS}/Robot/panda_link0",
            prim_path="{ENV_REGEX_NS}/Robot/base_link",
            debug_vis=False,
            visualizer_cfg=marker_cfg,
            target_frames=[
                FrameTransformerCfg.FrameCfg(
                    prim_path="{ENV_REGEX_NS}/Robot/gripper_base",
                    name="end_effector",
                    offset=OffsetCfg(
                        pos=[0.0, 0.0, 0.1034],
                        # pos=[0.0, 0.0, 0.0],
                    ),
                ),
                # FrameTransformerCfg.FrameCfg(
                #     prim_path="{ENV_REGEX_NS}/Robot/link7",
                #     name="tool_rightfinger",
                #     offset=OffsetCfg(
                #         pos=(0.0, 0.0, 0.046),
                #     ),
                # ),
                # FrameTransformerCfg.FrameCfg(
                #     prim_path="{ENV_REGEX_NS}/Robot/link8",
                #     name="tool_leftfinger",
                #     offset=OffsetCfg(
                #         pos=(0.0, 0.0, 0.046),
                #     ),
                # ),
                # FrameTransformerCfg.FrameCfg(
                #     prim_path="{ENV_REGEX_NS}/Robot/panda_hand",
                #     name="end_effector",
                #     offset=OffsetCfg(
                #         pos=[0.0, 0.0, 0.1034],
                #     ),
                # ),
                # FrameTransformerCfg.FrameCfg(
                #     prim_path="{ENV_REGEX_NS}/Robot/panda_rightfinger",
                #     name="tool_rightfinger",
                #     offset=OffsetCfg(
                #         pos=(0.0, 0.0, 0.046),
                #     ),
                # ),
                # FrameTransformerCfg.FrameCfg(
                #     prim_path="{ENV_REGEX_NS}/Robot/panda_leftfinger",
                #     name="tool_leftfinger",
                #     offset=OffsetCfg(
                #         pos=(0.0, 0.0, 0.046),
                #     ),
                # ),
            ],
        )
