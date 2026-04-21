"""
Usage:
Training:
python train.py --config-name=train_diffusion_lowdim_workspace
"""

# import sys
# # use line-buffering for both stdout and stderr
# sys.stdout = open(sys.stdout.fileno(), mode='w', buffering=1)
# sys.stderr = open(sys.stderr.fileno(), mode='w', buffering=1)

# import hydra
# from omegaconf import OmegaConf
# import pathlib
# from diffusion_policy.workspace.base_workspace import BaseWorkspace

# from scripts.imitation_learning.diffusion_policy.diffusion_policy.env_runner.stack_robomimic_image_runner import *
# from scripts.imitation_learning.diffusion_policy.diffusion_policy.workspace.train_isaaclab_diffusion_unet_image_workspace import *
# from scripts.imitation_learning.diffusion_policy.diffusion_policy.dataset.stack_robomimic_replay_image_dataset import *
# from scripts.imitation_learning.diffusion_policy.diffusion_policy.common.replay_buffer_stack import *


# # allows arbitrary python code execution in configs using the ${eval:''} resolver
# OmegaConf.register_new_resolver("eval", eval, replace=True)

# @hydra.main(
#     version_base=None,
#     config_path=str(pathlib.Path(__file__).parent.joinpath(
#         'diffusion_policy','config'))
# )
# def main(cfg: OmegaConf):
#     # resolve immediately so all the ${now:} resolvers
#     # will use the same time.
#     OmegaConf.resolve(cfg)

#     # print(cfg)

#     cls = hydra.utils.get_class(cfg._target_)
#     workspace: BaseWorkspace = cls(cfg)
#     workspace.run()

# if __name__ == "__main__":
#     main()





















# import sys
# # use line-buffering for both stdout and stderr
# sys.stdout = open(sys.stdout.fileno(), mode='w', buffering=1)
# sys.stderr = open(sys.stderr.fileno(), mode='w', buffering=1)


# import sys
# import os


# os.environ["ISAAC_SIM_ENABLE_CAMERAS"] = "1"

# original_argv = list(sys.argv)

# sys.argv = [original_argv[0], "--enable_cameras"]

# from isaacsim import SimulationApp

# sim_app = SimulationApp({
#     "headless": False,
#     "render": True,
#     "enable_cameras": True,
# })

# sys.argv = original_argv
# if "--enable_cameras" in sys.argv:
#     sys.argv.remove("--enable_cameras")


# from omni.isaac.core.utils.viewports import set_camera_view
# import carb

# carb.settings.get_settings().set_bool("/app/renderer/enabled", True)
# carb.settings.get_settings().set_bool("/app/omni.graph.scriptnode/enabled", True)

# os.environ["ISAACLAB_VIEWER_ENABLED"] = "1"


# from scripts.imitation_learning.diffusion_policy.diffusion_policy.env_runner.stack_robomimic_image_runner import *
# from scripts.imitation_learning.diffusion_policy.diffusion_policy.workspace.train_isaaclab_diffusion_unet_image_workspace import *
# from scripts.imitation_learning.diffusion_policy.diffusion_policy.dataset.stack_robomimic_replay_image_dataset import *
# from scripts.imitation_learning.diffusion_policy.diffusion_policy.common.replay_buffer_stack import *



# import hydra
# from omegaconf import OmegaConf
# import pathlib
# from diffusion_policy.workspace.base_workspace import BaseWorkspace

# # from scripts.imitation_learning.diffusion_policy.diffusion_policy.workspace.train_isaaclab_diffusion_transformer_lowdim_workspace import *
# # from scripts.imitation_learning.diffusion_policy.diffusion_policy.env_runner.stack_lowdim_runner import *
# # from scripts.imitation_learning.diffusion_policy.diffusion_policy.dataset.stack_lowdim_dataset import *



# # allows arbitrary python code execution in configs using the ${eval:''} resolver
# OmegaConf.register_new_resolver("eval", eval, replace=True)

# @hydra.main(
#     version_base=None,
#     config_path=str(pathlib.Path(__file__).parent.joinpath(
#         'diffusion_policy','config'))
# )
# def main(cfg: OmegaConf):
#     # resolve immediately so all the ${now:} resolvers
#     # will use the same time.
#     OmegaConf.resolve(cfg)

#     # print(cfg)

#     cls = hydra.utils.get_class(cfg._target_)
#     workspace: BaseWorkspace = cls(cfg)
#     workspace.run()

# if __name__ == "__main__":
#     main()



























# import sys
# import os


# os.environ["ISAAC_SIM_ENABLE_CAMERAS"] = "1"
# os.environ["ISAACLAB_VIEWER_ENABLED"] = "1"

# from isaacsim import SimulationApp

# original_argv = list(sys.argv)
# sys.argv = [original_argv[0], "--enable_cameras"]
# print(original_argv)

# sim_app = SimulationApp({
#     "headless": False,
#     "render": True,
#     "enable_cameras": True, 
# })


# # sim_app = SimulationApp({
# #     "headless": False,
# #     "render": True,
# #     "enable_cameras": True, 
# # }, experience="") #


# from scripts.imitation_learning.diffusion_policy.diffusion_policy.env_runner.stack_robomimic_image_runner import *
# from scripts.imitation_learning.diffusion_policy.diffusion_policy.workspace.train_isaaclab_diffusion_unet_image_workspace import *
# from scripts.imitation_learning.diffusion_policy.diffusion_policy.dataset.stack_robomimic_replay_image_dataset import *
# from scripts.imitation_learning.diffusion_policy.diffusion_policy.common.replay_buffer_stack import *

# print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

# import hydra
# from omegaconf import OmegaConf
# import pathlib


# from diffusion_policy.workspace.base_workspace import BaseWorkspace


# sys.argv = original_argv
# if "--enable_cameras" in sys.argv:
#     sys.argv.remove("--enable_cameras")


# @hydra.main(
#     version_base=None,
#     config_path=str(pathlib.Path(__file__).parent.joinpath('diffusion_policy','config'))
# )
# def main(cfg: OmegaConf):
#     # resolve immediately so all the ${now:} resolvers
#     # will use the same time.
#     OmegaConf.resolve(cfg)
#     cls = hydra.utils.get_class(cfg._target_)



#     if "--enable_cameras" not in sys.argv:
#         sys.argv.append("--enable_cameras")

#     import carb
#     settings = carb.settings.get_settings()
#     settings.set("/app/renderer/enabled", True)
#     settings.set("/app/omni.graph.scriptnode/enabled", True)

#     workspace: BaseWorkspace = cls(cfg)
#     print("/////////////////////////////////")
#     workspace.run()

# if __name__ == "__main__":
#     main()

















import sys
import os


os.environ["ISAAC_SIM_ENABLE_CAMERAS"] = "1"
os.environ["ISAACLAB_VIEWER_ENABLED"] = "1"

from isaaclab.app import AppLauncher

original_argv = list(sys.argv)
sys.argv = [original_argv[0], "--enable_cameras"]
print(original_argv)

# sim_app = SimulationApp({
#     "headless": False,
#     "render": True,
#     "enable_cameras": True, 
# })

app_launcher = AppLauncher({
    "headless": False,
    "render": True,
    "enable_cameras": True, 
    "store_true": True,
    "device": "cuda",
    # "save": True,
})
simulation_app = app_launcher.app


# sim_app = SimulationApp({
#     "headless": False,
#     "render": True,
#     "enable_cameras": True, 
# }, experience="") #


from scripts.imitation_learning.diffusion_policy.diffusion_policy.env_runner.stack_robomimic_image_runner import *
from scripts.imitation_learning.diffusion_policy.diffusion_policy.workspace.train_isaaclab_diffusion_unet_image_workspace import *
from scripts.imitation_learning.diffusion_policy.diffusion_policy.dataset.stack_robomimic_replay_image_dataset import *
from scripts.imitation_learning.diffusion_policy.diffusion_policy.common.replay_buffer_stack import *


import hydra
from omegaconf import OmegaConf
import pathlib


from diffusion_policy.workspace.base_workspace import BaseWorkspace


sys.argv = original_argv
if "--enable_cameras" in sys.argv:
    sys.argv.remove("--enable_cameras")


@hydra.main(
    version_base=None,
    config_path=str(pathlib.Path(__file__).parent.joinpath('diffusion_policy','config'))
)
def main(cfg: OmegaConf):
    # resolve immediately so all the ${now:} resolvers
    # will use the same time.
    OmegaConf.resolve(cfg)
    cls = hydra.utils.get_class(cfg._target_)



    if "--enable_cameras" not in sys.argv:
        sys.argv.append("--enable_cameras")

    import carb
    settings = carb.settings.get_settings()
    settings.set("/app/renderer/enabled", True)
    settings.set("/app/omni.graph.scriptnode/enabled", True)

    workspace: BaseWorkspace = cls(cfg)
    workspace.run()

if __name__ == "__main__":
    main()