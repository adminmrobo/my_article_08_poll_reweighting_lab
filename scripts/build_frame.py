"""
임시 사후층화 표 v0: 가상 한국인(Nemotron-Personas-Korea) 집계표 + 2025 대선 지난 투표 층

입력
  - 감사 저장소의 이변량 집계표 (원자료 100만 행에서 나온 칸별 인원)
  - region_2025.py: 시도별 득표·투표율 (최종 개표 + 출구조사 보충, 출처 표시)
  - kep_exitpoll_2025_age_sex.csv: 연령대×성별 출구조사
출력 (out/)
  - frame_v0_age_sex_prov_edu.csv : 연령6×성2×시도17×학력4 인원 (합 = 1)
  - frame_v0_with_pastvote.csv    : 연령6×성2×시도17×지난투표5 비율 (이재명·김문수·이준석·기타·기권)
  - frame_v0_checks.json          : 맞춤 오차와 가정 목록
"""
import csv, json, sys
from pathlib import Path
import numpy as np

REPO = Path(sys.argv[1])
TAB = REPO / "data/processed/bivariate_detail_all"
HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "data"; OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(HERE))
from region_2025 import table as region_table

def read(name):
    r = list(csv.reader(open(TAB / name, encoding="utf-8")))
    cols = r[0][1:]; idx = [x[0] for x in r[1:]]
    return idx, cols, np.array([[float(v) for v in x[1:]] for x in r[1:]])

AGE8 = ["19-24","25-34","35-44","45-54","55-64","65-74","75-84","85+"]
EDU7 = ["무학","초등학교","중학교","고등학교","2~3년제 전문대학","4년제 대학교","대학원"]
EDU4 = ["중졸 이하","고졸","전문대졸","대졸 이상"]; EDU_MAP = [0,0,0,1,2,3,3]

def ordered(idx, cols, M, rows, cs):
    return M[[idx.index(r) for r in rows]][:, [cols.index(c) for c in cs]]

i, c, AP = read("contingency_age_bin__x__province.csv"); PROV = c
AP = ordered(i, c, AP, AGE8, PROV)
i, c, AS = read("contingency_age_bin__x__sex.csv"); SEX = c; AS = ordered(i, c, AS, AGE8, SEX)
i, c, SP = read("contingency_sex__x__province.csv"); SP = ordered(i, c, SP, SEX, PROV)
i, c, AE = read("contingency_age_bin__x__education_level.csv"); AE = ordered(i, c, AE, AGE8, EDU7)
i, c, SE = read("contingency_sex__x__education_level.csv"); SE = ordered(i, c, SE, SEX, EDU7)
i, c, EP = read("contingency_education_level__x__province.csv"); EP = ordered(i, c, EP, EDU7, PROV).T
N = AP.sum()

# 1) 4차원 표 (연령8 × 성2 × 시도17 × 학력7) 를 2차원 표 6개에 맞춤 (IPF)
#    3차 이상 상호작용은 원자료에 있어도 여기서는 복원되지 않음 → 원자료 표로 교체할 것
T = np.ones((8, 2, 17, 7)); T *= N / T.sum()
for it in range(200):
    T *= (AS / T.sum((2, 3)))[:, :, None, None]
    T *= (AP / T.sum((1, 3)))[:, None, :, None]
    T *= (SP / T.sum((0, 3)))[None, :, :, None]
    T *= (AE / T.sum((1, 2)))[:, None, None, :]
    T *= (SE / T.sum((0, 2)))[None, :, None, :]
    T *= (EP / T.sum((0, 1)))[None, None, :, :]
fit_err = max(np.abs(T.sum((2,3))-AS).max(), np.abs(T.sum((1,3))-AP).max(), np.abs(T.sum((0,1))-EP).max()) / N

# 2) 연령 8구간 → 여론조사·출구조사 10세 구간 (구간 안 나이는 고르게 분포한다고 가정)
AGE6 = ["19-29","30-39","40-49","50-59","60-69","70+"]
# 각 8구간이 6구간에 나눠 들어가는 비율 (19-24: 6개 나이 전부 20대, 25-34: 25-29 반 / 30-34 반 …)
W = np.zeros((8, 6))
W[0,0]=1; W[1,0]=.5; W[1,1]=.5; W[2,1]=.5; W[2,2]=.5; W[3,2]=.5; W[3,3]=.5
W[4,3]=.5; W[4,4]=.5; W[5,4]=.5; W[5,5]=.5; W[6,5]=1; W[7,5]=1
T6 = np.einsum("asxe,ab->bsxe", T, W)
E4 = np.zeros((6, 2, 17, 4))
for e7, e4 in enumerate(EDU_MAP): E4[..., e4] += T6[..., e7]
F = E4 / E4.sum()

with open(OUT / "frame_v0_age_sex_prov_edu.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f); w.writerow(["age_grp","sex","province","edu4","share"])
    for a in range(6):
        for s in range(2):
            for p in range(17):
                for e in range(4): w.writerow([AGE6[a], SEX[s], PROV[p], EDU4[e], f"{F[a,s,p,e]:.8f}"])

# 3) 지난 투표 층: 칸(연령6×성2×시도17) × 투표 5범주 를 두 기준에 동시에 맞춤
#    기준 A: 시도별 득표 × 시도 투표율 (기권 = 1 − 투표율)
#    기준 B: 연령×성별 출구조사 득표 × 전국 투표율 (연령·성별 투표율 차이는 모름 → 가정)
V = ["이재명","김문수","이준석","기타","기권"]
F3 = F.sum(3)                                  # 6×2×17
reg = {r["prov"]: r for r in region_table()}
TA = np.zeros((17, 5))
for p, name in enumerate(PROV):
    r = reg[name]; t = r["turnout"] / 100
    shares = np.array([r["lee_jm"], r["kim_ms"], r["lee_js"], r["other"]]) / 100
    TA[p, :4] = F3[:, :, p].sum() * t * shares / shares.sum(); TA[p, 4] = F3[:, :, p].sum() * (1 - t)
turn_nat = TA[:, :4].sum() / TA.sum()
ex = {(row["age_grp"], row["sex"]): row for row in csv.DictReader(open(HERE.parent / "data/kep_exitpoll_2025_age_sex.csv", encoding="utf-8"))}
EXA = ["20대","30대","40대","50대","60대","70대 이상"]; SEXK = {SEX[0]: None, SEX[1]: None}
sex_label = {s: ("남" if ("남" in s) else "여") for s in SEX}
TB = np.zeros((6, 2, 5))
for a in range(6):
    for s in range(2):
        row = ex[(EXA[a], sex_label[SEX[s]])]
        sh = np.array([float(row["lee_jm"]), float(row["kim_ms"]), float(row["lee_js"])]) / 100
        sh = np.append(sh, max(0.0, 1 - sh.sum()))
        tot = F3[a, s].sum()
        TB[a, s, :4] = tot * turn_nat * sh / sh.sum(); TB[a, s, 4] = tot * (1 - turn_nat)
# 출구조사는 표본 추정치라 시도별 합계와 정확히 맞지 않음 → 투표 범주 전국 합계를 기준 A에 맞춰 조정
TB[:, :, :4] *= (TA[:, :4].sum(0) / TB[:, :, :4].sum((0, 1)))[None, None, :]
TB *= (F3.sum((2,)) / TB.sum(2))[:, :, None]
G = np.repeat(F3[:, :, :, None], 5, axis=3) / 5
for it in range(500):
    G *= (F3 / G.sum(3))[..., None]
    G *= (TA / G.sum((0, 1)))[None, None, :, :]
    G *= (TB / G.sum(2))[:, :, None, :]
errA = np.abs(G.sum((0,1)) - TA).max(); errB = np.abs(G.sum(2) - TB).max(); errF = np.abs(G.sum(3) - F3).max()

with open(OUT / "frame_v0_with_pastvote.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f); w.writerow(["age_grp","sex","province","pastvote","share"])
    for a in range(6):
        for s in range(2):
            for p in range(17):
                for v in range(5): w.writerow([AGE6[a], SEX[s], PROV[p], V[v], f"{G[a,s,p,v]:.8f}"])

# 4) 검증: 전국 결과 재현, 출구조사와의 차이(조정 전)
voters = G[..., :4].sum()
nat = {V[v]: round(G[..., v].sum() / voters * 100, 2) for v in range(4)}
raw_nat_exit = {}
cells = []
for a in range(6):
    for s in range(2):
        g = G[a, s]; vv = g[:, :4].sum()
        row = ex[(EXA[a], sex_label[SEX[s]])]
        cells.append({"age": AGE6[a], "sex": SEX[s], "frame_lee_jm": round(g[:, 0].sum()/vv*100, 1), "exit_lee_jm": float(row["lee_jm"]),
                      "frame_kim_ms": round(g[:, 1].sum()/vv*100, 1), "exit_kim_ms": float(row["kim_ms"]),
                      "frame_lee_js": round(g[:, 2].sum()/vv*100, 1), "exit_lee_js": float(row["lee_js"])})
checks = {
  "version": "v0 (임시)", "frame_rows_source": "감사 저장소 이변량 집계표 6개 → IPF 4차원 복원",
  "ipf_fit_max_rel_err": float(fit_err), "pastvote_fit_abs_err": {"시도기준": float(errA), "연령성별기준": float(errB), "칸합": float(errF)},
  "national_shares_reproduced": nat, "national_official": {"이재명": 49.42, "김문수": 41.15, "이준석": 8.34, "기타": 1.08},
  "national_turnout_frame": round(float(turn_nat) * 100, 2), "national_turnout_official": 79.4,
  "age_sex_vs_exitpoll": cells,
  "region_sources": {r["prov"]: r["src"] for r in region_table()},
  "assumptions": [
    "4차원 결합은 2차원 표 6개만 맞춘 근사 — 원자료로 만든 표(make_poststrat_frame.py)로 교체하면 3차 상호작용까지 반영됨",
    "연령 8구간 → 10세 구간 변환은 구간 안 나이가 고르게 분포한다고 가정",
    "19세 이상만 포함 (18세 없음)",
    "시도별 득표: 최종 개표(0.1%p 반올림, 이재명·김문수 모두 확인 12개 시도) + 일부 출구조사 보충, 이준석은 나머지로 계산, 투표율 7개 시도는 전국값 대체",
    "연령·성별 투표율 차이를 모름 → 모든 연령·성별에 같은 투표율 가정 (출구조사 득표만 반영)",
    "출구조사 연령·성별 득표는 시도 합계와 맞도록 비례 조정됨",
  ],
}
(OUT / "frame_v0_checks.json").write_text(json.dumps(checks, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: checks[k] for k in ["ipf_fit_max_rel_err","pastvote_fit_abs_err","national_shares_reproduced","national_turnout_frame"]}, ensure_ascii=False, indent=1))
for c_ in cells: print(c_)
