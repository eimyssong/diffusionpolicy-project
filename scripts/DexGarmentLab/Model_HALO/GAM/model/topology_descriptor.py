import numpy as np


def _smoothstep(edge0, edge1, x):
    x = np.clip((x - edge0) / (edge1 - edge0 + 1e-6), 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)


def compute_topology_descriptor(points: np.ndarray, garment_type: str = "tops") -> np.ndarray:
    """
    Output dim = 6:
    [left_branch, right_branch, branch_progress, endpoint_score, center_score, boundary_score]

    tops:
      sleeve cuff가 branch endpoint가 되도록 x 방향 progress 사용.
    trousers:
      pants hem이 branch endpoint가 되도록 y 방향 progress 사용.
    """
    p = np.asarray(points, dtype=np.float32)
    x = p[:, 0]
    y = p[:, 1]

    x_mid = np.median(x)
    x_span = np.percentile(x, 95) - np.percentile(x, 5) + 1e-6
    y_span = np.percentile(y, 95) - np.percentile(y, 5) + 1e-6

    left_branch = (x <= x_mid).astype(np.float32)
    right_branch = 1.0 - left_branch

    garment_type = garment_type.lower()

    if "trouser" in garment_type or "pants" in garment_type or "pant" in garment_type:
        y_top = np.percentile(y, 95)
        branch_progress = np.clip((y_top - y) / y_span, 0.0, 1.0)
    else:
        branch_progress = np.clip(np.abs(x - x_mid) / (0.5 * x_span), 0.0, 1.0)

    endpoint_score = _smoothstep(0.72, 0.95, branch_progress)
    center_score = 1.0 - branch_progress

    y_low_score = _smoothstep(0.72, 0.95, np.clip((np.percentile(y, 95) - y) / y_span, 0.0, 1.0))
    boundary_score = np.maximum(endpoint_score, 0.5 * y_low_score)

    topo = np.stack(
        [
            left_branch,
            right_branch,
            branch_progress,
            endpoint_score,
            center_score,
            boundary_score,
        ],
        axis=1,
    )

    return topo.astype(np.float32)








# def compute_topology_descriptor(points: np.ndarray, garment_type: str = "tops") -> np.ndarray:
#     p = np.asarray(points, dtype=np.float32)

#     xy = p[:, :2]
#     x = p[:, 0]
#     y = p[:, 1]

#     center = np.median(xy, axis=0)

#     x_mid = np.median(x)

#     x_span = np.percentile(x, 95) - np.percentile(x, 5) + 1e-6
#     y_span = np.percentile(y, 95) - np.percentile(y, 5) + 1e-6

#     xy_span = np.percentile(xy, 95, axis=0) - np.percentile(xy, 5, axis=0) + 1e-6
#     xy_norm = (xy - center) / xy_span

#     radial = np.linalg.norm(xy_norm, axis=1)
#     radial = radial / (np.percentile(radial, 95) + 1e-6)
#     radial_progress = np.clip(radial, 0.0, 1.0)

#     left_branch = (x <= x_mid).astype(np.float32)
#     right_branch = 1.0 - left_branch

#     garment_type = garment_type.lower()

#     if "trouser" in garment_type or "pants" in garment_type or "pant" in garment_type:
#         y_top = np.percentile(y, 95)
#         directional_progress = np.clip((y_top - y) / y_span, 0.0, 1.0)
#     else:
#         directional_progress = np.clip(np.abs(x - x_mid) / (0.5 * x_span), 0.0, 1.0)

#     branch_progress = np.clip(
#         0.6 * directional_progress + 0.4 * radial_progress,
#         0.0,
#         1.0,
#     )

#     endpoint_score = _smoothstep(0.70, 0.95, branch_progress)
#     center_score = 1.0 - branch_progress
#     boundary_score = endpoint_score

#     topo = np.stack(
#         [
#             left_branch,
#             right_branch,
#             branch_progress,
#             endpoint_score,
#             center_score,
#             boundary_score,
#         ],
#         axis=1,
#     )

#     return topo.astype(np.float32)








# def compute_topology_descriptor(points: np.ndarray, garment_type: str = "tops") -> np.ndarray:
#     p = np.asarray(points, dtype=np.float32)

#     xy = p[:, :2]
#     x = p[:, 0]
#     y = p[:, 1]

#     x_mid = np.median(x)
#     y_low = np.percentile(y, 5)
#     y_high = np.percentile(y, 95)

#     x_span = np.percentile(x, 95) - np.percentile(x, 5) + 1e-6
#     y_span = y_high - y_low + 1e-6

#     left_branch = (x <= x_mid).astype(np.float32)
#     right_branch = 1.0 - left_branch

#     x_out = np.clip(np.abs(x - x_mid) / (0.5 * x_span), 0.0, 1.0)
#     y_from_top = np.clip((y_high - y) / y_span, 0.0, 1.0)
#     y_from_bottom = np.clip((y - y_low) / y_span, 0.0, 1.0)

#     center = np.median(xy, axis=0)
#     xy_span = np.percentile(xy, 95, axis=0) - np.percentile(xy, 5, axis=0) + 1e-6
#     radial = np.linalg.norm((xy - center) / xy_span, axis=1)
#     radial = np.clip(radial / (np.percentile(radial, 95) + 1e-6), 0.0, 1.0)

#     garment_type = garment_type.lower()

#     if "trouser" in garment_type or "pants" in garment_type or "pant" in garment_type:
#         limb_progress = np.clip(0.7 * y_from_top + 0.3 * radial, 0.0, 1.0)
#         limb_endpoint_score = _smoothstep(0.72, 0.95, y_from_top)
#         waist_score = _smoothstep(0.72, 0.95, y_from_bottom)
#     else:
#         limb_progress = np.clip(0.7 * x_out + 0.3 * radial, 0.0, 1.0)
#         limb_endpoint_score = _smoothstep(0.72, 0.95, x_out)
#         waist_score = _smoothstep(0.72, 0.95, y_from_top)

#     center_score = 1.0 - np.maximum(limb_endpoint_score, waist_score)
#     boundary_score = np.maximum(limb_endpoint_score, waist_score)

#     topo = np.stack(
#         [
#             left_branch,
#             right_branch,
#             limb_progress,
#             limb_endpoint_score,
#             waist_score,
#             center_score,
#             boundary_score,
#         ],
#         axis=1,
#     )

#     return topo.astype(np.float32)