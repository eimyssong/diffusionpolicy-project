# Copyright (c) 2022-2026, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Script to run teleoperation with Isaac Lab manipulation environments.

Supports multiple input devices (e.g., keyboard, spacemouse, gamepad) and devices
configured within the environment (including OpenXR-based hand tracking or motion
controllers)."""

"""Launch Isaac Sim Simulator first."""

import argparse
from collections.abc import Callable

from isaaclab.app import AppLauncher

# add argparse arguments
parser = argparse.ArgumentParser(description="Teleoperation for Isaac Lab environments.")
parser.add_argument("--num_envs", type=int, default=1, help="Number of environments to simulate.")
parser.add_argument(
    "--teleop_device",
    type=str,
    default="keyboard",
    help=(
        "Teleop device. Set here (legacy) or via the environment config. If using the environment config, pass the"
        " device key/name defined under 'teleop_devices' (it can be a custom name, not necessarily 'handtracking')."
        " Built-ins: keyboard, spacemouse, gamepad. Not all tasks support all built-ins."
    ),
)
parser.add_argument("--task", type=str, default=None, help="Name of the task.")
parser.add_argument("--sensitivity", type=float, default=1.0, help="Sensitivity factor.")
parser.add_argument(
    "--enable_pinocchio",
    action="store_true",
    default=False,
    help="Enable Pinocchio.",
)

parser.add_argument(
    "--save",
    action="store_true",
    default=False,
    help="Save the data from the environment's camera on key press.",
)

# append AppLauncher cli args
AppLauncher.add_app_launcher_args(parser)
# parse the arguments
args_cli = parser.parse_args()

app_launcher_args = vars(args_cli)

if args_cli.enable_pinocchio:
    # Import pinocchio before AppLauncher to force the use of the version installed by IsaacLab and
    # not the one installed by Isaac Sim pinocchio is required by the Pink IK controllers and the
    # GR1T2 retargeter
    import pinocchio  # noqa: F401
if "handtracking" in args_cli.teleop_device.lower():
    app_launcher_args["xr"] = True

# launch omniverse app
app_launcher = AppLauncher(app_launcher_args)
simulation_app = app_launcher.app

"""Rest everything follows."""


import gymnasium as gym
import logging
import torch

from isaaclab.devices import Se3Gamepad, Se3GamepadCfg, Se3Keyboard, Se3KeyboardCfg, Se3SpaceMouse, Se3SpaceMouseCfg
from isaaclab.devices.openxr import remove_camera_configs
from isaaclab.devices.teleop_device_factory import create_teleop_device
from isaaclab.managers import TerminationTermCfg as DoneTerm

import isaaclab_tasks  # noqa: F401
from isaaclab_tasks.manager_based.manipulation.lift import mdp
from isaaclab_tasks.utils import parse_env_cfg

if args_cli.enable_pinocchio:
    import isaaclab_tasks.manager_based.locomanipulation.pick_place  # noqa: F401
    import isaaclab_tasks.manager_based.manipulation.pick_place  # noqa: F401


import omni.log
# more libraray for save image and joint states
import os 
import json
import numpy as np 
import datetime
import omni.replicator.core as rep 
from isaaclab.utils import convert_dict_to_backend 
from PIL import Image


# import logger
logger = logging.getLogger(__name__)


def main() -> None:
    """
    Run teleoperation with an Isaac Lab manipulation environment.

    Creates the environment, sets up teleoperation interfaces and callbacks,
    and runs the main simulation loop until the application is closed.

    Returns:
        None
    """
    # parse configuration
    env_cfg = parse_env_cfg(args_cli.task, device=args_cli.device, num_envs=args_cli.num_envs)
    env_cfg.env_name = args_cli.task
    # modify configuration
    env_cfg.terminations.time_out = None
    if "Lift" in args_cli.task:
        # set the resampling time range to large number to avoid resampling
        env_cfg.commands.object_pose.resampling_time_range = (1.0e9, 1.0e9)
        # add termination condition for reaching the goal otherwise the environment won't reset
        env_cfg.terminations.object_reached_goal = DoneTerm(func=mdp.object_reached_goal)

    if args_cli.xr:
        env_cfg = remove_camera_configs(env_cfg)
        env_cfg.sim.render.antialiasing_mode = "DLSS"


    urdf_path = "/workspace/isaaclab/piper_isaac_sim/piper_description/urdf/piper_description.urdf"

    try:
        model = pinocchio.buildModelFromUrdf(urdf_path)
        data = model.createData()
        eef_frame_id = model.getFrameId("gripper_base")
        # eef_frame_id = model.getFrameId("link6")
        print("Pinocchio model for Piper loaded successfully.")
    except Exception as e:
        print(f"Failed to load Pinocchio model from URDF: {e}")
        simulation_app.close()
        return

    try:
        # create environment
        env = gym.make(args_cli.task, cfg=env_cfg).unwrapped
        # check environment name (for reach , we don't allow the gripper)
        if "Reach" in args_cli.task:
            logger.warning(
                f"The environment '{args_cli.task}' does not support gripper control. The device command will be"
                " ignored."
            )
    except Exception as e:
        logger.error(f"Failed to create environment: {e}")
        simulation_app.close()
        return


    print('gym creation sucess!!!')
 
    robot = env.scene["robot"]
    # teeth = env.scene["teeth"]

    print("="*50)
    print(f"Robot asset path: {robot.cfg.prim_path}")
    print(f"Number of joints found: {robot.num_joints}")
    print("List of available joint names:")
    for i, name in enumerate(robot.joint_names):
        print(f"  [{i}]: {name}")
    print("="*50)

    # print(f"Teeth: {teeth}")


    # Flags for controlling teleoperation flow
    should_reset_recording_instance = False
    teleoperation_active = True


    rep_writer = None
    if args_cli.save:
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", args_cli.task)
        print(f"[INFO]: Saving camera data to: {output_dir}")
        rep_writer = rep.BasicWriter(output_dir=output_dir, frame_padding=0)


    should_save_image = False
    
    def save_image_callback() -> None:
        nonlocal should_save_image
        if args_cli.save:
            should_save_image = True
            print("Image save triggered - Saving on next step")
        else:
            print("Save not enabled. Use the --save flag to enable saving.")

    # Callback handlers
    def reset_recording_instance() -> None:
        """
        Reset the environment to its initial state.

        Sets a flag to reset the environment on the next simulation step.

        Returns:
            None
        """
        nonlocal should_reset_recording_instance
        should_reset_recording_instance = True
        print("Reset triggered - Environment will reset on next step")

    def start_teleoperation() -> None:
        """
        Activate teleoperation control of the robot.

        Enables the application of teleoperation commands to the environment.

        Returns:
            None
        """
        nonlocal teleoperation_active
        teleoperation_active = True
        print("Teleoperation activated")

    def stop_teleoperation() -> None:
        """
        Deactivate teleoperation control of the robot.

        Disables the application of teleoperation commands to the environment.

        Returns:
            None
        """
        nonlocal teleoperation_active
        teleoperation_active = False
        print("Teleoperation deactivated")

    def dump_joint_positions() -> None:
        q = robot.data.joint_pos[0].cpu().numpy()
        print("Current joint positions:", q.tolist())

    # Create device config if not already in env_cfg
    teleoperation_callbacks: dict[str, Callable[[], None]] = {
        "R": reset_recording_instance,
        "START": start_teleoperation,
        "STOP": stop_teleoperation,
        "RESET": reset_recording_instance,
        "P": save_image_callback,
        "J": dump_joint_positions, 
    }

    # For hand tracking devices, add additional callbacks
    if args_cli.xr:
        # Default to inactive for hand tracking
        teleoperation_active = False
    else:
        # Always active for other devices
        teleoperation_active = True

    # Create teleop device from config if present, otherwise create manually
    teleop_interface = None
    try:
        if hasattr(env_cfg, "teleop_devices") and args_cli.teleop_device in env_cfg.teleop_devices.devices:
            teleop_interface = create_teleop_device(
                args_cli.teleop_device, env_cfg.teleop_devices.devices, teleoperation_callbacks
            )
        else:
            logger.warning(
                f"No teleop device '{args_cli.teleop_device}' found in environment config. Creating default."
            )
            # Create fallback teleop device
            sensitivity = args_cli.sensitivity
            if args_cli.teleop_device.lower() == "keyboard":
                teleop_interface = Se3Keyboard(
                    Se3KeyboardCfg(pos_sensitivity=0.05 * sensitivity, rot_sensitivity=0.05 * sensitivity)
                )
            elif args_cli.teleop_device.lower() == "spacemouse":
                teleop_interface = Se3SpaceMouse(
                    Se3SpaceMouseCfg(pos_sensitivity=0.05 * sensitivity, rot_sensitivity=0.05 * sensitivity)
                )
            elif args_cli.teleop_device.lower() == "gamepad":
                teleop_interface = Se3Gamepad(
                    Se3GamepadCfg(pos_sensitivity=0.1 * sensitivity, rot_sensitivity=0.1 * sensitivity)
                )
            else:
                logger.error(f"Unsupported teleop device: {args_cli.teleop_device}")
                logger.error("Configure the teleop device in the environment config.")
                env.close()
                simulation_app.close()
                return

            # Add callbacks to fallback device
            for key, callback in teleoperation_callbacks.items():
                try:
                    teleop_interface.add_callback(key, callback)
                except (ValueError, TypeError) as e:
                    logger.warning(f"Failed to add callback for key {key}: {e}")
    except Exception as e:
        logger.error(f"Failed to create teleop device: {e}")
        env.close()
        simulation_app.close()
        return

    if teleop_interface is None:
        logger.error("Failed to create teleop interface")
        env.close()
        simulation_app.close()
        return

    print(f"Using teleop device: {teleop_interface}")

    # reset environment
    env.reset()
    teleop_interface.reset()

    print("Teleoperation started. Press 'R' to reset the environment.")

    # simulate environment
    while simulation_app.is_running():
        try:
            # run everything in inference mode
            with torch.inference_mode():
                # get device command
                action = teleop_interface.advance()

                # Only apply teleop commands when active
                if teleoperation_active:
                    # process actions
                    actions = action.repeat(env.num_envs, 1)
                    # apply actions
                    env.step(actions)
                else:
                    env.sim.render()

                if should_save_image:
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                    
                    scene = env.unwrapped.scene
                    camera = scene["wrist_camera"]
                    robot = scene["robot"]
                    camera_index = 0

                    if "rgb" in camera.data.output:
                        rgb_data = camera.data.output["rgb"][camera_index]
                        rgb_np = rgb_data.cpu().numpy()[..., :3].astype(np.uint8)
                        rgb_img = Image.fromarray(rgb_np, 'RGB')
                        rgb_filename = os.path.join(output_dir, f"rgb_{timestamp}.png")
                        rgb_img.save(rgb_filename)
                        print(f"Saved RGB image to: {rgb_filename}")

                    if "distance_to_image_plane" in camera.data.output:
                        depth_data = camera.data.output["distance_to_image_plane"][camera_index]
                        depth_np_raw = depth_data.cpu().numpy()
                        depth_np = np.squeeze(depth_np_raw)

                        depth_raw_filename = os.path.join(output_dir, f"depth_raw_{timestamp}.npy")
                        np.save(depth_raw_filename, depth_np)
                        print(f"Saved RAW Depth data to: {depth_raw_filename}")
                        
                        depth_min, depth_max = depth_np.min(), depth_np.max()
                        if depth_max > depth_min:
                            depth_normalized = (depth_np - depth_min) / (depth_max - depth_min) * 255.0
                        else:
                            depth_normalized = np.zeros_like(depth_np)
                        depth_img = Image.fromarray(depth_normalized.astype(np.uint8))
                        depth_visual_filename = os.path.join(output_dir, f"depth_visual_{timestamp}.png")
                        depth_img.save(depth_visual_filename)
                        print(f"Saved VISUAL Depth image to: {depth_visual_filename}")

                    joint_pos_tensor = robot.data.joint_pos[camera_index]
                    joint_pos_np = joint_pos_tensor.cpu().numpy()
                    


                    
                    joint_pos_tensor = robot.data.joint_pos[camera_index]
                    q = joint_pos_tensor.cpu().numpy()

                    pinocchio.forwardKinematics(model, data, q)
                    pinocchio.updateFramePlacements(model, data)

                    eef_pose = data.oMf[eef_frame_id]
                    eef_pos = eef_pose.translation
                    eef_rot_matrix = eef_pose.rotation

                    cam_pos_np_pin = np.zeros(3)
                    cam_quat_ros_np = np.array([1.0, 0.0, 0.0, 0.0])
                    if camera:
                        offset_pos = np.array(camera.cfg.offset.pos)
                        offset_quat_pin = pinocchio.Quaternion(np.array([
                            camera.cfg.offset.rot[1], # x
                            camera.cfg.offset.rot[2], # y
                            camera.cfg.offset.rot[3], # z
                            camera.cfg.offset.rot[0]  # w
                        ]))
                        offset_se3 = pinocchio.SE3(offset_quat_pin, offset_pos)
                        
                        final_cam_pose = eef_pose * offset_se3
                        
                        cam_pos_np_pin = final_cam_pose.translation
                        cam_quat_pin = pinocchio.Quaternion(final_cam_pose.rotation)
                        cam_quat_ros_np = np.array([cam_quat_pin.w, cam_quat_pin.x, cam_quat_pin.y, cam_quat_pin.z])
                    

                    # cam_pos_tensor = camera.data.pos_w[camera_index]
                    # cam_quat_tensor = camera.data.quat_w_ros[camera_index]
                    # cam_pos_np = cam_pos_tensor.cpu().numpy()
                    # cam_quat_np = cam_quat_tensor.cpu().numpy()

                    cam_intrinsics = camera.data.intrinsic_matrices[camera_index].cpu().numpy()
                    
                    metadata = {
                        "timestamp": timestamp,
                        "rgb_image_path": f"rgb_{timestamp}.png",
                        "depth_visual_path": f"depth_visual_{timestamp}.png",
                        "depth_raw_path": f"depth_raw_{timestamp}.npy",
                        "joint_positions": joint_pos_np.tolist(),
                        "joint_names": robot.joint_names,
                        "camera_position_world_calculated": cam_pos_np_pin.tolist(),
                        "camera_orientation_world_ros_calculated": cam_quat_ros_np.tolist(),
                        # "camera_position_world": cam_pos_np.tolist(),
                        # "camera_orientation_world_ros": cam_quat_np.tolist(),
                        "camera_intrinsics": cam_intrinsics.tolist(),
                    }
                    json_filename = os.path.join(output_dir, f"data_{timestamp}.json")
                    with open(json_filename, 'w') as f:
                        json.dump(metadata, f, indent=4)
                    print(f"Saved metadata to: {json_filename}")

                    should_save_image = False


                if should_reset_recording_instance:
                    env.reset()
                    teleop_interface.reset()
                    should_reset_recording_instance = False
                    print("Environment reset complete")
        except Exception as e:
            logger.error(f"Error during simulation step: {e}")
            break

    # close the simulator
    env.close()
    print("Environment closed")


if __name__ == "__main__":
    # run the main function
    main()
    # close sim app
    simulation_app.close()
