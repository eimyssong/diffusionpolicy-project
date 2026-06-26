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

- `682383af Document official comparison analysis`
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

### 공식 DexGarmentLab 대비 상세 분석

이 절은 로컬 `scripts/DexGarmentLab/`에서 무엇을 바꿨는지 기억하기 쉽도록, 공식 DexGarmentLab(`https://github.com/wayrise/DexGarmentLab/tree/main`)과 직접 비교한 결과를 정리한 것이다.

#### 비교 기준과 교차검증

- 공식 기준: `wayrise/DexGarmentLab` HEAD `e4e298e696bae5d866ded3b31e0ae27becea5376`.
- 로컬 기준: 이 저장소의 `scripts/DexGarmentLab/`를 현재 git HEAD 기준으로 archive한 tracked snapshot.
- 비교 방식: 공식 repo와 로컬 tracked snapshot을 각각 `/tmp`에 분리한 뒤 `git diff --no-index`, 파일 목록 비교, 주요 파일별 diff를 확인했다.
- 멀티 에이전트 교차검증: 세 개의 explorer가 각각 파일 인벤토리/복원 리스크, 코드 변경 내용, 독립 검증 관점으로 비교했다. 세 결과가 공통으로 확인한 핵심은 `tracked 코드 변경 19개`, `로컬 추가 tracked 파일 46개`, `tracked snapshot 기준 공식-only 57개`, 그리고 `git에는 없지만 실제 로컬에 존재하는 대형 asset/data/checkpoint`다.
- 주의: `scripts/DexGarmentLab` 전체 실제 로컬 폴더에는 `.gitignore`로 제외된 asset, data, checkpoint가 많이 있으므로, “git에 들어간 코드 비교”와 “실제 로컬 디스크에 있는 대형 산출물”을 분리해서 봐야 한다.

tracked snapshot 기준 수치는 다음과 같다.

- 공식 tracked 파일: 761개.
- 로컬 tracked 파일: 750개.
- 공통 파일: 704개.
- 공통 파일 중 내용 수정: 19개.
- 로컬에만 tracked된 파일: 46개.
- 공식에는 있으나 로컬 tracked snapshot에는 없는 파일: 57개.
- 전체 diff 규모: `122 files changed, 6969 insertions(+), 473 deletions(-)`.

#### 수정된 tracked 파일 19개

공식 대비 내용이 바뀐 파일은 아래 19개다.

- `.gitignore`
- `Data_Collection.sh`
- `Validation.sh`
- `requirements.txt`
- `Env_Config/Garment/Deformable_Garment.py`
- `Env_Config/Garment/Particle_Garment.py`
- `Env_StandAlone/Fold_Tops_Env.py`
- `Env_StandAlone/Fold_Trousers_Env.py`
- `Env_Validation/Fling_Trousers_HALO.py`
- `Env_Validation/Fold_Tops_HALO.py`
- `Env_Validation/Fold_Trousers_HALO.py`
- `Env_Validation/Hang_Coat_HALO.py`
- `Model_HALO/GAM/GAM_Encapsulation.py`
- `Model_HALO/GAM/model/pointnet2_GAM.py`
- `Model_HALO/SADP/data2zarr_sadp.sh`
- `Model_HALO/SADP/train.sh`
- `Model_HALO/SADP_G/data2zarr_sadp_g.sh`
- `Model_HALO/SADP_G/train.py`
- `Model_HALO/SADP_G/train.sh`

#### 1. 실행 경로와 shell script 변경

- `Data_Collection.sh`는 Isaac Sim 실행 경로를 공식 기본값 `~/isaacsim_4.5.0/python.sh`에서 `/workspace/isaaclab/_isaac_sim/python.sh`로 바꿨다.
- `Validation.sh`도 동일하게 `/workspace/isaaclab/_isaac_sim/python.sh`를 사용하도록 바뀌었다.
- 두 script 모두 `/isaac-sim/extscache/...` 경로를 `PYTHONPATH`에 여러 개 추가한다. 이 설정은 현재 Docker/Isaac Sim 환경에 맞춘 것이다.
- `Data_Collection.sh`와 `Validation.sh`의 산출물 base directory가 `Data/...` 상대경로에서 `/workspace/isaaclab/scripts/DexGarmentLab/Data/...` 절대경로로 바뀌었다.
- 공식 script는 실행 로그를 `/dev/null`로 버렸지만, 로컬 script는 redirect를 제거해서 stdout/stderr를 볼 수 있게 했다.
- `Model_HALO/SADP/data2zarr_sadp.sh`, `Model_HALO/SADP/train.sh`, `Model_HALO/SADP_G/data2zarr_sadp_g.sh`, `Model_HALO/SADP_G/train.sh`는 Isaac Python 경로를 `/isaac-sim/python.sh`로 바꿨다.
- `Model_HALO/SADP_G/train.sh`는 `training.resume=True`를 추가해서 기존 checkpoint에서 이어서 학습하는 흐름을 기본으로 만든다.
- `Model_HALO/SADP_G/train.py`는 resume checkpoint path를 출력하는 debug print를 추가했다.

복원 시 이 경로들이 그대로 존재하지 않으면 script가 바로 실패한다. 다른 workspace에서 실행하려면 `/workspace/isaaclab`, `/isaac-sim`, `PYTHONPATH`, `Data` 절대경로를 먼저 수정해야 한다.

#### 2. garment asset 경로와 물리 파라미터 변경

- `Env_Config/Garment/Deformable_Garment.py`에서 기본 `usd_path`와 `visual_material_usd`를 공식 상대경로에서 `/workspace/isaaclab/scripts/DexGarmentLab/...` 절대경로로 바꿨다.
- `Deformable_Garment.py`의 기본 scale은 공식 `0.0085`에서 `1.0`으로 바뀌었다.
- `Env_Config/Garment/Particle_Garment.py`도 기본 garment USD와 material USD를 절대경로로 바꿨고, 기본 scale을 `0.0085`에서 `1.0`으로 바꿨다.
- `Particle_Garment.py`에서는 cloth/particle 물성이 크게 달라졌다.
  - `friction`: `25.0 -> 25000.0`
  - `stretch_stiffness`: `1e12 -> 1e6`
  - `bend_stiffness`: `100.0 -> 250.0`
  - `shear_stiffness`: `100.0 -> 150.0`
  - `spring_damping`: `10.0 -> 50.0`

이 변경은 공식 DexGarmentLab과 시뮬레이션 결과가 달라지는 핵심 원인이다. 특히 scale과 friction이 크게 바뀌어 garment 크기, 접촉 안정성, 접힘 결과가 공식 환경과 다를 수 있다.

#### 3. Fold Tops 실험 변경

- `Env_StandAlone/Fold_Tops_Env.py`에서 기본 tops USD 경로를 `/workspace/isaaclab/scripts/DexGarmentLab/...` 절대경로로 바꿨다.
- 공식은 `GAM_Encapsulation(catogory="Tops_LongSleeve")`를 바로 쓰지만, 로컬에는 `input_garment_type="trousers"`를 넣는 실험 코드와 topology fine-tune 관련 주석이 추가되어 있다.
- `FoldTops()`에서 garment point cloud 저장을 `save_or_not=True`로 바꿨다.
- GAM correspondence visualization 호출을 추가했다. 입력 point cloud와 demo garment의 feature correspondence를 `.ply`로 확인하기 위한 실험 코드다.
- video, log, final image 저장 경로를 `/workspace/isaaclab/scripts/DexGarmentLab/Data/Fold_Tops/...` 절대경로로 바꿨다.
- random garment list가 공식 `Tops_LongSleeve/assets_training_list.txt`에서 `Trousers/assets_training_list.txt`로 바뀐 실험 흔적이 있다. 즉 “상의 folding 환경에서 하의 asset list를 써 보는” cross-category 실험 설정이 들어 있다.

#### 4. Fold Trousers standalone 실험 변경

- `Env_StandAlone/Fold_Trousers_Env.py`에서 GAM 초기화를 `GAM_Encapsulation(catogory="Trousers", force_finetune=True)`로 바꿨다. 즉 기존 topology layer checkpoint가 있어도 강제로 다시 fine-tune하는 흐름이다.
- `FoldTrousers()`에 correspondence `.ply` 저장과 visualization 코드가 추가되었다.
- 공식 manipulation index는 6개였지만, 로컬은 `[983, 521, 1801, 471, 1170, 214, 338, 1222]`처럼 8개 point를 사용한다.
- 첫 접기 이후 right hand 단독 pick/fold stage가 크게 추가되었다. 중간 조작점 `manipulation_points[6]`, `manipulation_points[7]`를 사용해 오른손으로 집고 이동한 뒤 release하는 절차가 들어 있다.
- stage 중간에 `env.record(task_name="Fold_Trousers", stage_index=2)`를 호출하는 데이터 수집 로직이 추가되었다.
- release 시 gravity scale을 `10.0`으로 올렸다가 다시 `1.0`으로 되돌리는 안정화 로직이 추가되었다.
- video 저장 조건이 공식의 `record_video_flag and success`에서 `record_video_flag`로 완화되었다.
- random garment list가 `Trousers/assets_training_list.txt`에서 `Dress_LongSleeve/assets_list.txt`로 바뀐 흔적과, 특정 dress USD를 직접 지정한 실험 코드가 있다.

이 파일은 단순 경로 수정이 아니라 fold trousers 조작 정책 자체를 확장한 핵심 실험 파일이다.

#### 5. validation 환경 변경

아래 validation 파일들은 공통으로 `SimulationApp({"headless": True})`에서 `SimulationApp({"headless": False})`로 바뀌었다.

- `Env_Validation/Fling_Trousers_HALO.py`
- `Env_Validation/Fold_Tops_HALO.py`
- `Env_Validation/Fold_Trousers_HALO.py`
- `Env_Validation/Hang_Coat_HALO.py`

이 때문에 로컬 validation은 GUI/display가 있는 환경을 전제로 한다. 서버나 headless Docker에서 돌리려면 다시 `headless=True`로 바꾸거나 display 설정이 필요하다.

각 파일의 주요 변경은 다음과 같다.

- `Fling_Trousers_HALO.py`
  - correspondence visualization 저장을 추가했다.
  - random validation asset list를 `Trousers/assets_list.txt`에서 `Tops_LongSleeve/assets_list.txt`로 바꿨다.
  - 주석상 “하의로 학습하고 상의로 테스트”하는 cross-category 평가 목적이다.

- `Fold_Tops_HALO.py`
  - 기본 USD와 output 경로를 `/workspace/isaaclab/scripts/DexGarmentLab/...` 절대경로로 바꿨다.
  - correspondence `.ply` 저장을 추가했다.
  - random asset list를 `Trousers/assets_list.txt`로 바꾼 실험 흔적이 있다.
  - video, validation log, final image 저장 경로가 절대경로로 바뀌었다.

- `Fold_Trousers_HALO.py`
  - 기본 USD를 절대경로로 바꿨다.
  - `GAM_Encapsulation(catogory="Trousers", force_finetune=True)`를 사용한다.
  - 공식에는 `Fold_Dress_stage_1`, `Fold_Dress_stage_2` task 이름이 들어 있었는데, 로컬은 `Fold_Trousers_stage_1`, `Fold_Trousers_stage_2`로 수정했다.
  - `Fold_Trousers_stage_3_source_target` SADP_G stage를 추가했다.
  - garment bbox와 stage unit을 출력하는 debug code가 추가되었다.
  - manipulation index를 6개에서 8개로 확장했다.
  - stage 1 반복은 `12 -> 9`, action inner loop는 `4 -> 2`로 줄였다.
  - stage 2 반복은 `8 -> 6`, action inner loop는 `4 -> 3`으로 줄였다.
  - source-target/left-arm 실험 block이 큰 주석 코드로 들어 있다.
  - validation video/log/image 저장 경로가 절대경로로 바뀌었다.

- `Hang_Coat_HALO.py`
  - 기본 coat USD 경로를 절대경로로 바꿨다.
  - correspondence visualization 저장을 추가했다.
  - validation video/log/final image 경로를 절대경로로 바꿨다.
  - 상의로 학습하고 하의로 테스트하는 asset list 실험 주석이 추가되어 있다.

#### 6. GAM correspondence와 topology fine-tune 변경

`Model_HALO/GAM/GAM_Encapsulation.py`가 공식 대비 가장 크게 바뀐 파일이다. diff 기준으로 `5464 insertions, 111 deletions`이고, 사실상 새로운 실험 구현이 누적된 파일이다.

중요한 점은 Python에서 같은 이름의 class가 여러 번 정의되면 마지막 정의가 실제로 유효하다는 것이다. 이 파일에는 여러 실험 버전이 주석 또는 중간 정의 형태로 남아 있지만, 실제 import 시 핵심이 되는 것은 파일 하단의 `GAM_Encapsulation` 구현이다.

주요 변경은 다음과 같다.

- 공식의 단순 GAM feature wrapper를 확장해서, frozen GAM backbone 위에 topology/correspondence 보정 layer를 얹었다.
- `_features_bnd`, `_points_bnd` helper를 추가해 tensor shape를 `[batch, point, feature]`, `[batch, point, xyz]` 형태로 정규화한다.
- `PantsBilateralLayer`를 추가했다.
  - symmetric/antisymmetric MLP를 사용한다.
  - mirror index를 계산해 좌우 반사 구조를 feature에 반영한다.
  - balanced multi-scale k-NN geometry를 만든다.
  - trousers coordinate와 topology warp를 이용해 바지 형태를 상의처럼 변형한 training shape를 만든다.
- `GAMWithPantsBilateralLayer`는 기존 GAM backbone을 frozen으로 두고, 추가된 bilateral layer만 학습/적용한다.
- `GAM_Encapsulation.__init__`는 기존 `checkpoint.pth`를 backbone으로 읽고, `checkpoint_pants_topology_layer.pth`가 있으면 로드한다.
- `force_finetune=True`가 들어오면 기존 topology layer checkpoint가 있어도 다시 학습한다.
- `catogory="Trousers"`이고 topology layer checkpoint가 없으면 `fine_tune_bilateral_layer()`를 자동 실행한다.
- `fine_tune_bilateral_layer()`는 trousers demo garment에서 teacher feature를 만들고, sleeve/hem anchor mask와 topology warp augmentation을 사용해 bilateral layer를 학습한 뒤 `checkpoint_pants_topology_layer.pth`로 저장한다.

이 변경의 목적은 공식 GAM의 점 대응을 그대로 쓰는 것이 아니라, 바지-상의 또는 좌우 branch 구조가 다른 garment 사이에서도 더 안정적인 correspondence를 얻기 위한 것으로 보인다.

#### 7. 새로 추가된 topology 관련 파일

로컬에만 추가된 tracked 파일 중 topology/GAM 관련 핵심 파일은 다음과 같다.

- `Model_HALO/GAM/model/gam_topo_model.py`
  - `GAM_Topo_Model`을 추가했다.
  - 기존 backbone feature에 topology descriptor projection을 더하고, `mix_logit`으로 영향도를 조절한다.
  - backbone freeze와 일부 layer unfreeze helper가 있다.

- `Model_HALO/GAM/model/topology_descriptor.py`
  - `compute_topology_descriptor()`를 추가했다.
  - point cloud에서 left/right branch, branch progress, endpoint score, center score, boundary score를 만든다.
  - trousers와 tops의 branch progress 기준을 다르게 둔다.

- `Model_HALO/GAM/model/train_topology_finetune.py`
  - topology fine-tune 학습 script다.
  - `TopsPointCloudDataset`, `topology_feature_loss`, `topology_cluster_loss`, `feature_keep_loss`, `train()`이 포함되어 있다.
  - `/workspace/isaaclab/scripts/DexGarmentLab/pointcloud`를 dataset 경로로 사용한다.

- `Model_HALO/GAM/checkpoints/Trousers/assets_list_top.txt`
  - 이름은 Trousers checkpoint 아래 있지만, 내용은 tops asset list다.
  - 바지 모델/실험에서 상의 asset을 source/target 또는 cross-category 테스트로 쓰기 위한 목록으로 보인다.

- `pointcloud_top/data_0.ply`부터 `pointcloud_top/data_40.ply`
  - 총 41개 point cloud 예시 파일이다.
  - 각 파일은 약 55KB이며 전체 약 2.3MB다.
  - topology/correspondence fine-tune 또는 시각화 검증용 작은 point cloud snapshot으로 보인다.

#### 8. SADP/SADP-G fine-tune 관련 변경

- `finetune.sh`가 공식에는 없고 로컬에 새로 추가되었다.
- 이 script는 `Fold_Trousers_stage_3_target_guided` 같은 target-guided SADP_G fine-tune을 위한 wrapper다.
- 기본 project root는 `/workspace/isaaclab/scripts/DexGarmentLab`이고, SADP_G checkpoint/data 경로도 이 구조를 전제로 한다.
- learning rate, target/direction/progress/motion/keep loss weight, left/right side weight, target affordance sigma 등을 command line으로 넘긴다.
- 중요한 주의점: `finetune.sh`는 `finetune_sadp_g.py`를 호출하지만, 이 파일은 root-level `*.py` ignore 규칙 때문에 git tracked snapshot에는 없다. 현재 실제 로컬 경로에는 `scripts/DexGarmentLab/finetune_sadp_g.py`가 존재하지만, git clone만 하면 복원되지 않는다.

따라서 `finetune.sh`를 나중에 실행하려면 `finetune_sadp_g.py`를 별도로 백업하거나 git에 포함할지 다시 결정해야 한다.

#### 9. 공식 대비 그대로인 영역

다음 영역은 공식 DexGarmentLab과 내용 차이가 없다고 교차검증했다.

- `IL_Baselines/`
- `Data/data_download.py`
- `README.md` 내부 DexGarmentLab 원본 문서 내용

즉, 이 로컬 작업의 핵심은 IL baseline 전체 수정이 아니라 GAM/topology correspondence, Fold/Fling/Hang validation 실험, SADP_G fine-tune wrapper, Isaac/컨테이너 경로 조정에 집중되어 있다.

#### 10. 로컬 추가 tracked 파일 46개

로컬에만 tracked된 파일은 아래로 요약된다.

- `finetune.sh`
- `Model_HALO/GAM/checkpoints/Trousers/assets_list_top.txt`
- `Model_HALO/GAM/model/gam_topo_model.py`
- `Model_HALO/GAM/model/topology_descriptor.py`
- `Model_HALO/GAM/model/train_topology_finetune.py`
- `pointcloud_top/data_0.ply`부터 `pointcloud_top/data_40.ply`

이 중 `pointcloud_top` 41개 파일은 작아서 git에 포함되어 있지만, 학습/검증에 필요한 전체 dataset과 checkpoint는 포함되어 있지 않다.

#### 11. 공식에는 있으나 로컬 tracked snapshot에는 없는 57개

tracked snapshot 기준으로 공식에는 있지만 로컬 tracked 파일에는 없는 항목은 다음 유형이다.

- `TeleOp_Env.py`
- `Assets/Flatten_Scarf/*`
- `Assets/Material/Floor/*`
- `Assets/Material/Garment/linen_Blue.usd`
- `Assets/Material/Garment/linen_Pumpkin.usd`
- `Model_HALO/GAM/checkpoints/*/checkpoint.pth`
- `Env_Config/Teleoperation/retarget/poselib/*/tests/*`

하지만 이 파일들이 현재 로컬 디스크에서 삭제됐다는 뜻은 아니다. 실제 `/home/cv25/workspaces/eunsong/lab/IsaacLab/scripts/DexGarmentLab` 전체 폴더에는 대부분 존재한다. 다만 git tracked snapshot에는 `.gitignore` 규칙과 이전 커밋 제외 정책 때문에 들어가지 않았다.

복원 관점에서는 이 항목들을 “git으로는 복원 안 되는 파일”로 봐야 한다. 특히 `checkpoint.pth`는 `*.pth` ignore 때문에 git에 들어가지 않는다.

#### 12. 실제 로컬에만 있는 대형 asset/data/checkpoint

실제 로컬 `scripts/DexGarmentLab`에는 git에 들어가지 않은 대형 파일이 많다. 교차검증 시 확인한 대략적인 크기는 다음과 같다.

- `scripts/DexGarmentLab/Assets`: 약 13GB
- `scripts/DexGarmentLab/Data`: 약 53GB
- `scripts/DexGarmentLab/Model_HALO`: 약 879GB
- `scripts/DexGarmentLab/Model_HALO/SADP/checkpoints`: 약 121GB
- `scripts/DexGarmentLab/Model_HALO/SADP_G/checkpoints`: 약 753GB 이상
- `scripts/DexGarmentLab/Model_HALO/GAM/checkpoints`: 약 118MB
- zip backup류: `Garment.zip` 약 6.1GB, `Scene.zip` 약 2.4GB, `LeapMotion.zip` 약 747MB, `Human.zip` 약 85MB, `Robots.zip` 약 76MB

이 파일들은 git clone만으로는 복원되지 않는다. 학습 재현이나 validation 재실행이 목적이면 asset, data, checkpoint, zip backup을 별도로 보관해야 한다.

#### 13. DexGarmentLab 복원 시 반드시 확인할 점

- 이 로컬 DexGarmentLab 코드는 `/workspace/isaaclab/scripts/DexGarmentLab`와 `/isaac-sim` 절대경로에 강하게 의존한다. 다른 위치에서 복원하면 경로를 수정해야 한다.
- validation 파일 일부는 `headless=False`다. display가 없는 서버에서는 실행 실패할 수 있다.
- `*.pth`, `*.zip`, `Assets/Garment`, `Assets/LeapMotion`, `Assets/Robots`, `Assets/Scene`, `Assets/Human`, `Data/*`는 git에서 제외되어 있다.
- `scripts/DexGarmentLab/*.py`도 ignore 대상이다. 그래서 `finetune_sadp_g.py`처럼 root-level Python script는 현재 로컬에는 있어도 git clone으로 복원되지 않는다.
- `finetune.sh`를 실제로 쓰려면 `finetune_sadp_g.py`, SADP_G data zarr, SADP_G checkpoint가 별도로 있어야 한다.
- `GAM_Encapsulation.py`의 topology layer는 `checkpoint_pants_topology_layer.pth`를 만들거나 로드한다. 이 파일은 `.pth`라서 git에 없다.
- `Fold_Tops`, `Fold_Trousers`, `Fling_Trousers`, `Hang_Coat` 일부는 task 이름과 실제 garment asset category가 다르게 설정된 cross-category 실험 버전이다. 결과를 해석할 때 “상의 task에서 하의 asset”, “하의 task에서 상의 asset”, “하의 task에서 dress asset” 같은 설정이 의도인지 반드시 확인해야 한다.
- 실제 asset tree에는 일부 권한 제한 폴더가 있다. `find`, `du`, `git diff --no-index`, 압축 백업을 할 때 permission denied가 날 수 있으므로 백업 전 권한을 확인해야 한다.
- 공식 DexGarmentLab와 다시 동기화하려면, 먼저 `Model_HALO/GAM/GAM_Encapsulation.py`, `Env_StandAlone/Fold_Trousers_Env.py`, `Env_Validation/Fold_Trousers_HALO.py`를 우선 검토해야 한다. 이 세 파일이 로컬 실험 변경의 중심이다.

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





## 실행 방법
<teleop>
./isaaclab.sh -p scripts/environments/teleoperation/teleop_se3_agent.py --task Isaac-Stack-Cube-Piper-IK-Rel-v0 --num_envs 1 --teleop_device keyboard --enable_camera --enable_pinocchio --save


./isaaclab.sh -p scripts/environments/teleoperation/teleop_se3_agent.py --task Isaac-Stack-Cube-Franka-IK-Rel-v0 --num_envs 1 --teleop_device keyboard --enable_camera --enable_pinocchio --save


./isaaclab.sh -p scripts/environments/teleoperation/teleop_se3_agent.py --task Isaac-Square-Piper-IK-Rel-v0 --num_envs 1 --teleop_device keyboard --enable_camera --enable_pinocchio --save

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
<diffusion policy 2D, 3D 실행할 때 설치>
pip install dill
pip install diffusers
pip install av
pip install usd-core
pip install threadpoolctl
./isaaclab.sh -p -m pip install fvcore iopath
./isaaclab.sh -p -m pip install "git+https://github.com/facebookresearch/pytorch3d.git" --no-build-isolation
pip install imagecodecs
/workspace/isaaclab/_isaac_sim/python.sh -m pip uninstall numcodecs -y
/workspace/isaaclab/_isaac_sim/python.sh -m pip install numcodecs==0.11.0
/workspace/isaaclab/_isaac_sim/python.sh -m pip uninstall zarr -y
/workspace/isaaclab/_isaac_sim/python.sh -m pip install zarr==2.16.1
/workspace/isaaclab/_isaac_sim/python.sh -m pip install numpy==1.26.4
pip uninstall diffusers transformers huggingface_hub tokenizers -y
pip install diffusers==0.11.1
pip install transformers==4.25.1
pip install huggingface_hub==0.14.1
pip install tokenizers==0.13.2
pip install open3d


<zarr 데이터셋 만들기>
python scripts/imitation_learning/diffusion_policy/diffusion_policy/scripts/conversion_stack.py
python scripts/imitation_learning/diffusion_policy_3d/diffusion_policy_3d/conversion.py
  
  
<diffusion policy 2d low dim 실행>
./isaaclab.sh -p scripts/imitation_learning/diffusion_policy/train.py   --config-name=train_isaaclab_diffusion_transformer_lowdim_workspace   task.dataset.zarr_path=/workspace/isaaclab/scripts/imitation_learning/datasets/blockpush/blockpush_lowdim.zarr
  
  
<diffusion policy 2d 실행>
./isaaclab.sh -p scripts/imitation_learning/diffusion_policy/train.py   --config-name=train_isaaclab_diffusion_unet_image_workspace   task.dataset.zarr_path=/workspace/isaaclab/scripts/imitation_learning/datasets/stack/stack_image.zarr


<diffusion policy 2d gpu 여러 대 사용해서 실행>
./isaaclab.sh -p -m torch.distributed.run --nproc_per_node=2 \
scripts/imitation_learning/diffusion_policy/train.py \
--config-name=train_isaaclab_diffusion_unet_image_workspace \
task.dataset.zarr_path=/workspace/isaaclab/scripts/imitation_learning/datasets/stack/stack_image.zarr


<diffusion policy 2d 체크 포인트 불러와서 eval>
./isaaclab.sh -p scripts/imitation_learning/diffusion_policy/eval.py   --checkpoint=/workspace/isaaclab/scripts/imitation_learning/datasets/stack_ckpt_good/epoch=9850-train_loss=0.000.ckpt   --output_dir=/workspace/isaaclab/scripts/imitation_learning/datasets/stack_output


<diffusion policy 3d 실행>
./isaaclab.sh -p scripts/imitation_learning/diffusion_policy_3d/diffusion_policy_3d/train.py   --config-name=isaaclab_dp3

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
<이미 있는 데이터셋 mimic>
./isaaclab.sh -p scripts/imitation_learning/isaaclab_mimic/annotate_demos.py \
--device cpu --enable_cameras --task Isaac-Stack-Cube-Franka-IK-Rel-Visuomotor-Mimic-v0 --auto \
--input_file ./data_storage/dataset.hdf5 --output_file ./data_storage/dataset15.hdf5


<telop으로 데이터셋 만들기>
./isaaclab.sh -p scripts/tools/record_demos.py --task Isaac-Stack-Cube-Franka-IK-Rel-Visuomotor-v0 --device cpu --teleop_device keyboard --dataset_file ./datasets/dataset3.hdf5 --num_demos 10 --enable_camera


<wandb login>
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

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
<lehome challenge train>
./isaaclab.sh -p lerobot/src/lerobot/scripts/lerobot_train.py --config_path scripts/lehome_challenge/configs/train_dp.yaml


<lehome challenge eval>
./isaaclab.sh -p scripts/lehome_challenge/scripts/eval.py     --policy_type lerobot     --policy_path scripts/outputs/train/dp_top_long/checkpoints/001000/pretrained_model     --garment_type "top_long"     --dataset_root scripts/lehome_challenge/Datasets/example/top_long_merged     --num_episodes 2     --enable_cameras     --device cpu


./isaaclab.sh -p scripts/lehome_challenge/scripts/eval.py     --policy_type lerobot     --policy_path scripts/outputs/train/dp_top_long/checkpoints/001000/pretrained_model     --garment_type "top_long"     --dataset_root scripts/lehome_challenge/Datasets/example/top_long_merged     --num_episodes 2     --enable_cameras     --device cpu      --save_video      --video_dir scripts/lehome_challenge/video      --headless

./isaaclab.sh -p scripts/lehome_challenge/scripts/eval.py     --policy_type lerobot     --policy_path scripts/outputs/train/dp_top_long/checkpoints/001000/pretrained_model     --garment_type "top_long"     --dataset_root scripts/lehome_challenge/Datasets/example/top_long_merged     --num_episodes 2     --enable_cameras      --save_video      --video_dir scripts/lehome_challenge/video      --headless




<lehome challenge 실행할 때 설치>
pip install pyarrow
pip install lerobot --no-deps
pip install datasets
pip install accelerate
pip install av
pip install draccus
pip install diffusers
pip install pyserial
pip install deepdiff
pip install plotly
pip install pynput
pip install open3d
git clone https://github.com/huggingface/lerobot.git


lerobot/src/lerobot/scripts/lerobot_train.py 227번째 줄 if getattr(cfg, "cudnn_deterministic", False):
이걸로 바꾸기




/workspace/isaaclab/_isaac_sim/kit/python/lib/python3.11/site-packages/lerobot/policies/groot/groot_n1.py
176번째 줄에서 
@dataclass
class GR00TN15Config(PretrainedConfig):
    model_type = "gr00t_n1_5"
    backbone_cfg: dict = field(default=None, init=False, metadata={"help": "Backbone configuration."})

    action_head_cfg: dict = field(default=None, init=False, metadata={"help": "Action head configuration."})

    action_horizon: int = field(default=None, init=False, metadata={"help": "Action horizon."})

    action_dim: int = field(default=None, init=False, metadata={"help": "Action dimension."})
    compute_dtype: str = field(default="float32", metadata={"help": "Compute dtype."})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)
            
이걸로 고치기





<lehome 처음 다운받을 때>
apt update
apt install -y git-lfs
git lfs install
cd /workspace/isaaclab/scripts/lehome_challenge
git clone https://huggingface.co/datasets/lehome/asset_challenge Assets

cd /workspace/isaaclab/scripts/lehome_challenge
git clone https://huggingface.co/datasets/lehome/dataset_challenge_merged Datasets/example

"asset_path": "/scripts/lehome_challenge/Assets/objects/Challenge_Garment/Release/Top_Long/Top_Long_Seen_0/TCLC_002_obj_exp.usd",

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
<docker 옮기기>

docker commit <container> isaac-lab-base
docker save -o isaac-lab-s.tar isaac-lab-base
scp -P 2222 isaac-lab-s.tar user@remote-server:/path/
scp -P 2222 isaac-lab-es.tar cv25@10.150.20.249:~/workspaces/eunsong/lab
docker load -i isaac-lab-s.tar


mkdir lab
cd lab
scp -P 2222 -r scanbot@scanbot2.cvlab.kr:~/Desktop/IsaacLab ~/workspaces/eunsong/lab
cd IsaacLab
docker tag isaac-lab-base nvcr.io/nvidia/isaac-sim:5.1.0


du -sh .
du -h --max-depth=1 . | sort -hr


<github login>
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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
isaac-lab-base-es1이 원래 25.6GB로 옮긴 이미지

export NVIDIA_VISIBLE_DEVICES=0
export CUDA_VISIBLE_DEVICES=0

./docker/container.py start --suffix es
./docker/container.py enter --suffix es

nvidia-smi
echo $NVIDIA_VISIBLE_DEVICES
python -c "import torch; print(torch.cuda.device_count())"
python -c "import torch; print(torch.cuda.get_device_name(0))"


export XDG_RUNTIME_DIR=/tmp/runtime-root
mkdir -p /tmp/runtime-root
chmod 700 /tmp/runtime-root
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
<DexGarmentLab 필요한 데이터 다운로드>
/isaac-sim/python.sh Assets/assets_download.py
unzip Robots.zip -d ./Assets
unzip LeapMotion.zip -d ./Assets
unzip Scene.zip -d ./Assets
unzip Garment.zip -d ./Assets
unzip Human.zip -d ./Assets

/isaac-sim/python.sh -m pip install -r requirements.txt


/isaac-sim/python.sh -m pip install --upgrade hydra-core==1.3.2
/isaac-sim/python.sh -m pip uninstall transformers -y
/isaac-sim/python.sh -m pip install transformers==4.26.1


/isaac-sim/python.sh Data/data_download.py
unzip Fling_Dress.zip -d ./Data
unzip Fling_Tops.zip -d ./Data
unzip Fling_Trousers.zip -d ./Data
unzip Fold_Dress.zip -d ./Data
unzip Fold_Tops.zip -d ./Data
unzip Fold_Trousers.zip -d ./Data
unzip Hang_Dress.zip -d ./Data
unzip Hang_Tops.zip -d ./Data
unzip Hang_Trousers.zip -d ./Data
unzip Hang_Coat.zip -d ./Data
unzip Store_Tops.zip -d ./Data
unzip Wear_Baseballcap.zip -d ./Data
unzip Wear_Bowlhat.zip -d ./Data
unzip Wear_Scarf.zip -d ./Data


export PYTHONPATH=$PYTHONPATH:/isaac-sim/extscache/omni.physx.demos-107.3.26+107.3.3.cp311.u353
export PYTHONPATH=$PYTHONPATH:/isaac-sim/extscache/omni.kit.stage_templates-2.0.0+69cbf6ad
export PYTHONPATH=$PYTHONPATH:/isaac-sim/extscache/omni.physx.ui-107.3.26+107.3.3.lx64.r.cp311.u353
export PYTHONPATH=$PYTHONPATH:/isaac-sim/extscache/omni.usdphysics.ui-107.3.26+107.3.3.lx64.r.cp311.u353
export PYTHONPATH=$PYTHONPATH:/isaac-sim/extscache/omni.physx.commands-107.3.26+107.3.3.cp311.u353/omni/physxcommands


<논문에 나오는 HALO 모델>
cd Model_HALO/SADP
/isaac-sim/python.sh -m pip install -e .
cd Model_HALO/SADP
bash data2zarr_sadp.sh Hang_Coat 1 100
bash train.sh Hang_Coat_stage_1 100 42 0 False
bash Validation.sh Hang_Coat 100 100

cd Model_HALO/SADP_G
/isaac-sim/python.sh -m pip install -e .
bash data2zarr_sadp_g.sh Fold_Tops 1 100
bash data2zarr_sadp_g.sh Fold_Tops 2 100
bash data2zarr_sadp_g.sh Fold_Tops 3 100
bash train.sh Fold_Tops_stage_1 100 42 0 False
bash train.sh Fold_Tops_stage_2 100 42 0 False
bash train.sh Fold_Tops_stage_3 100 42 0 False

bash Validation.sh Fold_Tops 1 100

bash data2zarr_sadp_g.sh Fold_Trousers 1 100
bash data2zarr_sadp_g.sh Fold_Trousers 2 100
bash train.sh Fold_Trousers_stage_1 100 42 0 False
bash train.sh Fold_Trousers_stage_2 100 42 0 False

bash Validation.sh Fold_Trousers 1 100
bash Data_Collection.sh Fold_Trousers 10

bash data2zarr_sadp_g.sh Fling_Trousers 1 100
bash train.sh Fling_Trousers_stage_1 100 42 0 False
bash Validation.sh Fling_Trousers 1 100

bash Data_Collection.sh Fold_Tops 10


bash finetune.sh Fold_Trousers_stage_3_source_target 100 42 0 False

<baseline으로 사용하는 diffusion policy 2d>
cd IL_Baselines/Diffusion_Policy
isaac -m pip install -e .



<baseline으로 사용하는 diffusion policy 3d>
cd IL_Baselines/Diffusion_Policy_3D
isaac -m pip install -e .


export QT_X11_NO_MITSHM=1
export XDG_RUNTIME_DIR=/tmp/runtime-$USER
mkdir -p $XDG_RUNTIME_DIR
chmod 700 $XDG_RUNTIME_DIR


