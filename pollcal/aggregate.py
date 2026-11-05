"""⑤ 여러 조사를 시간에 따라 합치기(상태공간 모형 + 기관 효과)와 선거 단위 교차검증."""
import numpy as np


def poll_series(rng, bias, house, T=60, start=0.47, walk_sd=0.003, sizes=(1000, 1000, 800, 1500)):
    mu = start + np.cumsum(rng.normal(0, walk_sd, T + 1))
    polls = []
    for k, h in enumerate(house):
        t = int(rng.integers(0, 5))
        while t <= T:
            p = mu[t] + h + bias; sd = np.sqrt(p * (1 - p) / sizes[k])
            polls.append((t, k, p + rng.normal(0, sd), sizes[k])); t += 4 + int(rng.integers(0, 4))
    polls.sort()
    return {"T": T, "mu": mu, "polls": polls, "truth": mu[T]}


def kalman(series, house_on=True, q=0.003 ** 2):
    T = series["T"]; h = np.zeros(4); by_t = {}
    for p in series["polls"]: by_t.setdefault(p[0], []).append(p)
    for _ in range(6 if house_on else 1):
        m = np.zeros(T + 1); v = np.zeros(T + 1); x = series["polls"][0][2]; P = 0.01
        for t in range(T + 1):
            P += q
            for (_, k, val, n) in by_t.get(t, []):
                R = val * (1 - val) / n; K = P / (P + R); x += K * (val - h[k] - x); P *= 1 - K
            m[t] = x; v[t] = P
        ms, vs = m.copy(), v.copy()
        for t in range(T - 1, -1, -1):
            C = v[t] / (v[t] + q); ms[t] = m[t] + C * (ms[t + 1] - m[t]); vs[t] = v[t] + C * C * (vs[t + 1] - v[t] - q)
        if house_on:
            res = np.zeros(4); cnt = np.zeros(4)
            for (t, k, val, n) in series["polls"]: res[k] += val - ms[t]; cnt[k] += 1
            hh = np.where(cnt > 0, res / np.maximum(cnt, 1), 0); h = hh - hh.mean()
    return {"path": ms, "sd": np.sqrt(np.maximum(vs, 0)), "house": h}


def backtest(seed, K, bias_mean, bias_sd, house):
    """지난 선거 K개: 선거 하나를 통째로 빼고, 나머지 선거들의 최종 오차 평균을 공통 치우침으로 보고 뺀다."""
    rng = np.random.default_rng(seed); E = []
    for e in range(K):
        b = bias_mean + rng.normal(0, bias_sd)
        s = poll_series(rng, b, house, start=0.42 + rng.random() * 0.12)
        k = kalman(s); E.append({"bias": b, "est": k["path"][-1], "truth": s["truth"], "err": k["path"][-1] - s["truth"]})
    for i, x in enumerate(E):
        corr = np.mean([y["err"] for j, y in enumerate(E) if j != i]); x["corr"] = corr; x["after"] = x["err"] - corr
    return {"elections": E, "mae_before": float(np.mean([abs(x["err"]) for x in E])),
            "mae_after": float(np.mean([abs(x["after"]) for x in E]))}
