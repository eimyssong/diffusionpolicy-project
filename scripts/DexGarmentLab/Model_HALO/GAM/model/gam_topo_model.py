import torch
import torch.nn as nn
import torch.nn.functional as F


class GAM_Topo_Model(nn.Module):
    def __init__(self, backbone: nn.Module, topo_dim: int = 6, feature_dim: int = 512):
        super().__init__()
        self.backbone = backbone

        self.topo_proj = nn.Sequential(
            nn.Linear(topo_dim, 128),
            nn.ReLU(inplace=True),
            nn.Linear(128, feature_dim),
        )

        # 처음에는 기존 checkpoint feature를 거의 유지한다.
        self.mix_logit = nn.Parameter(torch.tensor(-2.0))
        # self.mix_logit = nn.Parameter(torch.tensor(-1.0))

    def forward(self, xyz: torch.Tensor, topo: torch.Tensor):
        base_feat = self.backbone(xyz)      # B, N, C
        topo_feat = self.topo_proj(topo)    # B, N, C

        alpha = torch.sigmoid(self.mix_logit)
        feat = base_feat + alpha * topo_feat

        return F.normalize(feat, p=2, dim=-1)

    def freeze_backbone(self):
        for p in self.backbone.parameters():
            p.requires_grad = False

    def unfreeze_light_backbone(self):
        for name, p in self.backbone.named_parameters():
            p.requires_grad = (
                name.startswith("fp1")
                or name.startswith("conv1")
                or name.startswith("bn1")
                or name.startswith("conv2")
            )