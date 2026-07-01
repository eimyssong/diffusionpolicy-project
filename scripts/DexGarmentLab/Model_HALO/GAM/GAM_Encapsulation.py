# import os
# import sys
# import random
# import numpy as np
# import torch
# import open3d as o3d
# from termcolor import cprint


# sys.path.append(os.getcwd()) # change to your specific path
# sys.path.append("Model_HALO/GAM")
# from Model_HALO.GAM.model.pointnet2_GAM import GAM_Model
# from Env_Config.Utils_Project.Point_Cloud_Manip import furthest_point_sampling, normalize_pcd_points_xy, visualize_pointcloud_with_colors, colormap

# import torch.nn.functional as F


# class GAM_Encapsulation:
    
#     def __init__(self, catogory:str="Tops_LongSleeve"):
#         '''
#         load model
#         '''
#         self.catogory = catogory
#         # set resume path
#         resume_path = f"Model_HALO/GAM/checkpoints/{self.catogory}/checkpoint.pth"
#         # resume_path = f"Model_HALO/GAM/checkpoints/Trousers/checkpoint.pth"
#         # set seed
#         seed = 42
#         torch.manual_seed(seed)
#         torch.cuda.manual_seed(seed)  
#         torch.cuda.manual_seed_all(seed)  
#         np.random.seed(seed)
#         random.seed(seed)
#         # define model
#         self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
#         self.model = GAM_Model(normal_channel=False, feature_dim=512).cuda()
#         self.model.load_state_dict(torch.load(resume_path, weights_only=False))
#         self.model = self.model.to(self.device)
#         self.model.eval()

    
#     def get_feature(self, input_pcd:np.ndarray, index_list:list=None):
#         '''
#         get feature of input point cloud
#         '''
#         normalized_pcd, *_ = normalize_pcd_points_xy(input_pcd)
#         normalize_pcd = np.expand_dims(normalized_pcd, axis=0)
        
#         with torch.no_grad():
        
#             pcd_features = self.model(
#                 torch.from_numpy(normalize_pcd).to(self.device).float(),
#             ).squeeze(0)
#             # print(pcd_features.shape)
        
#         if index_list is not None:
#             target_features_list = []
#             for i in index_list:
#                 target_features_list.append(pcd_features[i])
#             return torch.stack(target_features_list)
#         else:
#             return pcd_features
        
#     def get_manipulation_points(self, input_pcd:np.ndarray, index_list:list=None):
#         '''
#         get manipulation points of input point cloud
#         '''
#         #get model output (feature)
#         demo_pcd = o3d.io.read_point_cloud(f"Model_HALO/GAM/checkpoints/{self.catogory}/demo_garment.ply").points
#         print('ddd', np.array(demo_pcd).shape)

#         demo_feature = self.get_feature(demo_pcd, index_list)
#         manipulate_feature = self.get_feature(input_pcd)
        
#         # normalize feature
#         demo_feature_normalized = torch.nn.functional.normalize(demo_feature, p=2, dim=1)
#         manipulate_feature_normalized = torch.nn.functional.normalize(manipulate_feature, p=2, dim=1)
#         result = torch.matmul(demo_feature_normalized, manipulate_feature_normalized.T)
        
#         cprint("----------- GAM Inference Begin -----------", color="blue", attrs=["bold"])
        
#         # get max similarity score and indices
#         max_values, max_indices = torch.max(result, dim=1)
#         cprint(f"similarity score: {max_values}", color="blue")
#         cprint(f"relevant indices: {max_indices}", color="blue")
#         cprint(f"similarity result shape: {result.shape}", color="blue")
#         # get manipulation points
#         manipulation_points = input_pcd[max_indices.detach().cpu().numpy()]

#         cprint(f"manipulation points: \n {manipulation_points}", color="blue")
        
#         cprint("----------- GAM Inference End -----------", color="blue", attrs=["bold"])
        
#         return manipulation_points, max_indices.detach().cpu().numpy(), result.cpu().numpy()
    
#     def get_colormap_points(self, input_pcd:np.ndarray):
#         '''
#         get colors for each corresponding point in input pcd.
#         '''
        
#         #get model output (feature)
#         demo_pcd = o3d.io.read_point_cloud(f"Model_HALO/GAM/checkpoints/{self.catogory}/demo_garment.ply").points
#         demo_feature = self.get_feature(demo_pcd)
#         manipulate_feature = self.get_feature(input_pcd)
        
#         # normalize feature
#         demo_feature_normalized = torch.nn.functional.normalize(demo_feature, p=2, dim=1)
#         manipulate_feature_normalized = torch.nn.functional.normalize(manipulate_feature, p=2, dim=1)

#         result = torch.matmul(manipulate_feature_normalized, demo_feature_normalized.T)
        
#         # get max similarity score and indices
#         max_values, max_indices = torch.max(result, dim=1)
#         print("similarity score: ", max_values)
#         print("relevant indices: ", max_indices)
        
#         # get manipulation points
#         corresponding_demo_color = input_pcd[max_indices.detach().cpu().numpy()]
#         print("manipulation points: \n", corresponding_demo_color)
#         return corresponding_demo_color, max_indices.detach().cpu().numpy()
    
#     def get_demo_garment_with_color(self):
#         '''
#         get demo garment with color
#         '''
#         demo_pcd = o3d.io.read_point_cloud(f"Model_HALO/GAM/checkpoints/{self.catogory}/demo_garment.ply")
#         self.demo_points = np.asarray(demo_pcd.points)
#         self.demo_points_color = colormap(self.demo_points)
#         return self.demo_points, self.demo_points_color
    
#     def visualize_pcd_corresponce(self, input_pcd:np.ndarray, save_or_not:bool=False, save_path:str=None):
#         '''
#         visualize exact point corresponce between input pcd and demo garment.
#         '''
#         # visualize demo garment with color
#         self.get_demo_garment_with_color()
#         visualize_pointcloud_with_colors(self.demo_points, self.demo_points_color)
#         index_list = list(range(len(self.demo_points)))
#         print("index_list: ", index_list)
#         print("len(index_list): ", len(index_list))
#         _, color_indices = self.get_colormap_points(input_pcd)
#         # visualize input pcd with color
#         color = np.ones_like(input_pcd)
#         for i in range(len(color_indices)):
#             color[i] = self.demo_points_color[color_indices[i]]
#         print("color: ", color)
#         visualize_pointcloud_with_colors(input_pcd, color, save_or_not=save_or_not, save_path=save_path)

















# import os
# import sys
# import random
# import numpy as np
# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# import open3d as o3d
# from termcolor import cprint

# sys.path.append(os.getcwd()) # change to your specific path
# sys.path.append("Model_HALO/GAM")
# from Model_HALO.GAM.model.pointnet2_GAM import GAM_Model
# from Env_Config.Utils_Project.Point_Cloud_Manip import furthest_point_sampling, normalize_pcd_points_xy, visualize_pointcloud_with_colors, colormap


# class GAM_Encapsulation:
    
#     def __init__(self, catogory:str="Tops_LongSleeve"):
#         '''
#         load model
#         '''
#         self.catogory = catogory
#         resume_path = f"Model_HALO/GAM/checkpoints/{self.catogory}/checkpoint.pth"
        
#         seed = 42
#         torch.manual_seed(seed)
#         torch.cuda.manual_seed(seed)  
#         torch.cuda.manual_seed_all(seed)  
#         np.random.seed(seed)
#         random.seed(seed)
        
#         self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
#         self.model = GAM_Model(normal_channel=False, feature_dim=512).cuda()
#         self.model.load_state_dict(torch.load(resume_path, weights_only=False))
#         self.model = self.model.to(self.device)
#         self.model.eval()
        
#         # -----------------------------------------------------------------
#         # -----------------------------------------------------------------
#         self.feature_dim = 512
#         self.fusion_mlp = nn.Sequential(
#             nn.Linear(self.feature_dim * 2, self.feature_dim),
#             nn.BatchNorm1d(self.feature_dim),
#             nn.ReLU(),
#             nn.Linear(self.feature_dim, self.feature_dim)
#         ).to(self.device)

#     def fuse_features(self, local_features):
#         '''
#         local_features: (N, D)
#         '''
#         global_feature = torch.max(local_features, dim=0, keepdim=True)[0]
#         global_feature_expand = global_feature.expand(local_features.shape[0], -1)
        
#         fused = torch.cat([local_features, global_feature_expand], dim=-1)
#         return self.fusion_mlp(fused)

#     def augment_pointcloud(self, points):
#         pts = points.copy()
#         # Rotation around Z
#         theta = np.random.uniform(-np.pi, np.pi)
#         R = np.array([
#             [np.cos(theta), -np.sin(theta), 0],
#             [np.sin(theta),  np.cos(theta), 0],
#             [0,              0,             1]
#         ])
#         pts = pts @ R.T
#         # Scale
#         scale = np.random.uniform(0.95, 1.05)
#         pts *= scale
#         # Jitter
#         pts += np.random.normal(0, 0.003, pts.shape)
#         return pts

#     def train(self, input_pcd:np.ndarray, num_epochs=10000, topk_geom=500, sigma=0.02):
#         '''
#         '''
#         self.model.train()
#         self.fusion_mlp.train()

#         optimizer = torch.optim.Adam(
#             list(self.model.parameters()) + list(self.fusion_mlp.parameters()), 
#             lr=1e-5
#         )

#         pcd = np.asarray(input_pcd).copy()

#         for epoch in range(num_epochs):
#             optimizer.zero_grad()

#             view1_np = self.augment_pointcloud(pcd)
#             view2_np = self.augment_pointcloud(pcd)

#             view1_norm, *_ = normalize_pcd_points_xy(view1_np)
#             view2_norm, *_ = normalize_pcd_points_xy(view2_np)

#             v1_coord = torch.from_numpy(view1_norm).float().to(self.device)
#             v2_coord = torch.from_numpy(view2_norm).float().to(self.device)

#             dist_matrix = torch.cdist(v1_coord, v2_coord)
            
#             topk_dist, topk_idx = torch.topk(dist_matrix, k=topk_geom, dim=-1, largest=False)
            
#             soft_weights = torch.exp(-topk_dist**2 / (2 * sigma**2))
#             soft_weights = soft_weights / (soft_weights.sum(dim=-1, keepdim=True) + 1e-8)
            
#             soft_targets = torch.zeros_like(dist_matrix)
#             soft_targets.scatter_(1, topk_idx, soft_weights)

#             feat1_raw = self.model(v1_coord.unsqueeze(0)).squeeze(0) # (N, D)
#             feat2_raw = self.model(v2_coord.unsqueeze(0)).squeeze(0) # (N, D)

#             feat1 = self.fuse_features(feat1_raw)
#             feat2 = self.fuse_features(feat2_raw)

#             feat1 = F.normalize(feat1, dim=1)
#             feat2 = F.normalize(feat2, dim=1)

#             logits = torch.matmul(feat1, feat2.T) / 0.07 # (N, N)
#             log_probs = F.log_softmax(logits, dim=-1)
            
#             loss = -(soft_targets * log_probs).sum(dim=-1).mean()

#             loss.backward()
#             optimizer.step()

#             if epoch % 100 == 0 or epoch == num_epochs - 1:
#                 print(f"Epoch {epoch}: Loss = {loss.item():.4f}")
        
#         self.model.eval()
#         self.fusion_mlp.eval()

#     def get_feature(self, input_pcd:np.ndarray, index_list:list=None):
#         '''
#         '''
#         normalized_pcd, *_ = normalize_pcd_points_xy(input_pcd)
#         normalize_pcd = np.expand_dims(normalized_pcd, axis=0)
        
#         with torch.no_grad():
#             raw_features = self.model(
#                 torch.from_numpy(normalize_pcd).to(self.device).float(),
#             ).squeeze(0)
            
#             pcd_features = self.fuse_features(raw_features)
        
#         if index_list is not None:
#             target_features_list = []
#             for i in index_list:
#                 target_features_list.append(pcd_features[i])
#             return torch.stack(target_features_list)
#         else:
#             return pcd_features
        
#     def get_manipulation_points(self, input_pcd:np.ndarray, index_list:list=None):
#         '''
#         get manipulation points of input point cloud
#         '''
#         demo_pcd = o3d.io.read_point_cloud(f"Model_HALO/GAM/checkpoints/{self.catogory}/demo_garment.ply").points

#         self.train(demo_pcd)

#         demo_feature = self.get_feature(demo_pcd, index_list)
#         manipulate_feature = self.get_feature(input_pcd)
        
#         demo_feature_normalized = torch.nn.functional.normalize(demo_feature, p=2, dim=1)
#         manipulate_feature_normalized = torch.nn.functional.normalize(manipulate_feature, p=2, dim=1)
#         result = torch.matmul(demo_feature_normalized, manipulate_feature_normalized.T) # (M, N)
        
#         cprint("----------- GAM Inference Begin -----------", color="blue", attrs=["bold"])
        
#         # -----------------------------------------------------------------
#         # -----------------------------------------------------------------
#         topk_inf = 30
#         values, indices = torch.topk(result, topk_inf, dim=1) # (M, topk_inf)
        
#         weights = F.softmax(values / 0.02, dim=1).cpu().numpy() # (M, topk_inf)
#         indices_np = indices.cpu().numpy() # (M, topk_inf)

#         manipulation_points = np.zeros((result.shape[0], 3))
#         for i in range(result.shape[0]):
#             neighbor_points = input_pcd[indices_np[i]] # (topk_inf, 3)
#             manipulation_points[i] = np.sum(neighbor_points * weights[i][:, np.newaxis], axis=0)

#         cprint(f"similarity result shape: {result.shape}", color="blue")
#         cprint(f"manipulation points (Soft-Averaged): \n {manipulation_points}", color="blue")
#         cprint("----------- GAM Inference End -----------", color="blue", attrs=["bold"])
        
#         return manipulation_points, indices_np[:, 0], result.cpu().numpy()
    
#     def get_colormap_points(self, input_pcd:np.ndarray):
#         '''
#         get colors for each corresponding point in input pcd.
#         '''
#         demo_pcd = o3d.io.read_point_cloud(f"Model_HALO/GAM/checkpoints/{self.catogory}/demo_garment.ply").points
#         demo_feature = self.get_feature(demo_pcd)
#         manipulate_feature = self.get_feature(input_pcd)
        
#         demo_feature_normalized = torch.nn.functional.normalize(demo_feature, p=2, dim=1)
#         manipulate_feature_normalized = torch.nn.functional.normalize(manipulate_feature, p=2, dim=1)

#         result = torch.matmul(manipulate_feature_normalized, demo_feature_normalized.T)
        
#         max_values, max_indices = torch.max(result, dim=1)
#         print("similarity score: ", max_values)
#         print("relevant indices: ", max_indices)
        
#         corresponding_demo_color = input_pcd[max_indices.detach().cpu().numpy()]
#         print("manipulation points: \n", corresponding_demo_color)
#         return corresponding_demo_color, max_indices.detach().cpu().numpy()
    
#     def get_demo_garment_with_color(self):
#         demo_pcd = o3d.io.read_point_cloud(f"Model_HALO/GAM/checkpoints/{self.catogory}/demo_garment.ply")
#         self.demo_points = np.asarray(demo_pcd.points)
#         self.demo_points_color = colormap(self.demo_points)
#         return self.demo_points, self.demo_points_color
    
#     def visualize_pcd_corresponce(self, input_pcd:np.ndarray, save_or_not:bool=False, save_path:str=None):
#         self.get_demo_garment_with_color()
#         visualize_pointcloud_with_colors(self.demo_points, self.demo_points_color)
#         index_list = list(range(len(self.demo_points)))
#         _, color_indices = self.get_colormap_points(input_pcd)
#         color = np.ones_like(input_pcd)
#         for i in range(len(color_indices)):
#             color[i] = self.demo_points_color[color_indices[i]]
#         visualize_pointcloud_with_colors(input_pcd, color, save_or_not=save_or_not, save_path=save_path)

























# import os
# import sys
# import random
# import numpy as np
# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# import open3d as o3d
# from termcolor import cprint

# sys.path.append(os.getcwd()) # change to your specific path
# sys.path.append("Model_HALO/GAM")
# from Model_HALO.GAM.model.pointnet2_GAM import GAM_Model
# from Env_Config.Utils_Project.Point_Cloud_Manip import furthest_point_sampling, normalize_pcd_points_xy, visualize_pointcloud_with_colors, colormap


# class GAM_Encapsulation:
    
#     def __init__(self, catogory:str="Tops_LongSleeve"):
#         '''
#         load model
#         '''
#         self.catogory = catogory
#         resume_path = f"Model_HALO/GAM/checkpoints/{self.catogory}/checkpoint.pth"
        
#         seed = 42
#         torch.manual_seed(seed)
#         torch.cuda.manual_seed(seed)  
#         torch.cuda.manual_seed_all(seed)  
#         np.random.seed(seed)
#         random.seed(seed)
        
#         self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
#         self.model = GAM_Model(normal_channel=False, feature_dim=512).cuda()
#         self.model.load_state_dict(torch.load(resume_path, weights_only=False))
#         self.model = self.model.to(self.device)
#         self.model.eval()
        
#         self.feature_dim = 512
#         self.fusion_mlp = nn.Sequential(
#             nn.Linear(self.feature_dim * 2, self.feature_dim),
#             nn.BatchNorm1d(self.feature_dim),
#             nn.ReLU(),
#             nn.Linear(self.feature_dim, self.feature_dim)
#         ).to(self.device)

#     def fuse_features(self, local_features):
#         global_feature = torch.max(local_features, dim=0, keepdim=True)[0]
#         global_feature_expand = global_feature.expand(local_features.shape[0], -1)
#         fused = torch.cat([local_features, global_feature_expand], dim=-1)
#         return self.fusion_mlp(fused)

#     def augment_pointcloud(self, points):
#         pts = points.copy()
#         theta = np.random.uniform(-np.pi, np.pi)
#         R = np.array([
#             [np.cos(theta), -np.sin(theta), 0],
#             [np.sin(theta),  np.cos(theta), 0],
#             [0,              0,             1]
#         ])
#         pts = pts @ R.T
#         scale = np.random.uniform(0.95, 1.05)
#         pts *= scale
#         pts += np.random.normal(0, 0.003, pts.shape)
#         return pts

#     # -----------------------------------------------------------------
#     # -----------------------------------------------------------------
#     def train(self, garment_source, num_epochs=1000, topk_geom=50, sigma=0.02):
#         '''
#         '''
#         file_list = []
        
#         if isinstance(garment_source, str):
#             if os.path.isdir(garment_source):
#                 file_list = [os.path.join(garment_source, f) for f in os.listdir(garment_source) if f.endswith(('.ply', '.pcd'))]
#             elif os.path.isfile(garment_source) and garment_source.endswith('.txt'):
#                 with open(garment_source, 'r') as f:
#                     file_list = [line.strip() for line in f.readlines() if line.strip() and os.path.exists(line.strip())]
#             else:
#                 if os.path.exists(garment_source):
#                     file_list = [garment_source]
#         elif isinstance(garment_source, list):
#             file_list = [f for f in garment_source if os.path.exists(f)]

#         if not file_list:
#             return

#         all_garment_pcds = []
#         for path in file_list:
#             pcd_data = o3d.io.read_point_cloud(path)
#             all_garment_pcds.append(np.asarray(pcd_data.points))

#         self.model.train()
#         self.fusion_mlp.train()

#         optimizer = torch.optim.Adam(
#             list(self.model.parameters()) + list(self.fusion_mlp.parameters()), 
#             lr=1e-5
#         )

#         cprint(f"Epochs: {num_epochs}", color="yellow", attrs=["bold"])

#         for epoch in range(num_epochs):
#             random.shuffle(all_garment_pcds)
#             epoch_loss = 0.0

#             for pcd in all_garment_pcds:
#                 optimizer.zero_grad()

#                 view1_np = self.augment_pointcloud(pcd)
#                 view2_np = self.augment_pointcloud(pcd)

#                 view1_norm, *_ = normalize_pcd_points_xy(view1_np)
#                 view2_norm, *_ = normalize_pcd_points_xy(view2_np)

#                 v1_coord = torch.from_numpy(view1_norm).float().to(self.device)
#                 v2_coord = torch.from_numpy(view2_norm).float().to(self.device)

#                 dist_matrix = torch.cdist(v1_coord, v2_coord)
                
#                 actual_k = min(topk_geom, dist_matrix.shape[-1])
#                 topk_dist, topk_idx = torch.topk(dist_matrix, k=actual_k, dim=-1, largest=False)
                
#                 soft_weights = torch.exp(-topk_dist**2 / (2 * sigma**2))
#                 soft_weights = soft_weights / (soft_weights.sum(dim=-1, keepdim=True) + 1e-8)
                
#                 soft_targets = torch.zeros_like(dist_matrix)
#                 soft_targets.scatter_(1, topk_idx, soft_weights)

#                 feat1_raw = self.model(v1_coord.unsqueeze(0)).squeeze(0)
#                 feat2_raw = self.model(v2_coord.unsqueeze(0)).squeeze(0)

#                 feat1 = self.fuse_features(feat1_raw)
#                 feat2 = self.fuse_features(feat2_raw)

#                 feat1 = F.normalize(feat1, dim=1)
#                 feat2 = F.normalize(feat2, dim=1)

#                 logits = torch.matmul(feat1, feat2.T) / 0.07
#                 log_probs = F.log_softmax(logits, dim=-1)
                
#                 loss = -(soft_targets * log_probs).sum(dim=-1).mean()

#                 loss.backward()
#                 optimizer.step()
#                 epoch_loss += loss.item()

#             if epoch % 10 == 0 or epoch == num_epochs - 1:
#                 avg_loss = epoch_loss / len(all_garment_pcds)
#                 print(f"Epoch {epoch}: Average Dataset Loss = {avg_loss:.4f}")
        
#         self.model.eval()
#         self.fusion_mlp.eval()

#     def get_feature(self, input_pcd:np.ndarray, index_list:list=None):
#         normalized_pcd, *_ = normalize_pcd_points_xy(input_pcd)
#         normalize_pcd = np.expand_dims(normalized_pcd, axis=0)
        
#         with torch.no_grad():
#             raw_features = self.model(
#                 torch.from_numpy(normalize_pcd).to(self.device).float(),
#             ).squeeze(0)
#             pcd_features = self.fuse_features(raw_features)
        
#         if index_list is not None:
#             target_features_list = []
#             for i in index_list:
#                 target_features_list.append(pcd_features[i])
#             return torch.stack(target_features_list)
#         else:
#             return pcd_features
        
#     # -----------------------------------------------------------------
#     # -----------------------------------------------------------------
#     def get_manipulation_points(self, input_pcd:np.ndarray, index_list:list=None):
#         '''
#         '''
#         demo_path = f"Model_HALO/GAM/checkpoints/{self.catogory}/demo_garment.ply"
#         demo_pcd = o3d.io.read_point_cloud(demo_path).points
#         train_source = "/workspace/isaaclab/scripts/DexGarmentLab/pointcloud/"

#         if train_source is not None:
#             self.train(train_source)
#         else:
#             self.train(demo_path)

#         demo_feature = self.get_feature(demo_pcd, index_list)
#         manipulate_feature = self.get_feature(input_pcd)
        
#         demo_feature_normalized = torch.nn.functional.normalize(demo_feature, p=2, dim=1)
#         manipulate_feature_normalized = torch.nn.functional.normalize(manipulate_feature, p=2, dim=1)
#         result = torch.matmul(demo_feature_normalized, manipulate_feature_normalized.T)
        
#         cprint("----------- GAM Inference Begin -----------", color="blue", attrs=["bold"])
        
#         topk_inf = 10
#         values, indices = torch.topk(result, topk_inf, dim=1)
        
#         weights = F.softmax(values / 0.02, dim=1).cpu().numpy()
#         indices_np = indices.cpu().numpy()

#         manipulation_points = np.zeros((result.shape[0], 3))
#         for i in range(result.shape[0]):
#             neighbor_points = input_pcd[indices_np[i]]
#             manipulation_points[i] = np.sum(neighbor_points * weights[i][:, np.newaxis], axis=0)

#         cprint(f"similarity result shape: {result.shape}", color="blue")
#         cprint(f"manipulation points (Soft-Averaged): \n {manipulation_points}", color="blue")
#         cprint("----------- GAM Inference End -----------", color="blue", attrs=["bold"])
        
#         return manipulation_points, indices_np[:, 0], result.cpu().numpy()
    
#     def get_colormap_points(self, input_pcd:np.ndarray):
#         demo_pcd = o3d.io.read_point_cloud(f"Model_HALO/GAM/checkpoints/{self.catogory}/demo_garment.ply").points
#         demo_feature = self.get_feature(demo_pcd)
#         manipulate_feature = self.get_feature(input_pcd)
        
#         demo_feature_normalized = torch.nn.functional.normalize(demo_feature, p=2, dim=1)
#         manipulate_feature_normalized = torch.nn.functional.normalize(manipulate_feature, p=2, dim=1)

#         result = torch.matmul(manipulate_feature_normalized, demo_feature_normalized.T)
        
#         max_values, max_indices = torch.max(result, dim=1)
#         print("similarity score: ", max_values)
#         print("relevant indices: ", max_indices)
        
#         corresponding_demo_color = input_pcd[max_indices.detach().cpu().numpy()]
#         print("manipulation points: \n", corresponding_demo_color)
#         return corresponding_demo_color, max_indices.detach().cpu().numpy()
    
#     def get_demo_garment_with_color(self):
#         demo_pcd = o3d.io.read_point_cloud(f"Model_HALO/GAM/checkpoints/{self.catogory}/demo_garment.ply")
#         self.demo_points = np.asarray(demo_pcd.points)
#         self.demo_points_color = colormap(self.demo_points)
#         return self.demo_points, self.demo_points_color
    
#     def visualize_pcd_corresponce(self, input_pcd:np.ndarray, save_or_not:bool=False, save_path:str=None):
#         self.get_demo_garment_with_color()
#         visualize_pointcloud_with_colors(self.demo_points, self.demo_points_color)
#         index_list = list(range(len(self.demo_points)))
#         _, color_indices = self.get_colormap_points(input_pcd)
#         color = np.ones_like(input_pcd)
#         for i in range(len(color_indices)):
#             color[i] = self.demo_points_color[color_indices[i]]
#         visualize_pointcloud_with_colors(input_pcd, color, save_or_not=save_or_not, save_path=save_path)
























# import os
# import sys
# import random
# import numpy as np
# import torch
# import open3d as o3d
# from termcolor import cprint


# sys.path.append(os.getcwd()) # change to your specific path
# sys.path.append("Model_HALO/GAM")
# from Model_HALO.GAM.model.pointnet2_GAM import GAM_Model
# from Env_Config.Utils_Project.Point_Cloud_Manip import furthest_point_sampling, normalize_pcd_points_xy, visualize_pointcloud_with_colors, colormap

# import torch.nn.functional as F

# from Model_HALO.GAM.model.gam_topo_model import GAM_Topo_Model
# from Model_HALO.GAM.model.topology_descriptor import compute_topology_descriptor


# class GAM_Encapsulation:
    
#     def __init__(
#         self,
#         catogory: str = "Tops_LongSleeve",
#         use_topology: bool = False,
#         topology_checkpoint: str = None,
#         input_garment_type: str = None,
#     ):
#         self.catogory = catogory
#         self.use_topology = use_topology
#         self.input_garment_type = input_garment_type or catogory

#         resume_path = f"Model_HALO/GAM/checkpoints/{self.catogory}/checkpoint.pth"
#         # resume_path = "Model_HALO/GAM/checkpoints/Tops_LongSleeve/topology_finetune.pth"

#         seed = 42
#         torch.manual_seed(seed)
#         torch.cuda.manual_seed(seed)
#         torch.cuda.manual_seed_all(seed)
#         np.random.seed(seed)
#         random.seed(seed)

#         self.device = "cuda:0" if torch.cuda.is_available() else "cpu"

#         backbone = GAM_Model(normal_channel=False, feature_dim=512).to(self.device)
#         backbone.load_state_dict(torch.load(resume_path, weights_only=False))

#         if self.use_topology:
#             self.model = GAM_Topo_Model(
#                 backbone=backbone,
#                 topo_dim=6,
#                 feature_dim=512,
#             ).to(self.device)


#             print("?????????????????????????????????????????")
            
#             if topology_checkpoint is not None:
#                 state = torch.load(topology_checkpoint, map_location=self.device, weights_only=False)
#                 if "model" in state:
#                     state = state["model"]
#                 self.model.load_state_dict(state, strict=False)
#         else:
#             self.model = backbone

#         self.model.eval()


    
#     def get_feature(self, input_pcd: np.ndarray, index_list: list = None, garment_type: str = None):
#         normalized_pcd, *_ = normalize_pcd_points_xy(input_pcd)

#         xyz_np = np.expand_dims(normalized_pcd, axis=0)

#         with torch.no_grad():
#             xyz = torch.from_numpy(xyz_np).to(self.device).float()

#             if self.use_topology:
#                 topo_np = compute_topology_descriptor(
#                     normalized_pcd,
#                     garment_type=garment_type or self.input_garment_type,
#                 )
#                 topo_np = np.expand_dims(topo_np, axis=0)
#                 topo = torch.from_numpy(topo_np).to(self.device).float()
#                 pcd_features = self.model(xyz, topo).squeeze(0)
#             else:
#                 pcd_features = self.model(xyz).squeeze(0)

#         if index_list is not None:
#             return torch.stack([pcd_features[i] for i in index_list])

#         return pcd_features

        
#     def get_manipulation_points(self, input_pcd:np.ndarray, index_list:list=None):
#         '''
#         get manipulation points of input point cloud
#         '''

#         #get model output (feature)
#         demo_pcd = o3d.io.read_point_cloud(f"Model_HALO/GAM/checkpoints/{self.catogory}/demo_garment.ply").points
#         print('ddd', np.array(demo_pcd).shape)

#         # demo_feature = self.get_feature(demo_pcd, index_list)
#         # manipulate_feature = self.get_feature(input_pcd)

#         demo_feature = self.get_feature(demo_pcd, index_list, garment_type="tops")
#         manipulate_feature = self.get_feature(input_pcd, garment_type=self.input_garment_type)
        
#         # normalize feature
#         demo_feature_normalized = torch.nn.functional.normalize(demo_feature, p=2, dim=1)
#         manipulate_feature_normalized = torch.nn.functional.normalize(manipulate_feature, p=2, dim=1)
#         result = torch.matmul(demo_feature_normalized, manipulate_feature_normalized.T)
        
#         cprint("----------- GAM Inference Begin -----------", color="blue", attrs=["bold"])
        
#         # get max similarity score and indices
#         max_values, max_indices = torch.max(result, dim=1)
#         cprint(f"similarity score: {max_values}", color="blue")
#         cprint(f"relevant indices: {max_indices}", color="blue")
#         cprint(f"similarity result shape: {result.shape}", color="blue")
#         # get manipulation points
#         manipulation_points = input_pcd[max_indices.detach().cpu().numpy()]

#         cprint(f"manipulation points: \n {manipulation_points}", color="blue")
        
#         cprint("----------- GAM Inference End -----------", color="blue", attrs=["bold"])
        
#         return manipulation_points, max_indices.detach().cpu().numpy(), result.cpu().numpy()
    
#     def get_colormap_points(self, input_pcd:np.ndarray):
#         '''
#         get colors for each corresponding point in input pcd.
#         '''
        
#         #get model output (feature)
#         demo_pcd = o3d.io.read_point_cloud(f"Model_HALO/GAM/checkpoints/{self.catogory}/demo_garment.ply").points
#         demo_feature = self.get_feature(demo_pcd)
#         manipulate_feature = self.get_feature(input_pcd)
        
#         # normalize feature
#         demo_feature_normalized = torch.nn.functional.normalize(demo_feature, p=2, dim=1)
#         manipulate_feature_normalized = torch.nn.functional.normalize(manipulate_feature, p=2, dim=1)

#         result = torch.matmul(manipulate_feature_normalized, demo_feature_normalized.T)
        
#         # get max similarity score and indices
#         max_values, max_indices = torch.max(result, dim=1)
#         print("similarity score: ", max_values)
#         print("relevant indices: ", max_indices)
        
#         # get manipulation points
#         corresponding_demo_color = input_pcd[max_indices.detach().cpu().numpy()]
#         print("manipulation points: \n", corresponding_demo_color)
#         return corresponding_demo_color, max_indices.detach().cpu().numpy()
    
#     def get_demo_garment_with_color(self):
#         '''
#         get demo garment with color
#         '''
#         demo_pcd = o3d.io.read_point_cloud(f"Model_HALO/GAM/checkpoints/{self.catogory}/demo_garment.ply")
#         self.demo_points = np.asarray(demo_pcd.points)
#         self.demo_points_color = colormap(self.demo_points)
#         return self.demo_points, self.demo_points_color
    
#     def visualize_pcd_corresponce(self, input_pcd:np.ndarray, save_or_not:bool=False, save_path:str=None):
#         '''
#         visualize exact point corresponce between input pcd and demo garment.
#         '''
#         # visualize demo garment with color
#         self.get_demo_garment_with_color()
#         visualize_pointcloud_with_colors(self.demo_points, self.demo_points_color)
#         index_list = list(range(len(self.demo_points)))
#         print("index_list: ", index_list)
#         print("len(index_list): ", len(index_list))
#         _, color_indices = self.get_colormap_points(input_pcd)
#         # visualize input pcd with color
#         color = np.ones_like(input_pcd)
#         for i in range(len(color_indices)):
#             color[i] = self.demo_points_color[color_indices[i]]
#         print("color: ", color)
#         visualize_pointcloud_with_colors(input_pcd, color, save_or_not=save_or_not, save_path=save_path)





















# import os
# import sys
# import random
# import numpy as np
# import torch
# import open3d as o3d
# from termcolor import cprint


# sys.path.append(os.getcwd())
# sys.path.append("Model_HALO/GAM")
# from Model_HALO.GAM.model.pointnet2_GAM import GAM_Model
# from Env_Config.Utils_Project.Point_Cloud_Manip import (
#     normalize_pcd_points_xy,
#     visualize_pointcloud_with_colors,
#     colormap,
# )

# import torch.nn.functional as F


# class GAM_Encapsulation:
#     """
#     Drop-in GAM wrapper for the supplied SimulationApp1.py.

#     The pretrained top model is not retrained. For trousers, the six top query
#     features are retained as role prototypes and softly embedded into the
#     trouser feature map according to a final upper-left folding box.

#     Six roles remain unchanged for the top diffusion policy:
#         0: first fold source      -> outer/right ankle
#         1: first fold destination -> left ankle
#         2: second fold source     -> outer/right waist
#         3: second fold destination -> left waist
#         4: final fold left grasp  -> lower-left outer point
#         5: final fold right grasp -> lower-left inner point
#     """

#     MAIN_QUERY_INDICES = [957, 501, 1902, 448, 1196, 422]

#     def __init__(
#         self,
#         catogory: str = "Tops_LongSleeve",
#         input_garment_type: str = "auto",
#         enable_role_alignment: bool = True,
#         role_feature_strength: float = 0.88,
#         role_score_strength: float = 0.82,
#     ):
#         self.catogory = catogory
#         self.input_garment_type = input_garment_type.lower()
#         self.enable_role_alignment = enable_role_alignment
#         self.role_feature_strength = float(
#             np.clip(role_feature_strength, 0.0, 1.0)
#         )
#         self.role_score_strength = float(
#             np.clip(role_score_strength, 0.0, 1.0)
#         )

#         seed = 42
#         torch.manual_seed(seed)
#         if torch.cuda.is_available():
#             torch.cuda.manual_seed(seed)
#             torch.cuda.manual_seed_all(seed)
#         np.random.seed(seed)
#         random.seed(seed)

#         self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
#         self.model = GAM_Model(
#             normal_channel=False,
#             feature_dim=512,
#         ).to(self.device)

#         checkpoint = (
#             f"Model_HALO/GAM/checkpoints/{self.catogory}/checkpoint.pth"
#         )
#         self.model.load_state_dict(
#             torch.load(
#                 checkpoint,
#                 map_location=self.device,
#                 weights_only=False,
#             )
#         )
#         self.model.eval()

#         self._demo_points = None
#         self._demo_features = None
#         self._role_prototypes = None

#     def _extract_raw_feature(self, input_pcd: np.ndarray) -> torch.Tensor:
#         normalized_pcd, *_ = normalize_pcd_points_xy(input_pcd)
#         normalized_pcd = np.expand_dims(normalized_pcd, axis=0)

#         with torch.no_grad():
#             return self.model(
#                 torch.from_numpy(normalized_pcd).to(self.device).float()
#             ).squeeze(0)

#     @staticmethod
#     def _normalized_xy(input_pcd: np.ndarray) -> np.ndarray:
#         """
#         Robust garment coordinates:
#             x = -1(left) ... +1(right)
#             y =  0(bottom) ... 1(top/waist)
#         """
#         points = np.asarray(input_pcd, dtype=np.float32)
#         x = points[:, 0]
#         y = points[:, 1]

#         x_low, x_high = np.percentile(x, [2.0, 98.0])
#         y_low, y_high = np.percentile(y, [2.0, 98.0])

#         x = 2.0 * (x - x_low) / max(float(x_high - x_low), 1e-6) - 1.0
#         y = (y - y_low) / max(float(y_high - y_low), 1e-6)

#         return np.stack(
#             [
#                 np.clip(x, -1.0, 1.0),
#                 np.clip(y, 0.0, 1.0),
#             ],
#             axis=1,
#         ).astype(np.float32)

#     @classmethod
#     def _infer_garment_type(cls, input_pcd: np.ndarray) -> str:
#         """
#         Trousers have an empty lower-center region between the two legs.
#         """
#         xy = cls._normalized_xy(input_pcd)
#         x = xy[:, 0]
#         y = xy[:, 1]

#         center = np.abs(x) < 0.17
#         lower = y < 0.45
#         upper = y > 0.58

#         lower_center_density = (
#             np.mean(center & lower) / (np.mean(lower) + 1e-6)
#         )
#         upper_center_density = (
#             np.mean(center & upper) / (np.mean(upper) + 1e-6)
#         )

#         if lower_center_density < 0.52 * max(
#             upper_center_density, 1e-6
#         ):
#             return "trousers"
#         return "tops"

#     def _is_trousers(self, input_pcd: np.ndarray) -> bool:
#         garment_type = self.input_garment_type
#         if garment_type == "auto":
#             garment_type = self._infer_garment_type(input_pcd)
#         return "trouser" in garment_type or "pants" in garment_type

#     def _load_demo(self):
#         if self._demo_features is not None:
#             return

#         demo_path = (
#             f"Model_HALO/GAM/checkpoints/{self.catogory}/demo_garment.ply"
#         )
#         demo_pcd = o3d.io.read_point_cloud(demo_path)
#         self._demo_points = np.asarray(
#             demo_pcd.points,
#             dtype=np.float32,
#         )
#         self._demo_features = self._extract_raw_feature(
#             self._demo_points
#         ).detach()

#         if max(self.MAIN_QUERY_INDICES) >= len(self._demo_points):
#             raise IndexError(
#                 "The top demo point cloud is smaller than the configured "
#                 "six manipulation-point indices."
#             )

#         self._role_prototypes = F.normalize(
#             self._demo_features[self.MAIN_QUERY_INDICES],
#             p=2,
#             dim=1,
#         )

#     @staticmethod
#     def _role_centers() -> np.ndarray:
#         """
#         Role locations for a final upper-left trouser rectangle.

#         The final box is approximately:
#             x in [-1, 0], y in [0.5, 1]

#         Roles 0 and 2 lie outside the box and are folded left.
#         Roles 4 and 5 lie below the box and are folded upward.
#         """
#         return np.asarray(
#             [
#                 [0.68, 0.08],   # 0: outer/right ankle
#                 [-0.62, 0.08],  # 1: opposite/left ankle
#                 [0.68, 0.90],   # 2: outer/right waist
#                 [-0.62, 0.90],  # 3: opposite/left waist
#                 [-0.84, 0.08],  # 4: lower-left outer grasp
#                 [-0.18, 0.08],  # 5: lower-left inner grasp
#             ],
#             dtype=np.float32,
#         )

#     @staticmethod
#     def _role_sigmas() -> np.ndarray:
#         # Broad, anisotropic kernels produce top-like smooth affordance maps.
#         return np.asarray(
#             [
#                 [0.25, 0.18],
#                 [0.25, 0.18],
#                 [0.25, 0.20],
#                 [0.25, 0.20],
#                 [0.20, 0.18],
#                 [0.20, 0.18],
#             ],
#             dtype=np.float32,
#         )

#     def _role_prior(self, input_pcd: np.ndarray) -> torch.Tensor:
#         """
#         Return six smooth role maps with shape (6, N).

#         Besides local Gaussian peaks, weak fold-region gates keep:
#           - roles 0/2 on the half outside the final box;
#           - roles 4/5 below the final box.
#         """
#         xy = self._normalized_xy(input_pcd)
#         centers = self._role_centers()
#         sigmas = self._role_sigmas()

#         delta = (
#             xy[None, :, :] - centers[:, None, :]
#         ) / sigmas[:, None, :]
#         prior = np.exp(-0.5 * np.sum(delta * delta, axis=2))

#         x = xy[:, 0]
#         y = xy[:, 1]

#         right_outside = 1.0 / (1.0 + np.exp(-10.0 * (x - 0.02)))
#         left_half = 1.0 / (1.0 + np.exp(10.0 * (x + 0.02)))
#         lower_outside = 1.0 / (1.0 + np.exp(10.0 * (y - 0.48)))
#         upper_half = 1.0 / (1.0 + np.exp(-10.0 * (y - 0.52)))

#         prior[0] *= 0.25 + 0.75 * right_outside
#         prior[1] *= 0.25 + 0.75 * left_half
#         prior[2] *= 0.25 + 0.75 * right_outside * upper_half
#         prior[3] *= 0.25 + 0.75 * left_half * upper_half
#         prior[4] *= 0.25 + 0.75 * left_half * lower_outside
#         prior[5] *= 0.25 + 0.75 * left_half * lower_outside

#         prior /= np.maximum(prior.max(axis=1, keepdims=True), 1e-6)
#         return torch.from_numpy(prior.astype(np.float32)).to(self.device)

#     def _role_aligned_feature(
#         self,
#         input_pcd: np.ndarray,
#         raw_features: torch.Tensor,
#     ) -> torch.Tensor:
#         """
#         Embed top role prototypes into the trouser point features.

#         This is a smooth feature-space operation, not a hard replacement of
#         point indices. It therefore preserves a usable dense affordance map.
#         """
#         self._load_demo()
#         role_prior = self._role_prior(input_pcd).T  # (N, 6)

#         # Softmax creates a continuous mixture between neighboring roles.
#         role_weight = torch.softmax(4.0 * role_prior, dim=1)
#         role_feature = torch.matmul(
#             role_weight,
#             self._role_prototypes,
#         )
#         role_feature = F.normalize(role_feature, p=2, dim=1)

#         raw_feature = F.normalize(raw_features, p=2, dim=1)

#         # Alignment is strongest near a role center and weaker elsewhere.
#         local_confidence = torch.max(role_prior, dim=1).values.unsqueeze(1)
#         blend = self.role_feature_strength * (
#             0.10 + 0.90 * local_confidence
#         )

#         return F.normalize(
#             (1.0 - blend) * raw_feature + blend * role_feature,
#             p=2,
#             dim=1,
#         )

#     def get_feature(
#         self,
#         input_pcd: np.ndarray,
#         index_list: list = None,
#         apply_role_alignment: bool = True,
#     ):
#         raw_features = self._extract_raw_feature(input_pcd)
#         features = raw_features

#         if (
#             self.enable_role_alignment
#             and apply_role_alignment
#             and self._is_trousers(input_pcd)
#         ):
#             features = self._role_aligned_feature(
#                 input_pcd,
#                 raw_features,
#             )

#         if index_list is None:
#             return features

#         index_tensor = torch.as_tensor(
#             index_list,
#             dtype=torch.long,
#             device=features.device,
#         )
#         return features[index_tensor]

#     @staticmethod
#     def _select_unique_points(
#         score: torch.Tensor,
#         input_pcd: np.ndarray,
#     ):
#         """
#         Select one point per role without allowing role collapse.
#         """
#         xy = GAM_Encapsulation._normalized_xy(input_pcd)
#         selected = []
#         max_values = []

#         for role_index in range(score.shape[0]):
#             role_score = score[role_index].clone()

#             if selected:
#                 selected_xy = xy[np.asarray(selected)]
#                 distance_sq = np.min(
#                     np.sum(
#                         (
#                             xy[:, None, :]
#                             - selected_xy[None, :, :]
#                         )
#                         ** 2,
#                         axis=2,
#                     ),
#                     axis=1,
#                 )
#                 too_close = torch.from_numpy(
#                     distance_sq < (0.055 ** 2)
#                 ).to(role_score.device)
#                 role_score[too_close] = -torch.inf

#             value, index = torch.max(role_score, dim=0)
#             selected.append(int(index.item()))
#             max_values.append(value)

#         return (
#             torch.stack(max_values),
#             torch.as_tensor(
#                 selected,
#                 dtype=torch.long,
#                 device=score.device,
#             ),
#         )

#     def get_manipulation_points(
#         self,
#         input_pcd: np.ndarray,
#         index_list: list = None,
#     ):
#         self._load_demo()
#         demo_points = self._demo_points

#         if index_list is None:
#             index_list = list(range(len(demo_points)))

#         is_main_diffusion_query = (
#             self._is_trousers(input_pcd)
#             and list(index_list) == self.MAIN_QUERY_INDICES
#         )

#         demo_feature = self.get_feature(
#             demo_points,
#             index_list,
#             apply_role_alignment=False,
#         )
#         input_feature = self.get_feature(
#             input_pcd,
#             apply_role_alignment=is_main_diffusion_query,
#         )

#         demo_feature = F.normalize(demo_feature, p=2, dim=1)
#         input_feature = F.normalize(input_feature, p=2, dim=1)
#         feature_similarity = torch.matmul(
#             demo_feature,
#             input_feature.T,
#         )

#         result = feature_similarity
#         if is_main_diffusion_query:
#             role_prior = self._role_prior(input_pcd)

#             # Keep the top feature match while imposing the trouser folding
#             # role. Both terms remain in [-1, 1].
#             role_similarity = 2.0 * role_prior - 1.0
#             result = (
#                 (1.0 - self.role_score_strength) * feature_similarity
#                 + self.role_score_strength * role_similarity
#             )

#             max_values, max_indices = self._select_unique_points(
#                 result,
#                 input_pcd,
#             )
#         else:
#             max_values, max_indices = torch.max(result, dim=1)

#         indices_np = max_indices.detach().cpu().numpy()
#         manipulation_points = np.asarray(input_pcd)[indices_np]

#         cprint(
#             "----------- GAM Inference Begin -----------",
#             color="blue",
#             attrs=["bold"],
#         )
#         cprint(f"similarity score: {max_values}", color="blue")
#         cprint(f"relevant indices: {max_indices}", color="blue")
#         cprint(f"similarity result shape: {result.shape}", color="blue")
#         cprint(
#             f"manipulation points:\n{manipulation_points}",
#             color="blue",
#         )
#         cprint(
#             "----------- GAM Inference End -----------",
#             color="blue",
#             attrs=["bold"],
#         )

#         return (
#             manipulation_points,
#             indices_np,
#             result.detach().cpu().numpy(),
#         )

#     def get_colormap_points(self, input_pcd: np.ndarray):
#         self._load_demo()

#         demo_feature = F.normalize(
#             self._demo_features,
#             p=2,
#             dim=1,
#         )
#         input_feature = F.normalize(
#             self.get_feature(
#                 input_pcd,
#                 apply_role_alignment=True,
#             ),
#             p=2,
#             dim=1,
#         )

#         result = torch.matmul(input_feature, demo_feature.T)
#         max_values, max_indices = torch.max(result, dim=1)

#         print("similarity score: ", max_values)
#         print("relevant indices: ", max_indices)

#         indices_np = max_indices.detach().cpu().numpy()
#         corresponding_demo_points = self._demo_points[indices_np]
#         return corresponding_demo_points, indices_np

#     def get_demo_garment_with_color(self):
#         self._load_demo()
#         self.demo_points = self._demo_points
#         self.demo_points_color = colormap(self.demo_points)
#         return self.demo_points, self.demo_points_color

#     def visualize_pcd_corresponce(
#         self,
#         input_pcd: np.ndarray,
#         save_or_not: bool = False,
#         save_path: str = None,
#     ):
#         self.get_demo_garment_with_color()
#         visualize_pointcloud_with_colors(
#             self.demo_points,
#             self.demo_points_color,
#         )

#         _, color_indices = self.get_colormap_points(input_pcd)
#         color = self.demo_points_color[color_indices]

#         visualize_pointcloud_with_colors(
#             input_pcd,
#             color,
#             save_or_not=save_or_not,
#             save_path=save_path,
#         )


























# import os
# import random
# import sys
# from pathlib import Path
# from typing import Iterable, Optional, Sequence, Union

# import numpy as np
# import open3d as o3d
# import torch
# import torch.nn.functional as F
# from termcolor import cprint
# from torch import nn


# sys.path.append(os.getcwd())  # Change this if Model_HALO is in another directory.
# sys.path.append("Model_HALO/GAM")

# from Model_HALO.GAM.model.pointnet2_GAM import GAM_Model
# from Env_Config.Utils_Project.Point_Cloud_Manip import (
#     colormap,
#     normalize_pcd_points_xy,
#     visualize_pointcloud_with_colors,
# )


# ArrayOrPath = Union[np.ndarray, str, Path]


# def _load_state_dict(path: Union[str, Path], device: torch.device):
#     """Load both a plain state_dict and a wrapped training checkpoint."""
#     checkpoint = torch.load(path, map_location=device, weights_only=False)
#     if isinstance(checkpoint, dict):
#         for key in ("model_state_dict", "state_dict", "model"):
#             if key in checkpoint and isinstance(checkpoint[key], dict):
#                 return checkpoint[key]
#     return checkpoint


# def _nearest_indices(
#     query_xy: torch.Tensor,
#     reference_xy: torch.Tensor,
#     chunk_size: int = 512,
# ):
#     """Chunked nearest-neighbor search that avoids an N x N allocation."""
#     all_indices = []
#     all_distances = []

#     for start in range(0, query_xy.shape[1], chunk_size):
#         end = min(start + chunk_size, query_xy.shape[1])
#         distances = torch.cdist(query_xy[:, start:end], reference_xy)
#         min_distances, min_indices = distances.min(dim=-1)
#         all_distances.append(min_distances)
#         all_indices.append(min_indices)

#     return torch.cat(all_indices, dim=1), torch.cat(all_distances, dim=1)


# @torch.no_grad()
# def symmetry_metadata(points: torch.Tensor):
#     """
#     Estimate the better of the two PCA reflection axes.

#     Returns geometry descriptors, mirrored-point indices, and exactly reflected
#     points. The selected axis is whichever produces the smaller reflected
#     Chamfer-like nearest-neighbor distance.
#     """
#     xy = points[..., :2]
#     center = xy.mean(dim=1, keepdim=True)
#     centered = xy - center
#     covariance = centered.transpose(1, 2) @ centered
#     covariance = covariance / max(points.shape[1] - 1, 1)
#     _, eigenvectors = torch.linalg.eigh(covariance)

#     candidate_axes = (eigenvectors[..., 0], eigenvectors[..., 1])
#     candidate_scores = []

#     for axis in candidate_axes:
#         perpendicular = torch.stack((-axis[:, 1], axis[:, 0]), dim=-1)
#         axial = (centered * axis[:, None]).sum(dim=-1, keepdim=True)
#         lateral = (centered * perpendicular[:, None]).sum(dim=-1, keepdim=True)
#         reflected_xy = (
#             center
#             + axial * axis[:, None]
#             - lateral * perpendicular[:, None]
#         )
#         _, mirror_distance = _nearest_indices(reflected_xy, xy)
#         candidate_scores.append(mirror_distance.mean(dim=1))

#     choose_first = candidate_scores[0] <= candidate_scores[1]
#     axis = torch.where(
#         choose_first[:, None],
#         candidate_axes[0],
#         candidate_axes[1],
#     )

#     # Resolve the arbitrary eigenvector sign for stable signed descriptors.
#     major_component = axis.abs().argmax(dim=-1)
#     sign_reference = axis.gather(1, major_component[:, None]).squeeze(1)
#     axis = axis * torch.where(
#         sign_reference < 0,
#         -torch.ones_like(sign_reference),
#         torch.ones_like(sign_reference),
#     )[:, None]

#     perpendicular = torch.stack((-axis[:, 1], axis[:, 0]), dim=-1)
#     axial = (centered * axis[:, None]).sum(dim=-1)
#     lateral = (centered * perpendicular[:, None]).sum(dim=-1)
#     reflected_xy = (
#         center
#         + axial[..., None] * axis[:, None]
#         - lateral[..., None] * perpendicular[:, None]
#     )
#     mirror_indices, mirror_distance = _nearest_indices(reflected_xy, xy)

#     axial_scale = axial.abs().amax(dim=1, keepdim=True).clamp_min(1e-6)
#     lateral_scale = lateral.abs().amax(dim=1, keepdim=True).clamp_min(1e-6)
#     axial_normalized = axial / axial_scale
#     lateral_normalized = lateral / lateral_scale
#     extremity = torch.sqrt(
#         axial_normalized.square() + lateral_normalized.square()
#     ).clamp(max=np.sqrt(2.0)) / np.sqrt(2.0)

#     cloud_scale = centered.norm(dim=-1).amax(dim=1, keepdim=True).clamp_min(1e-6)
#     mirror_quality = torch.exp(-4.0 * mirror_distance / cloud_scale)
#     boundary = torch.maximum(
#         axial_normalized.abs(),
#         lateral_normalized.abs(),
#     )

#     geometry = torch.stack(
#         (
#             axial_normalized,
#             lateral_normalized,
#             axial_normalized.abs(),
#             lateral_normalized.abs(),
#             extremity,
#             mirror_quality,
#             boundary,
#         ),
#         dim=-1,
#     )

#     reflected_points = points.clone()
#     reflected_points[..., :2] = reflected_xy
#     return geometry, mirror_indices, reflected_points


# class SymmetryAwareFeatureRefiner(nn.Module):
#     """
#     A small residual layer placed after GAM.

#     The final linear layer starts at zero, so enabling this module does not
#     initially alter GAM's feature map. Fine-tuning learns only a correction.
#     """

#     def __init__(self, feature_dim: int = 512, hidden_dim: int = 256):
#         super().__init__()
#         geometry_dim = 7
#         input_dim = feature_dim * 3 + geometry_dim

#         self.refiner = nn.Sequential(
#             nn.Linear(input_dim, hidden_dim),
#             nn.LayerNorm(hidden_dim),
#             nn.GELU(),
#             nn.Linear(hidden_dim, hidden_dim),
#             nn.GELU(),
#             nn.Linear(hidden_dim, feature_dim),
#         )
#         nn.init.zeros_(self.refiner[-1].weight)
#         nn.init.zeros_(self.refiner[-1].bias)

#         # A small initial gate lets the last layer receive gradients while the
#         # zero-initialized output still preserves the original map exactly.
#         self.residual_gate_logit = nn.Parameter(torch.tensor(-4.0))

#     def forward(
#         self,
#         features: torch.Tensor,
#         points: torch.Tensor,
#         geometry: Optional[torch.Tensor] = None,
#         mirror_indices: Optional[torch.Tensor] = None,
#     ):
#         if geometry is None or mirror_indices is None:
#             geometry, mirror_indices, _ = symmetry_metadata(points)
#         gather_indices = mirror_indices[..., None].expand(
#             -1,
#             -1,
#             features.shape[-1],
#         )
#         mirror_features = torch.gather(features, dim=1, index=gather_indices)
#         refiner_input = torch.cat(
#             (
#                 features,
#                 mirror_features,
#                 features - mirror_features,
#                 geometry,
#             ),
#             dim=-1,
#         )
#         delta = self.refiner(refiner_input)
#         residual_gate = torch.sigmoid(self.residual_gate_logit)
#         refined = features + residual_gate * delta
#         return F.normalize(refined, p=2, dim=-1), geometry


# class GAM_Encapsulation:
#     def __init__(
#         self,
#         catogory: str = "Trousers",
#         refiner_checkpoint: Optional[Union[str, Path]] = None,
#         feature_dim: int = 512,
#         outer_weight: float = 0.12,
#     ):
#         """
#         Load a frozen GAM and a trainable symmetry-aware residual layer.

#         outer_weight controls geometry-aware reranking. 0.0 reproduces pure
#         cosine matching; 0.08-0.18 is a practical starting range.
#         """
#         self.catogory = catogory
#         self.feature_dim = feature_dim
#         self.outer_weight = outer_weight
#         self.device = torch.device(
#             "cuda:0" if torch.cuda.is_available() else "cpu"
#         )

#         seed = 42
#         torch.manual_seed(seed)
#         if torch.cuda.is_available():
#             torch.cuda.manual_seed(seed)
#             torch.cuda.manual_seed_all(seed)
#         np.random.seed(seed)
#         random.seed(seed)

#         checkpoint_dir = Path("Model_HALO/GAM/checkpoints") / self.catogory
#         self.demo_path = checkpoint_dir / "demo_garment.ply"
#         resume_path = checkpoint_dir / "checkpoint.pth"

#         self.model = GAM_Model(
#             normal_channel=False,
#             feature_dim=self.feature_dim,
#         ).to(self.device)
#         self.model.load_state_dict(_load_state_dict(resume_path, self.device))
#         self.model.eval()
#         for parameter in self.model.parameters():
#             parameter.requires_grad_(False)

#         self.refiner = SymmetryAwareFeatureRefiner(
#             feature_dim=self.feature_dim
#         ).to(self.device)
#         if refiner_checkpoint is not None:
#             self.load_refiner(refiner_checkpoint)
#         self.refiner.eval()

#     def _prepare_points(self, input_pcd: np.ndarray):
#         normalized_pcd, *_ = normalize_pcd_points_xy(input_pcd)
#         points = torch.from_numpy(
#             np.expand_dims(normalized_pcd, axis=0)
#         ).to(self.device, dtype=torch.float32)
#         return points

#     def _gam_forward(self, points: torch.Tensor):
#         features = self.model(points)
#         if features.ndim != 3:
#             raise ValueError(
#                 f"Expected GAM output [B, N, C] or [B, C, N], got "
#                 f"{tuple(features.shape)}"
#             )
#         if features.shape[-1] != self.feature_dim:
#             if features.shape[1] == self.feature_dim:
#                 features = features.transpose(1, 2)
#             else:
#                 raise ValueError(
#                     f"GAM output does not contain feature_dim="
#                     f"{self.feature_dim}: {tuple(features.shape)}"
#                 )
#         return features

#     def _get_feature_and_geometry(self, input_pcd: np.ndarray):
#         points = self._prepare_points(input_pcd)
#         with torch.no_grad():
#             base_features = self._gam_forward(points)
#             refined_features, geometry = self.refiner(base_features, points)
#         return refined_features.squeeze(0), geometry.squeeze(0)

#     def get_feature(
#         self,
#         input_pcd: np.ndarray,
#         index_list: Optional[Sequence[int]] = None,
#     ):
#         """Get symmetry-refined GAM features."""
#         features, _ = self._get_feature_and_geometry(input_pcd)
#         if index_list is not None:
#             indices = torch.as_tensor(
#                 index_list,
#                 device=self.device,
#                 dtype=torch.long,
#             )
#             features = features.index_select(0, indices)
#         return features

#     def _matching_score(
#         self,
#         demo_pcd: np.ndarray,
#         input_pcd: np.ndarray,
#         index_list: Optional[Sequence[int]] = None,
#         geometry_rerank: bool = True,
#     ):
#         demo_features, demo_geometry = self._get_feature_and_geometry(demo_pcd)
#         input_features, input_geometry = self._get_feature_and_geometry(input_pcd)

#         if index_list is not None:
#             indices = torch.as_tensor(
#                 index_list,
#                 device=self.device,
#                 dtype=torch.long,
#             )
#             demo_features = demo_features.index_select(0, indices)
#             demo_geometry = demo_geometry.index_select(0, indices)

#         cosine_score = F.normalize(demo_features, p=2, dim=-1) @ F.normalize(
#             input_features,
#             p=2,
#             dim=-1,
#         ).T

#         if not geometry_rerank or self.outer_weight <= 0:
#             return cosine_score

#         # Only an already-extreme demo query receives a strong outside bonus.
#         # A candidate is preferred when it is far from the center and has a
#         # reliable reflected partner on the opposite side of the garment.
#         query_extremity = demo_geometry[:, 4:5]
#         candidate_extremity = input_geometry[:, 4]
#         candidate_mirror_quality = input_geometry[:, 5]
#         symmetric_outer_prior = candidate_extremity * candidate_mirror_quality

#         return cosine_score + (
#             self.outer_weight
#             * query_extremity
#             * symmetric_outer_prior.unsqueeze(0)
#         )

#     def get_manipulation_points(
#         self,
#         input_pcd: np.ndarray,
#         index_list: Optional[Sequence[int]] = None,
#         geometry_rerank: bool = True,
#     ):
#         """Match demo manipulation points to the input point cloud."""
#         demo_pcd = np.asarray(
#             o3d.io.read_point_cloud(str(self.demo_path)).points
#         )
#         result = self._matching_score(
#             demo_pcd,
#             input_pcd,
#             index_list=index_list,
#             geometry_rerank=geometry_rerank,
#         )

#         max_values, max_indices = torch.max(result, dim=1)
#         manipulation_points = input_pcd[
#             max_indices.detach().cpu().numpy()
#         ]

#         cprint("----------- GAM Inference Begin -----------", "blue", attrs=["bold"])
#         cprint(f"similarity score: {max_values}", "blue")
#         cprint(f"relevant indices: {max_indices}", "blue")
#         cprint(f"manipulation points:\n{manipulation_points}", "blue")
#         cprint("----------- GAM Inference End -----------", "blue", attrs=["bold"])

#         return (
#             manipulation_points,
#             max_indices.detach().cpu().numpy(),
#             result.detach().cpu().numpy(),
#         )

#     def get_colormap_points(self, input_pcd: np.ndarray):
#         """Get each input point's corresponding demo point index."""
#         demo_pcd = np.asarray(
#             o3d.io.read_point_cloud(str(self.demo_path)).points
#         )
#         demo_features = self.get_feature(demo_pcd)
#         input_features = self.get_feature(input_pcd)
#         result = F.normalize(input_features, p=2, dim=-1) @ F.normalize(
#             demo_features,
#             p=2,
#             dim=-1,
#         ).T
#         max_values, max_indices = torch.max(result, dim=1)
#         print("similarity score:", max_values)
#         print("relevant indices:", max_indices)
#         return max_indices.detach().cpu().numpy()

#     def get_demo_garment_with_color(self):
#         demo_pcd = o3d.io.read_point_cloud(str(self.demo_path))
#         self.demo_points = np.asarray(demo_pcd.points)
#         self.demo_points_color = colormap(self.demo_points)
#         return self.demo_points, self.demo_points_color

#     def visualize_pcd_corresponce(
#         self,
#         input_pcd: np.ndarray,
#         save_or_not: bool = False,
#         save_path: Optional[str] = None,
#     ):
#         self.get_demo_garment_with_color()
#         visualize_pointcloud_with_colors(
#             self.demo_points,
#             self.demo_points_color,
#         )
#         color_indices = self.get_colormap_points(input_pcd)
#         input_colors = self.demo_points_color[color_indices]
#         visualize_pointcloud_with_colors(
#             input_pcd,
#             input_colors,
#             save_or_not=save_or_not,
#             save_path=save_path,
#         )

#     @staticmethod
#     def _read_pcd(point_cloud: ArrayOrPath):
#         if isinstance(point_cloud, (str, Path)):
#             return np.asarray(
#                 o3d.io.read_point_cloud(str(point_cloud)).points
#             )
#         return np.asarray(point_cloud)

#     def fine_tune_refiner(
#         self,
#         pants_point_clouds: Iterable[ArrayOrPath],
#         epochs: int = 30,
#         learning_rate: float = 1e-4,
#         preservation_weight: float = 8.0,
#         contrastive_weight: float = 0.25,
#         max_contrastive_points: int = 512,
#         save_path: Optional[Union[str, Path]] = None,
#     ):
#         """
#         Fine-tune only the post-GAM layer using trousers.

#         Reflection equivariance teaches symmetric structure. The preservation
#         term keeps the refined map close to the frozen GAM map. A sampled
#         contrastive term prevents all symmetric points from collapsing to one
#         feature.
#         """
#         point_clouds = [self._read_pcd(pcd) for pcd in pants_point_clouds]
#         if not point_clouds:
#             raise ValueError("pants_point_clouds must contain at least one cloud")

#         optimizer = torch.optim.AdamW(
#             self.refiner.parameters(),
#             lr=learning_rate,
#             weight_decay=1e-5,
#         )
#         history = []
#         self.model.eval()
#         self.refiner.train()

#         for epoch in range(epochs):
#             random.shuffle(point_clouds)
#             epoch_loss = 0.0

#             for point_cloud in point_clouds:
#                 points = self._prepare_points(point_cloud)
#                 with torch.no_grad():
#                     geometry, mirror_indices, reflected_points = (
#                         symmetry_metadata(points)
#                     )
#                     base_original = F.normalize(
#                         self._gam_forward(points),
#                         p=2,
#                         dim=-1,
#                     )
#                     base_reflected = F.normalize(
#                         self._gam_forward(reflected_points),
#                         p=2,
#                         dim=-1,
#                     )

#                 reflected_geometry = geometry.clone()
#                 reflected_geometry[..., 1] *= -1.0

#                 refined_original, _ = self.refiner(
#                     base_original,
#                     points,
#                     geometry=geometry,
#                     mirror_indices=mirror_indices,
#                 )
#                 refined_reflected, _ = self.refiner(
#                     base_reflected,
#                     reflected_points,
#                     geometry=reflected_geometry,
#                     mirror_indices=mirror_indices,
#                 )

#                 # Outer symmetric points receive more equivariance emphasis.
#                 point_weight = 1.0 + 2.0 * (
#                     geometry[..., 4] * geometry[..., 5]
#                 )
#                 equivariance_error = 1.0 - F.cosine_similarity(
#                     refined_original,
#                     refined_reflected,
#                     dim=-1,
#                 )
#                 equivariance_loss = (
#                     equivariance_error * point_weight
#                 ).mean()

#                 preservation_loss = (
#                     F.mse_loss(refined_original, base_original)
#                     + F.mse_loss(refined_reflected, base_reflected)
#                 )

#                 point_count = points.shape[1]
#                 sample_count = min(point_count, max_contrastive_points)
#                 sample_indices = torch.randperm(
#                     point_count,
#                     device=self.device,
#                 )[:sample_count]
#                 original_sample = refined_original[:, sample_indices].squeeze(0)
#                 reflected_sample = refined_reflected[:, sample_indices].squeeze(0)
#                 logits = original_sample @ reflected_sample.T / 0.07
#                 labels = torch.arange(sample_count, device=self.device)
#                 contrastive_loss = 0.5 * (
#                     F.cross_entropy(logits, labels)
#                     + F.cross_entropy(logits.T, labels)
#                 )

#                 loss = (
#                     equivariance_loss
#                     + preservation_weight * preservation_loss
#                     + contrastive_weight * contrastive_loss
#                 )

#                 optimizer.zero_grad(set_to_none=True)
#                 loss.backward()
#                 torch.nn.utils.clip_grad_norm_(
#                     self.refiner.parameters(),
#                     max_norm=1.0,
#                 )
#                 optimizer.step()
#                 epoch_loss += loss.item()

#             mean_loss = epoch_loss / len(point_clouds)
#             history.append(mean_loss)
#             print(
#                 f"[refiner] epoch {epoch + 1:03d}/{epochs:03d} "
#                 f"loss={mean_loss:.6f}"
#             )

#         self.refiner.eval()
#         if save_path is not None:
#             self.save_refiner(save_path)
#         return history

#     def save_refiner(self, path: Union[str, Path]):
#         path = Path(path)
#         path.parent.mkdir(parents=True, exist_ok=True)
#         torch.save(
#             {
#                 "refiner_state_dict": self.refiner.state_dict(),
#                 "feature_dim": self.feature_dim,
#                 "category": self.catogory,
#                 "outer_weight": self.outer_weight,
#             },
#             path,
#         )

#     def load_refiner(self, path: Union[str, Path]):
#         checkpoint = torch.load(
#             path,
#             map_location=self.device,
#             weights_only=False,
#         )
#         state_dict = checkpoint.get(
#             "refiner_state_dict",
#             checkpoint,
#         )
#         self.refiner.load_state_dict(state_dict)
#         if isinstance(checkpoint, dict) and "outer_weight" in checkpoint:
#             self.outer_weight = float(checkpoint["outer_weight"])
#         self.refiner.eval()


# # if __name__ == "__main__":
# #     # Example:
# #     #
# #     # gam = GAM_Encapsulation(catogory="Trousers")
# #     # gam.fine_tune_refiner(
# #     #     pants_point_clouds=["data/pants_01.ply", "data/pants_02.ply"],
# #     #     epochs=30,
# #     #     save_path="Model_HALO/GAM/checkpoints/Trousers/symmetry_refiner.pth",
# #     # )
# #     #
# #     # inference_gam = GAM_Encapsulation(
# #     #     catogory="Trousers",
# #     #     refiner_checkpoint=(
# #     #         "Model_HALO/GAM/checkpoints/Trousers/symmetry_refiner.pth"
# #     #     ),
# #     #     outer_weight=0.12,
# #     # )
# #     pass
















# import os
# import sys
# import random
# from pathlib import Path
# from typing import Optional, Tuple

# import numpy as np
# import open3d as o3d
# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# from termcolor import cprint


# sys.path.append(os.getcwd())  # change to your project root when needed
# sys.path.append("Model_HALO/GAM")

# from Model_HALO.GAM.model.pointnet2_GAM import GAM_Model
# from Env_Config.Utils_Project.Point_Cloud_Manip import (
#     colormap,
#     normalize_pcd_points_xy,
#     visualize_pointcloud_with_colors,
# )


# def _as_bnd_features(features: torch.Tensor, feature_dim: int) -> Tuple[torch.Tensor, bool]:
#     """Convert GAM output to [batch, points, feature] and record a transpose."""
#     if features.ndim == 2:
#         features = features.unsqueeze(0)

#     if features.ndim != 3:
#         raise ValueError(f"GAM feature must be 3-D, got {tuple(features.shape)}")

#     if features.shape[-1] == feature_dim:
#         return features, False
#     if features.shape[1] == feature_dim:
#         return features.transpose(1, 2).contiguous(), True

#     raise ValueError(
#         f"Cannot find feature dimension {feature_dim} in GAM output "
#         f"{tuple(features.shape)}"
#     )


# def _as_bnd_points(points: torch.Tensor) -> torch.Tensor:
#     """Convert point tensor to [batch, points, xyz]."""
#     if points.ndim == 2:
#         points = points.unsqueeze(0)

#     if points.ndim != 3:
#         raise ValueError(f"Point cloud must be 3-D, got {tuple(points.shape)}")

#     if points.shape[-1] == 3:
#         return points
#     if points.shape[1] == 3:
#         return points.transpose(1, 2).contiguous()

#     raise ValueError(f"Cannot find xyz dimension in point cloud {tuple(points.shape)}")


# class SymmetryResidualAdapter(nn.Module):
#     """
#     A small trainable layer placed after GAM.

#     The adapter receives the frozen GAM feature, point coordinates, and global
#     shape context. Its residual gate starts near zero, so the original trouser
#     feature map is preserved before and during fine-tuning.
#     """

#     def __init__(self, feature_dim: int = 512, hidden_dim: int = 128):
#         super().__init__()
#         self.feature_dim = feature_dim

#         self.feature_encoder = nn.Sequential(
#             nn.Linear(feature_dim, hidden_dim),
#             nn.LayerNorm(hidden_dim),
#             nn.GELU(),
#         )
#         self.xyz_encoder = nn.Sequential(
#             nn.Linear(6, 48),
#             nn.LayerNorm(48),
#             nn.GELU(),
#             nn.Linear(48, 64),
#             nn.GELU(),
#         )
#         self.residual_head = nn.Sequential(
#             nn.Linear(hidden_dim * 2 + 64, hidden_dim * 2),
#             nn.LayerNorm(hidden_dim * 2),
#             nn.GELU(),
#             nn.Linear(hidden_dim * 2, feature_dim),
#         )

#         # sigmoid(-3.0) ~= 0.047: begin very close to the original GAM map.
#         self.residual_gate_logit = nn.Parameter(torch.tensor(-3.0))

#     def forward(self, features: torch.Tensor, points: torch.Tensor) -> torch.Tensor:
#         features, was_transposed = _as_bnd_features(features, self.feature_dim)
#         points = _as_bnd_points(points)

#         if features.shape[:2] != points.shape[:2]:
#             raise ValueError(
#                 "GAM features and points have incompatible shapes: "
#                 f"{tuple(features.shape)} vs {tuple(points.shape)}"
#             )

#         centered = points - points.mean(dim=1, keepdim=True)
#         scale = centered.norm(dim=-1).amax(dim=1, keepdim=True).unsqueeze(-1)
#         normalized_xyz = centered / scale.clamp_min(1e-6)
#         xyz_input = torch.cat((normalized_xyz, normalized_xyz.abs()), dim=-1)

#         normalized_features = F.normalize(features, p=2, dim=-1)
#         local_context = self.feature_encoder(normalized_features)
#         global_context = local_context.amax(dim=1, keepdim=True)
#         global_context = global_context.expand(-1, local_context.shape[1], -1)
#         xyz_context = self.xyz_encoder(xyz_input)

#         delta = self.residual_head(
#             torch.cat((local_context, global_context, xyz_context), dim=-1)
#         )
#         # Keep the residual on the same scale as the frozen GAM feature.
#         feature_scale = features.norm(dim=-1, keepdim=True).clamp_min(1e-6)
#         delta = F.normalize(delta, p=2, dim=-1) * feature_scale
#         output = features + torch.sigmoid(self.residual_gate_logit) * delta

#         if was_transposed:
#             return output.transpose(1, 2).contiguous()
#         return output


# class GAMWithSymmetryAdapter(nn.Module):
#     """Frozen GAM backbone followed by the trainable residual adapter."""

#     def __init__(
#         self,
#         backbone: nn.Module,
#         adapter: SymmetryResidualAdapter,
#         feature_dim: int = 512,
#     ):
#         super().__init__()
#         self.backbone = backbone
#         self.adapter = adapter
#         self.feature_dim = feature_dim

#     def forward(self, points: torch.Tensor) -> torch.Tensor:
#         base_features = self.backbone(points)
#         return self.adapter(base_features, points)


# class GAM_Encapsulation:
#     """
#     GAM inference with automatic trousers-only symmetry fine-tuning.

#     Existing usage remains unchanged:

#         self.model = GAM_Encapsulation(catogory="Trousers")

#     If checkpoint_symmetry_adapter.pth exists, it is loaded. Otherwise only the
#     new post-GAM adapter is trained from demo_garment.ply and then saved.
#     """

#     def __init__(
#         self,
#         catogory: str = "Tops_LongSleeve",
#         auto_finetune: bool = True,
#         force_finetune: bool = False,
#         finetune_steps: int = 400,
#         deformation_count: int = 12,
#         training_points: int = 1024,
#     ):
#         self.catogory = catogory
#         self.feature_dim = 512
#         self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

#         checkpoint_dir = Path("Model_HALO/GAM/checkpoints") / self.catogory
#         self.resume_path = checkpoint_dir / "checkpoint.pth"
#         self.demo_path = checkpoint_dir / "demo_garment.ply"
#         self.adapter_path = checkpoint_dir / "checkpoint_symmetry_adapter.pth"

#         self._set_seed(42)

#         backbone = GAM_Model(normal_channel=False, feature_dim=self.feature_dim)
#         backbone_state = self._load_torch_checkpoint(self.resume_path)
#         backbone.load_state_dict(self._extract_state_dict(backbone_state))
#         backbone = backbone.to(self.device)
#         backbone.eval()
#         for parameter in backbone.parameters():
#             parameter.requires_grad_(False)

#         adapter = SymmetryResidualAdapter(feature_dim=self.feature_dim).to(self.device)
#         self.model = GAMWithSymmetryAdapter(
#             backbone=backbone,
#             adapter=adapter,
#             feature_dim=self.feature_dim,
#         ).to(self.device)

#         loaded = False
#         if self.adapter_path.exists() and not force_finetune:
#             loaded = self._load_adapter(self.adapter_path)

#         if not loaded:
#             if auto_finetune and self.catogory.lower() == "trousers":
#                 self.fine_tune_symmetry_adapter(
#                     steps=finetune_steps,
#                     deformation_count=deformation_count,
#                     training_points=training_points,
#                 )
#             else:
#                 cprint(
#                     "Symmetry adapter checkpoint was not found. Automatic "
#                     "trousers-only fine-tuning is enabled only for category "
#                     "'Trousers'; using the near-identity adapter.",
#                     color="yellow",
#                 )

#         self.model.eval()

#     @staticmethod
#     def _set_seed(seed: int) -> None:
#         torch.manual_seed(seed)
#         if torch.cuda.is_available():
#             torch.cuda.manual_seed(seed)
#             torch.cuda.manual_seed_all(seed)
#         np.random.seed(seed)
#         random.seed(seed)

#     def _load_torch_checkpoint(self, path: Path):
#         if not path.exists():
#             raise FileNotFoundError(f"GAM checkpoint does not exist: {path}")
#         try:
#             return torch.load(path, map_location=self.device, weights_only=False)
#         except TypeError:
#             return torch.load(path, map_location=self.device)

#     @staticmethod
#     def _extract_state_dict(checkpoint):
#         if not isinstance(checkpoint, dict):
#             return checkpoint

#         for key in ("model_state_dict", "state_dict", "model"):
#             candidate = checkpoint.get(key)
#             if isinstance(candidate, dict):
#                 checkpoint = candidate
#                 break

#         # Accept checkpoints saved from DataParallel/DistributedDataParallel.
#         if checkpoint and all(key.startswith("module.") for key in checkpoint):
#             checkpoint = {key[7:]: value for key, value in checkpoint.items()}
#         return checkpoint

#     @property
#     def backbone(self) -> nn.Module:
#         return self.model.backbone

#     @property
#     def adapter(self) -> SymmetryResidualAdapter:
#         return self.model.adapter

#     def _load_adapter(self, path: Path) -> bool:
#         try:
#             checkpoint = self._load_torch_checkpoint(path)
#             state_dict = checkpoint.get("adapter_state_dict", checkpoint)
#             self.adapter.load_state_dict(state_dict, strict=True)
#             cprint(f"Loaded fine-tuned GAM adapter: {path}", color="green")
#             return True
#         except (RuntimeError, KeyError, ValueError) as error:
#             cprint(
#                 f"Adapter checkpoint is incompatible and will be retrained: {error}",
#                 color="yellow",
#             )
#             return False

#     def _backbone_features(self, points: torch.Tensor) -> torch.Tensor:
#         with torch.no_grad():
#             features = self.backbone(points)
#         features, _ = _as_bnd_features(features, self.feature_dim)
#         return features

#     @staticmethod
#     def _principal_frame(points: torch.Tensor):
#         """Return centered xy points and a stable transverse/longitudinal frame."""
#         xy = points[0, :, :2]
#         center = xy.mean(dim=0, keepdim=True)
#         centered = xy - center
#         covariance = centered.T @ centered / max(centered.shape[0] - 1, 1)
#         _, eigenvectors = torch.linalg.eigh(covariance)
#         longitudinal_axis = eigenvectors[:, -1]
#         transverse_axis = torch.stack(
#             (-longitudinal_axis[1], longitudinal_axis[0])
#         )
#         transverse = centered @ transverse_axis
#         longitudinal = centered @ longitudinal_axis
#         return center, transverse_axis, longitudinal_axis, transverse, longitudinal

#     @staticmethod
#     def _infer_distal_sign(
#         transverse: torch.Tensor,
#         longitudinal: torch.Tensor,
#     ) -> float:
#         """
#         Find the trouser-cuff end without a garment-specific point index.

#         The cuff side has less occupancy around the center line because of the
#         gap between the two legs. This is used only to create training
#         deformations; inference itself contains no sleeve/cuff selection rule.
#         """
#         low_cut = torch.quantile(longitudinal, 0.18)
#         high_cut = torch.quantile(longitudinal, 0.82)
#         half_width = transverse.abs().amax().clamp_min(1e-6)
#         center_band = transverse.abs() < (0.18 * half_width)

#         low_occupancy = center_band[longitudinal <= low_cut].float().mean()
#         high_occupancy = center_band[longitudinal >= high_cut].float().mean()
#         return 1.0 if high_occupancy < low_occupancy else -1.0

#     def _bend_trouser_legs(
#         self,
#         points: torch.Tensor,
#         angle_degrees: float,
#         mirror: bool,
#         rotation_degrees: float,
#         scale_xy: Tuple[float, float],
#     ) -> torch.Tensor:
#         """
#         Topology-preserving deformation used as trousers-only training data.

#         It bends the two distal branches sideways. Point ordering never changes,
#         so each warped point has an exact feature target in the original pants.
#         """
#         (
#             center,
#             transverse_axis,
#             longitudinal_axis,
#             transverse,
#             longitudinal,
#         ) = self._principal_frame(points)
#         distal_sign = self._infer_distal_sign(transverse, longitudinal)

#         pivot = torch.quantile(
#             longitudinal,
#             0.52 if distal_sign > 0 else 0.48,
#         )
#         distal_distance = (
#             distal_sign * (longitudinal - pivot)
#         ).clamp_min(0.0)

#         angle = torch.tensor(
#             np.deg2rad(angle_degrees),
#             device=points.device,
#             dtype=points.dtype,
#         )
#         side = torch.where(
#             transverse >= 0,
#             torch.ones_like(transverse),
#             -torch.ones_like(transverse),
#         )

#         bent_transverse = transverse + side * distal_distance * torch.sin(angle)
#         bent_longitudinal = torch.where(
#             distal_distance > 0,
#             pivot + distal_sign * distal_distance * torch.cos(angle),
#             longitudinal,
#         )

#         if mirror:
#             bent_transverse = -bent_transverse

#         warped_xy = (
#             center
#             + bent_transverse.unsqueeze(-1) * transverse_axis
#             + bent_longitudinal.unsqueeze(-1) * longitudinal_axis
#         )
#         warped_xy = warped_xy - warped_xy.mean(dim=0, keepdim=True)
#         warped_xy[:, 0] *= scale_xy[0]
#         warped_xy[:, 1] *= scale_xy[1]

#         rotation = torch.tensor(
#             np.deg2rad(rotation_degrees),
#             device=points.device,
#             dtype=points.dtype,
#         )
#         cos_r, sin_r = torch.cos(rotation), torch.sin(rotation)
#         rotation_matrix = torch.stack(
#             (
#                 torch.stack((cos_r, -sin_r)),
#                 torch.stack((sin_r, cos_r)),
#             )
#         )
#         warped_xy = warped_xy @ rotation_matrix.T

#         warped = points.clone()
#         warped[0, :, :2] = warped_xy
#         warped[0, :, 2] = warped[0, :, 2] - warped[0, :, 2].mean()
#         return warped

#     @staticmethod
#     def _nearest_mirror_indices(points: torch.Tensor) -> torch.Tensor:
#         """Pair points across the PCA symmetry axis for a soft symmetry loss."""
#         xy = points[0, :, :2]
#         center = xy.mean(dim=0, keepdim=True)
#         centered = xy - center
#         covariance = centered.T @ centered / max(centered.shape[0] - 1, 1)
#         _, eigenvectors = torch.linalg.eigh(covariance)
#         longitudinal_axis = eigenvectors[:, -1]
#         transverse_axis = torch.stack(
#             (-longitudinal_axis[1], longitudinal_axis[0])
#         )

#         transverse = centered @ transverse_axis
#         longitudinal = centered @ longitudinal_axis
#         mirrored_xy = (
#             center
#             - transverse.unsqueeze(-1) * transverse_axis
#             + longitudinal.unsqueeze(-1) * longitudinal_axis
#         )
#         distances = torch.cdist(mirrored_xy.unsqueeze(0), xy.unsqueeze(0))[0]
#         return distances.argmin(dim=1)

#     def fine_tune_symmetry_adapter(
#         self,
#         steps: int = 400,
#         deformation_count: int = 12,
#         training_points: int = 1024,
#     ) -> None:
#         """
#         Train only the post-GAM adapter using the trousers demo.

#         Losses:
#           - deformation consistency: bent leg tips retain cuff features;
#           - identity distillation: the original trousers feature map is kept;
#           - soft bilateral contraction: paired sides become more similar, but
#             are not collapsed to identical features.
#         """
#         if not self.demo_path.exists():
#             raise FileNotFoundError(
#                 "Automatic fine-tuning needs the trousers demo point cloud: "
#                 f"{self.demo_path}"
#             )

#         demo_pcd = o3d.io.read_point_cloud(str(self.demo_path))
#         demo_points = np.asarray(demo_pcd.points)
#         if demo_points.size == 0:
#             raise ValueError(f"Demo point cloud is empty: {self.demo_path}")

#         normalized_points, *_ = normalize_pcd_points_xy(demo_points)
#         canonical_points = torch.from_numpy(
#             np.expand_dims(normalized_points, axis=0)
#         ).to(self.device, dtype=torch.float32)
#         canonical_features = self._backbone_features(canonical_points)

#         # Cache frozen-GAM outputs. Training the small adapter is then fast and
#         # the original GAM weights are never touched.
#         cached_deformations = []
#         generator = np.random.default_rng(42)
#         cprint("Preparing trousers-only symmetry deformations...", color="cyan")
#         for deformation_index in range(max(1, deformation_count)):
#             angle = float(generator.uniform(45.0, 105.0))
#             rotation = float(generator.uniform(-35.0, 35.0))
#             scale = (
#                 float(generator.uniform(0.82, 1.18)),
#                 float(generator.uniform(0.82, 1.18)),
#             )
#             warped_points = self._bend_trouser_legs(
#                 canonical_points,
#                 angle_degrees=angle,
#                 mirror=bool(deformation_index % 2),
#                 rotation_degrees=rotation,
#                 scale_xy=scale,
#             )
#             warped_features = self._backbone_features(warped_points)
#             cached_deformations.append(
#                 (warped_features.cpu(), warped_points.cpu())
#             )

#         mirror_indices = self._nearest_mirror_indices(canonical_points).to(
#             self.device
#         )
#         point_count = canonical_points.shape[1]
#         sample_count = min(max(64, training_points), point_count)

#         self.adapter.train()
#         optimizer = torch.optim.AdamW(
#             self.adapter.parameters(),
#             lr=2e-4,
#             weight_decay=1e-4,
#         )
#         scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
#             optimizer,
#             T_max=max(1, steps),
#             eta_min=2e-5,
#         )

#         cprint(
#             f"Fine-tuning post-GAM adapter ({steps} steps, backbone frozen)...",
#             color="cyan",
#             attrs=["bold"],
#         )
#         for step in range(max(1, steps)):
#             deformation_index = step % len(cached_deformations)
#             warped_features_cpu, warped_points_cpu = cached_deformations[
#                 deformation_index
#             ]
#             warped_features = warped_features_cpu.to(self.device)
#             warped_points = warped_points_cpu.to(self.device)

#             sample_indices = torch.randperm(
#                 point_count,
#                 device=self.device,
#             )[:sample_count]
#             paired_indices = mirror_indices[sample_indices]

#             deformed_output = self.adapter(
#                 warped_features[:, sample_indices],
#                 warped_points[:, sample_indices],
#             )
#             target_output = canonical_features[:, sample_indices]
#             deformation_loss = (
#                 1.0
#                 - F.cosine_similarity(
#                     deformed_output,
#                     target_output,
#                     dim=-1,
#                 )
#             ).mean()

#             canonical_pair_indices = torch.cat(
#                 (sample_indices, paired_indices),
#                 dim=0,
#             )
#             canonical_output = self.adapter(
#                 canonical_features[:, canonical_pair_indices],
#                 canonical_points[:, canonical_pair_indices],
#             )
#             first_output, mirrored_output = canonical_output.chunk(2, dim=1)
#             first_target = canonical_features[:, sample_indices]
#             mirrored_target = canonical_features[:, paired_indices]

#             identity_loss = (
#                 1.0
#                 - F.cosine_similarity(
#                     canonical_output,
#                     canonical_features[:, canonical_pair_indices],
#                     dim=-1,
#                 )
#             ).mean()
#             magnitude_loss = (
#                 (canonical_output - canonical_features[:, canonical_pair_indices])
#                 .pow(2)
#                 .mean()
#                 / canonical_features[:, canonical_pair_indices]
#                 .pow(2)
#                 .mean()
#                 .clamp_min(1e-8)
#             )

#             original_pair_distance = (
#                 1.0
#                 - F.cosine_similarity(
#                     first_target,
#                     mirrored_target,
#                     dim=-1,
#                 )
#             )
#             adapted_pair_distance = (
#                 1.0
#                 - F.cosine_similarity(
#                     first_output,
#                     mirrored_output,
#                     dim=-1,
#                 )
#             )
#             # Only reduce bilateral distance by 15%; do not collapse left/right.
#             symmetry_loss = F.relu(
#                 adapted_pair_distance - 0.85 * original_pair_distance
#             ).mean()

#             loss = (
#                 deformation_loss
#                 + 2.5 * identity_loss
#                 + 0.15 * symmetry_loss
#                 + 0.10 * magnitude_loss
#             )

#             optimizer.zero_grad(set_to_none=True)
#             loss.backward()
#             torch.nn.utils.clip_grad_norm_(self.adapter.parameters(), max_norm=1.0)
#             optimizer.step()
#             scheduler.step()

#             if step == 0 or (step + 1) % 50 == 0 or step + 1 == steps:
#                 cprint(
#                     "adapter step "
#                     f"{step + 1:4d}/{steps}: "
#                     f"loss={loss.item():.6f}, "
#                     f"deform={deformation_loss.item():.6f}, "
#                     f"preserve={identity_loss.item():.6f}",
#                     color="cyan",
#                 )

#         self.adapter.eval()
#         with torch.no_grad():
#             canonical_after = self.adapter(
#                 canonical_features,
#                 canonical_points,
#             )
#             preservation_similarity = F.cosine_similarity(
#                 canonical_after,
#                 canonical_features,
#                 dim=-1,
#             ).mean().item()

#         cprint(
#             "Mean trousers feature preservation cosine similarity: "
#             f"{preservation_similarity:.6f}",
#             color="green",
#         )
#         self.adapter_path.parent.mkdir(parents=True, exist_ok=True)
#         torch.save(
#             {
#                 "adapter_state_dict": self.adapter.state_dict(),
#                 "category": self.catogory,
#                 "feature_dim": self.feature_dim,
#                 "base_checkpoint": str(self.resume_path),
#                 "method": "frozen_gam_bending_consistency_v1",
#                 "trousers_preservation_cosine": preservation_similarity,
#             },
#             self.adapter_path,
#         )
#         cprint(f"Saved fine-tuned GAM adapter: {self.adapter_path}", color="green")

#     def get_feature(
#         self,
#         input_pcd: np.ndarray,
#         index_list: Optional[list] = None,
#     ):
#         """Get frozen-GAM features corrected by the fine-tuned adapter."""
#         normalized_pcd, *_ = normalize_pcd_points_xy(input_pcd)
#         normalized_pcd = np.expand_dims(normalized_pcd, axis=0)
#         points = torch.from_numpy(normalized_pcd).to(
#             self.device,
#             dtype=torch.float32,
#         )

#         with torch.no_grad():
#             pcd_features = self.model(points)
#             pcd_features, _ = _as_bnd_features(
#                 pcd_features,
#                 self.feature_dim,
#             )
#             pcd_features = pcd_features.squeeze(0)

#         if index_list is not None:
#             indices = torch.as_tensor(
#                 index_list,
#                 device=pcd_features.device,
#                 dtype=torch.long,
#             )
#             return pcd_features.index_select(0, indices)
#         return pcd_features

#     def get_manipulation_points(
#         self,
#         input_pcd: np.ndarray,
#         index_list: Optional[list] = None,
#     ):
#         """Get manipulation points by adapted feature correspondence."""
#         demo_pcd = np.asarray(
#             o3d.io.read_point_cloud(str(self.demo_path)).points
#         )
#         demo_feature = self.get_feature(demo_pcd, index_list)
#         manipulate_feature = self.get_feature(input_pcd)

#         demo_feature_normalized = F.normalize(demo_feature, p=2, dim=1)
#         manipulate_feature_normalized = F.normalize(
#             manipulate_feature,
#             p=2,
#             dim=1,
#         )
#         result = torch.matmul(
#             demo_feature_normalized,
#             manipulate_feature_normalized.T,
#         )

#         cprint(
#             "----------- GAM Inference Begin -----------",
#             color="blue",
#             attrs=["bold"],
#         )
#         max_values, max_indices = torch.max(result, dim=1)
#         cprint(f"similarity score: {max_values}", color="blue")
#         cprint(f"relevant indices: {max_indices}", color="blue")
#         cprint(f"similarity result shape: {result.shape}", color="blue")

#         output_indices = max_indices.detach().cpu().numpy()
#         manipulation_points = input_pcd[output_indices]
#         cprint(f"manipulation points:\n{manipulation_points}", color="blue")
#         cprint(
#             "----------- GAM Inference End -----------",
#             color="blue",
#             attrs=["bold"],
#         )
#         return (
#             manipulation_points,
#             output_indices,
#             result.detach().cpu().numpy(),
#         )

#     def get_colormap_points(self, input_pcd: np.ndarray):
#         """Return the demo-point correspondence index for every input point."""
#         demo_pcd = np.asarray(
#             o3d.io.read_point_cloud(str(self.demo_path)).points
#         )
#         demo_feature = self.get_feature(demo_pcd)
#         manipulate_feature = self.get_feature(input_pcd)

#         demo_feature_normalized = F.normalize(demo_feature, p=2, dim=1)
#         manipulate_feature_normalized = F.normalize(
#             manipulate_feature,
#             p=2,
#             dim=1,
#         )
#         result = torch.matmul(
#             manipulate_feature_normalized,
#             demo_feature_normalized.T,
#         )
#         max_values, max_indices = torch.max(result, dim=1)
#         print("similarity score: ", max_values)
#         print("relevant indices: ", max_indices)

#         color_indices = max_indices.detach().cpu().numpy()
#         corresponding_demo_points = demo_pcd[color_indices]
#         return corresponding_demo_points, color_indices

#     def get_demo_garment_with_color(self):
#         """Get the demo garment and its visualization colors."""
#         demo_pcd = o3d.io.read_point_cloud(str(self.demo_path))
#         self.demo_points = np.asarray(demo_pcd.points)
#         self.demo_points_color = colormap(self.demo_points)
#         return self.demo_points, self.demo_points_color

#     def visualize_pcd_corresponce(
#         self,
#         input_pcd: np.ndarray,
#         save_or_not: bool = False,
#         save_path: Optional[str] = None,
#     ):
#         """Visualize feature correspondence between input and demo garment."""
#         self.get_demo_garment_with_color()
#         visualize_pointcloud_with_colors(
#             self.demo_points,
#             self.demo_points_color,
#         )
#         _, color_indices = self.get_colormap_points(input_pcd)
#         colors = self.demo_points_color[color_indices]
#         visualize_pointcloud_with_colors(
#             input_pcd,
#             colors,
#             save_or_not=save_or_not,
#             save_path=save_path,
#         )


















# import os
# import random
# import sys
# from pathlib import Path
# from typing import Optional, Tuple

# import numpy as np
# import open3d as o3d
# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# from termcolor import cprint


# sys.path.append(os.getcwd())
# sys.path.append("Model_HALO/GAM")

# from Model_HALO.GAM.model.pointnet2_GAM import GAM_Model
# from Env_Config.Utils_Project.Point_Cloud_Manip import (
#     colormap,
#     normalize_pcd_points_xy,
#     visualize_pointcloud_with_colors,
# )


# def _features_bnd(
#     features: torch.Tensor,
#     feature_dim: int,
# ) -> Tuple[torch.Tensor, bool]:
#     """Convert GAM output to [batch, point, feature]."""
#     if features.ndim == 2:
#         features = features.unsqueeze(0)
#     if features.ndim != 3:
#         raise ValueError(f"Invalid GAM output shape: {tuple(features.shape)}")
#     if features.shape[-1] == feature_dim:
#         return features, False
#     if features.shape[1] == feature_dim:
#         return features.transpose(1, 2).contiguous(), True
#     raise ValueError(
#         f"Feature dimension {feature_dim} is absent from {tuple(features.shape)}"
#     )


# def _points_bnd(points: torch.Tensor) -> torch.Tensor:
#     """Convert point cloud to [batch, point, xyz]."""
#     if points.ndim == 2:
#         points = points.unsqueeze(0)
#     if points.ndim != 3:
#         raise ValueError(f"Invalid point-cloud shape: {tuple(points.shape)}")
#     if points.shape[-1] == 3:
#         return points
#     if points.shape[1] == 3:
#         return points.transpose(1, 2).contiguous()
#     raise ValueError(f"XYZ dimension is absent from {tuple(points.shape)}")


# class KNNLeftRightTopologyLayer(nn.Module):
#     """
#     Learned k-NN topology layer placed after frozen GAM.

#     It keeps local garment connectivity but deliberately emphasizes signed
#     left-to-right position. Thus the two horizontal semantic axes become:

#       sleeve: purple -> pink
#       body hem: blue -> green/cyan

#     Vertical position is weak, so a long low sleeve keeps its sleeve identity.
#     """

#     def __init__(
#         self,
#         feature_dim: int = 512,
#         hidden_dim: int = 320,
#         raw_feature_blend: float = 0.03,
#     ):
#         super().__init__()
#         self.feature_dim = feature_dim
#         self.raw_feature_blend = raw_feature_blend
#         self.geometry_dim = 32

#         self.topology_net = nn.Sequential(
#             nn.Linear(self.geometry_dim, hidden_dim),
#             nn.LayerNorm(hidden_dim),
#             nn.GELU(),
#             nn.Linear(hidden_dim, hidden_dim),
#             nn.LayerNorm(hidden_dim),
#             nn.GELU(),
#             nn.Linear(hidden_dim, feature_dim),
#         )
#         self.raw_projection = nn.Linear(
#             feature_dim,
#             feature_dim,
#             bias=False,
#         )
#         nn.init.eye_(self.raw_projection.weight)

#     @staticmethod
#     def _normalized_coordinates(
#         points: torch.Tensor,
#     ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
#         points = _points_bnd(points)
#         centered = points - points.mean(dim=1, keepdim=True)
#         scale = centered.abs().amax(dim=1, keepdim=True).clamp_min(1e-6)
#         normalized = centered / scale
#         return normalized[..., 0], normalized[..., 1], normalized[..., 2]

#     def geometry(self, points: torch.Tensor) -> torch.Tensor:
#         """
#         Build signed-X-heavy features plus two-scale k-NN connectivity.

#         Y is retained only weakly for separating the sleeve axis from the hem
#         axis. It cannot dominate when a sleeve happens to extend downward.
#         """
#         points = _points_bnd(points)
#         x, y, z = self._normalized_coordinates(points)

#         # Signed X channels are intentionally amplified. Multiple frequencies
#         # make the learned field progress smoothly from left to right.
#         x_lr = 2.75 * x
#         y_weak = 0.30 * y
#         base = torch.stack(
#             (
#                 x_lr,
#                 x_lr.square() * torch.sign(x_lr),
#                 x_lr.pow(3),
#                 torch.sin(np.pi * x),
#                 torch.cos(np.pi * x),
#                 torch.sin(2.0 * np.pi * x),
#                 x.abs(),
#                 y_weak,
#                 y_weak.square() * torch.sign(y_weak),
#                 z,
#                 x * y_weak,
#                 x.abs() * y_weak,
#                 torch.sqrt(x.square() + y_weak.square() + 1e-8),
#                 torch.maximum(x.abs(), y_weak.abs()),
#             ),
#             dim=-1,
#         )

#         normalized_xy = torch.stack((x, y), dim=-1)
#         pairwise = torch.cdist(normalized_xy, normalized_xy)
#         topology = []
#         point_count = points.shape[1]

#         for requested_k in (12, 48):
#             k = min(requested_k, max(point_count - 1, 1))
#             indices = pairwise.topk(
#                 k=min(k + 1, point_count),
#                 largest=False,
#                 dim=-1,
#             ).indices
#             if indices.shape[-1] > 1:
#                 indices = indices[..., 1:]

#             batch = torch.arange(
#                 points.shape[0],
#                 device=points.device,
#             ).view(-1, 1, 1).expand_as(indices)
#             neighbor_xy = normalized_xy[batch, indices]
#             offset = neighbor_xy - normalized_xy.unsqueeze(2)
#             dx = offset[..., 0]
#             dy = offset[..., 1]
#             distance = offset.norm(dim=-1)

#             topology.extend(
#                 (
#                     1.75 * dx.abs().mean(dim=-1),
#                     0.50 * dy.abs().mean(dim=-1),
#                     1.75 * dx.square().mean(dim=-1),
#                     0.50 * dy.square().mean(dim=-1),
#                     (dx * dy).abs().mean(dim=-1),
#                     distance.mean(dim=-1),
#                     distance.amax(dim=-1),
#                     # A narrow horizontal branch (sleeve) differs from the
#                     # broad body even when both occupy the same Y range.
#                     dx.abs().mean(dim=-1)
#                     / dy.abs().mean(dim=-1).clamp_min(1e-5),
#                     dy.abs().mean(dim=-1)
#                     / dx.abs().mean(dim=-1).clamp_min(1e-5),
#                 )
#             )

#         return torch.cat(
#             (base, torch.stack(topology, dim=-1)),
#             dim=-1,
#         )

#     def forward(
#         self,
#         raw_features: torch.Tensor,
#         points: torch.Tensor,
#     ) -> torch.Tensor:
#         raw_features, was_transposed = _features_bnd(
#             raw_features,
#             self.feature_dim,
#         )
#         learned = self.topology_net(self.geometry(points))

#         # The learned topology map controls correspondence. The tiny GAM blend
#         # only preserves local texture and cannot restore vertical banding.
#         if self.raw_feature_blend > 0:
#             learned_norm = learned.norm(
#                 dim=-1,
#                 keepdim=True,
#             ).clamp_min(1e-6)
#             raw = F.normalize(
#                 self.raw_projection(raw_features),
#                 p=2,
#                 dim=-1,
#             ) * learned_norm
#             output = (
#                 (1.0 - self.raw_feature_blend) * learned
#                 + self.raw_feature_blend * raw
#             )
#         else:
#             output = learned

#         if was_transposed:
#             return output.transpose(1, 2).contiguous()
#         return output


# class GAMWithKNNTopologyLayer(nn.Module):
#     """Frozen GAM followed by the learned k-NN topology layer."""

#     def __init__(
#         self,
#         backbone: nn.Module,
#         topology_layer: KNNLeftRightTopologyLayer,
#     ):
#         super().__init__()
#         self.backbone = backbone
#         self.topology_layer = topology_layer

#     def forward(self, points: torch.Tensor) -> torch.Tensor:
#         with torch.no_grad():
#             raw_features = self.backbone(points)
#         return self.topology_layer(raw_features, points)


# class GAM_Encapsulation:
#     """
#     Existing usage remains unchanged:

#         self.model = GAM_Encapsulation(catogory="Trousers")

#     The trousers GAM backbone stays frozen. Only the added k-NN topology layer
#     is trained and automatically loaded on later runs.
#     """

#     def __init__(
#         self,
#         catogory: str = "Tops_LongSleeve",
#         auto_finetune: bool = True,
#         force_finetune: bool = False,
#         finetune_steps: int = 3600,
#         training_points: int = 1536,
#         topology_augmentations: int = 28,
#     ):
#         self.catogory = catogory
#         self.feature_dim = 512
#         self.device = torch.device(
#             "cuda:0" if torch.cuda.is_available() else "cpu"
#         )
#         checkpoint_dir = Path("Model_HALO/GAM/checkpoints") / catogory
#         self.resume_path = checkpoint_dir / "checkpoint.pth"
#         self.demo_path = checkpoint_dir / "demo_garment.ply"
#         self.layer_path = (
#             checkpoint_dir / "checkpoint_knn_lr_topology_layer.pth"
#         )

#         self._set_seed(42)
#         backbone = GAM_Model(
#             normal_channel=False,
#             feature_dim=self.feature_dim,
#         )
#         checkpoint = self._load_checkpoint(self.resume_path)
#         backbone.load_state_dict(self._extract_state_dict(checkpoint))
#         backbone = backbone.to(self.device).eval()
#         for parameter in backbone.parameters():
#             parameter.requires_grad_(False)

#         topology_layer = KNNLeftRightTopologyLayer(
#             feature_dim=self.feature_dim,
#         ).to(self.device)
#         self.model = GAMWithKNNTopologyLayer(
#             backbone,
#             topology_layer,
#         ).to(self.device)

#         loaded = False
#         if self.layer_path.exists() and not force_finetune:
#             loaded = self._load_topology_layer()
#         if not loaded:
#             if auto_finetune and catogory.lower() == "trousers":
#                 self.fine_tune_topology_layer(
#                     steps=finetune_steps,
#                     training_points=training_points,
#                     topology_augmentations=topology_augmentations,
#                 )
#             else:
#                 cprint(
#                     "KNN topology checkpoint is absent. Initialize once with "
#                     "catogory='Trousers' to train it.",
#                     color="yellow",
#                 )
#         self.model.eval()

#     @staticmethod
#     def _set_seed(seed: int) -> None:
#         torch.manual_seed(seed)
#         if torch.cuda.is_available():
#             torch.cuda.manual_seed_all(seed)
#         np.random.seed(seed)
#         random.seed(seed)

#     def _load_checkpoint(self, path: Path):
#         if not path.exists():
#             raise FileNotFoundError(f"Checkpoint does not exist: {path}")
#         try:
#             return torch.load(
#                 path,
#                 map_location=self.device,
#                 weights_only=False,
#             )
#         except TypeError:
#             return torch.load(path, map_location=self.device)

#     @staticmethod
#     def _extract_state_dict(checkpoint):
#         if not isinstance(checkpoint, dict):
#             return checkpoint
#         for key in ("model_state_dict", "state_dict", "model"):
#             if isinstance(checkpoint.get(key), dict):
#                 checkpoint = checkpoint[key]
#                 break
#         if checkpoint and all(key.startswith("module.") for key in checkpoint):
#             checkpoint = {
#                 key.removeprefix("module."): value
#                 for key, value in checkpoint.items()
#             }
#         return checkpoint

#     @property
#     def backbone(self) -> nn.Module:
#         return self.model.backbone

#     @property
#     def topology_layer(self) -> KNNLeftRightTopologyLayer:
#         return self.model.topology_layer

#     def _load_topology_layer(self) -> bool:
#         try:
#             checkpoint = self._load_checkpoint(self.layer_path)
#             self.topology_layer.load_state_dict(
#                 checkpoint["topology_layer_state_dict"],
#                 strict=True,
#             )
#             cprint(
#                 f"Loaded left-right k-NN GAM layer: {self.layer_path}",
#                 color="green",
#             )
#             return True
#         except (RuntimeError, KeyError, ValueError) as error:
#             cprint(
#                 f"KNN topology layer will be retrained: {error}",
#                 color="yellow",
#             )
#             return False

#     def _read_demo(self) -> Tuple[np.ndarray, torch.Tensor]:
#         if not self.demo_path.exists():
#             raise FileNotFoundError(
#                 f"Trousers demo point cloud does not exist: {self.demo_path}"
#             )
#         demo = np.asarray(
#             o3d.io.read_point_cloud(str(self.demo_path)).points
#         )
#         if demo.size == 0:
#             raise ValueError(f"Demo point cloud is empty: {self.demo_path}")
#         normalized, *_ = normalize_pcd_points_xy(demo)
#         tensor = torch.from_numpy(normalized).unsqueeze(0).to(
#             self.device,
#             dtype=torch.float32,
#         )
#         return demo, tensor

#     @staticmethod
#     def _trousers_coordinates(
#         points: torch.Tensor,
#     ) -> Tuple[torch.Tensor, torch.Tensor, float]:
#         """Return left/right X and cuff(0)-to-waist(1) coordinates."""
#         points = _points_bnd(points)
#         centered = points - points.mean(dim=1, keepdim=True)
#         x = centered[0, :, 0]
#         y = centered[0, :, 1]
#         x_scale = x.abs().amax().clamp_min(1e-6)
#         center_band = x.abs() < (0.16 * x_scale)
#         lower = y <= torch.quantile(y, 0.20)
#         upper = y >= torch.quantile(y, 0.80)
#         waist_sign = (
#             1.0
#             if center_band[upper].float().mean()
#             > center_band[lower].float().mean()
#             else -1.0
#         )
#         semantic_y = waist_sign * y
#         cuff_to_waist = (
#             (semantic_y - semantic_y.amin())
#             / (semantic_y.amax() - semantic_y.amin()).clamp_min(1e-6)
#         )
#         return x / x_scale, cuff_to_waist, waist_sign

#     def _make_top_like_warp(
#         self,
#         points: torch.Tensor,
#         sleeve_extension: float,
#         sleeve_drop: float,
#         hem_width: float,
#     ) -> torch.Tensor:
#         """
#         Stretch trousers waist branches into sleeves without changing point IDs.

#         The original left-to-right GAM feature order is therefore retained:
#         waist purple->pink becomes sleeves purple->pink, and cuffs blue->green
#         become the shirt hem blue->green.
#         """
#         points = _points_bnd(points)
#         mean = points.mean(dim=1, keepdim=True)
#         centered = points - mean
#         x = centered[0, :, 0]
#         y = centered[0, :, 1]
#         lr, cuff_to_waist, waist_sign = self._trousers_coordinates(points)
#         side = torch.where(lr >= 0, 1.0, -1.0)
#         x_scale = x.abs().amax().clamp_min(1e-6)

#         shoulder = torch.exp(
#             -0.5 * ((cuff_to_waist - 0.76) / 0.18).square()
#         )
#         outer = lr.abs().pow(0.52)
#         extension = (
#             side * x_scale * sleeve_extension * shoulder * outer
#         )
#         warped_x = x + extension

#         semantic_y = waist_sign * y
#         warped_semantic_y = (
#             semantic_y
#             - sleeve_drop * extension.abs() * shoulder
#         )
#         hem = ((0.34 - cuff_to_waist) / 0.34).clamp(0.0, 1.0)
#         warped_x = warped_x + side * x_scale * hem_width * hem

#         centered[0, :, 0] = warped_x
#         centered[0, :, 1] = waist_sign * warped_semantic_y
#         return centered + mean

#     def fine_tune_topology_layer(
#         self,
#         steps: int = 1800,
#         training_points: int = 1536,
#         topology_augmentations: int = 28,
#     ) -> None:
#         """
#         Train only the post-GAM layer from trousers and top-like deformations.

#         Signed left/right consistency receives the highest endpoint weight.
#         """
#         _, demo_points = self._read_demo()
#         with torch.no_grad():
#             teacher_features = self.backbone(demo_points)
#             teacher_features, _ = _features_bnd(
#                 teacher_features,
#                 self.feature_dim,
#             )

#         lr, cuff_to_waist, _ = self._trousers_coordinates(demo_points)
#         outer = lr.abs()
#         masks = (
#             (lr < -0.52) & (cuff_to_waist > 0.62),
#             (lr > 0.52) & (cuff_to_waist > 0.62),
#             (lr < -0.52) & (cuff_to_waist < 0.32),
#             (lr > 0.52) & (cuff_to_waist < 0.32),
#         )
#         names = (
#             "left_sleeve_purple",
#             "right_sleeve_pink",
#             "left_hem_blue",
#             "right_hem_green",
#         )
#         for name, mask in zip(names, masks):
#             if not bool(mask.any()):
#                 raise ValueError(f"Cannot form training region: {name}")

#         with torch.no_grad():
#             anchor_targets = torch.stack(
#                 [
#                     teacher_features[0, mask].mean(dim=0)
#                     for mask in masks
#                 ],
#                 dim=0,
#             )

#         shapes = [demo_points]
#         generator = np.random.default_rng(42)
#         for _ in range(max(1, topology_augmentations)):
#             shapes.append(
#                 self._make_top_like_warp(
#                     demo_points,
#                     sleeve_extension=float(generator.uniform(1.0, 3.4)),
#                     sleeve_drop=float(generator.uniform(0.05, 1.80)),
#                     hem_width=float(generator.uniform(0.05, 0.40)),
#                 )
#             )

#         cprint(
#             "Caching k-NN garment topology features...",
#             color="cyan",
#         )
#         with torch.no_grad():
#             geometry_cache = [
#                 self.topology_layer.geometry(shape)
#                 for shape in shapes
#             ]

#         point_count = demo_points.shape[1]
#         sample_count = min(max(128, training_points), point_count)
#         # Left/right endpoint points receive stronger supervision than vertical
#         # interior points. This is the requested small horizontal correction.
#         horizontal_weight = (
#             1.0
#             + 3.0 * outer
#             + 5.0
#             * (
#                 (outer > 0.52)
#                 & (
#                     (cuff_to_waist > 0.62)
#                     | (cuff_to_waist < 0.32)
#                 )
#             ).float()
#         ).unsqueeze(0)

#         optimizer = torch.optim.AdamW(
#             self.topology_layer.parameters(),
#             lr=3e-4,
#             weight_decay=1e-5,
#         )
#         scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
#             optimizer,
#             T_max=max(1, steps),
#             eta_min=2e-5,
#         )
#         self.topology_layer.train()

#         for step in range(max(1, steps)):
#             shape_index = step % len(shapes)
#             indices = torch.randperm(
#                 point_count,
#                 device=self.device,
#             )[:sample_count]
#             predicted = self.topology_layer.topology_net(
#                 geometry_cache[shape_index][:, indices]
#             )
#             target = teacher_features[:, indices]

#             cosine_error = (
#                 1.0
#                 - F.cosine_similarity(predicted, target, dim=-1)
#             )
#             weight = horizontal_weight[:, indices]
#             point_loss = (
#                 (cosine_error * weight).sum()
#                 / weight.sum().clamp_min(1e-6)
#             )
#             scale_loss = F.mse_loss(predicted, target)

#             # Explicitly keep each horizontal axis ordered left-to-right.
#             full_prediction = self.topology_layer.topology_net(
#                 geometry_cache[shape_index]
#             )
#             predicted_anchors = torch.stack(
#                 [
#                     full_prediction[0, mask].mean(dim=0)
#                     for mask in masks
#                 ],
#                 dim=0,
#             )
#             anchor_loss = (
#                 1.0
#                 - F.cosine_similarity(
#                     predicted_anchors,
#                     anchor_targets,
#                     dim=-1,
#                 )
#             ).mean()

#             # Prevent left/right collapse on sleeve and hem axes.
#             predicted_lr_distance = torch.stack(
#                 (
#                     1.0
#                     - F.cosine_similarity(
#                         predicted_anchors[0:1],
#                         predicted_anchors[1:2],
#                         dim=-1,
#                     ),
#                     1.0
#                     - F.cosine_similarity(
#                         predicted_anchors[2:3],
#                         predicted_anchors[3:4],
#                         dim=-1,
#                     ),
#                 )
#             ).mean()
#             target_lr_distance = torch.stack(
#                 (
#                     1.0
#                     - F.cosine_similarity(
#                         anchor_targets[0:1],
#                         anchor_targets[1:2],
#                         dim=-1,
#                     ),
#                     1.0
#                     - F.cosine_similarity(
#                         anchor_targets[2:3],
#                         anchor_targets[3:4],
#                         dim=-1,
#                     ),
#                 )
#             ).mean()
#             lr_separation_loss = F.relu(
#                 0.90 * target_lr_distance - predicted_lr_distance
#             )

#             loss = (
#                 1.5 * point_loss
#                 + 3.0 * anchor_loss
#                 + 2.0 * lr_separation_loss
#                 + 0.08 * scale_loss
#             )
#             optimizer.zero_grad(set_to_none=True)
#             loss.backward()
#             torch.nn.utils.clip_grad_norm_(
#                 self.topology_layer.parameters(),
#                 max_norm=2.0,
#             )
#             optimizer.step()
#             scheduler.step()

#             if step == 0 or (step + 1) % 100 == 0 or step + 1 == steps:
#                 cprint(
#                     f"kNN-LR step {step + 1:4d}/{steps}: "
#                     f"loss={loss.item():.6f}, "
#                     f"point_cos={1.0 - point_loss.item():.6f}, "
#                     f"anchor_cos={1.0 - anchor_loss.item():.6f}",
#                     color="cyan",
#                 )

#         self.topology_layer.eval()
#         self.layer_path.parent.mkdir(parents=True, exist_ok=True)
#         torch.save(
#             {
#                 "topology_layer_state_dict": (
#                     self.topology_layer.state_dict()
#                 ),
#                 "method": "knn_topology_left_right_emphasis_v5",
#                 "anchor_order": names,
#             },
#             self.layer_path,
#         )
#         cprint(
#             f"Saved left-right k-NN GAM layer: {self.layer_path}",
#             color="green",
#         )

#     def get_feature(
#         self,
#         input_pcd: np.ndarray,
#         index_list: Optional[list] = None,
#     ) -> torch.Tensor:
#         normalized, *_ = normalize_pcd_points_xy(
#             np.asarray(input_pcd)
#         )
#         points = torch.from_numpy(normalized).unsqueeze(0).to(
#             self.device,
#             dtype=torch.float32,
#         )
#         with torch.no_grad():
#             features = self.model(points)
#             features, _ = _features_bnd(features, self.feature_dim)
#             features = features.squeeze(0)

#         if index_list is not None:
#             indices = torch.as_tensor(
#                 index_list,
#                 device=self.device,
#                 dtype=torch.long,
#             )
#             return features.index_select(0, indices)
#         return features

#     def get_manipulation_points(
#         self,
#         input_pcd: np.ndarray,
#         index_list: Optional[list] = None,
#     ):
#         demo_pcd = np.asarray(
#             o3d.io.read_point_cloud(str(self.demo_path)).points
#         )
#         demo_feature = self.get_feature(demo_pcd, index_list)
#         input_feature = self.get_feature(input_pcd)
#         result = torch.matmul(
#             F.normalize(demo_feature, p=2, dim=1),
#             F.normalize(input_feature, p=2, dim=1).T,
#         )
#         max_values, max_indices = torch.max(result, dim=1)
#         indices = max_indices.detach().cpu().numpy()
#         manipulation_points = np.asarray(input_pcd)[indices]

#         cprint(
#             "----------- GAM Inference Begin -----------",
#             color="blue",
#             attrs=["bold"],
#         )
#         cprint(f"similarity score: {max_values}", color="blue")
#         cprint(f"relevant indices: {max_indices}", color="blue")
#         cprint(f"manipulation points:\n{manipulation_points}", color="blue")
#         cprint(
#             "----------- GAM Inference End -----------",
#             color="blue",
#             attrs=["bold"],
#         )
#         return (
#             manipulation_points,
#             indices,
#             result.detach().cpu().numpy(),
#         )

#     def get_colormap_points(self, input_pcd: np.ndarray):
#         demo_pcd = np.asarray(
#             o3d.io.read_point_cloud(str(self.demo_path)).points
#         )
#         demo_feature = self.get_feature(demo_pcd)
#         input_feature = self.get_feature(input_pcd)
#         result = torch.matmul(
#             F.normalize(input_feature, p=2, dim=1),
#             F.normalize(demo_feature, p=2, dim=1).T,
#         )
#         max_values, max_indices = torch.max(result, dim=1)
#         print("similarity score: ", max_values)
#         print("relevant indices: ", max_indices)
#         color_indices = max_indices.detach().cpu().numpy()
#         return demo_pcd[color_indices], color_indices

#     def get_demo_garment_with_color(self):
#         demo_pcd = o3d.io.read_point_cloud(str(self.demo_path))
#         self.demo_points = np.asarray(demo_pcd.points)
#         self.demo_points_color = colormap(self.demo_points)
#         return self.demo_points, self.demo_points_color

#     def visualize_pcd_corresponce(
#         self,
#         input_pcd: np.ndarray,
#         save_or_not: bool = False,
#         save_path: Optional[str] = None,
#     ):
#         self.get_demo_garment_with_color()
#         visualize_pointcloud_with_colors(
#             self.demo_points,
#             self.demo_points_color,
#         )
#         _, color_indices = self.get_colormap_points(input_pcd)
#         colors = self.demo_points_color[color_indices]
#         visualize_pointcloud_with_colors(
#             input_pcd,
#             colors,
#             save_or_not=save_or_not,
#             save_path=save_path,
#         )















########################################################################################################################
import os
import random
import sys
from pathlib import Path
from typing import Optional, Tuple

import numpy as np
import open3d as o3d
import torch
import torch.nn as nn
import torch.nn.functional as F
from termcolor import cprint


sys.path.append(os.getcwd())
sys.path.append("Model_HALO/GAM")

from Model_HALO.GAM.model.pointnet2_GAM import GAM_Model
from Env_Config.Utils_Project.Point_Cloud_Manip import (
    colormap,
    normalize_pcd_points_xy,
    visualize_pointcloud_with_colors,
)


def _features_bnd(
    features: torch.Tensor,
    feature_dim: int,
) -> Tuple[torch.Tensor, bool]:
    """Convert GAM output to [batch, point, feature]."""
    if features.ndim == 2:
        features = features.unsqueeze(0)
    if features.ndim != 3:
        raise ValueError(f"Invalid GAM output shape: {tuple(features.shape)}")
    if features.shape[-1] == feature_dim:
        return features, False
    if features.shape[1] == feature_dim:
        return features.transpose(1, 2).contiguous(), True
    raise ValueError(
        f"Feature dimension {feature_dim} is absent from {tuple(features.shape)}"
    )


def _points_bnd(points: torch.Tensor) -> torch.Tensor:
    """Convert point cloud to [batch, point, xyz]."""
    if points.ndim == 2:
        points = points.unsqueeze(0)
    if points.ndim != 3:
        raise ValueError(f"Invalid point-cloud shape: {tuple(points.shape)}")
    if points.shape[-1] == 3:
        return points
    if points.shape[1] == 3:
        return points.transpose(1, 2).contiguous()
    raise ValueError(f"XYZ dimension is absent from {tuple(points.shape)}")


class PantsBilateralLayer(nn.Module):
    """
    Original balanced multi-scale k-NN topology layer.

    This is the version before signed-X reinforcement. X and Y geometry are
    treated at comparable scale, so both sleeves and the body/hem contribute to
    correspondence instead of concentrating matches on sleeves only.
    """

    def __init__(
        self,
        feature_dim: int = 512,
        hidden_dim: int = 256,
        geometry_dim: int = 24,
    ):
        super().__init__()
        self.feature_dim = feature_dim
        self.geometry_dim = geometry_dim

        self.symmetric_net = nn.Sequential(
            nn.Linear(geometry_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, feature_dim),
        )
        self.antisymmetric_net = nn.Sequential(
            nn.Linear(geometry_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, feature_dim),
        )
        self.gam_symmetric_projection = nn.Linear(
            feature_dim,
            feature_dim,
            bias=False,
        )
        self.gam_antisymmetric_projection = nn.Linear(
            feature_dim,
            feature_dim,
            bias=False,
        )
        nn.init.eye_(self.gam_symmetric_projection.weight)
        nn.init.eye_(self.gam_antisymmetric_projection.weight)

        # Keep the learned topology field dominant while retaining a small
        # amount of the original GAM detail.
        self.template_gate_logit = nn.Parameter(torch.tensor(2.94))

    @staticmethod
    def _bilateral_geometry(
        points: torch.Tensor,
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Balanced coordinates plus two-scale k-NN connectivity descriptors.

        Unlike the removed left-right-heavy variant, neither X nor Y is
        amplified or suppressed here.
        """
        points = _points_bnd(points)
        center = points.mean(dim=1, keepdim=True)
        centered = points - center

        x_scale = centered[..., 0].abs().amax(
            dim=1,
            keepdim=True,
        ).clamp_min(1e-6)
        y_scale = centered[..., 1].abs().amax(
            dim=1,
            keepdim=True,
        ).clamp_min(1e-6)
        z_scale = centered[..., 2].abs().amax(
            dim=1,
            keepdim=True,
        ).clamp_min(1e-6)

        x = centered[..., 0] / x_scale
        y = centered[..., 1] / y_scale
        z = centered[..., 2] / z_scale
        abs_x = x.abs()
        radius = torch.sqrt(abs_x.square() + y.square() + 1e-8)
        extremity = torch.maximum(abs_x, y.abs())

        base_geometry = torch.stack(
            (
                abs_x,
                y,
                z,
                radius,
                extremity,
                abs_x * y,
                abs_x.square(),
                y.square(),
                torch.sin(np.pi * abs_x),
                torch.sin(np.pi * y),
            ),
            dim=-1,
        )

        normalized_xy = torch.stack((x, y), dim=-1)
        pairwise_distance = torch.cdist(
            normalized_xy,
            normalized_xy,
        )
        topology_features = []
        point_count = points.shape[1]

        for requested_k in (12, 48):
            k = min(requested_k, max(point_count - 1, 1))
            neighbor_indices = pairwise_distance.topk(
                k=min(k + 1, point_count),
                dim=-1,
                largest=False,
            ).indices
            if neighbor_indices.shape[-1] > 1:
                neighbor_indices = neighbor_indices[..., 1:]

            batch_indices = torch.arange(
                points.shape[0],
                device=points.device,
            ).view(-1, 1, 1).expand_as(neighbor_indices)
            neighbor_xy = normalized_xy[
                batch_indices,
                neighbor_indices,
            ]
            offsets = neighbor_xy - normalized_xy.unsqueeze(2)
            dx = offsets[..., 0]
            dy = offsets[..., 1]
            distance = offsets.norm(dim=-1)

            topology_features.extend(
                (
                    dx.abs().mean(dim=-1),
                    dy.abs().mean(dim=-1),
                    dx.square().mean(dim=-1),
                    dy.square().mean(dim=-1),
                    (dx * dy).abs().mean(dim=-1),
                    distance.mean(dim=-1),
                    distance.amax(dim=-1),
                )
            )

        geometry = torch.cat(
            (
                base_geometry,
                torch.stack(topology_features, dim=-1),
            ),
            dim=-1,
        )
        side_sign = torch.where(
            x >= 0,
            torch.ones_like(x),
            -torch.ones_like(x),
        ).unsqueeze(-1)
        return geometry, side_sign, centered

    @staticmethod
    def _mirror_indices(centered_points: torch.Tensor) -> torch.Tensor:
        reflected = centered_points.clone()
        reflected[..., 0] = -reflected[..., 0]
        scale = centered_points.abs().amax(
            dim=1,
            keepdim=True,
        ).clamp_min(1e-6)
        query = reflected / scale
        key = centered_points / scale
        return torch.cdist(query, key).argmin(dim=-1)

    @staticmethod
    def _gather_features(
        features: torch.Tensor,
        indices: torch.Tensor,
    ) -> torch.Tensor:
        gather_indices = indices.unsqueeze(-1).expand(
            -1,
            -1,
            features.shape[-1],
        )
        return torch.gather(features, dim=1, index=gather_indices)

    def decompose_gam(
        self,
        features: torch.Tensor,
        points: torch.Tensor,
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        """Split GAM features into reflection-even and canonical odd parts."""
        features, _ = _features_bnd(features, self.feature_dim)
        geometry, side_sign, centered = self._bilateral_geometry(points)
        mirror_indices = self._mirror_indices(centered)
        mirror_features = self._gather_features(
            features,
            mirror_indices,
        )
        symmetric = 0.5 * (features + mirror_features)
        antisymmetric = 0.5 * side_sign * (
            features - mirror_features
        )
        return symmetric, antisymmetric, geometry, side_sign

    @staticmethod
    def _trousers_coordinates(
        points: torch.Tensor,
    ) -> Tuple[torch.Tensor, torch.Tensor, float]:
        """Return left/right and cuff(0)-to-waist(1) coordinates."""
        points = _points_bnd(points)
        centered = points - points.mean(dim=1, keepdim=True)
        x = centered[0, :, 0]
        y = centered[0, :, 1]
        x_scale = x.abs().amax().clamp_min(1e-6)
        center_band = x.abs() < (0.16 * x_scale)

        lower = y <= torch.quantile(y, 0.20)
        upper = y >= torch.quantile(y, 0.80)
        lower_occupancy = center_band[lower].float().mean()
        upper_occupancy = center_band[upper].float().mean()
        waist_sign = (
            1.0 if upper_occupancy > lower_occupancy else -1.0
        )
        semantic_y = waist_sign * y
        cuff_to_waist = (
            (semantic_y - semantic_y.amin())
            / (semantic_y.amax() - semantic_y.amin()).clamp_min(1e-6)
        )
        return x / x_scale, cuff_to_waist, waist_sign

    def make_topology_training_warp(
        self,
        points: torch.Tensor,
        sleeve_extension: float,
        sleeve_drop: float,
        hem_width: float,
    ) -> torch.Tensor:
        """
        Make top-like trousers deformations while preserving point identities.
        """
        points = _points_bnd(points)
        mean = points.mean(dim=1, keepdim=True)
        centered = points - mean
        x = centered[0, :, 0]
        y = centered[0, :, 1]
        lr, cuff_to_waist, waist_sign = (
            self._trousers_coordinates(points)
        )
        x_scale = x.abs().amax().clamp_min(1e-6)
        side = torch.where(
            lr >= 0,
            torch.ones_like(lr),
            -torch.ones_like(lr),
        )

        shoulder_profile = torch.exp(
            -0.5 * ((cuff_to_waist - 0.76) / 0.18).square()
        )
        outer_profile = lr.abs().pow(0.55)
        extension = (
            side
            * x_scale
            * sleeve_extension
            * shoulder_profile
            * outer_profile
        )
        warped_x = x + extension
        semantic_y = waist_sign * y
        warped_semantic_y = (
            semantic_y
            - sleeve_drop
            * extension.abs()
            * shoulder_profile
        )
        hem_profile = (
            (0.34 - cuff_to_waist) / 0.34
        ).clamp(0.0, 1.0)
        warped_x = (
            warped_x
            + side * x_scale * hem_width * hem_profile
        )

        centered[0, :, 0] = warped_x
        centered[0, :, 1] = waist_sign * warped_semantic_y
        return centered + mean

    def forward(
        self,
        features: torch.Tensor,
        points: torch.Tensor,
    ) -> torch.Tensor:
        features, was_transposed = _features_bnd(
            features,
            self.feature_dim,
        )
        gam_even, gam_odd, geometry, side_sign = self.decompose_gam(
            features,
            points,
        )
        template_even = self.symmetric_net(geometry)
        template_odd = side_sign * self.antisymmetric_net(geometry)
        gam_equivariant = (
            self.gam_symmetric_projection(gam_even)
            + side_sign
            * self.gam_antisymmetric_projection(gam_odd)
        )
        gate = torch.sigmoid(self.template_gate_logit)
        output = (
            gate * (template_even + template_odd)
            + (1.0 - gate) * gam_equivariant
        )
        if was_transposed:
            return output.transpose(1, 2).contiguous()
        return output


class GAMWithPantsBilateralLayer(nn.Module):
    """Frozen GAM followed by the original balanced k-NN layer."""

    def __init__(
        self,
        backbone: nn.Module,
        bilateral_layer: PantsBilateralLayer,
    ):
        super().__init__()
        self.backbone = backbone
        self.bilateral_layer = bilateral_layer

    def forward(self, points: torch.Tensor) -> torch.Tensor:
        with torch.no_grad():
            features = self.backbone(points)
        return self.bilateral_layer(features, points)


class GAM_Encapsulation:
    """
    Existing usage remains unchanged:

        self.model = GAM_Encapsulation(catogory="Trousers")

    This restores the original balanced multi-scale k-NN topology version.
    """

    def __init__(
        self,
        catogory: str = "Tops_LongSleeve",
        auto_finetune: bool = True,
        force_finetune: bool = False,
        finetune_steps: int = 3200,
        training_points: int = 1536,
        # training_points: int = 2048,
        topology_augmentations: int = 24,
    ):
        self.catogory = catogory
        self.feature_dim = 512
        self.device = torch.device(
            "cuda:0" if torch.cuda.is_available() else "cpu"
        )
        checkpoint_dir = Path("Model_HALO/GAM/checkpoints") / catogory
        self.resume_path = checkpoint_dir / "checkpoint.pth"
        self.demo_path = checkpoint_dir / "demo_garment.ply"
        self.layer_path = (
            checkpoint_dir / "checkpoint_pants_topology_layer.pth"
        )

        self._set_seed(42)
        backbone = GAM_Model(
            normal_channel=False,
            feature_dim=self.feature_dim,
        )
        checkpoint = self._load_checkpoint(self.resume_path)
        backbone.load_state_dict(self._extract_state_dict(checkpoint))
        backbone = backbone.to(self.device).eval()
        for parameter in backbone.parameters():
            parameter.requires_grad_(False)

        layer = PantsBilateralLayer(
            feature_dim=self.feature_dim,
        ).to(self.device)
        self.model = GAMWithPantsBilateralLayer(
            backbone,
            layer,
        ).to(self.device)

        loaded = False
        if self.layer_path.exists() and not force_finetune:
            loaded = self._load_layer()
        if not loaded:
            if auto_finetune and catogory.lower() == "trousers":
                self.fine_tune_bilateral_layer(
                    steps=finetune_steps,
                    training_points=training_points,
                    topology_augmentations=topology_augmentations,
                )
            else:
                cprint(
                    "Balanced k-NN checkpoint is absent. Initialize once "
                    "with catogory='Trousers' to train it.",
                    color="yellow",
                )
        self.model.eval()

    @staticmethod
    def _set_seed(seed: int) -> None:
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
        np.random.seed(seed)
        random.seed(seed)

    def _load_checkpoint(self, path: Path):
        if not path.exists():
            raise FileNotFoundError(f"Checkpoint does not exist: {path}")
        try:
            return torch.load(
                path,
                map_location=self.device,
                weights_only=False,
            )
        except TypeError:
            return torch.load(path, map_location=self.device)

    @staticmethod
    def _extract_state_dict(checkpoint):
        if not isinstance(checkpoint, dict):
            return checkpoint
        for key in ("model_state_dict", "state_dict", "model"):
            if isinstance(checkpoint.get(key), dict):
                checkpoint = checkpoint[key]
                break
        if checkpoint and all(key.startswith("module.") for key in checkpoint):
            checkpoint = {
                key.removeprefix("module."): value
                for key, value in checkpoint.items()
            }
        return checkpoint

    @property
    def backbone(self) -> nn.Module:
        return self.model.backbone

    @property
    def bilateral_layer(self) -> PantsBilateralLayer:
        return self.model.bilateral_layer

    def _load_layer(self) -> bool:
        try:
            checkpoint = self._load_checkpoint(self.layer_path)
            state = checkpoint.get(
                "bilateral_layer_state_dict",
                checkpoint,
            )
            self.bilateral_layer.load_state_dict(state, strict=True)
            cprint(
                f"Loaded balanced k-NN GAM layer: {self.layer_path}",
                color="green",
            )
            return True
        except (RuntimeError, KeyError, ValueError) as error:
            cprint(
                f"Balanced k-NN layer will be retrained: {error}",
                color="yellow",
            )
            return False

    def _read_demo(self) -> Tuple[np.ndarray, torch.Tensor]:
        if not self.demo_path.exists():
            raise FileNotFoundError(
                f"Trousers demo point cloud does not exist: {self.demo_path}"
            )
        demo = np.asarray(
            o3d.io.read_point_cloud(str(self.demo_path)).points
        )
        if demo.size == 0:
            raise ValueError(f"Demo point cloud is empty: {self.demo_path}")
        normalized, *_ = normalize_pcd_points_xy(demo)
        tensor = torch.from_numpy(normalized).unsqueeze(0).to(
            self.device,
            dtype=torch.float32,
        )
        return demo, tensor

    def fine_tune_bilateral_layer(
        self,
        steps: int = 3200,
        training_points: int = 1536,
        topology_augmentations: int = 24,
    ) -> None:
        """Train the restored balanced k-NN layer with the frozen GAM teacher."""
        _, demo_points = self._read_demo()
        with torch.no_grad():
            teacher_features = self.backbone(demo_points)
            teacher_features, _ = _features_bnd(
                teacher_features,
                self.feature_dim,
            )
            (
                teacher_even,
                teacher_odd,
                _,
                _,
            ) = self.bilateral_layer.decompose_gam(
                teacher_features,
                demo_points,
            )

        lr, cuff_to_waist, _ = (
            self.bilateral_layer._trousers_coordinates(demo_points)
        )
        outer = lr.abs()
        endpoint_weight = (
            1.0
            + 4.0
            * (
                (outer > 0.52)
                & (
                    (cuff_to_waist > 0.62)
                    | (cuff_to_waist < 0.32)
                )
            ).float()
        ).unsqueeze(0)

        masks = (
            (lr < -0.52) & (cuff_to_waist > 0.62),
            (lr > 0.52) & (cuff_to_waist > 0.62),
            (lr < -0.52) & (cuff_to_waist < 0.32),
            (lr > 0.52) & (cuff_to_waist < 0.32),
        )
        names = (
            "left_sleeve_purple",
            "right_sleeve_pink",
            "left_hem_blue",
            "right_hem_green",
        )
        for name, mask in zip(names, masks):
            if not bool(mask.any()):
                raise ValueError(f"Cannot form training region: {name}")

        with torch.no_grad():
            anchor_targets = torch.stack(
                [
                    teacher_features[0, mask].mean(dim=0)
                    for mask in masks
                ],
                dim=0,
            )

        shapes = [demo_points]
        generator = np.random.default_rng(42)
        for _ in range(max(1, topology_augmentations)):
            shapes.append(
                self.bilateral_layer.make_topology_training_warp(
                    demo_points,
                    sleeve_extension=float(generator.uniform(1.0, 3.4)),
                    sleeve_drop=float(generator.uniform(0.05, 1.80)),
                    hem_width=float(generator.uniform(0.05, 0.38)),
                )
            )

        cprint(
            "Caching balanced multi-scale k-NN topology features...",
            color="cyan",
        )
        with torch.no_grad():
            cached = [
                self.bilateral_layer._bilateral_geometry(shape)[:2]
                for shape in shapes
            ]

        point_count = demo_points.shape[1]
        sample_count = min(max(128, training_points), point_count)
        optimizer = torch.optim.AdamW(
            self.bilateral_layer.parameters(),
            lr=3e-4,
            weight_decay=1e-5,
        )
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer,
            T_max=max(1, steps),
            eta_min=2e-5,
        )
        self.bilateral_layer.train()

        for step in range(max(1, steps)):
            geometry, side_sign = cached[step % len(cached)]
            indices = torch.randperm(
                point_count,
                device=self.device,
            )[:sample_count]
            sampled_geometry = geometry[:, indices]
            sampled_sign = side_sign[:, indices]
            target_even = teacher_even[:, indices]
            target_odd = teacher_odd[:, indices]

            predicted_even = self.bilateral_layer.symmetric_net(
                sampled_geometry
            )
            predicted_odd = (
                sampled_sign
                * self.bilateral_layer.antisymmetric_net(
                    sampled_geometry
                )
            )
            target_odd_signed = sampled_sign * target_odd

            even_cosine = (
                1.0
                - F.cosine_similarity(
                    predicted_even,
                    target_even,
                    dim=-1,
                )
            ).mean()
            odd_cosine = (
                1.0
                - F.cosine_similarity(
                    predicted_odd,
                    target_odd_signed,
                    dim=-1,
                )
            ).mean()
            predicted_full = predicted_even + predicted_odd
            target_full = target_even + target_odd_signed
            point_error = (
                1.0
                - F.cosine_similarity(
                    predicted_full,
                    target_full,
                    dim=-1,
                )
            )
            weight = endpoint_weight[:, indices]
            full_cosine = (
                (point_error * weight).sum()
                / weight.sum().clamp_min(1e-6)
            )

            full_prediction = (
                self.bilateral_layer.symmetric_net(geometry)
                + side_sign
                * self.bilateral_layer.antisymmetric_net(geometry)
            )
            predicted_anchors = torch.stack(
                [
                    full_prediction[0, mask].mean(dim=0)
                    for mask in masks
                ],
                dim=0,
            )
            anchor_loss = (
                1.0
                - F.cosine_similarity(
                    predicted_anchors,
                    anchor_targets,
                    dim=-1,
                )
            ).mean()
            mse_loss = (
                F.mse_loss(predicted_even, target_even)
                + F.mse_loss(predicted_odd, target_odd_signed)
            )

            # Original balanced objective: no signed-X amplification and no
            # extra left/right separation term.
            loss = (
                even_cosine
                + 0.75 * odd_cosine
                + 1.5 * full_cosine
                + 2.0 * anchor_loss
                + 0.10 * mse_loss
            )
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(
                self.bilateral_layer.parameters(),
                max_norm=2.0,
            )
            optimizer.step()
            scheduler.step()

            if step == 0 or (step + 1) % 100 == 0 or step + 1 == steps:
                cprint(
                    f"balanced-kNN step {step + 1:4d}/{steps}: "
                    f"loss={loss.item():.6f}, "
                    f"point_cos={1.0 - full_cosine.item():.6f}, "
                    f"anchor_cos={1.0 - anchor_loss.item():.6f}",
                    color="cyan",
                )

        self.bilateral_layer.eval()
        self.layer_path.parent.mkdir(parents=True, exist_ok=True)
        torch.save(
            {
                "bilateral_layer_state_dict": (
                    self.bilateral_layer.state_dict()
                ),
                "method": "pants_to_top_knn_topology_field_v4",
                "anchor_order": names,
            },
            self.layer_path,
        )
        cprint(
            f"Saved balanced k-NN GAM layer: {self.layer_path}",
            color="green",
        )

    def get_feature(
        self,
        input_pcd: np.ndarray,
        index_list: Optional[list] = None,
    ) -> torch.Tensor:
        normalized, *_ = normalize_pcd_points_xy(
            np.asarray(input_pcd)
        )
        points = torch.from_numpy(normalized).unsqueeze(0).to(
            self.device,
            dtype=torch.float32,
        )
        with torch.no_grad():
            features = self.model(points)
            features, _ = _features_bnd(features, self.feature_dim)
            features = features.squeeze(0)
        if index_list is not None:
            indices = torch.as_tensor(
                index_list,
                device=self.device,
                dtype=torch.long,
            )
            return features.index_select(0, indices)
        return features

    def get_manipulation_points(
        self,
        input_pcd: np.ndarray,
        index_list: Optional[list] = None,
    ):
        demo_pcd = np.asarray(
            o3d.io.read_point_cloud(str(self.demo_path)).points
        )
        demo_feature = self.get_feature(demo_pcd, index_list)
        input_feature = self.get_feature(input_pcd)
        result = torch.matmul(
            F.normalize(demo_feature, p=2, dim=1),
            F.normalize(input_feature, p=2, dim=1).T,
        )
        max_values, max_indices = torch.max(result, dim=1)
        indices = max_indices.detach().cpu().numpy()
        manipulation_points = np.asarray(input_pcd)[indices]

        cprint(
            "----------- GAM Inference Begin -----------",
            color="blue",
            attrs=["bold"],
        )
        cprint(f"similarity score: {max_values}", color="blue")
        cprint(f"relevant indices: {max_indices}", color="blue")
        cprint(f"manipulation points:\n{manipulation_points}", color="blue")
        cprint(
            "----------- GAM Inference End -----------",
            color="blue",
            attrs=["bold"],
        )
        return (
            manipulation_points,
            indices,
            result.detach().cpu().numpy(),
        )

    def get_colormap_points(self, input_pcd: np.ndarray):
        demo_pcd = np.asarray(
            o3d.io.read_point_cloud(str(self.demo_path)).points
        )
        demo_feature = self.get_feature(demo_pcd)
        input_feature = self.get_feature(input_pcd)
        result = torch.matmul(
            F.normalize(input_feature, p=2, dim=1),
            F.normalize(demo_feature, p=2, dim=1).T,
        )
        max_values, max_indices = torch.max(result, dim=1)
        print("similarity score: ", max_values)
        print("relevant indices: ", max_indices)
        color_indices = max_indices.detach().cpu().numpy()
        return demo_pcd[color_indices], color_indices

    def get_demo_garment_with_color(self):
        demo_pcd = o3d.io.read_point_cloud(str(self.demo_path))
        self.demo_points = np.asarray(demo_pcd.points)
        self.demo_points_color = colormap(self.demo_points)
        return self.demo_points, self.demo_points_color

    def visualize_pcd_corresponce(
        self,
        input_pcd: np.ndarray,
        save_or_not: bool = False,
        save_path: Optional[str] = None,
    ):
        self.get_demo_garment_with_color()
        visualize_pointcloud_with_colors(
            self.demo_points,
            self.demo_points_color,
        )
        _, color_indices = self.get_colormap_points(input_pcd)
        colors = self.demo_points_color[color_indices]
        visualize_pointcloud_with_colors(
            input_pcd,
            colors,
            save_or_not=save_or_not,
            save_path=save_path,
        )
########################################################################################################################


















# import os
# import random
# import sys
# from pathlib import Path
# from typing import Optional, Tuple

# import numpy as np
# import open3d as o3d
# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# from termcolor import cprint


# sys.path.append(os.getcwd())
# sys.path.append("Model_HALO/GAM")

# from Model_HALO.GAM.model.pointnet2_GAM import GAM_Model
# from Env_Config.Utils_Project.Point_Cloud_Manip import (
#     colormap,
#     normalize_pcd_points_xy,
#     visualize_pointcloud_with_colors,
# )


# def _features_bnd(
#     features: torch.Tensor,
#     feature_dim: int,
# ) -> Tuple[torch.Tensor, bool]:
#     """Convert GAM output to [batch, point, feature]."""
#     if features.ndim == 2:
#         features = features.unsqueeze(0)
#     if features.ndim != 3:
#         raise ValueError(f"Invalid GAM output shape: {tuple(features.shape)}")
#     if features.shape[-1] == feature_dim:
#         return features, False
#     if features.shape[1] == feature_dim:
#         return features.transpose(1, 2).contiguous(), True
#     raise ValueError(
#         f"Feature dimension {feature_dim} is absent from {tuple(features.shape)}"
#     )


# def _points_bnd(points: torch.Tensor) -> torch.Tensor:
#     """Convert point cloud to [batch, point, xyz]."""
#     if points.ndim == 2:
#         points = points.unsqueeze(0)
#     if points.ndim != 3:
#         raise ValueError(f"Invalid point-cloud shape: {tuple(points.shape)}")
#     if points.shape[-1] == 3:
#         return points
#     if points.shape[1] == 3:
#         return points.transpose(1, 2).contiguous()
#     raise ValueError(f"XYZ dimension is absent from {tuple(points.shape)}")


# class PantsBilateralLayer(nn.Module):
#     """
#     Original balanced multi-scale k-NN topology layer.

#     This is the version before signed-X reinforcement. X and Y geometry are
#     treated at comparable scale, so both sleeves and the body/hem contribute to
#     correspondence instead of concentrating matches on sleeves only.
#     """

#     def __init__(
#         self,
#         feature_dim: int = 512,
#         hidden_dim: int = 256,
#         geometry_dim: int = 24,
#     ):
#         super().__init__()
#         self.feature_dim = feature_dim
#         self.geometry_dim = geometry_dim

#         self.symmetric_net = nn.Sequential(
#             nn.Linear(geometry_dim, hidden_dim),
#             nn.LayerNorm(hidden_dim),
#             nn.GELU(),
#             nn.Linear(hidden_dim, hidden_dim),
#             nn.GELU(),
#             nn.Linear(hidden_dim, feature_dim),
#         )
#         self.antisymmetric_net = nn.Sequential(
#             nn.Linear(geometry_dim, hidden_dim),
#             nn.LayerNorm(hidden_dim),
#             nn.GELU(),
#             nn.Linear(hidden_dim, hidden_dim),
#             nn.GELU(),
#             nn.Linear(hidden_dim, feature_dim),
#         )
#         self.gam_symmetric_projection = nn.Linear(
#             feature_dim,
#             feature_dim,
#             bias=False,
#         )
#         self.gam_antisymmetric_projection = nn.Linear(
#             feature_dim,
#             feature_dim,
#             bias=False,
#         )
#         nn.init.eye_(self.gam_symmetric_projection.weight)
#         nn.init.eye_(self.gam_antisymmetric_projection.weight)

#         # Keep the learned topology field dominant while retaining a small
#         # amount of the original GAM detail.
#         self.template_gate_logit = nn.Parameter(torch.tensor(2.94))

#     @staticmethod
#     def _bilateral_geometry(
#         points: torch.Tensor,
#     ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
#         """
#         Balanced coordinates plus multi-scale k-NN connectivity descriptors.

#         Unlike the removed left-right-heavy variant, neither X nor Y is
#         amplified or suppressed here.
#         """
#         points = _points_bnd(points)
#         center = points.mean(dim=1, keepdim=True)
#         centered = points - center

#         x_scale = centered[..., 0].abs().amax(
#             dim=1,
#             keepdim=True,
#         ).clamp_min(1e-6)
#         y_scale = centered[..., 1].abs().amax(
#             dim=1,
#             keepdim=True,
#         ).clamp_min(1e-6)
#         z_scale = centered[..., 2].abs().amax(
#             dim=1,
#             keepdim=True,
#         ).clamp_min(1e-6)

#         x = centered[..., 0] / x_scale
#         y = centered[..., 1] / y_scale
#         z = centered[..., 2] / z_scale
#         abs_x = x.abs()
#         radius = torch.sqrt(abs_x.square() + y.square() + 1e-8)
#         extremity = torch.maximum(abs_x, y.abs())

#         base_geometry = torch.stack(
#             (
#                 abs_x,
#                 y,
#                 z,
#                 radius,
#                 extremity,
#                 abs_x * y,
#                 abs_x.square(),
#                 y.square(),
#                 torch.sin(np.pi * abs_x),
#                 torch.sin(np.pi * y),
#             ),
#             dim=-1,
#         )

#         normalized_xy = torch.stack((x, y), dim=-1)
#         pairwise_distance = torch.cdist(
#             normalized_xy,
#             normalized_xy,
#         )
#         topology_features = []
#         point_count = points.shape[1]

#         for requested_k in (12, 24):
#             k = min(requested_k, max(point_count - 1, 1))
#             neighbor_indices = pairwise_distance.topk(
#                 k=min(k + 1, point_count),
#                 dim=-1,
#                 largest=False,
#             ).indices
#             if neighbor_indices.shape[-1] > 1:
#                 neighbor_indices = neighbor_indices[..., 1:]

#             batch_indices = torch.arange(
#                 points.shape[0],
#                 device=points.device,
#             ).view(-1, 1, 1).expand_as(neighbor_indices)
#             neighbor_xy = normalized_xy[
#                 batch_indices,
#                 neighbor_indices,
#             ]
#             offsets = neighbor_xy - normalized_xy.unsqueeze(2)
#             dx = offsets[..., 0]
#             dy = offsets[..., 1]
#             distance = offsets.norm(dim=-1)

#             topology_features.extend(
#                 (
#                     dx.abs().mean(dim=-1),
#                     dy.abs().mean(dim=-1),
#                     dx.square().mean(dim=-1),
#                     dy.square().mean(dim=-1),
#                     (dx * dy).abs().mean(dim=-1),
#                     distance.mean(dim=-1),
#                     distance.amax(dim=-1),
#                 )
#             )

#         geometry = torch.cat(
#             (
#                 base_geometry,
#                 torch.stack(topology_features, dim=-1),
#             ),
#             dim=-1,
#         )
#         side_sign = torch.where(
#             x >= 0,
#             torch.ones_like(x),
#             -torch.ones_like(x),
#         ).unsqueeze(-1)
#         return geometry, side_sign, centered

#     @staticmethod
#     def _mirror_indices(centered_points: torch.Tensor) -> torch.Tensor:
#         reflected = centered_points.clone()
#         reflected[..., 0] = -reflected[..., 0]
#         scale = centered_points.abs().amax(
#             dim=1,
#             keepdim=True,
#         ).clamp_min(1e-6)
#         query = reflected / scale
#         key = centered_points / scale
#         return torch.cdist(query, key).argmin(dim=-1)

#     @staticmethod
#     def _gather_features(
#         features: torch.Tensor,
#         indices: torch.Tensor,
#     ) -> torch.Tensor:
#         gather_indices = indices.unsqueeze(-1).expand(
#             -1,
#             -1,
#             features.shape[-1],
#         )
#         return torch.gather(features, dim=1, index=gather_indices)

#     def decompose_gam(
#         self,
#         features: torch.Tensor,
#         points: torch.Tensor,
#     ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
#         """Split GAM features into reflection-even and canonical odd parts."""
#         features, _ = _features_bnd(features, self.feature_dim)
#         geometry, side_sign, centered = self._bilateral_geometry(points)
#         mirror_indices = self._mirror_indices(centered)
#         mirror_features = self._gather_features(
#             features,
#             mirror_indices,
#         )
#         symmetric = 0.5 * (features + mirror_features)
#         antisymmetric = 0.5 * side_sign * (
#             features - mirror_features
#         )
#         return symmetric, antisymmetric, geometry, side_sign

#     @staticmethod
#     def _trousers_coordinates(
#         points: torch.Tensor,
#     ) -> Tuple[torch.Tensor, torch.Tensor, float]:
#         """Return left/right and cuff(0)-to-waist(1) coordinates."""
#         points = _points_bnd(points)
#         centered = points - points.mean(dim=1, keepdim=True)
#         x = centered[0, :, 0]
#         y = centered[0, :, 1]
#         x_scale = x.abs().amax().clamp_min(1e-6)
#         center_band = x.abs() < (0.16 * x_scale)

#         lower = y <= torch.quantile(y, 0.20)
#         upper = y >= torch.quantile(y, 0.80)
#         lower_occupancy = center_band[lower].float().mean()
#         upper_occupancy = center_band[upper].float().mean()
#         waist_sign = (
#             1.0 if upper_occupancy > lower_occupancy else -1.0
#         )
#         semantic_y = waist_sign * y
#         cuff_to_waist = (
#             (semantic_y - semantic_y.amin())
#             / (semantic_y.amax() - semantic_y.amin()).clamp_min(1e-6)
#         )
#         return x / x_scale, cuff_to_waist, waist_sign

#     def make_topology_training_warp(
#         self,
#         points: torch.Tensor,
#         sleeve_extension: float,
#         sleeve_drop: float,
#         hem_width: float,
#         sleeve_extension_skew: float = 0.0,
#         sleeve_drop_skew: float = 0.0,
#     ) -> torch.Tensor:
#         """
#         Make top-like trousers deformations while preserving point identities.
#         """
#         points = _points_bnd(points)
#         mean = points.mean(dim=1, keepdim=True)
#         centered = points - mean
#         x = centered[0, :, 0]
#         y = centered[0, :, 1]
#         lr, cuff_to_waist, waist_sign = (
#             self._trousers_coordinates(points)
#         )
#         x_scale = x.abs().amax().clamp_min(1e-6)
#         side = torch.where(
#             lr >= 0,
#             torch.ones_like(lr),
#             -torch.ones_like(lr),
#         )

#         shoulder_profile = torch.exp(
#             -0.5 * ((cuff_to_waist - 0.76) / 0.18).square()
#         )
#         outer_profile = lr.abs().pow(0.55)
#         extension_side_scale = (
#             1.0 + side * sleeve_extension_skew
#         ).clamp(0.55, 1.45)
#         extension = (
#             side
#             * x_scale
#             * sleeve_extension
#             * extension_side_scale
#             * shoulder_profile
#             * outer_profile
#         )
#         warped_x = x + extension
#         semantic_y = waist_sign * y
#         drop_side_scale = (
#             1.0 + side * sleeve_drop_skew
#         ).clamp(0.45, 1.55)
#         warped_semantic_y = (
#             semantic_y
#             - sleeve_drop
#             * drop_side_scale
#             * extension.abs()
#             * shoulder_profile
#         )
#         hem_profile = (
#             (0.34 - cuff_to_waist) / 0.34
#         ).clamp(0.0, 1.0)
#         warped_x = (
#             warped_x
#             + side * x_scale * hem_width * hem_profile
#         )

#         centered[0, :, 0] = warped_x
#         centered[0, :, 1] = waist_sign * warped_semantic_y
#         return centered + mean

#     def forward(
#         self,
#         features: torch.Tensor,
#         points: torch.Tensor,
#     ) -> torch.Tensor:
#         features, was_transposed = _features_bnd(
#             features,
#             self.feature_dim,
#         )
#         gam_even, gam_odd, geometry, side_sign = self.decompose_gam(
#             features,
#             points,
#         )
#         template_even = self.symmetric_net(geometry)
#         template_odd = side_sign * self.antisymmetric_net(geometry)
#         gam_equivariant = (
#             self.gam_symmetric_projection(gam_even)
#             + side_sign
#             * self.gam_antisymmetric_projection(gam_odd)
#         )
#         gate = torch.sigmoid(self.template_gate_logit)
#         output = (
#             gate * (template_even + template_odd)
#             + (1.0 - gate) * gam_equivariant
#         )
#         if was_transposed:
#             return output.transpose(1, 2).contiguous()
#         return output


# class GAMWithPantsBilateralLayer(nn.Module):
#     """Frozen GAM followed by the original balanced k-NN layer."""

#     def __init__(
#         self,
#         backbone: nn.Module,
#         bilateral_layer: PantsBilateralLayer,
#     ):
#         super().__init__()
#         self.backbone = backbone
#         self.bilateral_layer = bilateral_layer

#     def forward(self, points: torch.Tensor) -> torch.Tensor:
#         with torch.no_grad():
#             features = self.backbone(points)
#         return self.bilateral_layer(features, points)


# class GAM_Encapsulation:
#     """
#     Existing usage remains unchanged:

#         self.model = GAM_Encapsulation(catogory="Trousers")

#     This restores the original balanced multi-scale k-NN topology version.
#     """

#     def __init__(
#         self,
#         catogory: str = "Tops_LongSleeve",
#         auto_finetune: bool = True,
#         force_finetune: bool = False,
#         finetune_steps: int = 5000,
#         training_points: int = 1536,
#         # training_points: int = 2048,
#         topology_augmentations: int = 24,
#     ):
#         self.catogory = catogory
#         self.feature_dim = 512
#         self.device = torch.device(
#             "cuda:0" if torch.cuda.is_available() else "cpu"
#         )
#         checkpoint_dir = Path("Model_HALO/GAM/checkpoints") / catogory
#         self.resume_path = checkpoint_dir / "checkpoint.pth"
#         self.demo_path = checkpoint_dir / "demo_garment.ply"
#         self.layer_path = (
#             checkpoint_dir
#             / "checkpoint_pants_topology_correspondence_v5.pth"
#         )
#         self.legacy_layer_path = (
#             checkpoint_dir / "checkpoint_pants_topology_layer.pth"
#         )

#         self._set_seed(42)
#         backbone = GAM_Model(
#             normal_channel=False,
#             feature_dim=self.feature_dim,
#         )
#         checkpoint = self._load_checkpoint(self.resume_path)
#         backbone.load_state_dict(self._extract_state_dict(checkpoint))
#         backbone = backbone.to(self.device).eval()
#         for parameter in backbone.parameters():
#             parameter.requires_grad_(False)

#         layer = PantsBilateralLayer(
#             feature_dim=self.feature_dim,
#         ).to(self.device)
#         self.model = GAMWithPantsBilateralLayer(
#             backbone,
#             layer,
#         ).to(self.device)

#         loaded = False
#         if self.layer_path.exists() and not force_finetune:
#             loaded = self._load_layer()
#         if not loaded:
#             warm_started = False
#             if self.legacy_layer_path.exists():
#                 warm_started = self._load_layer(self.legacy_layer_path)
#                 if warm_started:
#                     cprint(
#                         "Warm-starting correspondence training from the "
#                         "existing balanced k-NN layer.",
#                         color="cyan",
#                     )
#             if auto_finetune and catogory.lower() == "trousers":
#                 self.fine_tune_bilateral_layer(
#                     steps=finetune_steps,
#                     training_points=training_points,
#                     topology_augmentations=topology_augmentations,
#                 )
#             elif warm_started:
#                 loaded = True
#             else:
#                 cprint(
#                     "Balanced k-NN checkpoint is absent. Initialize once "
#                     "with catogory='Trousers' to train it.",
#                     color="yellow",
#                 )
#         self.model.eval()

#     @staticmethod
#     def _set_seed(seed: int) -> None:
#         torch.manual_seed(seed)
#         if torch.cuda.is_available():
#             torch.cuda.manual_seed_all(seed)
#         np.random.seed(seed)
#         random.seed(seed)

#     def _load_checkpoint(self, path: Path):
#         if not path.exists():
#             raise FileNotFoundError(f"Checkpoint does not exist: {path}")
#         try:
#             return torch.load(
#                 path,
#                 map_location=self.device,
#                 weights_only=False,
#             )
#         except TypeError:
#             return torch.load(path, map_location=self.device)

#     @staticmethod
#     def _extract_state_dict(checkpoint):
#         if not isinstance(checkpoint, dict):
#             return checkpoint
#         for key in ("model_state_dict", "state_dict", "model"):
#             if isinstance(checkpoint.get(key), dict):
#                 checkpoint = checkpoint[key]
#                 break
#         if checkpoint and all(key.startswith("module.") for key in checkpoint):
#             checkpoint = {
#                 key.removeprefix("module."): value
#                 for key, value in checkpoint.items()
#             }
#         return checkpoint

#     @property
#     def backbone(self) -> nn.Module:
#         return self.model.backbone

#     @property
#     def bilateral_layer(self) -> PantsBilateralLayer:
#         return self.model.bilateral_layer

#     def _load_layer(self, path: Optional[Path] = None) -> bool:
#         path = self.layer_path if path is None else path
#         try:
#             checkpoint = self._load_checkpoint(path)
#             state = checkpoint.get(
#                 "bilateral_layer_state_dict",
#                 checkpoint,
#             )
#             self.bilateral_layer.load_state_dict(state, strict=True)
#             cprint(
#                 f"Loaded balanced k-NN GAM layer: {path}",
#                 color="green",
#             )
#             return True
#         except (RuntimeError, KeyError, ValueError) as error:
#             cprint(
#                 f"Balanced k-NN layer will be retrained: {error}",
#                 color="yellow",
#             )
#             return False

#     def _read_demo(self) -> Tuple[np.ndarray, torch.Tensor]:
#         if not self.demo_path.exists():
#             raise FileNotFoundError(
#                 f"Trousers demo point cloud does not exist: {self.demo_path}"
#             )
#         demo = np.asarray(
#             o3d.io.read_point_cloud(str(self.demo_path)).points
#         )
#         if demo.size == 0:
#             raise ValueError(f"Demo point cloud is empty: {self.demo_path}")
#         normalized, *_ = normalize_pcd_points_xy(demo)
#         tensor = torch.from_numpy(normalized).unsqueeze(0).to(
#             self.device,
#             dtype=torch.float32,
#         )
#         return demo, tensor

#     def fine_tune_bilateral_layer(
#         self,
#         steps: int = 3200,
#         training_points: int = 1536,
#         topology_augmentations: int = 24,
#         correspondence_temperature: float = 0.07,
#         correspondence_sigma: float = 0.055,
#     ) -> None:
#         """
#         Train topology features to retrieve their source-trouser neighborhood.

#         Every synthetic top point keeps the identity of the trouser point from
#         which it was warped. The retrieval loss therefore supervises actual
#         trouser-to-top correspondence without defining a target sleeve area on
#         the top.
#         """
#         _, demo_points = self._read_demo()
#         with torch.no_grad():
#             teacher_features = self.backbone(demo_points)
#             teacher_features, _ = _features_bnd(
#                 teacher_features,
#                 self.feature_dim,
#             )
#             (
#                 teacher_even,
#                 teacher_odd,
#                 _,
#                 _,
#             ) = self.bilateral_layer.decompose_gam(
#                 teacher_features,
#                 demo_points,
#             )

#         lr, cuff_to_waist, _ = (
#             self.bilateral_layer._trousers_coordinates(demo_points)
#         )
#         source_coordinates = torch.stack(
#             (lr, cuff_to_waist),
#             dim=-1,
#         )
#         teacher_bank = F.normalize(
#             teacher_features[0].detach(),
#             p=2,
#             dim=-1,
#         )
#         outer = lr.abs()
#         endpoint_weight = (
#             1.0
#             + 4.0
#             * (
#                 (outer > 0.52)
#                 & (
#                     (cuff_to_waist > 0.62)
#                     | (cuff_to_waist < 0.32)
#                 )
#             ).float()
#         ).unsqueeze(0)

#         masks = (
#             (lr < -0.52) & (cuff_to_waist > 0.62),
#             (lr > 0.52) & (cuff_to_waist > 0.62),
#             (lr < -0.52) & (cuff_to_waist < 0.32),
#             (lr > 0.52) & (cuff_to_waist < 0.32),
#         )
#         names = (
#             "left_sleeve_purple",
#             "right_sleeve_pink",
#             "left_hem_blue",
#             "right_hem_green",
#         )
#         for name, mask in zip(names, masks):
#             if not bool(mask.any()):
#                 raise ValueError(f"Cannot form training region: {name}")

#         with torch.no_grad():
#             anchor_targets = torch.stack(
#                 [
#                     teacher_features[0, mask].mean(dim=0)
#                     for mask in masks
#                 ],
#                 dim=0,
#             )

#         shapes = [demo_points]
#         generator = np.random.default_rng(42)
#         for _ in range(max(1, topology_augmentations)):
#             shapes.append(
#                 self.bilateral_layer.make_topology_training_warp(
#                     demo_points,
#                     sleeve_extension=float(generator.uniform(1.0, 3.4)),
#                     sleeve_drop=float(generator.uniform(0.05, 1.80)),
#                     hem_width=float(generator.uniform(0.05, 0.38)),
#                     sleeve_extension_skew=float(
#                         generator.uniform(-0.35, 0.35)
#                     ),
#                     sleeve_drop_skew=float(
#                         generator.uniform(-0.45, 0.45)
#                     ),
#                 )
#             )

#         cprint(
#             "Caching balanced multi-scale k-NN topology features...",
#             color="cyan",
#         )
#         with torch.no_grad():
#             cached = [
#                 self.bilateral_layer._bilateral_geometry(shape)[:2]
#                 for shape in shapes
#             ]

#         point_count = demo_points.shape[1]
#         sample_count = min(max(128, training_points), point_count)
#         optimizer = torch.optim.AdamW(
#             self.bilateral_layer.parameters(),
#             lr=3e-4,
#             weight_decay=1e-5,
#         )
#         scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
#             optimizer,
#             T_max=max(1, steps),
#             eta_min=2e-5,
#         )
#         self.bilateral_layer.train()

#         for step in range(max(1, steps)):
#             geometry, side_sign = cached[step % len(cached)]
#             indices = torch.randperm(
#                 point_count,
#                 device=self.device,
#             )[:sample_count]
#             sampled_geometry = geometry[:, indices]
#             sampled_sign = side_sign[:, indices]
#             target_even = teacher_even[:, indices]
#             target_odd = teacher_odd[:, indices]

#             predicted_even = self.bilateral_layer.symmetric_net(
#                 sampled_geometry
#             )
#             predicted_odd = (
#                 sampled_sign
#                 * self.bilateral_layer.antisymmetric_net(
#                     sampled_geometry
#                 )
#             )
#             target_odd_signed = sampled_sign * target_odd

#             even_cosine = (
#                 1.0
#                 - F.cosine_similarity(
#                     predicted_even,
#                     target_even,
#                     dim=-1,
#                 )
#             ).mean()
#             odd_cosine = (
#                 1.0
#                 - F.cosine_similarity(
#                     predicted_odd,
#                     target_odd_signed,
#                     dim=-1,
#                 )
#             ).mean()
#             predicted_full = predicted_even + predicted_odd
#             target_full = target_even + target_odd_signed
#             point_error = (
#                 1.0
#                 - F.cosine_similarity(
#                     predicted_full,
#                     target_full,
#                     dim=-1,
#                 )
#             )
#             weight = endpoint_weight[:, indices]
#             full_cosine = (
#                 (point_error * weight).sum()
#                 / weight.sum().clamp_min(1e-6)
#             )

#             # Optimize the same nearest-feature retrieval used at inference.
#             # The soft target is a small neighborhood on the source trousers,
#             # not a hand-authored region on the deformed top.
#             predicted_normalized = F.normalize(
#                 predicted_full[0],
#                 p=2,
#                 dim=-1,
#             )
#             retrieval_logits = (
#                 torch.matmul(predicted_normalized, teacher_bank.T)
#                 / correspondence_temperature
#             )
#             sampled_source_coordinates = source_coordinates[indices]
#             source_distances = torch.cdist(
#                 sampled_source_coordinates,
#                 source_coordinates,
#             )
#             target_logits = (
#                 -source_distances.square()
#                 / (2.0 * correspondence_sigma**2)
#             )

#             # Keep separated trouser legs distinct while allowing a smooth
#             # transition through the center/waist area.
#             sampled_lr = sampled_source_coordinates[:, 0:1]
#             bank_lr = source_coordinates[:, 0].unsqueeze(0)
#             opposite_outer_sides = (
#                 (sampled_lr.abs() > 0.15)
#                 & (bank_lr.abs() > 0.15)
#                 & (sampled_lr * bank_lr < 0.0)
#             )
#             target_logits = (
#                 target_logits
#                 - 12.0 * opposite_outer_sides.to(target_logits.dtype)
#             )
#             target_distribution = F.softmax(target_logits, dim=-1)
#             retrieval_log_distribution = F.log_softmax(
#                 retrieval_logits,
#                 dim=-1,
#             )
#             correspondence_error = F.kl_div(
#                 retrieval_log_distribution,
#                 target_distribution,
#                 reduction="none",
#             ).sum(dim=-1)
#             correspondence_loss = (
#                 (
#                     correspondence_error
#                     * weight.squeeze(0)
#                 ).sum()
#                 / weight.sum().clamp_min(1e-6)
#             )

#             full_prediction = (
#                 self.bilateral_layer.symmetric_net(geometry)
#                 + side_sign
#                 * self.bilateral_layer.antisymmetric_net(geometry)
#             )
#             predicted_anchors = torch.stack(
#                 [
#                     full_prediction[0, mask].mean(dim=0)
#                     for mask in masks
#                 ],
#                 dim=0,
#             )
#             anchor_loss = (
#                 1.0
#                 - F.cosine_similarity(
#                     predicted_anchors,
#                     anchor_targets,
#                     dim=-1,
#                 )
#             ).mean()
#             mse_loss = (
#                 F.mse_loss(predicted_even, target_even)
#                 + F.mse_loss(predicted_odd, target_odd_signed)
#             )

#             # Original balanced objective: no signed-X amplification and no
#             # extra left/right separation term.
#             loss = (
#                 even_cosine
#                 + 0.75 * odd_cosine
#                 + 1.5 * full_cosine
#                 + 2.0 * anchor_loss
#                 + 0.35 * correspondence_loss
#                 + 0.10 * mse_loss
#             )
#             optimizer.zero_grad(set_to_none=True)
#             loss.backward()
#             torch.nn.utils.clip_grad_norm_(
#                 self.bilateral_layer.parameters(),
#                 max_norm=2.0,
#             )
#             optimizer.step()
#             scheduler.step()

#             if step == 0 or (step + 1) % 100 == 0 or step + 1 == steps:
#                 cprint(
#                     f"balanced-kNN step {step + 1:4d}/{steps}: "
#                     f"loss={loss.item():.6f}, "
#                     f"point_cos={1.0 - full_cosine.item():.6f}, "
#                     f"anchor_cos={1.0 - anchor_loss.item():.6f}, "
#                     f"retrieval_kl={correspondence_loss.item():.6f}",
#                     color="cyan",
#                 )

#         self.bilateral_layer.eval()
#         self.layer_path.parent.mkdir(parents=True, exist_ok=True)
#         torch.save(
#             {
#                 "bilateral_layer_state_dict": (
#                     self.bilateral_layer.state_dict()
#                 ),
#                 "method": "pants_to_top_correspondence_retrieval_v5",
#                 "anchor_order": names,
#                 "correspondence_temperature": correspondence_temperature,
#                 "correspondence_sigma": correspondence_sigma,
#             },
#             self.layer_path,
#         )
#         cprint(
#             f"Saved balanced k-NN GAM layer: {self.layer_path}",
#             color="green",
#         )

#     def get_feature(
#         self,
#         input_pcd: np.ndarray,
#         index_list: Optional[list] = None,
#     ) -> torch.Tensor:
#         normalized, *_ = normalize_pcd_points_xy(
#             np.asarray(input_pcd)
#         )
#         points = torch.from_numpy(normalized).unsqueeze(0).to(
#             self.device,
#             dtype=torch.float32,
#         )
#         with torch.no_grad():
#             features = self.model(points)
#             features, _ = _features_bnd(features, self.feature_dim)
#             features = features.squeeze(0)
#         if index_list is not None:
#             indices = torch.as_tensor(
#                 index_list,
#                 device=self.device,
#                 dtype=torch.long,
#             )
#             return features.index_select(0, indices)
#         return features

#     def get_manipulation_points(
#         self,
#         input_pcd: np.ndarray,
#         index_list: Optional[list] = None,
#     ):
#         demo_pcd = np.asarray(
#             o3d.io.read_point_cloud(str(self.demo_path)).points
#         )
#         demo_feature = self.get_feature(demo_pcd, index_list)
#         input_feature = self.get_feature(input_pcd)
#         result = torch.matmul(
#             F.normalize(demo_feature, p=2, dim=1),
#             F.normalize(input_feature, p=2, dim=1).T,
#         )
#         max_values, max_indices = torch.max(result, dim=1)
#         indices = max_indices.detach().cpu().numpy()
#         manipulation_points = np.asarray(input_pcd)[indices]

#         cprint(
#             "----------- GAM Inference Begin -----------",
#             color="blue",
#             attrs=["bold"],
#         )
#         cprint(f"similarity score: {max_values}", color="blue")
#         cprint(f"relevant indices: {max_indices}", color="blue")
#         cprint(f"manipulation points:\n{manipulation_points}", color="blue")
#         cprint(
#             "----------- GAM Inference End -----------",
#             color="blue",
#             attrs=["bold"],
#         )
#         return (
#             manipulation_points,
#             indices,
#             result.detach().cpu().numpy(),
#         )

#     def get_colormap_points(self, input_pcd: np.ndarray):
#         demo_pcd = np.asarray(
#             o3d.io.read_point_cloud(str(self.demo_path)).points
#         )
#         demo_feature = self.get_feature(demo_pcd)
#         input_feature = self.get_feature(input_pcd)
#         result = torch.matmul(
#             F.normalize(input_feature, p=2, dim=1),
#             F.normalize(demo_feature, p=2, dim=1).T,
#         )
#         max_values, max_indices = torch.max(result, dim=1)
#         print("similarity score: ", max_values)
#         print("relevant indices: ", max_indices)
#         color_indices = max_indices.detach().cpu().numpy()
#         return demo_pcd[color_indices], color_indices

#     def get_demo_garment_with_color(self):
#         demo_pcd = o3d.io.read_point_cloud(str(self.demo_path))
#         self.demo_points = np.asarray(demo_pcd.points)
#         self.demo_points_color = colormap(self.demo_points)
#         return self.demo_points, self.demo_points_color

#     def visualize_pcd_corresponce(
#         self,
#         input_pcd: np.ndarray,
#         save_or_not: bool = False,
#         save_path: Optional[str] = None,
#     ):
#         self.get_demo_garment_with_color()
#         visualize_pointcloud_with_colors(
#             self.demo_points,
#             self.demo_points_color,
#         )
#         _, color_indices = self.get_colormap_points(input_pcd)
#         colors = self.demo_points_color[color_indices]
#         visualize_pointcloud_with_colors(
#             input_pcd,
#             colors,
#             save_or_not=save_or_not,
#             save_path=save_path,
#         )
