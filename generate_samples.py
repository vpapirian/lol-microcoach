import numpy as np, pandas as pd, os

os.makedirs("data", exist_ok=True)

def synth(path, seed=0, zigzag=1.0, jitter=0.5):
    rng = np.random.default_rng(seed)
    T = 1200  # 120s at 10 Hz (100 ms steps)
    dt_ms = 100
    xs, ys = [0.0], [0.0]
    heading = 0.0
    for _ in range(1, T):
        heading += rng.normal(0, 0.03*zigzag)
        step = max(0.5 + rng.normal(0, 0.05*jitter), 0)
        xs.append(xs[-1] + np.cos(heading)*step)
        ys.append(ys[-1] + np.sin(heading)*step)
    time_ms = np.arange(T)*dt_ms
    atk = ((time_ms % 1100) < 150).astype(int)
    df = pd.DataFrame({
        "time_ms": time_ms,
        "x": xs, "y": ys,
        "is_attacking": atk,
        "attack_cd": np.where(atk==1, 0.0, (time_ms % 1100)/1000.0)
    })
    df.to_csv(path, index=False)

synth("data/sample_user.csv", seed=1, zigzag=0.8, jitter=0.8)
synth("data/sample_pro.csv",  seed=2, zigzag=1.2, jitter=0.4)
print("✅ Wrote data/sample_user.csv and data/sample_pro.csv")
