# Copyright (c) 2022-2026, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

import torch
from typing import TYPE_CHECKING, Literal

import isaaclab.utils.math as math_utils
from isaaclab.assets import Articulation, RigidObject, RigidObjectCollection
from isaaclab.managers import SceneEntityCfg
from isaaclab.sensors import FrameTransformer

if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedRLEnv


def square_positions_in_world_frame(
    env: ManagerBasedRLEnv,
    square_cfg: SceneEntityCfg = SceneEntityCfg("square"),
    square_hole_cfg: SceneEntityCfg = SceneEntityCfg("square_hole"),
) -> torch.Tensor:
    """The position of the squares in the world frame."""
    square: RigidObject = env.scene[square_cfg.name]
    square_hole: RigidObject = env.scene[square_hole_cfg.name]

    return torch.cat((square.data.root_pos_w, square_hole.data.root_pos_w), dim=1)


def instance_randomize_square_positions_in_world_frame(
    env: ManagerBasedRLEnv,
    square_cfg: SceneEntityCfg = SceneEntityCfg("square"),
    square_hole_cfg: SceneEntityCfg = SceneEntityCfg("square_hole"),
) -> torch.Tensor:
    """The position of the squares in the world frame."""
    if not hasattr(env, "rigid_objects_in_focus"):
        return torch.full((env.num_envs, 9), fill_value=-1)

    square: RigidObjectCollection = env.scene[square_cfg.name]
    square_hole: RigidObjectCollection = env.scene[square_hole_cfg.name]

    square_pos_w = []
    square_hole_pos_w = []
    for env_id in range(env.num_envs):
        square_pos_w.append(square.data.object_pos_w[env_id, env.rigid_objects_in_focus[env_id][0], :3])
        square_hole_pos_w.append(square_hole.data.object_pos_w[env_id, env.rigid_objects_in_focus[env_id][1], :3])
    square_pos_w = torch.stack(square_pos_w)
    square_hole_pos_w = torch.stack(square_hole_pos_w)

    return torch.cat((square_pos_w, square_hole_pos_w), dim=1)


def square_orientations_in_world_frame(
    env: ManagerBasedRLEnv,
    square_cfg: SceneEntityCfg = SceneEntityCfg("square"),
    square_hole_cfg: SceneEntityCfg = SceneEntityCfg("square_hole"),
):
    """The orientation of the squares in the world frame."""
    square: RigidObject = env.scene[square_cfg.name]
    square_hole: RigidObject = env.scene[square_hole_cfg.name]

    return torch.cat((square.data.root_quat_w, square_hole.data.root_quat_w), dim=1)


def instance_randomize_square_orientations_in_world_frame(
    env: ManagerBasedRLEnv,
    square_cfg: SceneEntityCfg = SceneEntityCfg("square"),
    square_hole_cfg: SceneEntityCfg = SceneEntityCfg("square_hole"),
) -> torch.Tensor:
    """The orientation of the squares in the world frame."""
    if not hasattr(env, "rigid_objects_in_focus"):
        return torch.full((env.num_envs, 9), fill_value=-1)

    square: RigidObjectCollection = env.scene[square_cfg.name]
    square_hole: RigidObjectCollection = env.scene[square_hole_cfg.name]

    square_quat_w = []
    square_hole_quat_w = []
    for env_id in range(env.num_envs):
        square_quat_w.append(square.data.object_quat_w[env_id, env.rigid_objects_in_focus[env_id][0], :4])
        square_hole_quat_w.append(square_hole.data.object_quat_w[env_id, env.rigid_objects_in_focus[env_id][1], :4])
    square_quat_w = torch.stack(square_quat_w)
    square_hole_quat_w = torch.stack(square_hole_quat_w)

    return torch.cat((square_quat_w, square_hole_quat_w), dim=1)


def object_obs(
    env: ManagerBasedRLEnv,
    square_cfg: SceneEntityCfg = SceneEntityCfg("square"),
    square_hole_cfg: SceneEntityCfg = SceneEntityCfg("square_hole"),
    ee_frame_cfg: SceneEntityCfg = SceneEntityCfg("ee_frame"),
):
    """
    Object observations (in world frame):
        square pos,
        square quat,
        square_hole pos,
        square_hole quat,
        gripper to square,
        gripper to square_hole,
        square to square_hole,
    """
    square: RigidObject = env.scene[square_cfg.name]
    square_hole: RigidObject = env.scene[square_hole_cfg.name]
    ee_frame: FrameTransformer = env.scene[ee_frame_cfg.name]

    square_pos_w = square.data.root_pos_w
    square_quat_w = square.data.root_quat_w

    square_hole_pos_w = square_hole.data.root_pos_w
    square_hole_quat_w = square_hole.data.root_quat_w

    ee_pos_w = ee_frame.data.target_pos_w[:, 0, :]
    gripper_to_square = square_pos_w - ee_pos_w
    gripper_to_square_hole = square_hole_pos_w - ee_pos_w

    square_to_2 = square_pos_w - square_hole_pos_w

    return torch.cat(
        (
            square_pos_w - env.scene.env_origins,
            square_quat_w,
            square_hole_pos_w - env.scene.env_origins,
            square_hole_quat_w,
            gripper_to_square,
            gripper_to_square_hole,
            square_to_2,
        ),
        dim=1,
    )


def instance_randomize_object_obs(
    env: ManagerBasedRLEnv,
    square_cfg: SceneEntityCfg = SceneEntityCfg("square"),
    square_hole_cfg: SceneEntityCfg = SceneEntityCfg("square_hole"),
    ee_frame_cfg: SceneEntityCfg = SceneEntityCfg("ee_frame"),
):
    """
    Object observations (in world frame):
        square pos,
        square quat,
        square_hole pos,
        square_hole quat,
        gripper to square,
        gripper to square_hole,
        square to square_hole,
    """
    if not hasattr(env, "rigid_objects_in_focus"):
        return torch.full((env.num_envs, 9), fill_value=-1)

    square: RigidObjectCollection = env.scene[square_cfg.name]
    square_hole: RigidObjectCollection = env.scene[square_hole_cfg.name]
    ee_frame: FrameTransformer = env.scene[ee_frame_cfg.name]

    square_pos_w = []
    square_hole_pos_w = []
    square_quat_w = []
    square_hole_quat_w = []
    for env_id in range(env.num_envs):
        square_pos_w.append(square.data.object_pos_w[env_id, env.rigid_objects_in_focus[env_id][0], :3])
        square_hole_pos_w.append(square_hole.data.object_pos_w[env_id, env.rigid_objects_in_focus[env_id][1], :3])
        square_quat_w.append(square.data.object_quat_w[env_id, env.rigid_objects_in_focus[env_id][0], :4])
        square_hole_quat_w.append(square_hole.data.object_quat_w[env_id, env.rigid_objects_in_focus[env_id][1], :4])
    square_pos_w = torch.stack(square_pos_w)
    square_hole_pos_w = torch.stack(square_hole_pos_w)
    square_quat_w = torch.stack(square_quat_w)
    square_hole_quat_w = torch.stack(square_hole_quat_w)

    ee_pos_w = ee_frame.data.target_pos_w[:, 0, :]
    gripper_to_square = square_pos_w - ee_pos_w
    gripper_to_square_hole = square_hole_pos_w - ee_pos_w

    square_to_2 = square_pos_w - square_hole_pos_w

    return torch.cat(
        (
            square_pos_w - env.scene.env_origins,
            square_quat_w,
            square_hole_pos_w - env.scene.env_origins,
            square_hole_quat_w,
            gripper_to_square,
            gripper_to_square_hole,
            square_to_2,
        ),
        dim=1,
    )


def ee_frame_pos(env: ManagerBasedRLEnv, ee_frame_cfg: SceneEntityCfg = SceneEntityCfg("ee_frame")) -> torch.Tensor:
    ee_frame: FrameTransformer = env.scene[ee_frame_cfg.name]
    ee_frame_pos = ee_frame.data.target_pos_w[:, 0, :] - env.scene.env_origins[:, 0:3]

    return ee_frame_pos


def ee_frame_quat(env: ManagerBasedRLEnv, ee_frame_cfg: SceneEntityCfg = SceneEntityCfg("ee_frame")) -> torch.Tensor:
    ee_frame: FrameTransformer = env.scene[ee_frame_cfg.name]
    ee_frame_quat = ee_frame.data.target_quat_w[:, 0, :]

    return ee_frame_quat


def gripper_pos(
    env: ManagerBasedRLEnv,
    robot_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
) -> torch.Tensor:
    """
    Obtain the versatile gripper position of both Gripper and Suction Cup.
    """
    robot: Articulation = env.scene[robot_cfg.name]

    if hasattr(env.scene, "surface_grippers") and len(env.scene.surface_grippers) > 0:
        # Handle multiple surface grippers by concatenating their states
        gripper_states = []
        for gripper_name, surface_gripper in env.scene.surface_grippers.items():
            gripper_states.append(surface_gripper.state.view(-1, 1))

        if len(gripper_states) == 1:
            return gripper_states[0]
        else:
            return torch.cat(gripper_states, dim=1)

    else:
        if hasattr(env.cfg, "gripper_joint_names"):
            gripper_joint_ids, _ = robot.find_joints(env.cfg.gripper_joint_names)
            assert len(gripper_joint_ids) == 2, "Observation gripper_pos only support parallel gripper for now"
            finger_joint_1 = robot.data.joint_pos[:, gripper_joint_ids[0]].clone().unsqueeze(1)
            finger_joint_2 = -1 * robot.data.joint_pos[:, gripper_joint_ids[1]].clone().unsqueeze(1)
            return torch.cat((finger_joint_1, finger_joint_2), dim=1)
        else:
            raise NotImplementedError("[Error] Cannot find gripper_joint_names in the environment config")


def object_grasped(
    env: ManagerBasedRLEnv,
    robot_cfg: SceneEntityCfg,
    ee_frame_cfg: SceneEntityCfg,
    object_cfg: SceneEntityCfg,
    diff_threshold: float = 0.06,
) -> torch.Tensor:
    """Check if an object is grasped by the specified robot."""

    robot: Articulation = env.scene[robot_cfg.name]
    ee_frame: FrameTransformer = env.scene[ee_frame_cfg.name]
    object: RigidObject = env.scene[object_cfg.name]

    object_pos = object.data.root_pos_w
    end_effector_pos = ee_frame.data.target_pos_w[:, 0, :]
    pose_diff = torch.linalg.vector_norm(object_pos - end_effector_pos, dim=1)

    if hasattr(env.scene, "surface_grippers") and len(env.scene.surface_grippers) > 0:
        surface_gripper = env.scene.surface_grippers["surface_gripper"]
        suction_cup_status = surface_gripper.state.view(-1, 1)  # 1: closed, 0: closing, -1: open
        suction_cup_is_closed = (suction_cup_status == 1).to(torch.float32)
        grasped = torch.logical_and(suction_cup_is_closed, pose_diff < diff_threshold)

    else:
        if hasattr(env.cfg, "gripper_joint_names"):
            gripper_joint_ids, _ = robot.find_joints(env.cfg.gripper_joint_names)
            assert len(gripper_joint_ids) == 2, "Observations only support parallel gripper for now"

            grasped = torch.logical_and(
                pose_diff < diff_threshold,
                torch.abs(
                    robot.data.joint_pos[:, gripper_joint_ids[0]]
                    - torch.tensor(env.cfg.gripper_open_val, dtype=torch.float32).to(env.device)
                )
                > env.cfg.gripper_threshold,
            )
            grasped = torch.logical_and(
                grasped,
                torch.abs(
                    robot.data.joint_pos[:, gripper_joint_ids[1]]
                    - torch.tensor(env.cfg.gripper_open_val, dtype=torch.float32).to(env.device)
                )
                > env.cfg.gripper_threshold,
            )

    return grasped


def object_stacked(
    env: ManagerBasedRLEnv,
    robot_cfg: SceneEntityCfg,
    upper_object_cfg: SceneEntityCfg,
    lower_object_cfg: SceneEntityCfg,
    xy_threshold: float = 0.05,
    height_threshold: float = 0.005,
    height_diff: float = 0.0468,
) -> torch.Tensor:
    """Check if an object is stacked by the specified robot."""

    robot: Articulation = env.scene[robot_cfg.name]
    upper_object: RigidObject = env.scene[upper_object_cfg.name]
    lower_object: RigidObject = env.scene[lower_object_cfg.name]

    pos_diff = upper_object.data.root_pos_w - lower_object.data.root_pos_w
    height_dist = torch.linalg.vector_norm(pos_diff[:, 2:], dim=1)
    xy_dist = torch.linalg.vector_norm(pos_diff[:, :2], dim=1)

    stacked = torch.logical_and(xy_dist < xy_threshold, (height_dist - height_diff) < height_threshold)

    if hasattr(env.scene, "surface_grippers") and len(env.scene.surface_grippers) > 0:
        surface_gripper = env.scene.surface_grippers["surface_gripper"]
        suction_cup_status = surface_gripper.state.view(-1, 1)  # 1: closed, 0: closing, -1: open
        suction_cup_is_open = (suction_cup_status == -1).to(torch.float32)
        stacked = torch.logical_and(suction_cup_is_open, stacked)

    else:
        if hasattr(env.cfg, "gripper_joint_names"):
            gripper_joint_ids, _ = robot.find_joints(env.cfg.gripper_joint_names)
            assert len(gripper_joint_ids) == 2, "Observations only support parallel gripper for now"
            stacked = torch.logical_and(
                torch.isclose(
                    robot.data.joint_pos[:, gripper_joint_ids[0]],
                    torch.tensor(env.cfg.gripper_open_val, dtype=torch.float32).to(env.device),
                    atol=1e-4,
                    rtol=1e-4,
                ),
                stacked,
            )
            stacked = torch.logical_and(
                torch.isclose(
                    robot.data.joint_pos[:, gripper_joint_ids[1]],
                    torch.tensor(env.cfg.gripper_open_val, dtype=torch.float32).to(env.device),
                    atol=1e-4,
                    rtol=1e-4,
                ),
                stacked,
            )
        else:
            raise ValueError("No gripper_joint_names found in environment config")

    return stacked


def square_poses_in_base_frame(
    env: ManagerBasedRLEnv,
    square_cfg: SceneEntityCfg = SceneEntityCfg("square"),
    square_hole_cfg: SceneEntityCfg = SceneEntityCfg("square_hole"),
    robot_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
    return_key: Literal["pos", "quat", None] = None,
) -> torch.Tensor:
    """The position and orientation of the squares in the robot base frame."""

    square: RigidObject = env.scene[square_cfg.name]
    square_hole: RigidObject = env.scene[square_hole_cfg.name]

    pos_square_world = square.data.root_pos_w
    pos_square_hole_world = square_hole.data.root_pos_w

    quat_square_world = square.data.root_quat_w
    quat_square_hole_world = square_hole.data.root_quat_w

    robot: Articulation = env.scene[robot_cfg.name]
    root_pos_w = robot.data.root_pos_w
    root_quat_w = robot.data.root_quat_w

    pos_square_base, quat_square_base = math_utils.subtract_frame_transforms(
        root_pos_w, root_quat_w, pos_square_world, quat_square_world
    )
    pos_square_hole_base, quat_square_hole_base = math_utils.subtract_frame_transforms(
        root_pos_w, root_quat_w, pos_square_hole_world, quat_square_hole_world
    )

    if return_key == "pos":
        return pos_squares_base
    elif return_key == "quat":
        return quat_squares_base
    else:
        return torch.cat((pos_squares_base, quat_squares_base), dim=1)


def object_abs_obs_in_base_frame(
    env: ManagerBasedRLEnv,
    square_cfg: SceneEntityCfg = SceneEntityCfg("square"),
    square_hole_cfg: SceneEntityCfg = SceneEntityCfg("square_hole"),
    ee_frame_cfg: SceneEntityCfg = SceneEntityCfg("ee_frame"),
    robot_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
):
    """
    Object Abs observations (in base frame): remove the relative observations, and add abs gripper pos and quat in robot base frame
        square pos,
        square quat,
        square_hole pos,
        square_hole quat,
        gripper pos,
        gripper quat,
    """
    square: RigidObject = env.scene[square_cfg.name]
    square_hole: RigidObject = env.scene[square_hole_cfg.name]
    ee_frame: FrameTransformer = env.scene[ee_frame_cfg.name]
    robot: Articulation = env.scene[robot_cfg.name]

    root_pos_w = robot.data.root_pos_w
    root_quat_w = robot.data.root_quat_w

    square_pos_w = square.data.root_pos_w
    square_quat_w = square.data.root_quat_w

    square_hole_pos_w = square_hole.data.root_pos_w
    square_hole_quat_w = square_hole.data.root_quat_w

    pos_square_base, quat_square_base = math_utils.subtract_frame_transforms(
        root_pos_w, root_quat_w, square_pos_w, square_quat_w
    )
    pos_square_hole_base, quat_square_hole_base = math_utils.subtract_frame_transforms(
        root_pos_w, root_quat_w, square_hole_pos_w, square_hole_quat_w
    )

    ee_pos_w = ee_frame.data.target_pos_w[:, 0, :]
    ee_quat_w = ee_frame.data.target_quat_w[:, 0, :]
    ee_pos_base, ee_quat_base = math_utils.subtract_frame_transforms(root_pos_w, root_quat_w, ee_pos_w, ee_quat_w)

    return torch.cat(
        (
            pos_square_base,
            quat_square_base,
            pos_square_hole_base,
            quat_square_hole_base,
            ee_pos_base,
            ee_quat_base,
        ),
        dim=1,
    )


def ee_frame_pose_in_base_frame(
    env: ManagerBasedRLEnv,
    ee_frame_cfg: SceneEntityCfg = SceneEntityCfg("ee_frame"),
    robot_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
    return_key: Literal["pos", "quat", None] = None,
) -> torch.Tensor:
    """
    The end effector pose in the robot base frame.
    """
    ee_frame: FrameTransformer = env.scene[ee_frame_cfg.name]
    ee_frame_pos_w = ee_frame.data.target_pos_w[:, 0, :]
    ee_frame_quat_w = ee_frame.data.target_quat_w[:, 0, :]

    robot: Articulation = env.scene[robot_cfg.name]
    root_pos_w = robot.data.root_pos_w
    root_quat_w = robot.data.root_quat_w
    ee_pos_in_base, ee_quat_in_base = math_utils.subtract_frame_transforms(
        root_pos_w, root_quat_w, ee_frame_pos_w, ee_frame_quat_w
    )

    if return_key == "pos":
        return ee_pos_in_base
    elif return_key == "quat":
        return ee_quat_in_base
    else:
        return torch.cat((ee_pos_in_base, ee_quat_in_base), dim=1)
