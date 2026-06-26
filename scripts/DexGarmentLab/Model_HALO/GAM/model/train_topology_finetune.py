import os
import numpy as np
import torch
import torch.nn.functional as F
import open3d as o3d
from torch.utils.data import Dataset, DataLoader

from Model_HALO.GAM.model.pointnet2_GAM import GAM_Model
from Model_HALO.GAM.model.gam_topo_model import GAM_Topo_Model
from Model_HALO.GAM.model.topology_descriptor import compute_topology_descriptor
from Env_Config.Utils_Project.Point_Cloud_Manip import normalize_pcd_points_xy




from pathlib import Path
import numpy as np
import torch
import open3d as o3d
from torch.utils.data import Dataset


class TopsPointCloudDataset(Dataset):
    def __init__(self, pcd_dir):
        self.paths = sorted(Path(pcd_dir).glob("*.ply"))

        if len(self.paths) == 0:
            raise RuntimeError(f"No .ply files found in {pcd_dir}")

        print(f"Loaded {len(self.paths)} point clouds from {pcd_dir}")

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, idx):
        pcd = o3d.io.read_point_cloud(str(self.paths[idx]))
        points = np.asarray(pcd.points).astype(np.float32)

        points, *_ = normalize_pcd_points_xy(points)

        topo = compute_topology_descriptor(points, garment_type="tops")

        return torch.from_numpy(points).float(), torch.from_numpy(topo).float()



def topology_feature_loss(feat, topo, sigma=0.15, temperature=0.07):
    feat = F.normalize(feat, p=2, dim=-1)

    topo_dist = torch.cdist(topo, topo, p=2)
    target_prob = F.softmax(-topo_dist / sigma, dim=-1).detach()

    feat_logits = torch.bmm(feat, feat.transpose(1, 2)) / temperature

    return F.kl_div(
        F.log_softmax(feat_logits, dim=-1),
        target_prob,
        reduction="batchmean",
    )


# def topology_feature_loss(feat, topo, sigma=0.10, temperature=0.04):
#     feat = F.normalize(feat, p=2, dim=-1)

#     weights = torch.tensor(
#         [1.0, 1.0, 2.0, 4.0, 4.0, 0.5, 2.0],
#         device=topo.device,
#         dtype=topo.dtype,
#     )

#     topo_weighted = topo * weights

#     topo_dist = torch.cdist(topo_weighted, topo_weighted, p=2)
#     target_prob = F.softmax(-topo_dist / sigma, dim=-1).detach()

#     feat_logits = torch.bmm(feat, feat.transpose(1, 2)) / temperature

#     return F.kl_div(
#         F.log_softmax(feat_logits, dim=-1),
#         target_prob,
#         reduction="batchmean",
#     )


def topology_cluster_loss(feat, topo, score_index, eps=1e-6):
    feat = F.normalize(feat, p=2, dim=-1)

    score = topo[..., score_index:score_index + 1]
    left = topo[..., 0:1]
    right = topo[..., 1:2]

    left_w = score * left
    right_w = score * right

    left_proto = (feat * left_w).sum(dim=1, keepdim=True) / (left_w.sum(dim=1, keepdim=True) + eps)
    right_proto = (feat * right_w).sum(dim=1, keepdim=True) / (right_w.sum(dim=1, keepdim=True) + eps)

    left_loss = (1.0 - F.cosine_similarity(feat, left_proto, dim=-1)) * left_w.squeeze(-1)
    right_loss = (1.0 - F.cosine_similarity(feat, right_proto, dim=-1)) * right_w.squeeze(-1)

    loss = (
        left_loss.sum() / (left_w.sum() + eps)
        + right_loss.sum() / (right_w.sum() + eps)
    )

    return loss    


def feature_keep_loss(new_feat, base_feat):
    new_feat = F.normalize(new_feat, p=2, dim=-1)
    base_feat = F.normalize(base_feat.detach(), p=2, dim=-1)
    return 1.0 - F.cosine_similarity(new_feat, base_feat, dim=-1).mean()


def train():
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    ckpt_dir = "Model_HALO/GAM/checkpoints/Tops_LongSleeve"
    backbone_ckpt = os.path.join(ckpt_dir, "checkpoint.pth")
    save_path = os.path.join(ckpt_dir, "topology_finetune.pth")

    dataset = TopsPointCloudDataset("/workspace/isaaclab/scripts/DexGarmentLab/pointcloud")
    loader = DataLoader(dataset, batch_size=4, shuffle=True, num_workers=4, drop_last=True)

    backbone = GAM_Model(normal_channel=False, feature_dim=512).to(device)
    backbone.load_state_dict(torch.load(backbone_ckpt, map_location=device, weights_only=False))

    model = GAM_Topo_Model(backbone=backbone, topo_dim=6, feature_dim=512).to(device)

    model.freeze_backbone()

    optimizer = torch.optim.AdamW(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=1e-3,
        weight_decay=1e-4,
    )

    num_epochs = 8000

    for epoch in range(num_epochs):
        if epoch == 20:
            model.unfreeze_light_backbone()
            optimizer = torch.optim.AdamW(
                filter(lambda p: p.requires_grad, model.parameters()),
                lr=3e-5,
                weight_decay=1e-4,
            )

        model.train()
        total_loss = 0.0

        for xyz, topo in loader:
            xyz = xyz.to(device)
            topo = topo.to(device)

            with torch.no_grad():
                base_feat = model.backbone(xyz)

            new_feat = model(xyz, topo)

            loss_topo = topology_feature_loss(new_feat, topo)
            loss_keep = feature_keep_loss(new_feat, base_feat)

            loss = loss_topo + 0.1 * loss_keep



            # loss_topo = topology_feature_loss(
            #     new_feat,
            #     topo,
            #     sigma=0.10,
            #     temperature=0.04,
            # )

            # loss_limb = topology_cluster_loss(
            #     new_feat,
            #     topo,
            #     score_index=3,
            # )

            # loss_waist = topology_cluster_loss(
            #     new_feat,
            #     topo,
            #     score_index=4,
            # )

            # loss_keep = feature_keep_loss(new_feat, base_feat)

            # loss = (
            #     3.0 * loss_topo
            #     + 2.0 * loss_limb
            #     + 2.0 * loss_waist
            #     + 0.03 * loss_keep
            # )

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"epoch {epoch:03d} loss {total_loss / len(loader):.6f}")

    torch.save({"model": model.state_dict()}, save_path)
    print(f"saved: {save_path}")


# if __name__ == "__main__":
#     main()