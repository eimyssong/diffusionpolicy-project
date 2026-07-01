# """
# Usage:
# python eval.py --checkpoint data/image/pusht/diffusion_policy_cnn/train_0/checkpoints/latest.ckpt -o data/pusht_eval_output
# """

# import sys
# # use line-buffering for both stdout and stderr
# sys.stdout = open(sys.stdout.fileno(), mode='w', buffering=1)
# sys.stderr = open(sys.stderr.fileno(), mode='w', buffering=1)

# import os
# import pathlib
# import click
# import hydra
# import torch
# import dill
# import wandb
# import json
# from diffusion_policy.workspace.base_workspace import BaseWorkspace

# @click.command()
# @click.option('-c', '--checkpoint', required=True)
# @click.option('-o', '--output_dir', required=True)
# @click.option('-d', '--device', default='cuda:0')
# def main(checkpoint, output_dir, device):
#     if os.path.exists(output_dir):
#         click.confirm(f"Output path {output_dir} already exists! Overwrite?", abort=True)
#     pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
    
#     # load checkpoint
#     payload = torch.load(open(checkpoint, 'rb'), pickle_module=dill)
#     cfg = payload['cfg']
#     cls = hydra.utils.get_class(cfg._target_)
#     workspace = cls(cfg, output_dir=output_dir)
#     workspace: BaseWorkspace
#     workspace.load_payload(payload, exclude_keys=None, include_keys=None)
    
#     # get policy from workspace
#     policy = workspace.model
#     if cfg.training.use_ema:
#         policy = workspace.ema_model
    
#     device = torch.device(device)
#     policy.to(device)
#     policy.eval()
    
#     # run eval
#     env_runner = hydra.utils.instantiate(
#         cfg.task.env_runner,
#         output_dir=output_dir)
#     runner_log = env_runner.run(policy)
    
#     # dump log to json
#     json_log = dict()
#     for key, value in runner_log.items():
#         if isinstance(value, wandb.sdk.data_types.video.Video):
#             json_log[key] = value._path
#         else:
#             json_log[key] = value
#     out_path = os.path.join(output_dir, 'eval_log.json')
#     json.dump(json_log, open(out_path, 'w'), indent=2, sort_keys=True)

# if __name__ == '__main__':
#     main()












import sys
import os
import pathlib
import torch
import dill
import json
import click
import numpy as np

from isaaclab.app import AppLauncher

@click.command()
@click.option('-c', '--checkpoint', required=True, help='학습된 체크포인트(.ckpt) 경로')
@click.option('-o', '--output_dir', required=True, help='결과 저장 폴더')
@click.option('-d', '--device', default='cuda:0', help='사용할 장치 (cuda:0, cpu 등)')
@click.option('-n', '--num_rollouts', default=10, type=int, help='평가 반복 횟수')
@click.option('--headless/--no-headless', default=False, help='화면 출력 여부 (기본값: 화면 보임)')
def main(checkpoint, output_dir, device, num_rollouts, headless):
    app_launcher = AppLauncher({
        "headless": headless,
        "render": True,
        "enable_cameras": True,
        "device": device.split(':')[0] if ':' in device else device,
    })
    simulation_app = app_launcher.app

    import carb
    import hydra
    from diffusion_policy.workspace.base_workspace import BaseWorkspace

    if os.path.exists(output_dir):
        click.confirm(f"Output path {output_dir} already exists! Overwrite?", abort=True)
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    settings = carb.settings.get_settings()
    settings.set("/app/sensors/cameras/enabled", True)
    settings.set("/app/renderer/enabled", True)

    print(f"Loading checkpoint from: {checkpoint}")
    payload = torch.load(open(checkpoint, 'rb'), pickle_module=dill)
    
    for sd_type in ['model', 'ema_model']:
        if sd_type in payload['state_dicts']:
            new_sd = {k.replace('module.', ''): v for k, v in payload['state_dicts'][sd_type].items()}
            payload['state_dicts'][sd_type] = new_sd

    cfg = payload['cfg']
    cls = hydra.utils.get_class(cfg._target_)
    workspace = cls(cfg, output_dir=output_dir)
    workspace.load_payload(payload)
    
    policy = workspace.model
    if cfg.training.use_ema:
        policy = workspace.ema_model
    
    device = torch.device(device)
    policy.to(device)
    policy.eval()
    
    print(f"Instantiating Env Runner...")
    env_runner = hydra.utils.instantiate(cfg.task.env_runner, output_dir=output_dir)
    
    all_results = []
    successes = 0

    print(f"Starting {num_rollouts} manual rollouts...")
    for i in range(num_rollouts):
        with torch.no_grad():
            runner_log = env_runner.run(policy)
            
            is_success = runner_log.get('test/success_rate', 0.0) 
            if is_success > 0:
                successes += 1
                
            all_results.append(runner_log)
            print(f"Rollout [{i+1}/{num_rollouts}] - Success: {is_success}")

    final_success_rate = successes / num_rollouts
    print(f"\n" + "="*30)
    print(f"Evaluation complete.")
    print(f"Final Success Rate: {final_success_rate:.2%}")
    print("="*30)

    summary = {
        "num_rollouts": num_rollouts,
        "success_rate": final_success_rate,
        "raw_logs": []
    }

    for log in all_results:
        clean_log = {}
        for k, v in log.items():
            if isinstance(v, (float, int, str, list, dict)):
                clean_log[k] = v
            elif isinstance(v, np.ndarray):
                clean_log[k] = v.tolist()
        summary["raw_logs"].append(clean_log)

    out_path = os.path.join(output_dir, 'eval_summary.json')
    with open(out_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    simulation_app.close()

if __name__ == '__main__':
    main()