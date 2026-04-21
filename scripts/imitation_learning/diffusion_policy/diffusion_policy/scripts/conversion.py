

A = '/workspace/isaaclab/scripts/imitation_learning/datasets/blockpush/dataset.hdf5'
# A = '/workspace/isaaclab/scripts/imitation_learning/datasets/blockpush/demo_v15.hdf5'
# A = '/workspace/isaaclab/scripts/imitation_learning/datasets/blockpush/annotated_dataset.hdf5'

B = '/workspace/isaaclab/scripts/imitation_learning/datasets/blockpush/blockpush_lowdim.zarr'



import h5py
import zarr
import numpy as np
from pathlib import Path

def convert(hdf5_path, zarr_path):
    h5 = h5py.File(hdf5_path, "r")

    obs_list = []
    action_list = []
    episode_ends = []

    total_steps = 0

    demos = sorted([k for k in h5["data"].keys() if k.startswith("demo_")])

    for demo in demos:
        g = h5["data"][demo]

        action = g["actions"][:]            # (T, 7)

        obs = np.concatenate([
            g["obs"]["cube_orientations"][:],   # (T, 12)    
            g["obs"]["cube_positions"][:],      # (T, 9)                    
            g["obs"]["eef_pos"][:],             # (T, 3)
            g["obs"]["eef_quat"][:],            # (T, 4)
            g["obs"]["gripper_pos"][:],         # (T, 2)
            g["obs"]["joint_pos"][:],           # (T, 9)
            g["obs"]["joint_vel"][:]            # (T, 9)
        ], axis=1).astype(np.float32)

        assert obs.shape[1] == 48

        obs_list.append(obs)
        action_list.append(action)

        total_steps += obs.shape[0]
        episode_ends.append(total_steps)



    obs = np.concatenate(obs_list, axis=0)
    action = np.concatenate(action_list, axis=0)

    z = zarr.open(zarr_path, mode="w")

    data = z.create_group("data")
    data.create_dataset("obs", data=obs, chunks=(1024, obs.shape[1]))
    data.create_dataset("action", data=action, chunks=(1024, action.shape[1]))

    meta = z.create_group("meta")
    meta.create_dataset("episode_ends", data=np.array(episode_ends, dtype=np.int64))


if __name__ == "__main__":
    convert(
        hdf5_path=A,
        zarr_path=B
    )