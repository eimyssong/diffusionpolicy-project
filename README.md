![Isaac Lab](docs/source/_static/isaaclab.jpg)

---

# Isaac Lab

[![IsaacSim](https://img.shields.io/badge/IsaacSim-5.1.0-silver.svg)](https://docs.isaacsim.omniverse.nvidia.com/latest/index.html)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://docs.python.org/3/whatsnew/3.11.html)
[![Linux 플랫폼](https://img.shields.io/badge/platform-linux--64-orange.svg)](https://releases.ubuntu.com/22.04/)
[![Windows 플랫폼](https://img.shields.io/badge/platform-windows--64-orange.svg)](https://www.microsoft.com/en-us/)
[![pre-commit](https://img.shields.io/github/actions/workflow/status/isaac-sim/IsaacLab/pre-commit.yaml?logo=pre-commit&logoColor=white&label=pre-commit&color=brightgreen)](https://github.com/isaac-sim/IsaacLab/actions/workflows/pre-commit.yaml)
[![문서 상태](https://img.shields.io/github/actions/workflow/status/isaac-sim/IsaacLab/docs.yaml?label=docs&color=brightgreen)](https://github.com/isaac-sim/IsaacLab/actions/workflows/docs.yaml)
[![라이선스](https://img.shields.io/badge/license-BSD--3-yellow.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![라이선스](https://img.shields.io/badge/license-Apache--2.0-yellow.svg)](https://opensource.org/license/apache-2-0)

**Isaac Lab**은 강화학습, 모방학습, 모션 플래닝 같은 로봇 연구 워크플로를 하나로 묶고 단순화하기 위한 GPU 가속 오픈소스 프레임워크다.
[NVIDIA Isaac Sim](https://docs.isaacsim.omniverse.nvidia.com/latest/index.html) 위에서 동작하며, 정확한 물리 시뮬레이션과 센서 시뮬레이션을 제공해 sim-to-real 연구에 적합하다.

Isaac Lab은 RTX 기반 카메라, LiDAR, 접촉 센서 등 로봇 학습에 필요한 센서 기능을 제공한다. GPU 가속을 통해 복잡한 시뮬레이션과 데이터 중심 작업을 빠르게 반복할 수 있고, 로컬 환경뿐 아니라 클라우드 분산 환경에서도 사용할 수 있다.

Isaac Lab에 대한 자세한 설명은 [arXiv 논문](https://arxiv.org/abs/2511.04831)을 참고한다.

## 내가 작업한 내용과 복원 방법

이 저장소는 공식 Isaac Lab(`https://github.com/isaac-sim/IsaacLab`)에서 시작했지만, 로컬 연구와 실험을 위해 여러 작업이 추가된 버전이다. 공식 upstream 비교 기준은 `upstream/main`의 `b4c32102`이고, 로컬 작업 시작 기준은 `50fc46e8`이다.

현재 로컬 작업은 아래 주요 커밋들에 들어 있다. README를 추가로 수정하면 더 최신 커밋이 앞에 생길 수 있으므로, 최종 확인은 `git log --oneline -10`으로 한다.

- `838baa0a Translate README to Korean`
- `37fe9b86 Update README commit references`
- `1ddf9408 Add restore cautions to README`
- `946ee54e Add Korean local restore guide`
- `5b782dc8 Document local work and restore steps`
- `94611409 Track DexGarmentLab files directly`
- `65fa4a4f Document local IsaacLab customizations`

### 주요 작업 내용

- `scripts/DexGarmentLab/`를 submodule 포인터가 아니라 이 저장소의 일반 파일로 직접 추적하도록 변경했다.
- DexGarmentLab의 대형 asset, data, zip, checkpoint 파일은 git에 넣지 않고 `.gitignore`로 제외했다.
- `piper_isaac_sim/`에 Piper 로봇 설명 파일, 메시, URDF/Xacro, RealSense 관련 파일을 추가했다.
- Piper용 stack/square 조작 태스크 설정과 robomimic 설정을 추가했다.
- DP3 모방학습 쪽에 stack 데이터셋, point cloud 기반 평가, saliency video 저장 로직을 추가했다.
- DP3 설정은 `dataset15.hdf5`, 단일 rollout 평가, 마지막 checkpoint 저장 비활성화 쪽으로 수정했다.
- LeHome challenge evaluation에 W&B logging, GPU dynamics 설정, garment path 수정, garment object validation 로직을 추가했다.
- Docker 설정은 로컬 이미지 `isaac-lab-base-es:latest`를 쓰고 GPU `0`만 사용하도록 바꿨다.
- Franka stack visuomotor camera 위치를 `pos=(1.3, 0.3, 0.4)`로 수정했다.

### 공식 Isaac Lab 대비 코드 분석

비교 기준은 공식 저장소 `https://github.com/isaac-sim/IsaacLab`의 `upstream/main` commit `b4c32102`다. 현재 로컬 git 히스토리에서는 공식 `upstream/main`과 공통 `merge-base`가 잡히지 않으므로, 아래 내용은 공통 조상 기준 diff가 아니라 공식 현재 트리와 로컬 현재 트리의 직접 비교 결과다.

핵심 로컬 작업 경로만 보면 `2718 files changed, 302150 insertions(+), 168 deletions(-)` 규모의 차이가 있다. 대부분은 공식 Isaac Lab 자체 수정이라기보다, 로컬 실험에 필요한 robot asset, garment simulation, imitation learning, evaluation code를 Isaac Lab 작업공간 안에 추가한 것이다.

#### 1. Docker와 로컬 실행 환경

- `.dockerignore`에 DexGarmentLab의 `Data/`, `Assets/`, `Model_HALO/SADP/checkpoints/`, `Model_HALO/SADP_G/checkpoints/`를 추가해서 Docker build context에 대형 asset과 checkpoint가 들어가지 않게 했다.
- `.gitignore`에 `*.hdf5`, `*.ckpt`를 추가해서 대형 dataset과 checkpoint가 실수로 git에 들어가는 것을 막았다.
- `docker/Dockerfile.base`는 공식처럼 `ISAACSIM_BASE_IMAGE_ARG`와 `ISAACSIM_VERSION_ARG`를 받는 구조가 아니라, 로컬 이미지 `isaac-lab-base-es:latest`를 바로 사용하도록 바뀌었다.
- `docker/docker-compose.yaml`은 `NVIDIA_VISIBLE_DEVICES=0`, `device_ids: ["0"]`로 GPU `0`만 쓰도록 고정되어 있다.

이 변경은 현재 장비에서는 실행을 단순하게 만들지만, 다른 장비에서 복원할 때는 `isaac-lab-base-es:latest` 이미지와 GPU 번호가 맞지 않으면 Docker 실행이 실패할 수 있다.

#### 2. Piper 로봇과 stack/square 조작 태스크

- `piper_isaac_sim/`이 새로 추가되었다. Piper, Piper-H, Piper-L, Piper-X 설명 파일, URDF/Xacro, Mujoco XML, RViz 설정, STL/DAE mesh, RealSense description asset이 포함되어 있다.
- `source/isaaclab_tasks/isaaclab_tasks/manager_based/manipulation/stack/config/piper/`에 Piper용 cube stack 환경이 추가되었다.
- `source/isaaclab_tasks/isaaclab_tasks/manager_based/manipulation/square/`에 Piper square 조작 태스크가 새로 추가되었다.
- 등록된 Gym task에는 `Isaac-Stack-Cube-Piper-IK-Rel-v0`, `Isaac-Square-Piper-IK-Rel-v0`가 포함된다.
- Piper stack/square 모두 joint position, IK relative control, instance randomization, robomimic BC-RNN 설정을 갖는다.

공식 Isaac Lab에는 이 Piper 작업이 없으므로, 이 저장소의 핵심 로컬 변경 중 하나는 Piper 로봇을 Isaac Lab manager-based manipulation task에 붙인 것이다.

#### 3. Franka stack visuomotor 관측 수정

- `source/isaaclab_tasks/isaaclab_tasks/manager_based/manipulation/stack/config/franka/stack_ik_rel_visuomotor_env_cfg.py`에서 관측 항목에 `table_cam_depth`, `wrist_cam_depth`, `table_cam_pointcloud`를 추가했다.
- `table_cam`의 clipping range를 `(0.1, 2)`에서 `(0.0001, 2)`로 바꿨다.
- `table_cam` 위치를 기존 기본값 대신 `pos=(1.3, 0.3, 0.4)`, `rot=(0.46, -0.46, -0.74, 0.44)`로 바꿨다.

이 변경은 DP3와 point cloud 기반 평가에 필요한 관측을 추가한 것이다. 다만 camera 위치가 바뀌면 이미지와 point cloud 분포도 바뀌므로, 이전 dataset이나 checkpoint를 그대로 비교할 때는 같은 camera geometry를 사용했는지 확인해야 한다.

#### 4. DP3 모방학습과 평가 시각화

- `scripts/imitation_learning/diffusion_policy_3d/` 아래에 Isaac Lab용 DP3 설정과 runner가 추가되었다.
- `conversion.py`는 Isaac Lab HDF5 demo에서 `table_cam_pointcloud`, `eef_pos`, `eef_quat`, `gripper_pos`, `actions`를 읽어 DP3용 zarr dataset으로 변환한다.
- `isaaclab_dp3.yaml`은 point cloud 6채널 입력, horizon `16`, action step `8`, `num_rollout: 1`, `save_last_ckpt: False` 같은 로컬 실험 설정을 갖는다.
- `env_runner/isaaclab_runner.py`는 Isaac Lab 환경을 직접 생성하고, point cloud crop, farthest point sampling, Open3D offscreen rendering, SmoothGrad saliency 계산, RGB와 saliency point cloud를 합친 video 저장을 수행한다.
- runner는 reward/done 처리를 `mdp.cubes_stacked(self.env)` 기준으로 보강하고, observation tensor를 `.detach()`해서 평가 중 gradient 추적 문제를 줄였다.

이 영역은 공식 Isaac Lab 기능이라기보다, Franka stack visuomotor 환경을 DP3 policy 평가와 시각화에 연결한 로컬 연구 코드다.

#### 5. LeHome garment challenge 평가 환경

- `scripts/lehome_challenge/`가 새로 추가되었다. LeHome extension, garment asset, robot asset, bedroom task, policy evaluation, dataset utility, video output, training/evaluation config가 포함된다.
- `scripts/utils/evaluation.py`는 W&B run을 생성하고 episode별 return, length, success와 garment별 success rate, final metric을 기록한다.
- evaluation은 `env_cfg.sim.use_fabric = False`, `SimulationManager.enable_gpu_dynamics(True)`를 사용한다.
- `challenge_garment_loader.py`, `particle_garment_cfg.yaml`, `Garment.py`, `garment_bi_v2.py` 쪽에는 garment config loading, particle material, cloth object 생성/삭제, success check, reward 계산, garment switching, observation 초기화 로직이 들어 있다.
- 일부 경로는 `scripts/lehome_challenge` 내부 구조에 맞춰져 있으므로, workspace 배치가 바뀌면 asset path와 config path를 다시 확인해야 한다.

이 영역은 의류 접기/조작 challenge를 Isaac Lab 안에서 실행하고 평가하기 위한 별도 로컬 패키지에 가깝다. 복원 후에는 W&B 인증, LeRobot dependency, garment asset, GPU dynamics 설정을 우선 확인해야 한다.

#### 6. DexGarmentLab 직접 포함

- `scripts/DexGarmentLab/`는 submodule 포인터가 아니라 일반 파일로 직접 git에 들어 있다.
- 공식 Isaac Lab에는 없는 DexGarmentLab 환경 코드, validation script, garment parameter 문서, HALO/GAM/SADP/SADP-G 모델 코드, teleoperation/retargeting 코드, diffusion policy baseline 코드가 추가되었다.
- `scripts/DexGarmentLab`만 보면 `750 files changed, 60888 insertions(+)` 규모로 추가되어 있다.
- 단, `Assets/Garment`, `Assets/LeapMotion`, `Assets/Robots`, `Assets/Scene`, `Assets/Human`, `Data/*`, `*.zip`, `*.pth` 등은 git에서 제외했다.

따라서 clone만 하면 DexGarmentLab 코드 구조는 복원되지만, 실제 garment/robot/scene asset과 checkpoint는 별도로 다운로드해야 한다.

#### 7. 데이터와 실험 산출물

- DP3 관련 dataset 변환물과 LeHome failure video 일부가 저장소에 포함되어 있다.
- 반대로 HDF5 원본 dataset, checkpoint, DexGarmentLab 대형 asset/data, zip archive는 `.gitignore` 또는 DexGarmentLab 제외 규칙으로 빠져 있다.
- 복원 후 학습 재현이 목적이면, git clone만으로 끝나지 않고 원본 HDF5, checkpoint, W&B run, local output directory를 따로 찾아야 한다.

#### 8. 복원 시 특히 확인할 위험 요소

- 공식 Isaac Lab과 공통 `merge-base`가 없기 때문에, 나중에 공식 최신판을 merge할 때는 자동 merge보다 파일 단위 비교가 더 안전하다.
- Docker는 로컬 이미지와 GPU `0`에 의존한다.
- DP3 runner는 Open3D, PyTorch3D, SciPy, OpenCV, Matplotlib 같은 dependency가 필요하다.
- LeHome evaluation은 W&B와 LeRobot dependency가 필요하고, 일부 asset/config path는 현재 repo layout을 전제로 한다.
- DexGarmentLab는 submodule이 아니므로 `git submodule update`로 복원되지 않는다.

### 추가된 주요 작업 영역

- `piper_isaac_sim/`: Piper 로봇 설명 파일, 메시, URDF/Xacro, RealSense asset, 실행 파일, 사용 문서.
- `source/isaaclab_tasks/isaaclab_tasks/manager_based/manipulation/stack/config/piper/`: Piper stack 태스크 설정, robomimic 정책 설정, instance randomization 변형.
- `source/isaaclab_tasks/isaaclab_tasks/manager_based/manipulation/square/`: Piper square 조작 태스크, observation, termination, event, robomimic 설정, randomization 변형.
- `scripts/DexGarmentLab/`: 이 저장소에 직접 포함된 DexGarmentLab 코드. 대형 asset, dataset, archive, checkpoint는 제외되어 있다.
- `scripts/lehome_challenge/`: LeHome garment challenge asset, 태스크 코드, 평가 스크립트, object 설정, failure video.
- `scripts/imitation_learning/datasets/DP3/`: DP3 stack 데이터셋, point cloud, action, agent pose, 생성된 dataset 변형, 평가 결과.

### DexGarmentLab에서 git에 넣지 않은 것

다음 파일과 폴더는 용량이 크거나 재생성/재다운로드 대상이라 git에서 제외했다.

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

git에 포함된 DexGarmentLab 내용은 소스 코드, 설정 파일, 모델 정의, 다운로드 보조 스크립트, 일부 material asset, repository image, 작은 point-cloud/example file이다.

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
   git log --oneline -10
   ```

   최소한 아래 주요 커밋들이 보여야 한다. README를 나중에 다시 수정했다면 더 최신 커밋이 위에 추가로 있을 수 있다.

   ```text
   838baa0a Translate README to Korean
   37fe9b86 Update README commit references
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

   이 스크립트는 Hugging Face의 `wayrise/DexGarmentLab` dataset에서 zip 파일을 받는다. 자동으로 압축이 풀리지 않으면, 받은 zip 파일들을 `scripts/DexGarmentLab` 구조에 맞게 직접 압축 해제한다.

4. Docker를 쓸 경우 로컬 이미지가 필요하다.

   ```text
   isaac-lab-base-es:latest
   ```

   이 이미지가 없으면 Docker build가 실패할 수 있다. 그 경우 이미지를 다시 만들거나, `docker/Dockerfile.base`를 공식 Isaac Sim base image를 쓰는 형태로 되돌린다.

5. GPU 설정을 확인한다.

   `docker/docker-compose.yaml`은 GPU `0`만 쓰도록 설정되어 있다. 다른 GPU를 쓰려면 `NVIDIA_VISIBLE_DEVICES`와 `device_ids` 값을 수정한다.

6. 필요한 Python dependency를 다시 설치한다.

   - Isaac Lab dependency는 공식 Isaac Lab 설치 방법을 따른다.
   - DexGarmentLab dependency는 `scripts/DexGarmentLab/requirements.txt`를 사용한다.
   - LeHome evaluation은 W&B를 사용하므로, 로그인하거나 offline/disabled mode로 실행한다.

### 전체 복원 주의점

- GitHub에 올린 저장소와 로컬 저장소가 같은지 먼저 확인한다. 이 작업을 `intern.git`에 올릴 계획이면 remote는 `https://github.com/eimyssong/intern.git`이어야 한다.

  ```bash
  git remote -v
  git branch --show-current
  git status
  ```

- 이 README에 적힌 최신 복원 정보까지 포함하려면 최신 README 커밋까지 push되어야 한다. GitHub에서 README가 예전 내용으로 보이면 아직 push가 안 된 것이다.
- `scripts/DexGarmentLab/`는 더 이상 submodule이 아니다. 따라서 복원 후 `git submodule update --init --recursive`로 DexGarmentLab가 복구되는 구조가 아니다. DexGarmentLab 코드는 이 저장소에 일반 파일로 들어 있고, 제외된 asset/data만 별도로 다운로드해야 한다.
- DexGarmentLab 원본 내부 `.git` 디렉터리는 커밋 전에 제거했다. 기존 내부 git 메타데이터는 작업 당시 `/tmp/DexGarmentLab.git.backup`에 임시 백업했지만, `/tmp`는 재부팅이나 정리 작업으로 사라질 수 있다. 복원은 이 백업에 의존하지 말고 현재 저장소의 일반 파일과 다운로드 스크립트를 기준으로 한다.
- `*.zip`, `*.pth`, DexGarmentLab의 주요 asset/data 폴더는 git에 없다. 새 장비에서 clone만 하면 모델 checkpoint, garment asset, human/robot/scene asset, dataset zip은 없는 상태가 정상이다. 필요한 경우 Hugging Face 다운로드 스크립트나 별도 실험 저장소에서 다시 받아야 한다.
- DP3 `.zarr` 데이터와 LeHome failure video 일부는 커밋에 포함되어 있지만, 모든 실험 산출물이 들어간 것은 아니다. 학습을 재현하려면 사용한 원본 HDF5, checkpoint, W&B run, 로컬 output 폴더를 별도로 확인해야 한다.
- Docker 설정은 일반 Isaac Lab 기본값이 아니라 로컬 환경에 맞춰 바뀌어 있다. 특히 `isaac-lab-base-es:latest` 이미지와 GPU `0` 고정 설정이 맞지 않으면 Docker 실행이 실패한다.
- GitHub push 권한은 계정 인증에 따라 달라진다. `Permission denied to siwon7` 같은 메시지가 나오면 현재 GitHub 인증 계정이 `eimyssong`이 아닌 것이다. `gh auth status`로 계정을 확인하고, 필요한 경우 `gh auth logout -h github.com` 후 `gh auth login -h github.com`으로 다시 로그인한다.
- 복원 후 정상 여부는 아래 명령으로 먼저 확인한다.

  ```bash
  git status
  git log --oneline -10
  test -d scripts/DexGarmentLab
  test -f scripts/DexGarmentLab/README.md
  ```

## 주요 기능

Isaac Lab은 로봇 학습을 위한 다양한 도구와 환경을 제공한다.

- **로봇**: 매니퓰레이터, 사족보행 로봇, 휴머노이드 등 16개 이상의 널리 쓰이는 로봇 모델을 포함한다.
- **환경**: 30개 이상의 학습 가능한 환경을 제공하며, RSL RL, SKRL, RL Games, Stable Baselines 같은 강화학습 프레임워크와 함께 사용할 수 있다. 다중 에이전트 강화학습도 지원한다.
- **물리**: rigid body, articulated system, deformable object를 지원한다.
- **센서**: RGB/depth/segmentation camera, camera annotation, IMU, contact sensor, ray caster를 지원한다.

## 시작하기

### 문서

[공식 문서](https://isaac-sim.github.io/IsaacLab)에는 설치 방법, 튜토리얼, 사용 가이드가 정리되어 있다.

- [설치 방법](https://isaac-sim.github.io/IsaacLab/main/source/setup/installation/index.html#local-installation)
- [강화학습](https://isaac-sim.github.io/IsaacLab/main/source/overview/reinforcement-learning/rl_existing_scripts.html)
- [튜토리얼](https://isaac-sim.github.io/IsaacLab/main/source/tutorials/index.html)
- [사용 가능한 환경](https://isaac-sim.github.io/IsaacLab/main/source/overview/environments.html)

## Isaac Sim 버전 의존성

Isaac Lab은 Isaac Sim 위에서 동작하므로, Isaac Lab 버전에 맞는 Isaac Sim 버전이 필요하다. 최근 Isaac Lab release와 branch별 Isaac Sim 의존성은 다음과 같다.

| Isaac Lab 버전 | Isaac Sim 버전 |
| -------------- | -------------- |
| `main` branch  | Isaac Sim 4.5 / 5.0 / 5.1 |
| `v2.3.X`       | Isaac Sim 4.5 / 5.0 / 5.1 |
| `v2.2.X`       | Isaac Sim 4.5 / 5.0 |
| `v2.1.X`       | Isaac Sim 4.5 |
| `v2.0.X`       | Isaac Sim 4.5 |

## 기여

Isaac Lab은 커뮤니티의 기여를 환영한다. 버그 리포트, 기능 제안, 코드 기여 모두 가능하다. 자세한 내용은 [기여 가이드](https://isaac-sim.github.io/IsaacLab/main/source/refs/contributing.html)를 참고한다.

## 공유 및 쇼케이스

프로젝트, 튜토리얼, 학습 자료를 공유하려면 GitHub Discussions의 [Show & Tell](https://github.com/isaac-sim/IsaacLab/discussions/categories/show-and-tell) 공간을 사용할 수 있다.

- 직접 만든 튜토리얼 공유
- 학습 자료 소개
- 개발한 프로젝트 소개

공유된 작업은 다른 사용자에게 참고 자료가 되고, 로봇공학과 시뮬레이션 커뮤니티의 협업에 도움이 된다.

## 문제 해결

일반적인 문제는 [troubleshooting 문서](https://isaac-sim.github.io/IsaacLab/main/source/refs/troubleshooting.html)를 확인한다. 해결되지 않는 문제는 [GitHub Issue](https://github.com/isaac-sim/IsaacLab/issues)를 등록할 수 있다.

Isaac Sim 자체와 관련된 문제는 [Isaac Sim 문서](https://docs.isaacsim.omniverse.nvidia.com/latest/index.html)를 확인하거나 [NVIDIA developer forum](https://forums.developer.nvidia.com/c/agx-autonomous-machines/isaac/67)에 질문한다.

## 지원

- 아이디어 논의, 질문, 기능 요청은 GitHub [Discussions](https://github.com/isaac-sim/IsaacLab/discussions)를 사용한다.
- GitHub [Issues](https://github.com/isaac-sim/IsaacLab/issues)는 실행 가능한 범위와 명확한 결과물이 있는 작업을 추적하는 데 사용한다. 예를 들어 버그 수정, 문서 문제, 새 기능, 일반 업데이트가 이에 해당한다.

## NVIDIA Omniverse 커뮤니티

더 넓게 공유하고 싶은 프로젝트나 자료가 있다면 NVIDIA Omniverse Community 팀에 연락할 수 있다. 문의 주소는 OmniverseCommunity@nvidia.com 이다.

[Omniverse Discord](https://discord.com/invite/nvidiaomniverse)에 참여해 다른 개발자와 소통하고 프로젝트를 공유할 수도 있다.

## 라이선스

Isaac Lab 프레임워크는 [BSD-3 License](LICENSE)로 배포된다. `isaaclab_mimic` 확장과 관련 독립 실행 스크립트는 [Apache 2.0](LICENSE-mimic)으로 배포된다. 의존성과 asset의 license file은 [`docs/licenses`](docs/licenses) 디렉터리에 있다.

Isaac Lab은 Isaac Sim을 필요로 하며, Isaac Sim에는 독점 라이선스 조건이 적용되는 component가 포함되어 있다. 자세한 내용은 [Isaac Sim license](docs/licenses/dependencies/isaacsim-license.txt)를 참고한다.

`isaaclab_mimic` 확장은 cuRobo를 필요로 하며, cuRobo의 독점 라이선스 조건은 [`docs/licenses/dependencies/cuRobo-license.txt`](docs/licenses/dependencies/cuRobo-license.txt)에서 확인할 수 있다.

## 인용

연구에서 Isaac Lab을 사용했다면 아래 기술 보고서를 인용한다.

```
@article{mittal2025isaaclab,
  title={Isaac Lab: A GPU-Accelerated Simulation Framework for Multi-Modal Robot Learning},
  author={Mayank Mittal and Pascal Roth and James Tigue and Antoine Richard and Octi Zhang and Peter Du and Antonio Serrano-Muñoz and Xinjie Yao and René Zurbrügg and Nikita Rudin and Lukasz Wawrzyniak and Milad Rakhsha and Alain Denzler and Eric Heiden and Ales Borovicka and Ossama Ahmed and Iretiayo Akinola and Abrar Anwar and Mark T. Carlson and Ji Yuan Feng and Animesh Garg and Renato Gasoto and Lionel Gulich and Yijie Guo and M. Gussert and Alex Hansen and Mihir Kulkarni and Chenran Li and Wei Liu and Viktor Makoviychuk and Grzegorz Malczyk and Hammad Mazhar and Masoud Moghani and Adithyavairavan Murali and Michael Noseworthy and Alexander Poddubny and Nathan Ratliff and Welf Rehberg and Clemens Schwarke and Ritvik Singh and James Latham Smith and Bingjie Tang and Ruchik Thaker and Matthew Trepte and Karl Van Wyk and Fangzhou Yu and Alex Millane and Vikram Ramasamy and Remo Steiner and Sangeeta Subramanian and Clemens Volk and CY Chen and Neel Jawale and Ashwin Varghese Kuruttukulam and Michael A. Lin and Ajay Mandlekar and Karsten Patzwaldt and John Welsh and Huihua Zhao and Fatima Anes and Jean-Francois Lafleche and Nicolas Moënne-Loccoz and Soowan Park and Rob Stepinski and Dirk Van Gelder and Chris Amevor and Jan Carius and Jumyung Chang and Anka He Chen and Pablo de Heras Ciechomski and Gilles Daviet and Mohammad Mohajerani and Julia von Muralt and Viktor Reutskyy and Michael Sauter and Simon Schirm and Eric L. Shi and Pierre Terdiman and Kenny Vilella and Tobias Widmer and Gordon Yeoman and Tiffany Chen and Sergey Grizan and Cathy Li and Lotus Li and Connor Smith and Rafael Wiltz and Kostas Alexis and Yan Chang and David Chu and Linxi "Jim" Fan and Farbod Farshidian and Ankur Handa and Spencer Huang and Marco Hutter and Yashraj Narang and Soha Pouya and Shiwei Sheng and Yuke Zhu and Miles Macklin and Adam Moravanszky and Philipp Reist and Yunrong Guo and David Hoeller and Gavriel State},
  journal={arXiv preprint arXiv:2511.04831},
  year={2025},
  url={https://arxiv.org/abs/2511.04831}
}
```

## 감사의 말

Isaac Lab 개발은 [Orbit](https://isaac-orbit.github.io/) 프레임워크에서 시작되었다. Isaac Lab의 기반을 만든 Orbit 저자들에게 감사한다.
