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

현재 로컬 작업은 아래 주요 커밋들에 들어 있다. README를 추가로 수정하면 더 최신 커밋이 앞에 생길 수 있으므로, 최종 확인은 `git log --oneline -5`로 한다.

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
   git log --oneline -5
   ```

   최소한 아래 주요 커밋들이 보여야 한다. README를 나중에 다시 수정했다면 더 최신 커밋이 위에 추가로 있을 수 있다.

   ```text
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
  git log --oneline -5
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
