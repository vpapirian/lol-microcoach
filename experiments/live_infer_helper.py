# live_infer_helper.py
import pandas as pd
from pathlib import Path
from microcoach.features import extract_features

LIVE = Path("data/live.csv")

def latest_window_feats(window_s=5):
    if not LIVE.exists(): return None
    df = pd.read_csv(LIVE)
    if df.empty: return None
    tmax = df["time_ms"].max()
    dfw = df[df["time_ms"] >= tmax - int(window_s*1000)]
    if len(dfw) < 5: return None
    return extract_features(dfw)  # per-sec aggregated features
