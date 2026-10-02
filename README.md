<div align="center">

# 🎯 LoL MicroMotion Coach

**Compare your League of Legends movement against pro players and find out what to practice.**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-NumPy-150458?logo=pandas&logoColor=white)
![Status](https://img.shields.io/badge/status-MVP-blue)

</div>

---

## ✨ How it works

1. **Record** your champion's position about 10 times per second (`live_poller.py` reads Riot's Live Client Data API while you're in a game).
2. **Extract** micro-movement features from the path:

| Feature | Meaning |
|---|---|
| `step_len` | How far you move per click |
| `dir_change_rate` | Direction changes per second while trading |
| `curvature` | How curved your path is, versus walking in straight lines |
| `jitter` | Over-corrections between clicks |

3. **Compare** your features to pro baselines (a lower distance means more pro-like).
4. **Get coaching tips**, for example *"Your path is too straight; add slight arcs to avoid linear skillshots."*

## 🚀 Quick start

```bash
pip install -r requirements.txt
python generate_samples.py         # creates demo CSVs in data/
streamlit run app.py               # upload your CSV + pro CSVs
```

To record your own game, run `python live_poller.py` during a match. It writes `data/live.csv`.

## 📁 Structure

```
app.py                 # Streamlit UI
live_poller.py         # records your position from the Live Client API
generate_samples.py    # synthetic demo data
microcoach/
├── features.py        # movement feature extraction
├── compare.py         # distance to pro baselines
└── advice.py          # rule-based coaching tips
data/                  # sample user + pro CSVs
experiments/           # real-time inference prototypes
```

> ℹ️ Only uses Riot's read-only local API. No inputs are automated.

➡️ See **[lol-microcoach-pro](https://github.com/vpapirian/lol-microcoach-pro)** for the newer live dashboard.

---

<div align="center">Built by <a href="https://github.com/vpapirian">Vatche Papirian</a></div>
