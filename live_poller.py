# live_poller.py
import time, requests, csv
from pathlib import Path

OUT = Path("data/live.csv")
OUT.parent.mkdir(exist_ok=True)
FIELDS = ["time_ms","x","y","is_attacking","attack_cd","player_name"]

def grab():
    # try allgamedata; fall back to activeplayer/players if needed
    r = requests.get("http://127.0.0.1:2999/liveclientdata/allgamedata", timeout=0.4)
    r.raise_for_status()
    j = r.json()
    active = j.get("activePlayer") or {}
    pos = active.get("position", {"x":0,"y":0})
    is_attacking = int(active.get("isAttacking", False))
    attack_cd = float(active.get("attackCooldown", 0.0) or 0.0)
    name = active.get("summonerName", "you")
    return pos["x"], pos["y"], is_attacking, attack_cd, name

def main(hz=10):
    dt = 1.0 / hz
    t0 = time.time()
    # start fresh file
    with OUT.open("w", newline="") as f:
        csv.DictWriter(f, fieldnames=FIELDS).writeheader()
    print("Polling Live Client API… (Ctrl+C to stop)")
    while True:
        t_ms = int((time.time()-t0)*1000)
        try:
            x, y, atk, cd, name = grab()
            with OUT.open("a", newline="") as f:
                w = csv.DictWriter(f, fieldnames=FIELDS)
                w.writerow({"time_ms":t_ms, "x":x, "y":y, "is_attacking":atk,
                            "attack_cd":cd, "player_name":name})
        except Exception:
            # no game or transient; just wait
            pass
        time.sleep(dt)

if __name__ == "__main__":
    main()
