# microcoach/realtime.py
import numpy as np
import pandas as pd
from microcoach.features import extract_features

FEATURES = ["step_len","dir_change_rate","curvature","jitter"]

def summarize_feats(feats: pd.DataFrame) -> np.ndarray:
    v = feats[FEATURES].replace([np.inf,-np.inf], np.nan).fillna(0.0)
    return v.tail(5).mean(axis=0).values  # last ~5 seconds average

def build_pro_reference(pro_df: pd.DataFrame) -> dict:
    pro_feats = extract_features(pro_df)
    X = pro_feats[FEATURES].replace([np.inf,-np.inf], np.nan).fillna(0.0).values
    mu, sd = X.mean(axis=0), X.std(axis=0) + 1e-6
    ref = {
        "mu": mu, "sd": sd,
        "centroid": ((X - mu)/sd).mean(axis=0)  # normalized centroid
    }
    return ref

def live_score(user_feats: pd.DataFrame, ref: dict) -> float:
    u = summarize_feats(user_feats)
    z = (u - ref["mu"]) / ref["sd"]
    # smaller distance = more “pro-like”
    return float(np.linalg.norm(z - ref["centroid"]))
