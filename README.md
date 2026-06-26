![Isaac Lab](docs/source/_static/isaaclab.jpg)

---

# Isaac Lab

[![IsaacSim](https://img.shields.io/badge/IsaacSim-5.1.0-silver.svg)](https://docs.isaacsim.omniverse.nvidia.com/latest/index.html)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://docs.python.org/3/whatsnew/3.11.html)
[![Linux platform](https://img.shields.io/badge/platform-linux--64-orange.svg)](https://releases.ubuntu.com/22.04/)
[![Windows platform](https://img.shields.io/badge/platform-windows--64-orange.svg)](https://www.microsoft.com/en-us/)
[![pre-commit](https://img.shields.io/github/actions/workflow/status/isaac-sim/IsaacLab/pre-commit.yaml?logo=pre-commit&logoColor=white&label=pre-commit&color=brightgreen)](https://github.com/isaac-sim/IsaacLab/actions/workflows/pre-commit.yaml)
[![docs status](https://img.shields.io/github/actions/workflow/status/isaac-sim/IsaacLab/docs.yaml?label=docs&color=brightgreen)](https://github.com/isaac-sim/IsaacLab/actions/workflows/docs.yaml)
[![License](https://img.shields.io/badge/license-BSD--3-yellow.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![License](https://img.shields.io/badge/license-Apache--2.0-yellow.svg)](https://opensource.org/license/apache-2-0)


**Isaac Lab** is a GPU-accelerated, open-source framework designed to unify and simplify robotics research workflows,
such as reinforcement learning, imitation learning, and motion planning. Built on [NVIDIA Isaac Sim](https://docs.isaacsim.omniverse.nvidia.com/latest/index.html),
it combines fast and accurate physics and sensor simulation, making it an ideal choice for sim-to-real
transfer in robotics.

Isaac Lab provides developers with a range of essential features for accurate sensor simulation, such as RTX-based
cameras, LIDAR, or contact sensors. The framework's GPU acceleration enables users to run complex simulations and
computations faster, which is key for iterative processes like reinforcement learning and data-intensive tasks.
Moreover, Isaac Lab can run locally or be distributed across the cloud, offering flexibility for large-scale deployments.

A detailed description of Isaac Lab can be found in our [arXiv paper](https://arxiv.org/abs/2511.04831).

## 내가 작업한 내용과 복원 방법

이 저장소는 공식 Isaac Lab(`https://github.com/isaac-sim/IsaacLab`)에서 시작했지만, 아래 로컬 작업들이 추가된 버전이다.
공식 upstream 비교 기준은 `upstream/main`의 `b4c32102`이고, 로컬 작업 시작 기준은 `50fc46e8`이다.

현재 로컬 작업은 다음 주요 커밋들에 들어 있다. README를 추가로 수정하면 더 최신 커밋이 앞에 생길 수 있으므로,
최종 확인은 `git log --oneline -5`로 한다.

- `1ddf9408 Add restore cautions to README`
- `946ee54e Add Korean local restore guide`
- `5b782dc8 Document local work and restore steps`
- `94611409 Track DexGarmentLab files directly`
- `65fa4a4f Document local IsaacLab customizations`

### 주요 작업 내용

- `scripts/DexGarmentLab/`를 submodule 포인터가 아니라 이 저장소의 일반 파일로 직접 추적하도록 변경했다.
- DexGarmentLab의 대형 asset, data, zip, checkpoint 파일은 git에 넣지 않고 `.gitignore`로 제외했다.
- `piper_isaac_sim/`에 Piper robot description, mesh, URDF/Xacro, RealSense 관련 파일을 추가했다.
- Piper용 stack/square manipulation task config와 robomimic config를 추가했다.
- DP3 imitation learning 쪽에 stack dataset, point cloud 기반 evaluation, saliency video 저장 로직을 추가했다.
- DP3 설정은 `dataset15.hdf5`, single rollout evaluation, last checkpoint 저장 비활성화 쪽으로 수정했다.
- LeHome challenge evaluation에 W&B logging, GPU dynamics 설정, garment path 수정, garment object validation 로직을 추가했다.
- Docker 설정은 로컬 이미지 `isaac-lab-base-es:latest`를 쓰고 GPU `0`만 사용하도록 바꿨다.
- Franka stack visuomotor camera 위치를 `pos=(1.3, 0.3, 0.4)`로 수정했다.

### DexGarmentLab에서 git에 넣지 않은 것

다음 파일/폴더는 용량이 크거나 재생성/재다운로드 대상이라 git에서 제외했다.

- `scripts/DexGarmentLab/Assets/Garment`
- `scripts/DexGarmentLab/Assets/LeapMotion`
- `scripts/DexGarmentLab/Assets/Robots`
- `scripts/DexGarmentLab/Assets/Scene`
- `scripts/DexGarmentLab/Assets/Human`
- `scripts/DexGarmentLab/Data/*` 단, `Data/*.py`는 포함
- `scripts/DexGarmentLab/Tool_Scripts`
- `scripts/DexGarmentLab/Texture_Generate.sh`
- `scripts/DexGarmentLab/pipeline.sh`
- `scripts/DexGarmentLab/*.py`
- `scripts/DexGarmentLab/tmp*`
- `scripts/DexGarmentLab/**/__pycache__/`
- `*.zip`
- `*.pth`

### 나중에 복원하는 방법

1. 저장소를 clone한다.

   ```bash
   git clone https://github.com/eimyssong/intern.git IsaacLab
   cd IsaacLab
   git checkout main
   ```

   만약 `intern.git` 대신 기존 `isaacsim.git`에 올렸다면 아래 주소를 사용한다.

   ```bash
   git clone https://github.com/eimyssong/isaacsim.git IsaacLab
   cd IsaacLab
   git checkout main
   ```

2. 로컬 작업 커밋이 있는지 확인한다.

   ```bash
   git log --oneline -5
   ```

   최소한 아래 주요 커밋들이 보여야 한다. README를 나중에 다시 수정했다면 더 최신 커밋이 위에 추가로 있을 수 있다.

   ```text
   1ddf9408 Add restore cautions to README
   946ee54e Add Korean local restore guide
   5b782dc8 Document local work and restore steps
   94611409 Track DexGarmentLab files directly
   65fa4a4f Document local IsaacLab customizations
   ```

3. DexGarmentLab 대형 asset과 dataset을 다시 받는다.

   ```bash
   cd scripts/DexGarmentLab
   python Assets/assets_download.py
   python Data/data_download.py
   ```

   이 스크립트는 Hugging Face의 `wayrise/DexGarmentLab` dataset에서 zip 파일을 받는다. 자동으로 압축이 풀리지 않으면,
   받은 zip 파일들을 `scripts/DexGarmentLab` 구조에 맞게 직접 압축 해제한다.

4. Docker를 쓸 경우 로컬 이미지가 필요하다.

   ```text
   isaac-lab-base-es:latest
   ```

   이 이미지가 없으면 Docker build가 실패할 수 있다. 그 경우 이미지를 다시 만들거나,
   `docker/Dockerfile.base`를 공식 Isaac Sim base image를 쓰는 형태로 되돌린다.

5. GPU 설정을 확인한다.

   `docker/docker-compose.yaml`은 GPU `0`만 쓰도록 설정되어 있다. 다른 GPU를 쓰려면 `NVIDIA_VISIBLE_DEVICES`와
   `device_ids` 값을 수정한다.

6. 필요한 Python dependency를 다시 설치한다.

   - Isaac Lab dependency는 공식 Isaac Lab 설치 방법을 따른다.
   - DexGarmentLab dependency는 `scripts/DexGarmentLab/requirements.txt`를 사용한다.
   - LeHome evaluation은 W&B를 사용하므로, 로그인하거나 offline/disabled mode로 실행한다.

### 전체 복원 주의점

- GitHub에 올린 저장소와 로컬 저장소가 같은지 먼저 확인한다. 이 작업을 `intern.git`에 올릴 계획이면 remote는
  `https://github.com/eimyssong/intern.git`이어야 한다.

  ```bash
  git remote -v
  git branch --show-current
  git status
  ```

- 이 README에 적힌 최신 복원 정보까지 포함하려면 최소 `1ddf9408 Add restore cautions to README`까지, 그리고 그 이후
  README를 추가로 수정한 최신 커밋까지 push되어야 한다. GitHub에서 README가 예전 내용으로 보이면 아직 push가 안 된 것이다.

- `scripts/DexGarmentLab/`는 더 이상 submodule이 아니다. 따라서 복원 후 `git submodule update --init --recursive`로
  DexGarmentLab가 복구되는 구조가 아니다. DexGarmentLab 코드는 이 저장소에 일반 파일로 들어 있고, 제외된 asset/data만
  별도로 다운로드해야 한다.

- DexGarmentLab 원본 내부 `.git` 디렉터리는 커밋 전에 제거했다. 기존 내부 git 메타데이터는 작업 당시
  `/tmp/DexGarmentLab.git.backup`에 임시 백업했지만, `/tmp`는 재부팅이나 정리 작업으로 사라질 수 있다. 복원은 이 백업에
  의존하지 말고 현재 저장소의 일반 파일과 다운로드 스크립트를 기준으로 한다.

- `*.zip`, `*.pth`, DexGarmentLab의 주요 asset/data 폴더는 git에 없다. 새 장비에서 clone만 하면 모델 checkpoint,
  garment asset, human/robot/scene asset, dataset zip은 없는 상태가 정상이다. 필요한 경우 Hugging Face download script나
  별도 실험 저장소에서 다시 받아야 한다.

- DP3 `.zarr` 데이터와 LeHome failure video 일부는 커밋에 포함되어 있지만, 모든 실험 산출물이 들어간 것은 아니다. 학습을
  재현하려면 사용한 원본 HDF5, checkpoint, W&B run, 로컬 output 폴더를 별도로 확인해야 한다.

- Docker 설정은 일반 Isaac Lab 기본값이 아니라 로컬 환경에 맞춰 바뀌어 있다. 특히 `isaac-lab-base-es:latest` 이미지와
  GPU `0` 고정 설정이 맞지 않으면 Docker 실행이 실패한다.

- GitHub push 권한은 계정 인증에 따라 달라진다. `Permission denied to siwon7` 같은 메시지가 나오면 현재 GitHub 인증 계정이
  `eimyssong`이 아닌 것이다. `gh auth status`로 계정을 확인하고, 필요한 경우 `gh auth logout -h github.com` 후
  `gh auth login -h github.com`으로 다시 로그인한다.

- 복원 후 정상 여부는 아래 명령으로 먼저 확인한다.

  ```bash
  git status
  git log --oneline -5
  test -d scripts/DexGarmentLab
  test -f scripts/DexGarmentLab/README.md
  ```

## Local Project Notes

This checkout is based on the official Isaac Lab repository
[`isaac-sim/IsaacLab`](https://github.com/isaac-sim/IsaacLab), but includes local project work that is not part of
the official upstream. The comparison was checked against official `upstream/main` commit `b4c32102` and local
base commit `50fc46e8`.

The main local work is recorded in these commits. If this README is edited again, newer README-only commits may appear
above them; use `git log --oneline -5` to confirm the current tip.

- `1ddf9408 Add restore cautions to README`
- `946ee54e Add Korean local restore guide`
- `5b782dc8 Document local work and restore steps`
- `94611409 Track DexGarmentLab files directly`
- `65fa4a4f Document local IsaacLab customizations`

### What was changed

#### Added project areas

- `piper_isaac_sim/`: Piper robot descriptions, meshes, URDF/Xacro files, RealSense assets, launch files, and usage
  notes for Isaac Sim integration.
- `source/isaaclab_tasks/isaaclab_tasks/manager_based/manipulation/stack/config/piper/`: Piper-specific stack task
  configs, robomimic policy configs, and instance-randomization variants.
- `source/isaaclab_tasks/isaaclab_tasks/manager_based/manipulation/square/`: Piper square manipulation task,
  observations, terminations, events, robomimic configs, and randomized variants.
- `scripts/DexGarmentLab/`: DexGarmentLab code is tracked directly in this repository, not as a submodule. Large
  asset, dataset, archive, and checkpoint files are intentionally ignored.
- `scripts/lehome_challenge/`: LeHome garment challenge assets, task code, evaluation scripts, object configs, and
  failure-case videos.
- `scripts/imitation_learning/datasets/DP3/`: Local DP3 stack datasets in Zarr format, including point clouds,
  actions, agent poses, generated dataset variants, and evaluation outputs.

#### Main implementation changes

- Docker setup is pinned to a local base image (`isaac-lab-base-es:latest`) and restricted to GPU `0`; DexGarmentLab
  data, assets, and checkpoint folders are excluded from Docker build context.
- DP3 evaluation was extended with RGB plus point-cloud saliency rendering, SmoothGrad-style point-cloud saliency, and
  video export for inspection.
- DP3 conversion and training config were adjusted for `dataset15.hdf5`, single-rollout evaluation, and no last
  checkpoint saving.
- LeHome evaluation now initializes Weights & Biases logging, logs per-episode and per-garment metrics, enables GPU
  dynamics, and records final aggregate metrics.
- LeHome garment loading paths were adapted to `/scripts/lehome_challenge/...`, garment texture paths were made
  absolute for that layout, and garment creation was simplified with validation after object construction.
- Franka stack visuomotor camera placement was changed from the prior `dataset14` height setting to
  `pos=(1.3, 0.3, 0.4)`.
- Local generated artifacts include updated DP3 `.zarr` datasets, deletion of old blockpush/stack evaluation outputs,
  and new LeHome failure videos under `scripts/lehome_challenge/video/failure/`.

#### DexGarmentLab direct tracking policy

`scripts/DexGarmentLab` was converted from a gitlink/submodule-style entry into normal tracked files in this repo.
The following are excluded by `scripts/DexGarmentLab/.gitignore` and must be restored separately if needed:

- `Assets/Garment`
- `Assets/LeapMotion`
- `Assets/Robots`
- `Assets/Scene`
- `Assets/Human`
- `Data/*`, except `Data/*.py`
- `Tool_Scripts`
- `Texture_Generate.sh`
- `pipeline.sh`
- root-level `/*.py`
- `tmp*`
- `**/__pycache__/`
- `*.zip`
- `*.pth`

Tracked DexGarmentLab content includes source code, configs, model definitions, download helper scripts, selected
material assets, repository images, and small point-cloud/example files.

### How to restore this workspace later

1. Clone the project repository and check out the local branch:

   ```bash
   git clone https://github.com/eimyssong/isaacsim.git IsaacLab
   cd IsaacLab
   git checkout main
   git log --oneline -3
   ```

   The expected key local commits are `1ddf9408`, `946ee54e`, `5b782dc8`, `94611409`, and `65fa4a4f`
   on top of `50fc46e8`. Newer README-only commits may appear above them if this file is updated again.

2. If you start from the official Isaac Lab repository instead, add this project repository as a remote and check out
   the local branch:

   ```bash
   git remote add project https://github.com/eimyssong/isaacsim.git
   git fetch project
   git checkout -b project-main project/main
   ```

3. Restore DexGarmentLab large assets and datasets. These are not stored in git. From the repository root:

   ```bash
   cd scripts/DexGarmentLab
   python Assets/assets_download.py
   python Data/data_download.py
   ```

   The download scripts fetch zip archives from the `wayrise/DexGarmentLab` Hugging Face dataset. After download,
   unzip the archives into the same `scripts/DexGarmentLab` layout if they are not extracted automatically.

4. Restore DP3 and LeHome local datasets or outputs if they are missing. Some generated `.zarr`, evaluation video, and
   failure-video artifacts are committed, but very large local-only experiment outputs should be restored from the
   experiment storage used when they were generated.

5. Restore the local Docker/runtime assumptions:

   - `docker/Dockerfile.base` expects a local image named `isaac-lab-base-es:latest`.
   - `docker/docker-compose.yaml` is configured to use GPU `0`.
   - If that local image does not exist, rebuild it or change the Dockerfile back to the official Isaac Sim base image
     arguments before running Docker.

6. Reinstall dependencies as needed for each workflow:

   - Isaac Lab dependencies follow the official installation instructions below.
   - DexGarmentLab Python requirements are listed in `scripts/DexGarmentLab/requirements.txt`.
   - LeHome evaluation uses Weights & Biases logging, so configure W&B or run it in offline/disabled mode as needed.

## Key Features

Isaac Lab offers a comprehensive set of tools and environments designed to facilitate robot learning:

- **Robots**: A diverse collection of robots, from manipulators, quadrupeds, to humanoids, with more than 16 commonly available models.
- **Environments**: Ready-to-train implementations of more than 30 environments, which can be trained with popular reinforcement learning frameworks such as RSL RL, SKRL, RL Games, or Stable Baselines. We also support multi-agent reinforcement learning.
- **Physics**: Rigid bodies, articulated systems, deformable objects
- **Sensors**: RGB/depth/segmentation cameras, camera annotations, IMU, contact sensors, ray casters.


## Getting Started

### Documentation

Our [documentation page](https://isaac-sim.github.io/IsaacLab) provides everything you need to get started, including
detailed tutorials and step-by-step guides. Follow these links to learn more about:

- [Installation steps](https://isaac-sim.github.io/IsaacLab/main/source/setup/installation/index.html#local-installation)
- [Reinforcement learning](https://isaac-sim.github.io/IsaacLab/main/source/overview/reinforcement-learning/rl_existing_scripts.html)
- [Tutorials](https://isaac-sim.github.io/IsaacLab/main/source/tutorials/index.html)
- [Available environments](https://isaac-sim.github.io/IsaacLab/main/source/overview/environments.html)


## Isaac Sim Version Dependency

Isaac Lab is built on top of Isaac Sim and requires specific versions of Isaac Sim that are compatible with each
release of Isaac Lab. Below, we outline the recent Isaac Lab releases and GitHub branches and their corresponding
dependency versions for Isaac Sim.

| Isaac Lab Version             | Isaac Sim Version         |
| ----------------------------- | ------------------------- |
| `main` branch                 | Isaac Sim 4.5 / 5.0 / 5.1 |
| `v2.3.X`                      | Isaac Sim 4.5 / 5.0 / 5.1 |
| `v2.2.X`                      | Isaac Sim 4.5 / 5.0       |
| `v2.1.X`                      | Isaac Sim 4.5             |
| `v2.0.X`                      | Isaac Sim 4.5             |


## Contributing to Isaac Lab

We wholeheartedly welcome contributions from the community to make this framework mature and useful for everyone.
These may happen as bug reports, feature requests, or code contributions. For details, please check our
[contribution guidelines](https://isaac-sim.github.io/IsaacLab/main/source/refs/contributing.html).

## Show & Tell: Share Your Inspiration

We encourage you to utilize our [Show & Tell](https://github.com/isaac-sim/IsaacLab/discussions/categories/show-and-tell)
area in the `Discussions` section of this repository. This space is designed for you to:

* Share the tutorials you've created
* Showcase your learning content
* Present exciting projects you've developed

By sharing your work, you'll inspire others and contribute to the collective knowledge
of our community. Your contributions can spark new ideas and collaborations, fostering
innovation in robotics and simulation.

## Troubleshooting

Please see the [troubleshooting](https://isaac-sim.github.io/IsaacLab/main/source/refs/troubleshooting.html) section for
common fixes or [submit an issue](https://github.com/isaac-sim/IsaacLab/issues).

For issues related to Isaac Sim, we recommend checking its [documentation](https://docs.isaacsim.omniverse.nvidia.com/latest/index.html)
or opening a question on its [forums](https://forums.developer.nvidia.com/c/agx-autonomous-machines/isaac/67).

## Support

* Please use GitHub [Discussions](https://github.com/isaac-sim/IsaacLab/discussions) for discussing ideas,
  asking questions, and requests for new features.
* Github [Issues](https://github.com/isaac-sim/IsaacLab/issues) should only be used to track executable pieces of
  work with a definite scope and a clear deliverable. These can be fixing bugs, documentation issues, new features,
  or general updates.

## Connect with the NVIDIA Omniverse Community

Do you have a project or resource you'd like to share more widely? We'd love to hear from you!
Reach out to the NVIDIA Omniverse Community team at OmniverseCommunity@nvidia.com to explore opportunities
to spotlight your work.

You can also join the conversation on the [Omniverse Discord](https://discord.com/invite/nvidiaomniverse) to
connect with other developers, share your projects, and help grow a vibrant, collaborative ecosystem
where creativity and technology intersect. Your contributions can make a meaningful impact on the Isaac Lab
community and beyond!

## License

The Isaac Lab framework is released under [BSD-3 License](LICENSE). The `isaaclab_mimic` extension and its
corresponding standalone scripts are released under [Apache 2.0](LICENSE-mimic). The license files of its
dependencies and assets are present in the [`docs/licenses`](docs/licenses) directory.

Note that Isaac Lab requires Isaac Sim, which includes components under proprietary licensing terms. Please see the [Isaac Sim license](docs/licenses/dependencies/isaacsim-license.txt) for information on Isaac Sim licensing.

Note that the `isaaclab_mimic` extension requires cuRobo, which has proprietary licensing terms that can be found in [`docs/licenses/dependencies/cuRobo-license.txt`](docs/licenses/dependencies/cuRobo-license.txt).


## Citation

If you use Isaac Lab in your research, please cite the technical report:

```
@article{mittal2025isaaclab,
  title={Isaac Lab: A GPU-Accelerated Simulation Framework for Multi-Modal Robot Learning},
  author={Mayank Mittal and Pascal Roth and James Tigue and Antoine Richard and Octi Zhang and Peter Du and Antonio Serrano-Muñoz and Xinjie Yao and René Zurbrügg and Nikita Rudin and Lukasz Wawrzyniak and Milad Rakhsha and Alain Denzler and Eric Heiden and Ales Borovicka and Ossama Ahmed and Iretiayo Akinola and Abrar Anwar and Mark T. Carlson and Ji Yuan Feng and Animesh Garg and Renato Gasoto and Lionel Gulich and Yijie Guo and M. Gussert and Alex Hansen and Mihir Kulkarni and Chenran Li and Wei Liu and Viktor Makoviychuk and Grzegorz Malczyk and Hammad Mazhar and Masoud Moghani and Adithyavairavan Murali and Michael Noseworthy and Alexander Poddubny and Nathan Ratliff and Welf Rehberg and Clemens Schwarke and Ritvik Singh and James Latham Smith and Bingjie Tang and Ruchik Thaker and Matthew Trepte and Karl Van Wyk and Fangzhou Yu and Alex Millane and Vikram Ramasamy and Remo Steiner and Sangeeta Subramanian and Clemens Volk and CY Chen and Neel Jawale and Ashwin Varghese Kuruttukulam and Michael A. Lin and Ajay Mandlekar and Karsten Patzwaldt and John Welsh and Huihua Zhao and Fatima Anes and Jean-Francois Lafleche and Nicolas Moënne-Loccoz and Soowan Park and Rob Stepinski and Dirk Van Gelder and Chris Amevor and Jan Carius and Jumyung Chang and Anka He Chen and Pablo de Heras Ciechomski and Gilles Daviet and Mohammad Mohajerani and Julia von Muralt and Viktor Reutskyy and Michael Sauter and Simon Schirm and Eric L. Shi and Pierre Terdiman and Kenny Vilella and Tobias Widmer and Gordon Yeoman and Tiffany Chen and Sergey Grizan and Cathy Li and Lotus Li and Connor Smith and Rafael Wiltz and Kostas Alexis and Yan Chang and David Chu and Linxi "Jim" Fan and Farbod Farshidian and Ankur Handa and Spencer Huang and Marco Hutter and Yashraj Narang and Soha Pouya and Shiwei Sheng and Yuke Zhu and Miles Macklin and Adam Moravanszky and Philipp Reist and Yunrong Guo and David Hoeller and Gavriel State},
  journal={arXiv preprint arXiv:2511.04831},
  year={2025},
  url={https://arxiv.org/abs/2511.04831}
}
```

## Acknowledgement

Isaac Lab development initiated from the [Orbit](https://isaac-orbit.github.io/) framework.
We gratefully acknowledge the authors of Orbit for their foundational contributions.
