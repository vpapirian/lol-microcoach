import numpy as np
import pandas as pd
try:
    from fastdtw import fastdtw
except Exception:
    fastdtw = None
from scipy.spatial.distance import euclidean

FEATURES = ["step_len","dir_change_rate","curvature","jitter"]

def sequence_matrix(feats: pd.DataFrame):
    M = feats[FEATURES].replace([np.inf, -np.inf], np.nan).fillna(0.0).values
    mu = M.mean(axis=0, keepdims=True); sd = M.std(axis=0, keepdims=True) + 1e-6
    return (M - mu) / sd

def dtw_distance(A, B):
    if fastdtw is None:
        n = min(len(A), len(B))
        if n == 0: return 1e9
        return np.mean(np.linalg.norm(A[:n]-B[:n], axis=1))
    dist, _ = fastdtw(A, B, dist=euclidean)
    return dist / (len(A)+len(B))

def compare_to_baselines(user_feats, pro_feat_list):
    Au = sequence_matrix(user_feats)
    dists = []
    for name, F in pro_feat_list:
        Ap = sequence_matrix(F)
        d = dtw_distance(Au, Ap)
        dists.append((name, d))
    dists.sort(key=lambda x: x[1])
    return dists
