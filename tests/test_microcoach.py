import numpy as np
import pandas as pd
import pytest

from microcoach.advice import generate_advice
from microcoach.compare import FEATURES, compare_to_baselines, dtw_distance
from microcoach.features import extract_features


def make_path(n=100, noise=0.0, seed=0):
    rng = np.random.default_rng(seed)
    t = np.arange(n) * 100
    x = np.cumsum(np.full(n, 0.5)) + rng.normal(0, noise, n)
    y = np.sin(np.arange(n) / 10) + rng.normal(0, noise, n)
    return pd.DataFrame(
        {"time_ms": t, "x": x, "y": y, "is_attacking": 0, "attack_cd": 0.0}
    )


def test_extract_features_aggregates_per_second():
    feats = extract_features(make_path(100))  # 10 seconds at 10 Hz
    assert list(feats["time_s"]) == list(range(10))
    for col in FEATURES:
        assert col in feats.columns
        assert np.isfinite(feats[col]).all()


def test_extract_features_sorts_unordered_input():
    df = make_path(50)
    shuffled = df.sample(frac=1, random_state=1)
    pd.testing.assert_frame_equal(extract_features(df), extract_features(shuffled))


def test_extract_features_rejects_missing_columns():
    with pytest.raises(ValueError, match="missing column.*attack_cd"):
        extract_features(make_path(20).drop(columns=["attack_cd"]))


@pytest.mark.parametrize("rows", [0, 1, 2])
def test_extract_features_rejects_too_few_rows(rows):
    with pytest.raises(ValueError, match="at least 3"):
        extract_features(make_path(20).head(rows))


def test_dtw_distance_zero_for_identical_sequences():
    A = np.random.default_rng(0).normal(size=(20, 4))
    assert dtw_distance(A, A) == pytest.approx(0.0, abs=1e-9)


def test_compare_ranks_closest_baseline_first():
    user = extract_features(make_path(100, noise=0.01, seed=1))
    similar = extract_features(make_path(100, noise=0.01, seed=2))
    other = make_path(100, noise=0.0)
    other["x"] = np.cumsum(np.random.default_rng(3).uniform(0, 5, 100))
    other["y"] = np.cumsum(np.random.default_rng(4).uniform(-5, 5, 100))
    ranked = compare_to_baselines(
        user, [("other", extract_features(other)), ("similar", similar)]
    )
    assert [name for name, _ in ranked][0] == "similar"
    assert ranked[0][1] <= ranked[1][1]


def test_advice_flags_each_deviation():
    pro = {"step_len": 1.0, "dir_change_rate": 1.0, "curvature": 1.0, "jitter": 1.0}
    tips = generate_advice(
        {"step_len": 2.0, "dir_change_rate": 0.5, "curvature": 0.5, "jitter": 2.0}, pro
    )
    assert len(tips) == 4


def test_advice_defaults_to_encouragement_when_close_to_pro():
    pro = {"step_len": 1.0, "dir_change_rate": 1.0, "curvature": 1.0, "jitter": 1.0}
    assert generate_advice(dict(pro), pro) == [
        "Solid fundamentals—practice orbwalk timing next."
    ]
