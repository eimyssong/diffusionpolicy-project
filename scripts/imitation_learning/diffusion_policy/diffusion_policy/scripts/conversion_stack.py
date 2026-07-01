

# A = '/workspace/isaaclab/scripts/imitation_learning/datasets/stack/dataset3.hdf5'
# # A = '/workspace/isaaclab/scripts/imitation_learning/datasets/blockpush/demo_v15.hdf5'
# # A = '/workspace/isaaclab/scripts/imitation_learning/datasets/blockpush/annotated_dataset.hdf5'

# B = '/workspace/isaaclab/scripts/imitation_learning/datasets/stack/stack_image.zarr'


# import h5py
# import zarr
# import numpy as np
# from pathlib import Path
# import tqdm

# def convert(hdf5_path, zarr_path):
#     h5 = h5py.File(hdf5_path, "r")
#     z = zarr.open(zarr_path, mode="w")
#     data_group = z.create_group("data")
#     obs_group = data_group.create_group("obs")

#     demos = sorted([k for k in h5["data"].keys() if k.startswith("demo_")])
    
#     img_agent_list = []
#     img_wrist_list = []
#     eef_pos_list = []
#     eef_quat_list = []
#     gripper_pos_list = []
#     action_list = []
#     episode_ends = []
#     total_steps = 0

#     for demo in tqdm.tqdm(demos):
#         g = h5["data"][demo]

#         img_agent_list.append(g["obs"]["table_cam"][:])
#         # print(g["obs"]["table_cam"][:].shape) # (T, 200, 200, 3)
#         img_wrist_list.append(g["obs"]["wrist_cam"][:])
#         eef_pos_list.append(g["obs"]["eef_pos"][:])
#         eef_quat_list.append(g["obs"]["eef_quat"][:])
#         gripper_pos_list.append(g["obs"]["gripper_pos"][:])
#         action_list.append(g["actions"][:])
#         total_steps += g["actions"].shape[0]
#         episode_ends.append(total_steps)

#     def stack_and_transpose(lst):
#         res = np.concatenate(lst, axis=0)
#         if res.ndim == 4: 
#             res = res.transpose(0, 3, 1, 2)
#         return res

#     obs_group.create_dataset("agentview_image", data=stack_and_transpose(img_agent_list), chunks=(1, 3, 200, 200), dtype='uint8')
#     obs_group.create_dataset("robot0_eye_in_hand_image", data=stack_and_transpose(img_wrist_list), chunks=(1, 3, 200, 200), dtype='uint8')
#     obs_group.create_dataset("robot0_eef_pos", data=np.concatenate(eef_pos_list, axis=0), chunks=(1024, 3))
#     obs_group.create_dataset("robot0_eef_quat", data=np.concatenate(eef_quat_list, axis=0), chunks=(1024, 4))
#     obs_group.create_dataset("robot0_gripper_qpos", data=np.concatenate(gripper_pos_list, axis=0), chunks=(1024, 2))
#     data_group.create_dataset("action", data=np.concatenate(action_list, axis=0), chunks=(1024, 7))
#     meta_group = z.create_group("meta")
#     meta_group.create_dataset("episode_ends", data=np.array(episode_ends, dtype=np.int64))


# if __name__ == "__main__":
#     convert(hdf5_path=A,
#             zarr_path=B)




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
    
    img_agent_list = []
    img_wrist_list = []
    eef_pos_list = []
    eef_quat_list = []
    gripper_pos_list = []
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

        def preprocess_depth(imgs, depth_min=0.0, depth_max=2.0):
            processed_imgs = []
            for i in range(imgs.shape[0]):
                depth_np = np.squeeze(imgs[i])
                depth_np = np.clip(depth_np, depth_min, depth_max)

                if depth_max>depth_min:
                    depth_normalized = (depth_np - depth_min) / (depth_max - depth_min) * 255.0
                else:
                    depth_normalized = np.zeros_like(depth_np)
                depth_img = depth_normalized

                img_resized = cv2.resize(depth_img, target_size, interpolation=cv2.INTER_NEAREST)
                img_chw = img_resized
                img_chw = np.expand_dims(img_chw, axis=-1)
                processed_imgs.append(img_chw)
            return np.stack(processed_imgs, axis=0)


        table = g["obs"]["table_cam_depth"][:]
        wrist = g["obs"]["wrist_cam_depth"][:]

        # print(np.percentile(table, 80))
        # print(np.percentile(wrist, 80))

        # has_nan1 = np.isnan(table).any(axis=(1, 2, 3))
        # nan_indices1 = np.where(has_nan1)[0]
        # print(nan_indices1)

        # has_nan2 = np.isnan(wrist).any(axis=(1, 2, 3))
        # nan_indices2 = np.where(has_nan2)[0]
        # print(nan_indices2)

        # has_inf1 = np.isinf(table).any(axis=(1, 2, 3))
        # inf_indices1 = np.where(has_inf1)[0]
        # print(inf_indices1)

        # has_inf2 = np.isinf(wrist).any(axis=(1, 2, 3))
        # inf_indices2 = np.where(has_inf2)[0]
        # print(inf_indices2)


        table_rgbd = np.concatenate([preprocess_image(g["obs"]["table_cam"][:]), preprocess_depth(g["obs"]["table_cam_depth"][:])], axis=-1)
        wrist_rgbd = np.concatenate([preprocess_image(g["obs"]["wrist_cam"][:]), preprocess_depth(g["obs"]["wrist_cam_depth"][:])], axis=-1)

        img_agent_list.append(table_rgbd)
        img_wrist_list.append(wrist_rgbd)

        # img_agent_list.append(preprocess_image(g["obs"]["table_cam"][:]))
        # img_wrist_list.append(preprocess_image(g["obs"]["wrist_cam"][:]))



        eef_pos_list.append(g["obs"]["eef_pos"][:])
        eef_quat_list.append(g["obs"]["eef_quat"][:])
        gripper_pos_list.append(g["obs"]["gripper_pos"][:])
        action_list.append(g["actions"][:])
        total_steps += g["actions"].shape[0]
        episode_ends.append(total_steps)

    def stack_data(lst):
        return np.concatenate(lst, axis=0)


    print(len(img_agent_list))
    obs_group.create_dataset("table_cam", data=stack_data(img_agent_list), chunks=(1, 84, 84, 4), dtype='uint8')
    obs_group.create_dataset("wrist_cam", data=stack_data(img_wrist_list), chunks=(1, 84, 84, 4), dtype='uint8')
    

    print(np.min(obs_group["table_cam"][:,:,:,3]), np.max(obs_group["table_cam"][:,:,:,:3]))
    print(np.min(obs_group["wrist_cam"][:,:,:,3]), np.max(obs_group["wrist_cam"][:,:,:,:3]))

    obs_group.create_dataset("eef_pos", data=stack_data(eef_pos_list), chunks=(1024, 3))
    obs_group.create_dataset("eef_quat", data=stack_data(eef_quat_list), chunks=(1024, 4))
    obs_group.create_dataset("gripper_pos", data=stack_data(gripper_pos_list), chunks=(1024, 2))
    data_group.create_dataset("action", data=stack_data(action_list), chunks=(1024, 7))
    
    meta_group = z.create_group("meta")
    meta_group.create_dataset("episode_ends", data=np.array(episode_ends, dtype=np.int64))

if __name__ == "__main__":
    A = '/workspace/isaaclab/scripts/imitation_learning/datasets/stack/dataset3(my, rgb).hdf5'
    B = '/workspace/isaaclab/scripts/imitation_learning/datasets/stack/stack_image.zarr'
    convert(hdf5_path=A, zarr_path=B)

