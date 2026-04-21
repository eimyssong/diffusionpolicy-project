import matplotlib
matplotlib.use('Agg')  # 서버/도커 필수

import zarr
import numpy as np
import matplotlib.pyplot as plt
import cv2
from tqdm import tqdm


def visualize_pointcloud_to_video(
    zarr_path,
    save_path="pointcloud.mp4",
    fps=20,
    step=1
):
    # zarr 열기
    z = zarr.open(zarr_path, mode="r")
    pcs = z["data"]["obs"]["point_cloud"]  # (T, N, 6)

    T = pcs.shape[0]

    # 🎥 영상 해상도 (크게!)
    H, W = 720, 720

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(save_path, fourcc, fps, (W, H))

    # =========================
    # 1. 전체 데이터 기준으로 범위 고정
    # =========================
    all_xyz = pcs[:, :, :3].reshape(-1, 3)

    center = all_xyz.mean(axis=0)
    max_range = (all_xyz.max(axis=0) - all_xyz.min(axis=0)).max() / 2

    scale = 1.2  # zoom 정도 (작을수록 확대)

    xlim = (center[0] - max_range*scale, center[0] + max_range*scale)
    ylim = (center[1] - max_range*scale, center[1] + max_range*scale)
    zlim = (center[2] - max_range*scale, center[2] + max_range*scale)

    # =========================
    # 2. 프레임 루프
    # =========================
    for t in tqdm(range(0, T, step)):
        pc = pcs[t]

        xyz = pc[:, :3]

        if pc.shape[1] >= 6:
            rgb = np.clip(pc[:, 3:6], 0, 1)
        else:
            rgb = np.ones_like(xyz)

        # 고해상도 figure
        fig = plt.figure(figsize=(8, 8), dpi=150)
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter(
            xyz[:, 0],
            xyz[:, 1],
            xyz[:, 2],
            c=rgb,
            s=5
        )

        # 카메라 완전 고정
        ax.view_init(elev=30, azim=45)

        # 고정된 축 사용 (핵심!)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_zlim(zlim)

        # 비율 고정 (왜곡 방지)
        ax.set_box_aspect([1, 1, 1])

        # 여백 제거
        ax.set_axis_off()
        ax.set_position([0, 0, 1, 1])

        # 이미지 변환 (최신 방식)
        fig.canvas.draw()
        img = np.asarray(fig.canvas.buffer_rgba())[:, :, :3]
        plt.close(fig)

        # OpenCV 변환
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img = cv2.resize(img, (W, H))

        video.write(img)

    video.release()
    print(f"Saved video to {save_path}")


if __name__ == "__main__":
    zarr_path = "/workspace/isaaclab/scripts/imitation_learning/datasets/DP3/stack_image.zarr"

    visualize_pointcloud_to_video(
        zarr_path,
        save_path="pointcloud.mp4",
        fps=20,
        step=1   # 느리면 2~5로 올려
    )