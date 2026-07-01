import os
import torch
import numpy as np
import collections
import tqdm
import cv2

from pytorch3d.ops import sample_farthest_points


from diffusion_policy_3d.policy.base_policy import BasePolicy
from diffusion_policy_3d.common.pytorch_util import dict_apply
from diffusion_policy_3d.env_runner.base_runner import BaseRunner
import diffusion_policy_3d.common.logger_util as logger_util
from termcolor import cprint


from isaaclab.managers import DatasetExportMode
from isaaclab.envs.mdp.recorders.recorders_cfg import ActionStateRecorderManagerCfg
from isaaclab_tasks.manager_based.manipulation.stack import mdp

import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt 

class IsaaclabRunner(BaseRunner):
    def __init__(
        self,
        output_dir,
        eval_episodes=20,
        max_steps=1000,
        n_obs_steps=8,
        n_action_steps=8,
        fps=10,
        crf=22,
        render_size=84,
        tqdm_interval_sec=5.0,
        n_envs=None,
        task_name=None,
        n_train=None,
        n_test=None,
        device="cuda:0",
        use_point_crop=True,
        num_points=2048
    ):
        super().__init__(output_dir)

        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        self.device = device
        self.n_envs = n_envs
        self.max_steps = max_steps
        self.n_obs_steps = n_obs_steps
        self.n_action_steps = n_action_steps
        self.num_points = num_points
        self.m_num = 0
        self.m_epoch = 0

        self.render = o3d.visualization.rendering.OffscreenRenderer(512, 512)
        self.mtl = o3d.visualization.rendering.MaterialRecord()
        self.mtl.point_size = 3.0
        self.mtl.shader = "defaultUnlit"


        from isaaclab_tasks.utils import parse_env_cfg
        cfg = parse_env_cfg(
            "Isaac-Stack-Cube-Franka-IK-Rel-Visuomotor-v0",
            device=device,
            num_envs=n_envs
        )

        cfg.recorders = ActionStateRecorderManagerCfg()
        cfg.recorders.dataset_export_dir_path = output_dir
        cfg.recorders.dataset_filename = "eval_results"
        cfg.recorders.dataset_export_mode = DatasetExportMode.EXPORT_ALL

        if hasattr(cfg.sim, "render_settings"):
            cfg.sim.render_settings.enable_cameras = True

        from isaaclab.envs import ManagerBasedEnv
        self.env = ManagerBasedEnv(cfg)
        self.env.reset()




    def _preprocess_pointcloud(self, pc_tensor):
        pc_tensor = pc_tensor.to(self.device)
        
        in_channels = pc_tensor.shape[-1]

        # table = AssetBaseCfg(
        #     prim_path="{ENV_REGEX_NS}/Table",
        #     init_state=AssetBaseCfg.InitialStateCfg(pos=[0.5, 0, 0], rot=[0.707, 0, 0, 0.707]),
        #     spawn=UsdFileCfg(usd_path=f"{ISAAC_NUCLEUS_DIR}/Props/Mounts/SeattleLabTable/table_instanceable.usd"),
        # )
        
        xmin, xmax = -2.0, 2.0   
        ymin, ymax = -2.0, 2.0   
        zmin, zmax = 0.01, 2.0

        processed = []
        B = pc_tensor.shape[0]

        for b in range(B):
            sub_pc = pc_tensor[b]
            mask = (
                (sub_pc[:,0] > xmin) & (sub_pc[:,0] < xmax) &
                (sub_pc[:,1] > ymin) & (sub_pc[:,1] < ymax) &
                (sub_pc[:,2] > zmin) & (sub_pc[:,2] < zmax)
            )
            sub_pc = sub_pc[mask]

            if sub_pc.shape[0] == 0:
                sub_pc = torch.zeros((self.num_points, in_channels), device=self.device)
            else:
                sub_pc_batch = sub_pc.unsqueeze(0).cpu() 
                if sub_pc_batch.shape[1] >= self.num_points:
                    pc_sampled, idx = sample_farthest_points(sub_pc_batch[..., :3], K=self.num_points)
                    # _, idx = sample_farthest_points(sub_pc_batch[..., :3], K=self.num_points)
                    sub_pc = sub_pc[idx.squeeze(0)].to(self.device)
                else:
                    pad = self.num_points - sub_pc.shape[0]
                    sub_pc = torch.cat([sub_pc, torch.zeros((pad, in_channels), device=self.device)], dim=0)
            
            processed.append(sub_pc)
            
        return torch.stack(processed)




    # def render_pointcloud(self, pc, cam_eye, cam_target, cam_up):
    #     if np.all(pc[:, :3] == 0):
    #         return np.zeros((512, 512, 3), dtype=np.uint8)

    #     pcd = o3d.geometry.PointCloud()
    #     pcd.points = o3d.utility.Vector3dVector(pc[:, :3])

    #     colors = pc[:, 3:6]
    #     pcd.colors = o3d.utility.Vector3dVector(colors)

    #     self.render.scene.remove_geometry("pcd")
    #     self.render.scene.add_geometry("pcd", pcd, self.mtl)
        
    #     self.render.scene.set_background([0.05, 0.05, 0.05, 1.0])
    #     self.render.setup_camera(60.0, cam_target, cam_eye, cam_up)

    #     img = self.render.render_to_image()
    #     return np.asarray(img)


    def render_pointcloud(self, pc, cam_eye, cam_target, cam_up):
        if np.all(pc[:, :3] == 0):
            return np.zeros((512, 512, 3), dtype=np.uint8)

        pcd = o3d.geometry.PointCloud()
        points = pc[:, :3]
        pcd.points = o3d.utility.Vector3dVector(points)

        # dist = sqrt((x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2)
        distances = np.linalg.norm(points - cam_eye, axis=1)

        dist_min = np.min(distances)
        dist_max = np.max(distances)
        norm_distances = (distances - dist_min) / (dist_max - dist_min + 1e-7)

        cmap = plt.get_cmap('jet') 
        colors = cmap(norm_distances)[:, :3] 

        pcd.colors = o3d.utility.Vector3dVector(colors)

        self.render.scene.remove_geometry("pcd")
        self.render.scene.add_geometry("pcd", pcd, self.mtl)
        
        self.render.scene.set_background([0.05, 0.05, 0.05, 1.0])
        self.render.setup_camera(60.0, cam_target, cam_eye, cam_up)

        img = self.render.render_to_image()
        return np.asarray(img)



    # def _extract_obs(self, obs):
    #     if isinstance(obs, tuple): obs = obs[0]
    #     p_obs = obs["policy"]

    #     raw_pc = p_obs["table_cam_pointcloud"]
    #     pc = self._preprocess_pointcloud(raw_pc)

    #     cam = self.env.scene["table_cam"]
    #     cam_data = cam.data

    #     cam_eye = cam_data.pos_w[0].cpu().numpy()
        
    #     q_open_gl = cam_data.quat_w_opengl[0].cpu().numpy() 
        
    #     import scipy.spatial.transform as st
    #     r = st.Rotation.from_quat([q_open_gl[1], q_open_gl[2], q_open_gl[3], q_open_gl[0]])
        
    #     forward = r.apply(np.array([0, 0, -1])) 
    #     cam_target = cam_eye + forward
        
    #     cam_up = r.apply(np.array([0, 1, 0]))

    #     render_frame = p_obs["table_cam"][0][:,:,:3].cpu().numpy().astype(np.uint8)

    #     return {
    #         "obs_dict": {
    #             "point_cloud": pc,
    #             "agent_pos": torch.cat([p_obs["eef_pos"], p_obs["eef_quat"], p_obs["gripper_pos"]], dim=-1).float()
    #         },
    #         "render_frame": render_frame,
    #         "cam_info": (cam_eye, cam_target, cam_up)
    #     }



    # def run(self, policy: BasePolicy):
    #     device = policy.device
    #     policy.eval()

    #     obs_raw, _ = self.env.reset()
    #     self.env.recorder_manager.reset()

    #     extracted = self._extract_obs(obs_raw)
    #     obs_dict = extracted["obs_dict"]

    #     video_path = os.path.join(self.output_dir, f"eval_video_{self.m_num}.mp4")
    #     pc_video_path = os.path.join(self.output_dir, f"pc_video_{self.m_num}.mp4")
    #     self.m_num += 100
    #     h, w, _ = extracted["render_frame"].shape
    #     video_writer = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*"mp4v"), 30.0, (w, h))
    #     pc_video_writer = cv2.VideoWriter(pc_video_path, cv2.VideoWriter_fourcc(*"mp4v"), 30.0, (512, 512))


    #     obs_history = collections.deque(maxlen=self.n_obs_steps)

    #     for _ in range(self.n_obs_steps):
    #         obs_history.append(obs_dict)

    #     step_idx = 0
    #     reward_sum = 0

    #     pbar = tqdm.tqdm(total=self.max_steps, desc="IsaacLab DP3 Eval")

    #     while step_idx < self.max_steps:
    #         input_dict = {
    #             k: torch.stack([o[k] for o in obs_history], dim=1).to(device)
    #             for k in obs_history[0].keys()
    #         }

    #         with torch.no_grad():
    #             action_dict = policy.predict_action(input_dict)

    #         action_pred = action_dict["action_pred"]

    #         for i in range(self.n_action_steps):

    #             if step_idx >= self.max_steps:
    #                 break

    #             step_result = self.env.step(action_pred[:,i])

    #             if len(step_result) == 5:
    #                 obs_raw, reward, terminated, truncated, _ = step_result
    #             else:
    #                 obs_raw, extras = step_result
    #                 reward = mdp.cubes_stacked(self.env).int().item()
    #                 # reward = extras.get("reward", torch.tensor(0.0))
    #                 terminated = mdp.cubes_stacked(self.env)
    #                 truncated = extras.get("truncated", torch.tensor(False))

    #             extracted = self._extract_obs(obs_raw)
    #             obs_dict = extracted["obs_dict"]
    #             obs_history.append(obs_dict)

                
    #             frame = cv2.cvtColor(extracted["render_frame"],cv2.COLOR_RGB2BGR)
    #             video_writer.write(frame)

    #             pc_np = obs_dict["point_cloud"][0].cpu().numpy()
    #             eye, target, up = extracted["cam_info"]
    #             pc_img = self.render_pointcloud(pc_np, eye, target, up)

    #             pc_img = cv2.cvtColor(pc_img, cv2.COLOR_RGB2BGR)
    #             pc_video_writer.write(pc_img)

    #             step_idx += 1
    #             pbar.update(1)
    #             reward_sum = reward
    #             done = terminated | truncated

    #             if done.any():
    #                 break

    #         if done.any():
    #             break

    #     pbar.close()
    #     video_writer.release()
    #     pc_video_writer.release()

    #     self.env.recorder_manager.export_episodes([0])
    #     print(f"HDF5 Data & Video saved in: {self.output_dir}")

    #     return {
    #         "test/mean_score": reward_sum,
    #         "test/video_path": video_path
    #     }



    # def run(self, policy: BasePolicy):
    #     device = policy.device
    #     policy.eval()

    #     obs_raw, _ = self.env.reset()
    #     self.env.recorder_manager.reset()

    #     extracted = self._extract_obs(obs_raw)
    #     obs_dict = extracted["obs_dict"]

    #     combined_video_path = os.path.join(self.output_dir, f"dataset14_color_img+pc_video_{self.m_epoch}_{self.m_num}.mp4")
    #     self.m_num += 1
    #     self.m_num = self.m_num % 5
    #     if self.m_num == 0:
    #         self.m_epoch += 100

    #     # combined_video_path = os.path.join(self.output_dir, f"dataset13_img+pc_video_{self.m_epoch}.mp4")
    #     # self.m_epoch += 100
            
    #     combined_video_writer = cv2.VideoWriter(combined_video_path, cv2.VideoWriter_fourcc(*"mp4v"), 30.0, (1024, 512))


    #     obs_history = collections.deque(maxlen=self.n_obs_steps)

    #     for _ in range(self.n_obs_steps):
    #         obs_history.append(obs_dict)

    #     step_idx = 0
    #     reward_sum = 0

    #     pbar = tqdm.tqdm(total=self.max_steps, desc="IsaacLab DP3 Eval")

    #     while step_idx < self.max_steps:
    #         input_dict = {
    #             k: torch.stack([o[k] for o in obs_history], dim=1).to(device)
    #             for k in obs_history[0].keys()
    #         }

    #         with torch.no_grad():
    #             action_dict = policy.predict_action(input_dict)

    #         action_pred = action_dict["action_pred"]

    #         for i in range(self.n_action_steps):

    #             if step_idx >= self.max_steps:
    #                 break

    #             step_result = self.env.step(action_pred[:,i])

    #             if len(step_result) == 5:
    #                 obs_raw, reward, terminated, truncated, _ = step_result
    #             else:
    #                 obs_raw, extras = step_result
    #                 reward = mdp.cubes_stacked(self.env).int().item()
    #                 # reward = extras.get("reward", torch.tensor(0.0))
    #                 terminated = mdp.cubes_stacked(self.env)
    #                 truncated = extras.get("truncated", torch.tensor(False))

    #             extracted = self._extract_obs(obs_raw)
    #             obs_dict = extracted["obs_dict"]
    #             obs_history.append(obs_dict)



    #             rgb_frame = cv2.cvtColor(extracted["render_frame"], cv2.COLOR_RGB2BGR)
    #             rgb_frame = cv2.resize(rgb_frame, (512, 512))

    #             pc_np = obs_dict["point_cloud"][0].cpu().numpy()
    #             eye, target, up = extracted["cam_info"]
    #             pc_img = self.render_pointcloud(pc_np, eye, target, up)

    #             pc_img_bgr = cv2.cvtColor(pc_img, cv2.COLOR_RGB2BGR)

    #             combined_frame = np.hstack([rgb_frame, pc_img_bgr])
    #             combined_video_writer.write(combined_frame)

    #             step_idx += 1
    #             pbar.update(1)
    #             reward_sum = reward
    #             done = terminated | truncated

    #             if done.any():
    #                 break

    #         if done.any():
    #             break

    #     pbar.close()
    #     combined_video_writer.release()

    #     self.env.recorder_manager.export_episodes([0])
    #     print(f"HDF5 Data & Video saved in: {self.output_dir}")

    #     return {
    #         "test/mean_score": reward_sum,
    #         "test/video_path": combined_video_path
    #     }



    def _extract_obs(self, obs):
        if isinstance(obs, tuple): obs = obs[0]
        p_obs = obs["policy"]

        raw_pc = p_obs["table_cam_pointcloud"]
        pc = self._preprocess_pointcloud(raw_pc)

        cam = self.env.scene["table_cam"]
        cam_data = cam.data

        cam_eye = cam_data.pos_w[0].cpu().numpy()
        
        q_open_gl = cam_data.quat_w_opengl[0].cpu().numpy() 
        
        import scipy.spatial.transform as st
        r = st.Rotation.from_quat([q_open_gl[1], q_open_gl[2], q_open_gl[3], q_open_gl[0]])
        
        forward = r.apply(np.array([0, 0, -1])) 
        cam_target = cam_eye + forward
        
        cam_up = r.apply(np.array([0, 1, 0]))

        render_frame = p_obs["table_cam"][0][:,:,:3].cpu().numpy().astype(np.uint8)

        return {
            # "obs_dict": {
            #     "point_cloud": pc,
            #     "agent_pos": torch.cat([p_obs["eef_pos"], p_obs["eef_quat"], p_obs["gripper_pos"]], dim=-1).float()
            "obs_dict": {
                "point_cloud": pc.detach(),
                "agent_pos": torch.cat([p_obs["eef_pos"], p_obs["eef_quat"], p_obs["gripper_pos"]], dim=-1).float().detach()
            },
            "render_frame": render_frame,
            "cam_info": (cam_eye, cam_target, cam_up)
        }

    # def predict_action_with_saliency(self, policy, input_dict):
    #     pc = input_dict["point_cloud"]
    #     pc = pc.clone().detach().requires_grad_(True)

    #     # shallow copy
    #     input_dict = dict(input_dict)
    #     input_dict["point_cloud"] = pc

    #     # forward
    #     action_dict = policy.predict_action(input_dict)
    #     action = action_dict["action_pred"]

    #     score = action[:, 0].norm()

    #     # backward
    #     policy.zero_grad(set_to_none=True)

    #     if pc.grad is not None:
    #         pc.grad.zero_()

    #     score.backward()
    #     grads = pc.grad

    #     # saliency = grads[..., :3].abs().mean(dim=-1)
    #     # saliency_rgb = grads[..., 3:6].abs().mean(dim=-1)
    #     saliency = grads.abs().mean(dim=-1)
    #     saliency = saliency.detach().cpu().numpy()

    #     return action_dict, saliency


    # SmoothGrad
    def predict_action_with_saliency(self, policy, input_dict, n_samples=10, noise_std=0.01):
        clean_pc = input_dict["point_cloud"]

        clean_input = dict(input_dict)
        clean_input["point_cloud"] = clean_pc

        with torch.enable_grad():
            clean_action_dict = policy.predict_action(clean_input)

        action_dict = clean_action_dict

        saliency_accum = 0

        for _ in range(n_samples):
            noisy_pc = clean_pc.clone().detach()

            noise = torch.randn_like(noisy_pc) * noise_std
            noisy_pc = noisy_pc + noise

            noisy_pc.requires_grad_(True)

            noisy_input = dict(input_dict)
            noisy_input["point_cloud"] = noisy_pc

            noisy_action_dict = policy.predict_action(noisy_input)

            action = noisy_action_dict["action_pred"]

            score = action[:, 0].norm()

            policy.zero_grad(set_to_none=True)

            if noisy_pc.grad is not None:
                noisy_pc.grad.zero_()

            score.backward()

            grads = noisy_pc.grad

            saliency = grads.abs().mean(dim=-1)

            saliency_accum += saliency.detach()

        saliency = saliency_accum / n_samples
        saliency = saliency.cpu().numpy()

        return action_dict, saliency


    def render_saliency_pointcloud(self, pc, saliency, cam_eye, cam_target, cam_up):
        if np.all(pc[:, :3] == 0):
            return np.zeros((512, 512, 3), dtype=np.uint8)

        pcd = o3d.geometry.PointCloud()

        points = pc[:, :3].astype(np.float64)
        pcd.points = o3d.utility.Vector3dVector(points)

        saliency = np.asarray(saliency)

        # print("before:", saliency.shape)

        if saliency.ndim == 2:
            saliency = saliency[-1]

        # (1, N) -> (N,)
        saliency = saliency.squeeze()

        # print("after:", saliency.shape)

        # normalize
        saliency = saliency - saliency.min()
        saliency = saliency / (saliency.max() + 1e-7)

        cmap = plt.get_cmap("jet")

        colors = cmap(saliency)[:, :3]

        colors = colors.astype(np.float64)

        pcd.colors = o3d.utility.Vector3dVector(colors)

        try:
            self.render.scene.remove_geometry("pcd")
        except:
            pass

        self.render.scene.add_geometry("pcd", pcd, self.mtl)

        self.render.scene.set_background(
            [0.05, 0.05, 0.05, 1.0]
        )

        self.render.setup_camera(
            60.0,
            cam_target,
            cam_eye,
            cam_up
        )

        img = self.render.render_to_image()

        return np.asarray(img)


    def run(self, policy: BasePolicy):
        device = policy.device
        policy.eval()

        obs_raw, _ = self.env.reset()
        self.env.recorder_manager.reset()

        extracted = self._extract_obs(obs_raw)
        obs_dict = extracted["obs_dict"]

        # combined_video_path = os.path.join(self.output_dir, f"saliency_video_{self.m_epoch}_{self.m_num}.mp4")
        # self.m_num += 1
        # self.m_num = self.m_num % 5
        # if self.m_num == 0:
        #     self.m_epoch += 100

        combined_video_path = os.path.join(self.output_dir, f"*saliency_video_{self.m_epoch}.mp4")
        self.m_epoch += 100


        combined_video_writer = cv2.VideoWriter(
            combined_video_path,
            cv2.VideoWriter_fourcc(*"mp4v"),
            30.0,
            (1024, 512)
        )

        obs_history = collections.deque(
            maxlen=self.n_obs_steps
        )

        for _ in range(self.n_obs_steps):
            obs_history.append(obs_dict)

        step_idx = 0
        reward_sum = 0

        pbar = tqdm.tqdm(
            total=self.max_steps,
            desc="IsaacLab DP3 Eval"
        )

        done = torch.tensor([False], device=device)

        while step_idx < self.max_steps:
            input_dict = {
                k: torch.stack([o[k] for o in obs_history], dim=1).to(device)
                for k in obs_history[0].keys()
            }

            action_dict, saliency = \
                self.predict_action_with_saliency(
                    policy,
                    input_dict
                )

            action_pred = action_dict["action_pred"].detach()

            for i in range(self.n_action_steps):

                if step_idx >= self.max_steps:
                    break

                step_result = self.env.step(
                    action_pred[:, i]
                )

                if len(step_result) == 5:
                    obs_raw, reward, terminated, truncated, _ \
                        = step_result
                else:
                    obs_raw, extras = step_result
                    reward = mdp.cubes_stacked(
                        self.env
                    ).int().item()
                    terminated = mdp.cubes_stacked(
                        self.env
                    )
                    truncated = extras.get(
                        "truncated",
                        torch.tensor(False)
                    )

                extracted = self._extract_obs(obs_raw)
                obs_dict = extracted["obs_dict"]
                obs_history.append(obs_dict)

                rgb_frame = cv2.cvtColor(
                    extracted["render_frame"],
                    cv2.COLOR_RGB2BGR
                )
                rgb_frame = cv2.resize(
                    rgb_frame,
                    (512, 512)
                )

                pc_np = obs_dict["point_cloud"][0] \
                    .detach() \
                    .cpu() \
                    .numpy()
                eye, target, up = extracted["cam_info"]
                pc_img = self.render_saliency_pointcloud(
                    pc_np,
                    saliency[0],
                    eye,
                    target,
                    up
                )
                pc_img_bgr = cv2.cvtColor(
                    pc_img,
                    cv2.COLOR_RGB2BGR
                )

                pc_img_bgr = cv2.resize(
                    pc_img_bgr,
                    (512, 512)
                )

                combined_frame = np.hstack([
                    rgb_frame,
                    pc_img_bgr
                ])
                combined_video_writer.write(
                    combined_frame
                )


                step_idx += 1
                pbar.update(1)
                reward_sum = reward
                done = terminated | truncated

                if done.any():
                    break

            if done.any():
                break

        pbar.close()
        combined_video_writer.release()

        self.env.recorder_manager.export_episodes([0])
        print(
            f"HDF5 Data & Video saved in: "
            f"{self.output_dir}"
        )

        return {
            "test/mean_score": reward_sum,
            "test/video_path": combined_video_path
        }