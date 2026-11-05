"""보정법 7가지. 모두 같은 입력(표본)과 같은 정답지(모집단 표)를 받고, 같은 형식으로 결과를 돌려준다.

결과 형식: {"est": 추정값, "lo": 95% 하한 또는 None, "hi": 상한 또는 None, "info": {...}}
"""
import numpy as np

Z = 1.959964


def _wald(p, n):
    se = np.sqrt(max(p * (1 - p), 1e-9) / max(n, 1))
    return p - Z * se, p + Z * se


def raw(S, world):
    p = S.y.mean(); lo, hi = _wald(p, S.n)
    return {"est": p, "lo": lo, "hi": hi, "info": {"n_eff": S.n}}


def poststrat(S, world):
    """연령6×성별2×권역4 = 48칸. 빈 칸은 성별만 다른 칸으로 대신."""
    n = np.bincount(S.cell, minlength=48); ys = np.bincount(S.cell, weights=S.y, minlength=48)
    pc = np.where(n > 0, ys / np.maximum(n, 1), np.nan); empty = int((n == 0).sum())
    for c in np.where(n == 0)[0]:
        alt = c + 4 if (c // 4) % 2 == 0 else c - 4                # 같은 연령·권역, 다른 성별
        pc[c] = pc[alt] if n[alt] > 0 else S.y.mean()
    W = world.cell_share; est = float((W * pc).sum())
    var = float(np.nansum(np.where(n > 0, W ** 2 * pc * (1 - pc) / np.maximum(n, 1), 0)))
    w_i = W[S.cell] / (n[S.cell] / S.n)
    neff = w_i.sum() ** 2 / (w_i ** 2).sum()
    return {"est": est, "lo": est - Z * np.sqrt(var), "hi": est + Z * np.sqrt(var),
            "info": {"empty_cells": empty, "n_eff": float(neff), "w_max": float(w_i.max() / w_i.mean())}}


def rake(S, world, past=True, margins=("age", "sex", "region"), iters=40):
    """여러 기준의 모집단 분포에 번갈아 맞추기. past=True면 권역×지난 투표(정답지)에 맞춤."""
    w = np.ones(S.n); n = S.n
    keys = []
    if "age" in margins: keys.append((S.a, world.age_share))
    if "sex" in margins: keys.append((S.s, world.sex_share))
    if past:
        keys.append((S.r * 3 + S.past, (world.region_share[:, None] * world.region_past).ravel()))
    elif "region" in margins:
        keys.append((S.r, world.region_share))
    for _ in range(iters):
        for k, target in keys:
            tot = np.bincount(k, weights=w, minlength=len(target))
            f = np.where(tot > 0, target * n / np.maximum(tot, 1e-12), 1.0)
            w = w * f[k]
    est = float((w * S.y).sum() / w.sum()); neff = float(w.sum() ** 2 / (w ** 2).sum())
    lo, hi = _wald(est, neff)
    return {"est": est, "lo": lo, "hi": hi, "w": w,
            "info": {"n_eff": neff, "w_max": float(w.max() / w.mean()), "w_min": float(w.min() / w.mean())}}


def _design(a, s, r, past):
    """절편 + 연령(5) + 성별(1) + 권역(3) + 연령×성별(5) + 지난 투표(2) = 17열."""
    m = len(a); X = np.zeros((m, 17)); X[:, 0] = 1
    for k in range(1, 6): X[:, k] = a == k
    X[:, 6] = s == 1
    for k in range(1, 4): X[:, 6 + k] = r == k
    for k in range(1, 6): X[:, 9 + k] = (a == k) & (s == 1)
    X[:, 15] = past == 1; X[:, 16] = past == 2
    return X


def mrp(S, world, prior_sd=1.0, draws=400, rng=None):
    """다층 회귀 + 사후층화. 계수에 정규 사전분포(절편 제외 sd=1)를 두고 사후 최빈값과 라플라스 근사로 사후분포를 구한다.
    사후층화 표 = 칸 48 × 지난 투표 3 (실제 자료에서는 사후층화 표 v0의 지난 투표 층)."""
    rng = rng or np.random.default_rng(0)
    X = _design(S.a, S.s, S.r, S.past); y = S.y.astype(float)
    prec = np.full(17, 1 / prior_sd ** 2); prec[0] = 1 / 25.0
    b = np.zeros(17)
    for _ in range(30):
        p = 1 / (1 + np.exp(-X @ b)); g = X.T @ (y - p) - prec * b
        H = (X * (p * (1 - p))[:, None]).T @ X + np.diag(prec)
        step = np.linalg.solve(H, g); b += step
        if np.abs(step).max() < 1e-8: break
    cov = np.linalg.inv(H)
    cells = np.arange(48); ca, cs, cr = cells // 8, (cells // 4) % 2, cells % 4
    A = np.repeat(ca, 3); Ss = np.repeat(cs, 3); Rr = np.repeat(cr, 3); Pv = np.tile([0, 1, 2], 48)
    Xf = _design(A, Ss, Rr, Pv); wf = world.frame_past.ravel()
    B = rng.multivariate_normal(b, cov, size=draws)
    th = (1 / (1 + np.exp(-Xf @ B.T)) * wf[:, None]).sum(0)
    est = float((1 / (1 + np.exp(-Xf @ b)) * wf).sum())
    return {"est": est, "lo": float(np.percentile(th, 2.5)), "hi": float(np.percentile(th, 97.5)),
            "info": {"coef": b.tolist()}}


def tree_ps(S, world, kind="xgb", seed=0):
    """트리 모형 + 사후층화: 연령·성별·권역·지난 투표로 칸별 지지율을 예측하고 모집단 표로 더한다."""
    F = np.c_[S.a, S.s, S.r, S.past]
    cells = np.arange(48); A = np.repeat(cells // 8, 3); Ss = np.repeat((cells // 4) % 2, 3)
    Rr = np.repeat(cells % 4, 3); Pv = np.tile([0, 1, 2], 48); Ff = np.c_[A, Ss, Rr, Pv]
    if kind == "xgb":
        from xgboost import XGBClassifier
        m = XGBClassifier(n_estimators=150, max_depth=3, learning_rate=0.08, subsample=0.9, random_state=seed,
                          verbosity=0, n_jobs=1)
    else:
        from lightgbm import LGBMClassifier
        m = LGBMClassifier(n_estimators=150, max_depth=3, learning_rate=0.08, num_leaves=8, min_child_samples=10,
                           random_state=seed, verbose=-1, n_jobs=1)
    m.fit(F, S.y)
    est = float((m.predict_proba(Ff)[:, 1] * world.frame_past.ravel()).sum())
    return {"est": est, "lo": None, "hi": None, "info": {}}


def paper3(S, world, B=50, rng=None, hist=None):
    """원래 working paper의 3단계 가중식 (비교 기준선).
    극단점수: 규칙으로 붙인 라벨을 Random Forest가 다시 배움 → w_extreme = 1/(1+2·점수)
    투표 확률: 과거 자료로 학습한 XGBoost → w_turnout
    인구통계: 연령 비율 → w_demo.  w = w_extreme × w_turnout × w_demo"""
    from sklearn.ensemble import RandomForestClassifier
    rng = rng or np.random.default_rng(0)
    f = S.features()
    eng = 0.4 * f["interest"] + 0.3 * f["news"] + 0.3 * f["discuss"]
    ext = np.abs(f["ideology"] - 5); z = (f["resp_time"] - f["resp_time"].mean()) / f["resp_time"].std()
    label = ((eng > np.quantile(eng, 0.8)).astype(int) + (ext > 3) + (f["past_resp"] > np.median(f["past_resp"]))
             + (np.abs(z) > 2)) >= 2
    Xe = np.c_[ext, eng, f["party_strength"], z, f["past_resp"]]
    rf = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=0, n_jobs=1)
    rf.fit(Xe, label.astype(int)); score = rf.predict_proba(Xe)[:, 1] if label.any() and not label.all() else np.zeros(S.n)
    rf_acc = float((rf.predict(Xe) == label).mean())
    w_ext = 1 / (1 + 2 * score)
    w_turn = hist.predict_proba(np.c_[S.a, S.s, S.r, f["interest"]])[:, 1] if hist is not None else np.ones(S.n)
    samp_age = np.bincount(S.a, minlength=6) / S.n
    w_demo = world.age_share[S.a] / np.maximum(samp_age[S.a], 1e-9)
    w = w_ext * w_turn * w_demo
    est = float((w * S.y).sum() / w.sum())
    bs = []
    for _ in range(B):
        i = rng.integers(0, S.n, S.n); bs.append((w[i] * S.y[i]).sum() / w[i].sum())
    neff = float(w.sum() ** 2 / (w ** 2).sum())
    return {"est": est, "lo": float(np.percentile(bs, 2.5)), "hi": float(np.percentile(bs, 97.5)),
            "info": {"n_eff": neff, "rf_train_acc": rf_acc, "label_rate": float(label.mean())}}


def turnout_model(world, n=3000, seed=1):
    """원래 방식의 투표참여 예측기: '과거 자료'(모집단 무작위 표본)로 XGBoost 학습."""
    from xgboost import XGBClassifier
    rng = np.random.default_rng(seed); i = rng.choice(world.N, n, replace=False)
    X = np.c_[world.a[i], world.s[i], world.r[i], world.interest[i]]; y = (world.past[i] != 2).astype(int)
    m = XGBClassifier(n_estimators=100, max_depth=3, learning_rate=0.1, random_state=seed, verbosity=0, n_jobs=1)
    m.fit(X, y); return m


METHODS = [
    ("raw", "① 원시 평균", raw),
    ("ps", "② 사후층화 (연령×성별×권역)", poststrat),
    ("rake", "③ 레이킹 (연령·성별 + 권역×지난 투표)", rake),
    ("mrp", "④ MRP (베이지안 다층 회귀 + 사후층화)", mrp),
    ("xgb", "④' XGBoost + 사후층화", lambda S, w: tree_ps(S, w, "xgb")),
    ("lgbm", "④'' LightGBM + 사후층화", lambda S, w: tree_ps(S, w, "lgbm")),
    ("paper3", "원래 3단계 가중식 (RF·XGBoost·연령)", None),
]
