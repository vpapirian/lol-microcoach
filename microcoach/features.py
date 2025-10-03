import numpy as np
import pandas as pd

def _heading(x, y):
    dx = np.gradient(x); dy = np.gradient(y)
    return np.arctan2(dy, dx)

def _speed(x, y, dt_s):
    dx = np.gradient(x); dy = np.gradient(y)
    return np.hypot(dx, dy) / dt_s

def extract_features(df, hz=10):
    """df: columns time_ms,x,y,is_attacking,attack_cd (≈100 ms per row)."""
    df = df.sort_values("time_ms").reset_index(drop=True)
    dt_s = np.median(np.diff(df.time_ms.values)) / 1000.0
    if not np.isfinite(dt_s) or dt_s <= 0: dt_s = 1.0 / hz

    x, y = df.x.values, df.y.values
    theta = _heading(x, y)
    dtheta = np.unwrap(theta)
    dtheta = np.gradient(dtheta)  # rad/sample

    speed = _speed(x, y, dt_s)
    disp = np.hypot(np.diff(x, prepend=x[0]), np.diff(y, prepend=y[0]))
    step_len = pd.Series(disp).rolling(int(0.6/dt_s), min_periods=1).median().values

    sign = np.sign(dtheta)
    flips = (np.abs(np.diff(sign, prepend=sign[0])) > 0).astype(int)
    dchange_rate = pd.Series(flips).rolling(int(1.0/dt_s), min_periods=1).sum().values

    with np.errstate(divide='ignore', invalid='ignore'):
        curvature = np.abs(dtheta) / (speed + 1e-6)

    w = int(3.0/dt_s)
    jitter = np.zeros(len(df))
    for i in range(len(df)):
        a = max(0, i-w//2); b = min(len(df), i+w//2)
        xx, yy = x[a:b], y[a:b]
        if len(xx) < 3:
            jitter[i] = 0
            continue
        pts = np.column_stack([xx, yy]); pts -= pts.mean(axis=0, keepdims=True)
        _, _, vh = np.linalg.svd(pts, full_matrices=False)
        dirv = vh[0]
        proj = pts @ dirv[:,None] @ dirv[None,:]
        resid = pts - proj
        jitter[i] = np.sqrt((resid**2).sum(axis=1).mean())

    feats = pd.DataFrame({
        "time_s": df.time_ms.values/1000.0,
        "step_len": step_len,
        "dir_change_rate": dchange_rate,
        "curvature": curvature,
        "jitter": jitter,
        "is_attacking": df.is_attacking.astype(int),
        "attack_cd": df.attack_cd
    })
    feats["sec"] = feats["time_s"].astype(int)
    agg = feats.groupby("sec").agg({
        "step_len": "median",
        "dir_change_rate": "mean",
        "curvature": "mean",
        "jitter": "mean",
        "is_attacking": "mean",
        "attack_cd": "mean"
    }).reset_index().rename(columns={"sec":"time_s"})
    return agg
