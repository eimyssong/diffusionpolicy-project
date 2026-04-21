
A = '/workspace/isaaclab/scripts/imitation_learning/datasets/stack/dataset7(given, pointcloud, color, dataset4).hdf5'
# A = '/workspace/isaaclab/scripts/imitation_learning/datasets/blockpush/dataset1.hdf5'
# A = '/workspace/isaaclab/scripts/imitation_learning/datasets/blockpush/demo_v15.hdf5'
# A = '/workspace/isaaclab/scripts/imitation_learning/datasets/blockpush/annotated_dataset.hdf5'

B = '/workspace/isaaclab/scripts/imitation_learning/datasets/blockpush/blockpush_lowdim.zarr'



import h5py
def print_hdf5_structure(h5_path):
    with h5py.File(h5_path, "r") as f:
        def visitor(name, obj):
            indent = "  " * name.count("/")
            if isinstance(obj, h5py.Group):
                print(f"{indent}📁 {name}/")
            else:
                print(f"{indent}📄 {name}  shape={obj.shape} dtype={obj.dtype}")

        f.visititems(visitor)
print_hdf5_structure(A)




# import zarr

# z = zarr.open(
#     "/workspace/isaaclab/scripts/imitation_learning/datasets/blockpush/blockpush_lowdim.zarr",
#     mode="r"
# )

# print(z.tree())

# print("trajectory:", z["trajectory"].shape)




# import h5py
# import numpy as np

# # 학습에 쓴 hdf5 파일 경로
# dataset_path = A

# with h5py.File(dataset_path, 'r') as f:
#     # 예시로 첫 번째 데모의 EEF 위치 데이터를 꺼내봄
#     # robomimic 구조에 따라 경로가 다를 수 있으니 f.keys()로 확인 필요
#     raw_pos = f['data/demo_0/obs/eef_pos'][:]
#     raw_quat = f['data/demo_0/obs/eef_quat'][:]
#     raw_cube_pose = f['data/demo_0/obs/cube_positions'][:]
#     raw_cube_quat = f['data/demo_0/obs/cube_orientations'][:]
#     raw_gripper = f['data/demo_0/obs/gripper_pos'][:]
#     raw_joint_pos = f['data/demo_0/obs/joint_pos'][:]
#     raw_joint_vel = f['data/demo_0/obs/joint_vel'][:]

    
#     print("\n" + "="*50)
#     print("[Check 2] Raw Dataset Values (HDF5)")
#     # print(f"  - First 5 EEF Positions:\n{raw_pos[:5]}")
#     print(f"  - eef pos Range: {raw_pos.min()} ~ {raw_pos.max()}")

#     # print(f"  - First 5 EEF Positions:\n{raw_quat[:5]}")
#     print(f"  - eef quat Range: {raw_quat.min()} ~ {raw_quat.max()}")

#     # print(f"  - First 5 EEF Positions:\n{raw_cube_pose[:5]}")
#     print(f"  - cuve positions Range: {raw_cube_pose.min()} ~ {raw_cube_pose.max()}")

#     # print(f"  - First 5 EEF Positions:\n{raw_cube_quat[:5]}")
#     print(f"  - cube orientations Range: {raw_cube_quat.min()} ~ {raw_cube_quat.max()}")

#     # print(f"  - First 5 EEF Positions:\n{raw_gripper[:5]}")
#     print(f"  - gripper pos Range: {raw_gripper.min()} ~ {raw_gripper.max()}")

#     # print(f"  - First 5 EEF Positions:\n{raw_joint_pos[:5]}")
#     print(f"  - joint pos Range: {raw_joint_pos.min()} ~ {raw_joint_pos.max()}")

#     # print(f"  - First 5 EEF Positions:\n{raw_joint_vel[:5]}")
#     print(f"  - joint vel Range: {raw_joint_vel.min()} ~ {raw_joint_vel.max()}")        
#     print("="*50)
