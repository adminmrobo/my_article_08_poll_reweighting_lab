"""실험: 크기 맞춤 → 현실성 점검 → 보정법 비교 → 기여 분해 → 선거 단위 교차검증 → 공개 결과표 점검 예시."""
import json, os, platform, time
from datetime import datetime, timezone
import numpy as np

from . import methods as M
from .aggregate import backtest
from .config import AGES, SEXES, REGIONS
from .world import World


def environment():
    import numpy, sklearn, xgboost, lightgbm
    cpu = platform.processor() or platform.machine()
    try:
        for line in open("/proc/cpuinfo"):
            if line.startswith("model name"): cpu = line.split(":", 1)[1].strip(); break
    except OSError:
        pass
    return {"python": platform.python_version(), "os": platform.platform(), "cpu": cpu, "cpu_count": os.cpu_count(),
            "numpy": numpy.__version__, "scikit_learn": sklearn.__version__, "xgboost": xgboost.__version__,
            "lightgbm": lightgbm.__version__, "run_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}


def raw_margin(world, sc, n, reps, seed):
    rng = np.random.default_rng(seed); m = []
    for _ in range(reps):
        S = world.sample(sc, n, rng); m.append(2 * S.y.mean() - 1)
    return float(np.mean(m))


def calibrate_ars(world, cfg, reps=40):
    """ARS형 강성 배율 k: (ARS형 원시 격차 − 전화면접형 원시 격차) = 9.9%p 가 되는 A쪽 배율."""
    base = dict(age_response=True, mA=cfg["phone_like"]["value"]["mA"], mB=cfg["phone_like"]["value"]["mB"], recall=0)
    target = cfg["ars_gap_target_pp"]["value"] / 100
    m0 = raw_margin(world, base, 1000, reps, 11)
    lo, hi = 1.3, 8.0
    for _ in range(14):
        mid = (lo + hi) / 2
        d = raw_margin(world, dict(base, mA=mid), 1000, reps, 11) - m0
        lo, hi = (mid, hi) if d < target else (lo, mid)
    k = (lo + hi) / 2
    return {"k": round(k, 2), "phone_margin": m0, "ars_margin": raw_margin(world, dict(base, mA=k), 1000, reps, 11),
            "target_pp": cfg["ars_gap_target_pp"]["value"]}


def realism(world, cfg, ars):
    P = world.P; W = world.W
    as_world = (W * P).sum(2) / W.sum(2); reg_world = (W * P).sum((0, 1)) / W.sum((0, 1))
    pop_strong = float((world.t != 1).mean())
    sc4 = dict(age_response=True, mA=ars["k"], mB=1.3, recall=0)
    rng = np.random.default_rng(5); S = world.sample(sc4, 20000, rng)
    samp_age = np.bincount(S.a, minlength=6) / S.n
    params = []
    for key in ["composition", "vote_structure", "cell_deviation_sd", "strong_share", "strong_loyalty", "past_vote", "age_response",
                "phone_like", "ars_gap_target_pp"]:
        v = cfg[key]; params.append({"key": key, "anchor": v["anchor"], "value": v.get("value"), "note": v["note"]})
    params.append({"key": "ars_multiplier_k", "anchor": "calib", "value": ars["k"],
                   "note": "ARS형 시나리오(S4~S6)의 강성 A층 응답 배율 — 위 9.9%p에 맞춰 계산"})
    return {
        "params": params,
        "age_sex_vs_exitpoll": [{"age": AGES[a], "sex": SEXES[s], "world_A": float(as_world[a, s]),
                                 "exitpoll_lee": float(world.E_target[a, s]), "exitpoll_scaled": float(world.E_scaled[a, s])}
                                for a in range(6) for s in range(2)],
        "exit_logit_shift": float(world.exit_shift),
        "age_sex_shift_note": "출구조사를 인구에 곱하면 전국 이재명 득표가 실제보다 높게 나와, 연령·성별 모양은 유지하고 수준을 권역 득표에 맞춤",
        "age_sex_mae_pp": float(np.abs(as_world - world.E_scaled).mean() * 100),
        "age_sex_mae_raw_pp": float(np.abs(as_world - world.E_target).mean() * 100),
        "age_sex_corr": float(np.corrcoef(as_world.ravel(), world.E_target.ravel())[0, 1]),
        "region_vs_target": [{"region": REGIONS[r], "world_A": float(reg_world[r]), "target_lee": float(world.R_target[r])} for r in range(4)],
        "truth": float(world.truth), "population": int(world.N),
        "js_world": {"W": world.W.tolist(), "P": world.P.tolist(), "ages": AGES, "sexes": SEXES, "regions": REGIONS,
                     "age_response": cfg["age_response"]["value"], "strong_share": cfg["strong_share"]["value"],
                     "loyalty": cfg["strong_loyalty"]["value"], "past_vote": cfg["past_vote"]["value"]}, "strong_share_pop": pop_strong,
        "ars": ars,
        "sample_age_vs_pop_S4": [{"age": AGES[a], "sample": float(samp_age[a]), "pop": float(world.age_share[a])} for a in range(6)],
        "sample_strong_S4": float((world.t[S.idx] != 1).mean()),
        "region_sources": world.region_src,
    }


def run_methods(world, S, rng, hist, B):
    out = {}
    for key, label, fn in M.METHODS:
        t0 = time.perf_counter()
        if key == "paper3": r = M.paper3(S, world, B=B, rng=rng, hist=hist)
        elif key == "mrp": r = M.mrp(S, world, rng=rng)
        else: r = fn(S, world)
        r["sec"] = time.perf_counter() - t0
        out[key] = r
    return out


def benchmark(world, cfg, ars, reps=None, n=None, log=print):
    reps = reps or cfg["reps"]; n = n or cfg["sample_size"]; hist = M.turnout_model(world)
    res = {}
    for sc in cfg["scenarios"]:
        sc = dict(sc)
        for k in ("mA", "mB"):
            if sc[k] == "calib": sc[k] = ars["k"]
        rng = np.random.default_rng(1000 + int(sc["id"][1:]))
        rows = {key: {"err": [], "cover": [], "width": [], "sec": [], "neff": []} for key, _, _ in M.METHODS}
        extra = {"rf_train_acc": [], "label_rate": [], "strong_in_sample": []}
        for i in range(reps):
            S = world.sample(sc, n, rng)
            extra["strong_in_sample"].append(float((world.t[S.idx] != 1).mean()))
            out = run_methods(world, S, rng, hist, cfg["bootstrap_B"])
            for key, r in out.items():
                e = r["est"] - world.truth; rows[key]["err"].append(e); rows[key]["sec"].append(r["sec"])
                if r["lo"] is not None:
                    rows[key]["cover"].append(r["lo"] <= world.truth <= r["hi"]); rows[key]["width"].append(r["hi"] - r["lo"])
                if "n_eff" in r.get("info", {}): rows[key]["neff"].append(r["info"]["n_eff"])
            extra["rf_train_acc"].append(out["paper3"]["info"]["rf_train_acc"]); extra["label_rate"].append(out["paper3"]["info"]["label_rate"])
        summ = {}
        for key, label, _ in M.METHODS:
            d = rows[key]; e = np.array(d["err"])
            summ[key] = {"label": label, "bias_pp": float(e.mean() * 100), "rmse_pp": float(np.sqrt((e ** 2).mean()) * 100),
                         "mae_pp": float(np.abs(e).mean() * 100),
                         "coverage": float(np.mean(d["cover"])) if d["cover"] else None,
                         "ci_width_pp": float(np.mean(d["width"]) * 100) if d["width"] else None,
                         "n_eff": float(np.mean(d["neff"])) if d["neff"] else None,
                         "sec_mean": float(np.mean(d["sec"])), "sec_p95": float(np.percentile(d["sec"], 95))}
        res[sc["id"]] = {"scenario": sc, "methods": summ, "reps": reps, "n": n,
                         "paper3_rf_train_acc": float(np.mean(extra["rf_train_acc"])),
                         "paper3_label_rate": float(np.mean(extra["label_rate"])),
                         "strong_in_sample": float(np.mean(extra["strong_in_sample"]))}
        log(f"  {sc['id']} {sc['name']}: " + ", ".join(f"{k} {v['rmse_pp']:.2f}" for k, v in summ.items()))
    return res


def decomposition(world, ars, reps=100, n=1000, seed=77):
    """원시 평균에서 시작해 맞추는 기준을 하나씩 더할 때 추정이 얼마나 움직이나 (설명 가능성)."""
    sc = dict(age_response=True, mA=ars["k"], mB=1.3, recall=0); rng = np.random.default_rng(seed)
    steps = [("원시 평균", None), ("+ 연령", ("age",)), ("+ 성별", ("age", "sex")), ("+ 권역", ("age", "sex", "region")),
             ("+ 지난 투표 (권역×지난 투표)", "past")]
    acc = np.zeros(len(steps))
    for _ in range(reps):
        S = world.sample(sc, n, rng)
        for j, (name, m) in enumerate(steps):
            if m is None: acc[j] += S.y.mean()
            elif m == "past": acc[j] += M.rake(S, world, past=True)["est"]
            else: acc[j] += M.rake(S, world, past=False, margins=m)["est"]
    acc /= reps
    return {"scenario": "S4", "truth": float(world.truth),
            "steps": [{"step": steps[j][0], "est": float(acc[j]), "delta_pp": float((acc[j] - (acc[j - 1] if j else acc[j])) * 100),
                       "err_pp": float((acc[j] - world.truth) * 100)} for j in range(len(steps))]}


def published_table_demo(world, ars, n=1000, seed=303):
    """공개 결과표 점검: 결과표의 '지난 투표별 지지율'만으로 정답지(실제 지난 선거 결과)에 맞춰 다시 더하기."""
    sc = dict(age_response=True, mA=ars["k"], mB=1.3, recall=0); rng = np.random.default_rng(seed)
    S = world.sample(sc, n, rng)
    names = ["A계열", "B계열", "투표 안 함"]
    groups = []
    for v in range(3):
        m = S.past == v; groups.append({"group": names[v], "n": int(m.sum()), "support": float(S.y[m].mean())})
    target = np.bincount(world.past, minlength=3) / world.N
    reweighted = float(sum(target[v] * groups[v]["support"] for v in range(3)))
    return {"scenario": "S4", "table": groups, "raw": float(S.y.mean()), "target_shares": target.tolist(),
            "reweighted": reweighted, "truth": float(world.truth),
            "note": "공개 결과표에 흔히 실리는 '지난 대선 투표별' 교차표만 있으면 계산 가능. 실제 표에는 정답지로 선관위 결과를 씀"}


def run_all(cfg, out_dir, reps=None, log=print):
    t0 = time.time(); log("가상 세계 만들기…"); world = World(cfg)
    log(f"  유권자 {world.N:,}명, 참값 A 지지율 {world.truth:.4f}")
    log("ARS형 강성 배율 맞추기…"); ars = calibrate_ars(world, cfg); log(f"  k = {ars['k']}")
    real = realism(world, cfg, ars)
    log("보정법 비교…"); bench = benchmark(world, cfg, ars, reps=reps, log=log)
    log("기여 분해…"); deco = decomposition(world, ars)
    log("선거 단위 교차검증…"); bt = {}
    b = cfg["backtest"]; house = np.array(b["house_effects_pp"]) / 100
    def avg_bt(K, sd, reps=200):
        rs = [backtest(5000 + i, K, b["bias_mean_pp"] / 100, sd / 100, house) for i in range(reps)]
        return {"mae_before": float(np.mean([x["mae_before"] for x in rs])), "mae_after": float(np.mean([x["mae_after"] for x in rs])),
                "share_worse": float(np.mean([x["mae_after"] > x["mae_before"] for x in rs])), "reps": reps,
                "example": rs[0]}
    for K in (3, 6, 12):
        bt[str(K)] = avg_bt(K, b["bias_sd_pp"])
    sens = {str(sd): avg_bt(6, sd) for sd in (0.5, 1.5, 3.0)}
    demo = published_table_demo(world, ars)
    result = {"version": "pollcal 0.1", "environment": environment(), "config": cfg, "realism": real, "benchmark": bench,
              "decomposition": deco, "backtest": {"by_K": bt, "by_bias_sd": sens}, "published_table_demo": demo,
              "elapsed_sec": round(time.time() - t0, 1)}
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "results.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    write_tables(result, out_dir)
    log(f"끝. {result['elapsed_sec']}초")
    return result


def write_tables(r, out_dir):
    import csv
    with open(os.path.join(out_dir, "benchmark.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["scenario", "scenario_name", "method", "label", "bias_pp", "rmse_pp", "mae_pp",
                                       "coverage", "ci_width_pp", "n_eff", "sec_mean"])
        for sid, b in r["benchmark"].items():
            for k, m in b["methods"].items():
                w.writerow([sid, b["scenario"]["name"], k, m["label"], round(m["bias_pp"], 3), round(m["rmse_pp"], 3),
                            round(m["mae_pp"], 3), "" if m["coverage"] is None else round(m["coverage"], 3),
                            "" if m["ci_width_pp"] is None else round(m["ci_width_pp"], 2),
                            "" if m["n_eff"] is None else round(m["n_eff"], 1), round(m["sec_mean"], 4)])
