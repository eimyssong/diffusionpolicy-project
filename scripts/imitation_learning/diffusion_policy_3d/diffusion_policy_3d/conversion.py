import h5py
import zarr
import numpy as np
import cv2  
from pathlib import Path
import tqdm
from PIL import Image

def convert(hdf5_path, zarr_path):
    h5 = h5py.File(hdf5_path, "r")
    z = zarr.open(zarr_path, mode="w")
    data_group = z.create_group("data")
    obs_group = data_group.create_group("obs")

    demos = sorted([k for k in h5["data"].keys() if k.startswith("demo_")])
    
    img_list = []
    pointcloud_list = []
    agent_pos_list = []
    action_list = []
    episode_ends = []
    total_steps = 0

    target_size = (84, 84)

    for demo in tqdm.tqdm(demos):
        g = h5["data"][demo]

        def preprocess_image(imgs):
            processed_imgs = []
            for i in range(imgs.shape[0]):
                img_resized = cv2.resize(imgs[i], target_size, interpolation=cv2.INTER_AREA)
                img_chw = img_resized
                processed_imgs.append(img_chw)
            return np.stack(processed_imgs, axis=0)


        def preprocess_pointcloud(pointcloud, num_points=512):           
            xmin, xmax = -2.0, 2.0   
            ymin, ymax = -2.0, 2.0   
            zmin, zmax = 0.01, 2.0 

            processed = []

            for pc in pointcloud:
                mask = (
                    (pc[:,0] > xmin) & (pc[:,0] < xmax) &
                    (pc[:,1] > ymin) & (pc[:,1] < ymax) &
                    (pc[:,2] > zmin) & (pc[:,2] < zmax)
                )
                pc = pc[mask]

                if pc.shape[0] >= num_points:
                    sampled = []
                    sampled_idx = np.zeros(num_points, dtype=int)
                    sampled_idx[0] = np.random.randint(pc.shape[0])
                    coords = pc[:, :3] 
                    distances = np.linalg.norm(coords - coords[sampled_idx[0]], axis=1)

                    for i in range(1, num_points):
                        sampled_idx[i] = np.argmax(distances)
                        dist_new = np.linalg.norm(coords - coords[sampled_idx[i]], axis=1)
                        distances = np.minimum(distances, dist_new)
                    pc_sampled = pc[sampled_idx] 

                else:
                    pad = num_points - pc.shape[0]
                    pc_sampled = np.pad(pc, ((0,pad),(0,0)))

                processed.append(pc_sampled)

            return np.stack(processed)

        table_pointcloud = preprocess_pointcloud(g["obs"]["table_cam_pointcloud"][:], 2048)
        pointcloud_list.append(table_pointcloud)

        pos = np.concatenate([g["obs"]["eef_pos"][:], g["obs"]["eef_quat"][:], g["obs"]["gripper_pos"][:]], axis=-1)
        agent_pos_list.append(pos)

        action_list.append(g["actions"][:])
        total_steps += g["actions"].shape[0]
        episode_ends.append(total_steps)

    def stack_data(lst):
        return np.concatenate(lst, axis=0)

    obs_group.create_dataset("point_cloud", data=stack_data(pointcloud_list), chunks=(1, 2048, 6))
    obs_group.create_dataset("agent_pos", data=stack_data(agent_pos_list), chunks=(1024, 9))
    data_group.create_dataset("action", data=stack_data(action_list), chunks=(1024, 7))
    
    meta_group = z.create_group("meta")
    meta_group.create_dataset("episode_ends", data=np.array(episode_ends, dtype=np.int64))

if __name__ == "__main__":
    A = '/workspace/isaaclab/scripts/imitation_learning/datasets/DP3/dataset14.hdf5'
    B = '/workspace/isaaclab/scripts/imitation_learning/datasets/DP3/stack_image.zarr'
    convert(hdf5_path=A, zarr_path=B)





