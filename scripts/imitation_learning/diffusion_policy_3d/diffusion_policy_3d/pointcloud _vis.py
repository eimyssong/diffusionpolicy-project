import matplotlib
matplotlib.use('Agg')

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
    z = zarr.open(zarr_path, mode="r")
    pcs = z["data"]["obs"]["point_cloud"]  # (T, N, 6)

    T = pcs.shape[0]

    H, W = 720, 720

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(save_path, fourcc, fps, (W, H))

    # =========================
    # =========================
    all_xyz = pcs[:, :, :3].reshape(-1, 3)

    center = all_xyz.mean(axis=0)
    max_range = (all_xyz.max(axis=0) - all_xyz.min(axis=0)).max() / 2

    scale = 1.2

    xlim = (center[0] - max_range*scale, center[0] + max_range*scale)
    ylim = (center[1] - max_range*scale, center[1] + max_range*scale)
    zlim = (center[2] - max_range*scale, center[2] + max_range*scale)

    # =========================
    # =========================
    for t in tqdm(range(0, T, step)):
        pc = pcs[t]

        xyz = pc[:, :3]

        if pc.shape[1] >= 6:
            rgb = np.clip(pc[:, 3:6], 0, 1)
        else:
            rgb = np.ones_like(xyz)

        fig = plt.figure(figsize=(8, 8), dpi=150)
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter(
            xyz[:, 0],
            xyz[:, 1],
            xyz[:, 2],
            c=rgb,
            s=5
        )

        ax.view_init(elev=30, azim=45)

        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_zlim(zlim)

        ax.set_box_aspect([1, 1, 1])

        ax.set_axis_off()
        ax.set_position([0, 0, 1, 1])

        fig.canvas.draw()
        img = np.asarray(fig.canvas.buffer_rgba())[:, :, :3]
        plt.close(fig)

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
        step=1
    )