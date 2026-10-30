"""정답을 아는 가상 유권자 세계 만들기."""
import csv
from pathlib import Path
import numpy as np

from .config import AGES, SEXES, REGIONS, REGION_OF

ROOT = Path(__file__).resolve().parent.parent
EXIT_AGE = {"20대": 0, "30대": 1, "40대": 2, "50대": 3, "60대": 4, "70대 이상": 5}
logit = lambda p: np.log(p / (1 - p))
sig = lambda z: 1 / (1 + np.exp(-z))


def composition(path):
    """연령6 × 성별2 × 권역4 인구 비율 (사후층화 표 v0에서)."""
    W = np.zeros((6, 2, 4))
    for r in csv.DictReader(open(ROOT / path, encoding="utf-8-sig")):
        a = AGES.index(r["age_grp"]); s = 0 if r["sex"].startswith("남") else 1
        W[a, s, REGION_OF[r["province"]]] += float(r["share"])
    return W / W.sum()


def vote_targets():
    """2025 대선: 연령·성별 출구조사(이재명 득표)와 권역별 득표(이재명, 투표자 가중)."""
    E = np.zeros((6, 2))
    for r in csv.DictReader(open(ROOT / "data/kep_exitpoll_2025_age_sex.csv", encoding="utf-8")):
        E[EXIT_AGE[r["age_grp"]], 0 if r["sex"] == "남" else 1] = float(r["lee_jm"]) / 100
    import importlib.util
    spec = importlib.util.spec_from_file_location("region_2025", ROOT / "scripts/region_2025.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    shares = {}
    for r in csv.DictReader(open(ROOT / "data/frame_v0_age_sex_prov_edu.csv", encoding="utf-8-sig")):
        shares[r["province"]] = shares.get(r["province"], 0) + float(r["share"])
    num = np.zeros(4); den = np.zeros(4); src = {}
    for row in m.table():
        g = REGION_OF[row["prov"]]; v = shares[row["prov"]] * row["turnout"] / 100
        num[g] += v * row["lee_jm"] / 100; den[g] += v; src[row["prov"]] = row["src"]
    return E, num / den, src


def calibrate(W, E, Rt, dev=None, iters=200):
    """logit p[a,s,r] = α[a,s] + β[r].
    출구조사는 전국 수준이 실제 득표보다 높게 나오므로, 먼저 공통 이동 δ로 연령·성별 목표를 전국 득표에 맞춘 뒤(모양 유지)
    권역 목표와 연령·성별 목표를 번갈아 정확히 맞춘다(logit 척도의 레이킹)."""
    wr = W.sum((0, 1)); was = W.sum(2); nat = (wr * Rt).sum() / wr.sum()
    def solve(f, target, lo=-8, hi=8):
        for _ in range(50):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if f(mid) < target else (lo, mid)
        return (lo + hi) / 2
    dev = np.zeros(W.shape) if dev is None else dev
    LE = logit(np.clip(E, .02, .98))
    delta = solve(lambda d: (was * sig(LE + d)).sum() / was.sum(), nat)
    Et = sig(LE + delta)
    alpha = LE + delta; beta = np.zeros(4)
    for _ in range(iters):
        for r in range(4):
            beta[r] = solve(lambda b: (W[:, :, r] * sig(alpha + b + dev[:, :, r])).sum() / wr[r], Rt[r])
        for a in range(6):
            for x in range(2):
                alpha[a, x] = solve(lambda al: (W[a, x, :] * sig(al + beta + dev[a, x, :])).sum() / was[a, x], Et[a, x])
    return sig(alpha[:, :, None] + beta[None, None, :] + dev), Et, delta


class World:
    def __init__(self, cfg):
        self.cfg = cfg
        rng = np.random.default_rng(cfg["seed"])
        W = composition(cfg["composition"]["value"]); E, Rt, self.region_src = vote_targets()
        self.W, self.E_target, self.R_target = W, E, Rt
        dev = rng.normal(0, cfg["cell_deviation_sd"]["value"], W.shape); self.dev = dev
        P, self.E_scaled, self.exit_shift = calibrate(W, E, Rt, dev); self.P = P
        N = cfg["population_size"]; s = cfg["strong_share"]["value"]; lam = cfg["strong_loyalty"]["value"]
        counts = np.round(W * N).astype(int)
        rows = []
        for a in range(6):
            for x in range(2):
                for r in range(4):
                    n = counts[a, x, r]; p = P[a, x, r]
                    u = rng.random(n); t = np.where(u < s * p, 0, np.where(u < s, 2, 1))   # 0 강성A, 1 중도, 2 강성B
                    q = np.clip((p - s * p * lam - s * (1 - p) * (1 - lam)) / (1 - s), 0, 1)
                    pa = np.where(t == 0, lam, np.where(t == 2, 1 - lam, q))
                    y = (rng.random(n) < pa).astype(np.int8)
                    rows.append((np.full(n, a), np.full(n, x), np.full(n, r), t, y))
        self.a, self.s, self.r, self.t, self.y = [np.concatenate([z[i] for z in rows]) for i in range(5)]
        n = len(self.y); pv = cfg["past_vote"]["value"]
        probs = np.where(self.t[:, None] == 0, pv["strongA"], np.where(self.t[:, None] == 2, pv["strongB"],
                         np.where(self.y[:, None] == 1, pv["middle_if_A"], pv["middle_if_B"])))
        u = rng.random(n); c = probs.cumsum(1)
        self.past = (u[:, None] > c).sum(1).astype(np.int8)          # 0 A계열, 1 B계열, 2 투표 안 함
        strong = (self.t != 1).astype(float)
        # 원래 3단계 가중식(비교 기준선)이 쓰는 설문 문항들
        self.interest = np.clip(rng.normal(4.5 + 3.0 * strong, 1.4), 1, 10)
        self.news = np.clip(0.6 * self.interest + rng.normal(2.5, 1.3, n), 1, 10)
        self.discuss = np.clip(0.5 * self.interest + rng.normal(1.8, 1.4, n), 1, 10)
        ideo_mu = np.where(self.t == 0, 2.6, np.where(self.t == 2, 7.4, 5.0))
        self.ideology = np.clip(rng.normal(ideo_mu, 1.3), 1, 10)
        self.party_strength = np.clip(rng.normal(4 + 4 * strong, 1.6), 1, 10)
        self.past_resp = rng.poisson(1.5 + 2.5 * strong)
        self.resp_time = rng.lognormal(3, 0.9, n)
        self.N = n
        self.cell = (self.a * 2 + self.s) * 4 + self.r                # 48칸
        self.truth = self.y.mean()
        self.cell_n = np.bincount(self.cell, minlength=48)
        self.cell_truth = np.bincount(self.cell, weights=self.y, minlength=48) / np.maximum(self.cell_n, 1)
        # 정답지: 권역별 지난 선거 결과 (권역 × 지난 투표 3칸)
        self.region_past = np.zeros((4, 3))
        np.add.at(self.region_past, (self.r, self.past), 1); self.region_past /= self.region_past.sum(1, keepdims=True)
        # MRP 사후층화용 결합 표 (칸 48 × 지난 투표 3) — 실제로는 사후층화 표 v0의 지난 투표 층이 이 자리
        self.frame_past = np.zeros((48, 3)); np.add.at(self.frame_past, (self.cell, self.past), 1)
        self.frame_past /= self.N
        self.age_share = np.bincount(self.a, minlength=6) / n
        self.sex_share = np.bincount(self.s, minlength=2) / n
        self.region_share = np.bincount(self.r, minlength=4) / n
        self.cell_share = self.cell_n / n

    def propensity(self, sc):
        ar = np.array(self.cfg["age_response"]["value"]) if sc["age_response"] else np.ones(6)
        return ar[self.a] * np.where(self.t == 0, sc["mA"], np.where(self.t == 2, sc["mB"], 1.0))

    def sample(self, sc, n, rng):
        """응답 확률에 비례해 n명 뽑기. 기억 착오는 응답 단계에서 생긴다."""
        w = self.propensity(sc); idx = rng.choice(self.N, size=n, replace=True, p=w / w.sum())
        past = self.past[idx].copy()
        if sc.get("recall", 0):
            flip = (self.t[idx] == 1) & (past == 1) & (rng.random(n) < sc["recall"])
            past[flip] = 0
        return Sample(self, idx, past)


class Sample:
    def __init__(self, world, idx, past):
        self.w = world; self.idx = idx
        self.a, self.s, self.r, self.y = world.a[idx], world.s[idx], world.r[idx], world.y[idx]
        self.cell = world.cell[idx]; self.past = past; self.n = len(idx)

    def features(self):
        w, i = self.w, self.idx
        return {"interest": w.interest[i], "news": w.news[i], "discuss": w.discuss[i], "ideology": w.ideology[i],
                "party_strength": w.party_strength[i], "past_resp": w.past_resp[i], "resp_time": w.resp_time[i]}
