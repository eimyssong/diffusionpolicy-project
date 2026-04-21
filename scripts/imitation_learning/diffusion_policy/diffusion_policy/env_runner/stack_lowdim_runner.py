import wandb
import numpy as np
import torch
import collections
import pathlib
import tqdm
import dill
import math
import wandb.sdk.data_types.video as wv

from diffusion_policy.gym_util.async_vector_env import AsyncVectorEnv
from diffusion_policy.gym_util.sync_vector_env import SyncVectorEnv
from diffusion_policy.gym_util.multistep_wrapper import MultiStepWrapper
from diffusion_policy.gym_util.video_recording_wrapper import VideoRecordingWrapper, VideoRecorder
from gym.wrappers import FlattenObservation

from diffusion_policy.policy.base_lowdim_policy import BaseLowdimPolicy
from diffusion_policy.common.pytorch_util import dict_apply
from diffusion_policy.env_runner.base_lowdim_runner import BaseLowdimRunner

import copy


class IsaacLabStackLowdimRunner(BaseLowdimRunner):
    def __init__(
        self,
        n_envs=1,
        n_obs_steps=3,
        n_action_steps=1,
        max_steps=350,
        device="cuda:0",
        abs_action= False,
        **kwargs
    ):


        from omni.isaac.kit import SimulationApp
        import os
        asset_root_url = "http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/4.2"

        if "NUCLEUS_ASSET_ROOT" not in os.environ:
            os.environ["NUCLEUS_ASSET_ROOT"] = asset_root_url
                        
        sim_config = {
            "headless": False
        }
        self.sim_app = SimulationApp(sim_config)


        from isaaclab.envs import ManagerBasedEnv
        from isaaclab_tasks.manager_based.manipulation.stack.stack_env_cfg import StackEnvCfg
        from isaaclab_tasks.utils import parse_env_cfg

        self.device = device
        self.n_envs = n_envs
        self.max_steps = max_steps
        self.step_count = 0

        self.n_obs_steps = n_obs_steps
        self.n_action_steps = n_action_steps

        self.abs_action = abs_action
        
        cfg = parse_env_cfg(
            task_name="Isaac-Stack-Cube-Franka-IK-Rel-v0",
            device=device,
            num_envs=n_envs,
        )

        target_root = asset_root_url

        for attr_name in dir(cfg.scene):
            target_obj = getattr(cfg.scene, attr_name)
            
            if hasattr(target_obj, "spawn") and hasattr(target_obj.spawn, "usd_path"):
                original_path = target_obj.spawn.usd_path
                if original_path and original_path.startswith("None"):
                    new_path = original_path.replace("None", target_root)
                    target_obj.spawn.usd_path = new_path

        if hasattr(cfg.scene, "wrist_camera"):
            cfg.scene.wrist_camera = None

        self.env = ManagerBasedEnv(cfg)
        self.env.reset()


    def reset(self):
        self.step_count = 0
        obs, info = self.env.reset()
        return self._extract_obs(obs)


    def step(self, action):
            if not isinstance(action, torch.Tensor):
                action = torch.from_numpy(action).to(self.device)

            step_result = self.env.step(action)

            
            if len(step_result) == 5:
                obs, reward, terminated, truncated, info = step_result
                done = terminated | truncated
            elif len(step_result) == 2:
                obs, reward = step_result
                done = torch.zeros(self.n_envs, device=self.device, dtype=torch.bool)
                info = {}
            else:
                raise ValueError(f"Unexpected step result length: {len(step_result)}")


            if isinstance(reward, dict):
                reward_value = 0.0
                for v in reward.values():
                    if isinstance(v, torch.Tensor):
                        reward_value += v.mean().item()
                    elif isinstance(v, (int, float)):
                        reward_value += v
            else:
                reward_value = reward.mean().item() if isinstance(reward, torch.Tensor) else reward
            self.step_count += 1
            if self.step_count >= self.max_steps:
                if isinstance(done, torch.Tensor):
                    done = torch.ones_like(done)
                else:
                    done = True

            return self._extract_obs(obs), reward_value, done, info


    def _extract_obs(self, obs):
            if isinstance(obs, tuple): obs = obs[0]
            policy_obs = obs["policy"]

            obs_vec = np.concatenate([
                policy_obs["cube_orientations"][:].cpu().numpy(), 
                policy_obs["cube_positions"][:].cpu().numpy(),
                policy_obs["eef_pos"].cpu().numpy(),          
                policy_obs["eef_quat"].cpu().numpy(),          
                policy_obs["gripper_pos"].cpu().numpy(),       
                policy_obs["joint_pos"].cpu().numpy(),
                policy_obs["joint_vel"].cpu().numpy(),
            ], axis=-1)


            # print(f"[Check 3] Current Isaac Lab Raw Obs: {obs_vec[0, :48]}") # EEF pos 3개만


            return {"obs": obs_vec} 



    def run(self, policy: BaseLowdimPolicy):


        # if hasattr(policy, 'normalizer'):
        #     print("\n" + "="*60)
        #     print("[Check 1] Model's Normalization Stats (Offset & Scale)")
        #     obs_stats = policy.normalizer.params_dict['obs']
        #     offset = obs_stats['offset'].detach().cpu().numpy()
        #     scale = obs_stats['scale'].detach().cpu().numpy()
        #     print(f"  - Offset (Min): {offset[:48]}")
        #     print(f"  - Scale (Range): {scale[:48]}")
        #     print(f"  - Calculated Max: {offset[:48] + scale[:48]}")
        #     print(f"  - Total Observation Dimensions: {len(offset)}")
        #     print("="*60 + "\n")


        device = policy.device
        dtype = policy.dtype

        policy.reset()
        obs = self.reset()
        reward_sum = 0.0
        done = False
        obs_history = collections.deque(maxlen=self.n_obs_steps)

        for _ in range(self.n_obs_steps):
            obs_history.append(obs)

        step_idx = 0
        while step_idx < self.max_steps:
            np_obs = np.stack([o["obs"] for o in obs_history], axis=1)
            obs_dict = {
                "obs": torch.from_numpy(np_obs).to(device=device, dtype=dtype)
            }

            with torch.no_grad():
                action_dict = policy.predict_action(obs_dict)

            np_action_chunk = action_dict["action"].detach().cpu().numpy()

            for i in range(self.n_action_steps):
                if step_idx >= self.max_steps:
                    break
                
                current_action = np_action_chunk[:, i, :].astype(np.float32)

                obs, reward, done, info = self.step(current_action)

                reward_sum += reward
                obs_history.append(obs)
                step_idx += 1

                if isinstance(done, torch.Tensor):
                    if done.any(): break
                elif done: break
            
            if isinstance(done, torch.Tensor):
                if done.any(): break
            elif done: break

        return {
            "eval/episode_reward": reward_sum,
            "eval/episode_length": step_idx
        }






    # def run(self, policy: BaseLowdimPolicy):
    #         device = policy.device
    #         dtype = policy.dtype

    #         # 0. 정책 및 환경 초기화
    #         policy.reset()
    #         obs = self.reset()
    #         reward_sum = 0.0
    #         step_idx = 0

    #         # 초기 관측치 히스토리 설정
    #         obs_history = collections.deque(maxlen=self.n_obs_steps)
    #         for _ in range(self.n_obs_steps):
    #             obs_history.append(copy.deepcopy(obs))

    #         while step_idx < self.max_steps:
    #             # 1. Observation 준비 (B, T_obs, D_obs)
    #             np_obs = np.stack([o["obs"] for o in obs_history], axis=1)
                
    #             obs_dict_raw = {
    #                 "obs": torch.from_numpy(np_obs).to(device=device, dtype=dtype)
    #             }
                
    #             # policy에 포함된 normalizer를 사용하여 정규화 수행
    #             obs_dict = policy.normalizer.normalize(obs_dict_raw)

    #             # 2. Diffusion policy → action chunk 예측
    #             with torch.no_grad():
    #                 action_dict = policy.predict_action(obs_dict)

    #             # --- [AttributeError 방지 로직] ---
    #             # 모델 출력의 'action_pred'를 normalizer가 인식하는 'action'으로 변환
    #             if 'action_pred' in action_dict:
    #                 action_dict['action'] = action_dict.pop('action_pred')
                
    #             # Normalizer에 등록된 키('action')만 추출하여 역정규화 진행
    #             # 등록되지 않은 키가 섞여 들어오면 params_dict[key] 에러가 발생함
    #             clean_action_dict = {
    #                 k: v for k, v in action_dict.items() 
    #                 if k in policy.normalizer.params_dict
    #             }
                
    #             # 역정규화 실행
    #             unnormalized_dict = policy.normalizer.unnormalize(clean_action_dict)
    #             np_action_chunk = unnormalized_dict["action"].detach().cpu().numpy()
    #             # ----------------------------------

    #             # 3. Action Chunk 실행 루프 (T_action 단계만큼 실행)
    #             for i in range(self.n_action_steps):
    #                 if step_idx >= self.max_steps:
    #                     break
                    
    #                 # 현재 스텝의 액션 추출 (B, D_action)
    #                 current_action = np_action_chunk[:, i, :].astype(np.float32)

    #                 # Isaac IK-Rel 안정화를 위한 클리핑 (필요 시 조절)
    #                 # current_action = np.clip(current_action, -0.05, 0.05) 

    #                 # 환경 스텝 실행
    #                 obs, reward, done, info = self.step(current_action)

    #                 # 데이터 업데이트
    #                 reward_sum += reward
    #                 obs_history.append(copy.deepcopy(obs))
    #                 step_idx += 1

    #                 # 종료 조건 체크 (Vectorized Env 대응)
    #                 if isinstance(done, torch.Tensor):
    #                     if done.any():
    #                         break
    #                 elif done:
    #                     break

    #             # 루프 밖에서도 종료 여부 확인
    #             if isinstance(done, torch.Tensor):
    #                 if done.any(): break
    #             elif done: break

    #         return {
    #             "eval/episode_reward": reward_sum,
    #             "eval/episode_length": step_idx
    #         }



    