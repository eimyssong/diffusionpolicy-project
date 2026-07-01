# import os
# import torch
# import numpy as np
# import collections
# import tqdm
# from diffusion_policy.common.pytorch_util import dict_apply
# from diffusion_policy.policy.base_image_policy import BaseImagePolicy
# from diffusion_policy.env_runner.base_image_runner import BaseImageRunner
# import cv2


# class StackRobomimicImageRunner(BaseImageRunner):
#     def __init__(self, 
#                  output_dir,
#                  n_envs=1,
#                  max_steps=400,
#                  n_obs_steps=2,
#                  n_action_steps=8,
#                  device="cuda:0",
#                  **kwargs):
#         super().__init__(output_dir)

#         import carb
#         settings = carb.settings.get_settings()

#         renderer_enabled = settings.get("/app/renderer/enabled")
#         cameras_enabled = settings.get("/app/sensors/cameras/enabled")
#         scriptnode_enabled = settings.get("/app/omni.graph.scriptnode/enabled")

#         print("-" * 50)
#         print(f"[Check] Renderer Enabled: {renderer_enabled}")
#         print(f"[Check] Cameras Enabled: {cameras_enabled}")
#         print(f"[Check] ScriptNode Enabled: {scriptnode_enabled}")
#         print("-" * 50)


#         # from omni.isaac.kit import SimulationApp
#         # import os
#         asset_root_url = "http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/4.2"

#         if "NUCLEUS_ASSET_ROOT" not in os.environ:
#             os.environ["NUCLEUS_ASSET_ROOT"] = asset_root_url

#         os.environ["ISAAC_SIM_ENABLE_CAMERAS"] = "1"
#         os.environ["OMNI_KIT_ALLOW_CAMERA_RENDERING"] = "1"
                        
#         # sim_config = {
#         #     "headless": True,
#         #     "--enable_cameras": True,
#         #     # "render": True,
#         # }
#         # self.sim_app = SimulationApp(sim_config)
#         # # self.sim_app = SimulationApp(sim_config, experience="")


#         from isaaclab.envs import ManagerBasedEnv
#         from isaaclab_tasks.manager_based.manipulation.stack.stack_env_cfg import StackEnvCfg
#         from isaaclab_tasks.utils import parse_env_cfg

        
#         self.device = device
#         self.n_envs = n_envs
#         self.max_steps = max_steps
#         self.step_count = 0
#         self.n_obs_steps = n_obs_steps
#         self.n_action_steps = n_action_steps
        

#         cfg = parse_env_cfg(
#             "Isaac-Stack-Cube-Franka-IK-Rel-Visuomotor-v0",
#             # "Isaac-Stack-Cube-Franka-IK-Rel-v0",
#             device=device, 
#             num_envs=n_envs,
#         )

#         if hasattr(cfg.sim, "render_settings"):
#             cfg.sim.render_settings.enable_cameras = True
#             cfg.sim.disable_contact_processing = False

#         target_root = asset_root_url

#         for attr_name in dir(cfg.scene):
#             target_obj = getattr(cfg.scene, attr_name)
            
#             if hasattr(target_obj, "spawn") and hasattr(target_obj.spawn, "usd_path"):
#                 original_path = target_obj.spawn.usd_path
#                 if original_path and original_path.startswith("None"):
#                     new_path = original_path.replace("None", target_root)
#                     target_obj.spawn.usd_path = new_path



#         # import sys
#         # if "--enable_cameras" not in sys.argv:
#         #     sys.argv.append("--enable_cameras")

#         # import carb
#         # settings = carb.settings.get_settings()
#         # settings.set("/app/renderer/enabled", True)
#         # settings.set("/app/omni.graph.scriptnode/enabled", True)


#         self.env = ManagerBasedEnv(cfg)
#         self.env.reset()



#     def _extract_obs(self, obs):

#         if isinstance(obs, tuple): obs = obs[0]
        
#         p_obs = obs["policy"]

#         target_size = (84, 84)

#         def pre_img(img):
#             img = img.float() /255.0
#             # print("!!!!!!!!!!!!!!!!!!!img.ndim:", img.ndim)
#             # print('!!!!!!!!!!!!!!!!!!!img.shape:', img.shape)

#             if img.ndim == 4:
#                 img = img.permute(0, 3, 1, 2)
            
#             img_resized = torch.nn.functional.interpolate(
#                 img, size=target_size, mode='area'
#             )

#             return img_resized


#         return {
#             "table_cam": pre_img(p_obs["table_cam"]),
#             "wrist_cam": pre_img(p_obs["wrist_cam"]),
#             "eef_pos": p_obs["eef_pos"].float(),
#             "eef_quat": p_obs["eef_quat"].float(),
#             "gripper_pos": p_obs["gripper_pos"].float()
#         }


#     def run(self, policy: BaseImagePolicy):
#         device = policy.device
#         policy.eval()
        
#         obs_raw, _ = self.env.reset()
#         obs_dict = self._extract_obs(obs_raw)

        
#         obs_history = collections.deque(maxlen=self.n_obs_steps)
#         for _ in range(self.n_obs_steps):
#             obs_history.append(obs_dict)

#         reward_sum = np.zeros(self.n_envs)
#         step_idx = 0
#         pbar = tqdm.tqdm(total=self.max_steps, desc="Isaac Image Eval")



#         while step_idx < self.max_steps:
#             input_dict = {
#                 key: torch.stack([o[key] for o in obs_history], dim=1).to(device)
#                 for key in obs_history[0].keys()
#             }

#             with torch.no_grad():
#                 action_dict = policy.predict_action(input_dict)



#             action_pred = action_dict['action_pred']

#             for i in range(self.n_action_steps):
#                 if step_idx >= self.max_steps: break
                
#                 step_result = self.env.step(action_pred[:, i, :])
#                 if len(step_result) == 5:
#                     obs_raw, reward, terminated, truncated, _ = step_result
#                 else:
#                     obs_raw, extras = step_result
#                     reward = extras.get("reward", torch.tensor(0.0))
#                     terminated = extras.get("terminated", torch.tensor(False))
#                     truncated = extras.get("truncated", torch.tensor(False))

                
#                 obs_dict = self._extract_obs(obs_raw)
#                 obs_history.append(obs_dict)
                
#                 reward_sum += reward.cpu().numpy()
#                 step_idx += 1
#                 pbar.update(1)
                

#                 done = terminated | truncated
#                 if done.all(): break
            
#             if done.all(): break
            
#         pbar.close()
#         return {
#             "test/mean_score": np.mean(reward_sum),
#             "test/max_score": np.max(reward_sum)
#         }

















import os
import torch
import numpy as np
import collections
import tqdm
import cv2
from diffusion_policy.policy.base_image_policy import BaseImagePolicy
from diffusion_policy.env_runner.base_image_runner import BaseImageRunner


from isaaclab.managers import DatasetExportMode
from isaaclab.envs.mdp.recorders.recorders_cfg import ActionStateRecorderManagerCfg
from isaaclab.managers import TerminationTermCfg as DoneTerm
from isaaclab_tasks.manager_based.manipulation.stack import mdp


class StackRobomimicImageRunner(BaseImageRunner):
    def __init__(self, 
                 output_dir,
                 n_envs=1,
                 max_steps=400,
                 n_obs_steps=2,
                 n_action_steps=8,
                 device="cuda:0",
                 **kwargs):
        super().__init__(output_dir)
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        

        self.device = device
        self.n_envs = n_envs
        self.max_steps = max_steps
        self.n_obs_steps = n_obs_steps
        self.n_action_steps = n_action_steps
        self.m_epoch = 0
        self.m_num = 0


        from isaaclab_tasks.utils import parse_env_cfg
        cfg = parse_env_cfg("Isaac-Stack-Cube-Franka-IK-Rel-Visuomotor-v0", device=device, num_envs=n_envs)


        cfg.recorders = ActionStateRecorderManagerCfg()
        cfg.recorders.dataset_export_dir_path = self.output_dir
        cfg.recorders.dataset_filename = "eval_results" 

        cfg.recorders.dataset_export_mode = DatasetExportMode.EXPORT_ALL 


        if hasattr(cfg.sim, "render_settings"):
            cfg.sim.render_settings.enable_cameras = True


        from isaaclab.envs import ManagerBasedEnv
        self.env = ManagerBasedEnv(cfg)
        self.env.reset()

    def _extract_obs(self, obs):
        if isinstance(obs, tuple): obs = obs[0]
        p_obs = obs["policy"]
        

        raw_image = p_obs["table_cam"][0][:,:,:3].cpu().numpy().astype(np.uint8)
        
        target_size = (84, 84)
        def pre_img(img_rgb, img_depth):
            img_rgb = img_rgb
            img_depth = img_depth

            # print(img_rgb.shape)
            # print(img_depth.shape)
            # print(img_rgb.min(), img_rgb.max())
            # print(img_depth.min(), img_depth.max())


            img_rgb = img_rgb.float() / 255.0
            if img_rgb.ndim == 4:
                # print("1111111111111111111111111111111111111111111111")
                img_rgb = img_rgb.permute(0, 3, 1, 2)
            img_rgb = torch.nn.functional.interpolate(img_rgb, size=target_size, mode='area')


            min_depth=0.0
            max_depth=2.0
            img_depth = torch.clamp(img_depth, min_depth, max_depth)
            # print(img_depth.shape)
            # print(img_depth.min(), img_depth.max())
            img_depth = (img_depth - min_depth) / (max_depth - min_depth)

            if img_depth.ndim == 4:
                # print("2222222222222222222222222222222222222222222222")
                img_depth = img_depth.permute(0, 3, 1, 2)
            img_depth = torch.nn.functional.interpolate(img_depth, size=target_size, mode='nearest')            
            
            return torch.cat([img_rgb, img_depth], dim=1)


        return {
            "obs_dict": {
                "table_cam": pre_img(p_obs["table_cam"], p_obs["table_cam_depth"]),
                "wrist_cam": pre_img(p_obs["wrist_cam"], p_obs["wrist_cam_depth"]),
                "eef_pos": p_obs["eef_pos"].float(),
                "eef_quat": p_obs["eef_quat"].float(),
                "gripper_pos": p_obs["gripper_pos"].float()
            },
            "render_frame": raw_image
        }

    def run(self, policy: BaseImagePolicy):
        device = policy.device
        policy.eval()
        

        obs_raw, _ = self.env.reset()
        self.env.recorder_manager.reset() 
        
        extracted = self._extract_obs(obs_raw)
        obs_dict = extracted["obs_dict"]


        # video_path = os.path.join(self.output_dir, f"eval_video_{int(torch.randint(0, 10000, (1,)))}.mp4")
        video_path = os.path.join(self.output_dir, f"eval_video_{self.m_epoch}epoch_{self.m_num}.mp4")
        self.m_num += 1
        self.m_num = self.m_num % 10
        if self.m_num == 0:
            self.m_epoch += 100

        h, w, _ = extracted["render_frame"].shape
        video_writer = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), 30.0, (w, h))

        obs_history = collections.deque(maxlen=self.n_obs_steps)
        for _ in range(self.n_obs_steps):
            obs_history.append(obs_dict)

        reward_sum = np.zeros(self.n_envs)
        step_idx = 0
        pbar = tqdm.tqdm(total=self.max_steps, desc="Isaac Eval (HDF5+Video)")

        while step_idx < self.max_steps:
            input_dict = {
                key: torch.stack([o[key] for o in obs_history], dim=1).to(device)
                for key in obs_history[0].keys()
            }

            with torch.no_grad():
                action_dict = policy.predict_action(input_dict)
            action_pred = action_dict['action_pred']

            for i in range(self.n_action_steps):
                if step_idx >= self.max_steps: break
                

                step_result = self.env.step(action_pred[:, i, :])
                
                if len(step_result) == 5:
                    obs_raw, reward, terminated, truncated, _ = step_result
                else:
                    obs_raw, extras = step_result
                    t1 = obs_raw['subtask_terms']['grasp_1'].int().item()
                    t2 = obs_raw['subtask_terms']['stack_1'].int().item()
                    t3 = obs_raw['subtask_terms']['grasp_2'].int().item()

                    reward = mdp.cubes_stacked(self.env).int().item()

                    # reward = extras.get("reward", torch.tensor(0.0))
                    terminated = mdp.cubes_stacked(self.env)
                    truncated = extras.get("truncated", torch.tensor(False))

                extracted = self._extract_obs(obs_raw)
                obs_dict = extracted["obs_dict"]
                obs_history.append(obs_dict)
                

                frame = cv2.cvtColor(extracted["render_frame"], cv2.COLOR_RGB2BGR)
                video_writer.write(frame)
                
                reward_sum = reward
                step_idx += 1
                pbar.update(1)

                if (terminated | truncated).all(): break
            if (terminated | truncated).all(): break

        pbar.close()
        video_writer.release()


        self.env.recorder_manager.export_episodes([0]) 
        print(f"HDF5 Data & Video saved in: {self.output_dir}")

        return {
            # "test/mean_score": np.mean(reward_sum),
            "test/mean_score": reward_sum,
            "test/grasp_1" : t1,
            "test/stack_1" : t2,
            "test/grasp_2" : t3,
            "test/video_path": video_path
        }