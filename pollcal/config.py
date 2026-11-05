"""가상 세계와 실험 설정 — 모든 값이 이 파일 하나에 있다 (심사 의견: 합성 데이터 생성 절차 공개).

각 값에는 근거(anchor)를 단다.
  data   : 공개 자료에 맞춘 값 (출처는 sources 키)
  calib  : 공개 자료의 크기에 맞춰 프로그램이 계산해 정하는 값
  assume : 공개 자료로 확인할 수 없는 가정 → 결과가 이 값에 얼마나 민감한지 시나리오로 보여 준다
"""
import copy, json
from pathlib import Path

AGES = ["19-29", "30-39", "40-49", "50-59", "60-69", "70+"]
SEXES = ["남", "여"]
REGIONS = ["수도권", "영남", "호남", "충청·강원·제주"]
# 사후층화 표 v0 의 시도 약칭 → 4권역
REGION_OF = {"서울": 0, "경기": 0, "인천": 0, "부산": 1, "대구": 1, "울산": 1, "경상북": 1, "경상남": 1,
             "광주": 2, "전북": 2, "전라남": 2, "대전": 3, "세종": 3, "충청북": 3, "충청남": 3, "강원": 3, "제주": 3}

DEFAULT = {
    "seed": 20251029,
    "population_size": 200000,
    "composition": {"value": "data/frame_v0_age_sex_prov_edu.csv", "anchor": "data",
                    "note": "연령6×성별2×권역4 인구 비율 = 사후층화 표 v0 (가상 한국인 100만 명 집계, 감사 결과 시도·연령은 공식 통계와 근접)"},
    "vote_structure": {"anchor": "data",
                       "note": "가상 후보 A의 칸별 지지율 p_c를 logit(p)=α[연령,성별]+β[권역]로 두고, 2025 대선 연령·성별 출구조사와 권역별 득표(이재명 득표를 A로 본뜸)에 맞춰 계산. 실제 후보와 무관한 가상 세계"},
    "cell_deviation_sd": {"value": 0.3, "anchor": "assume",
                          "note": "칸(연령×성별×권역)마다 주효과로 설명되지 않는 지지율 차이 (logit 척도 표준편차). 부분 풀링(④)이 다루는 몫"},
    "strong_share": {"value": 0.5, "anchor": "assume",
                     "note": "칸마다 강성층(강성 A + 강성 B) 비율. 강성층 안에서 A·B는 칸 지지율 비례로 나뉨"},
    "strong_loyalty": {"value": 0.95, "anchor": "assume", "note": "강성 A층이 A를 지지할 확률 (강성 B층은 1−이 값)"},
    "past_vote": {"anchor": "assume", "value": {"strongA": [0.82, 0.06, 0.12], "strongB": [0.06, 0.82, 0.12],
                                                 "middle_if_A": [0.45, 0.27, 0.28], "middle_if_B": [0.27, 0.45, 0.28]},
                  "note": "지난 선거 [A계열, B계열, 투표 안 함] 확률. 지난 선거 결과 표(정답지)는 이 세계 안에서 계산됨"},
    "age_response": {"value": [0.6, 0.75, 0.95, 1.15, 1.35, 1.5], "anchor": "assume",
                     "note": "연령별 상대 응답 확률. 고령층이 더 잘 답한다는 국내 보고의 방향만 반영 (크기는 가정)"},
    "phone_like": {"value": {"mA": 1.3, "mB": 1.3}, "anchor": "assume", "note": "응답률이 비교적 높은 전화면접형 조사의 강성층 응답 배율"},
    "ars_gap_target_pp": {"value": 9.9, "anchor": "data",
                          "note": "같은 주 ARS(응답률 2.2%)와 전화면접(14.2%)의 두 큰 정당 격차 차이 10.9−1.0 (문화일보 2023-10-23 보도). 크기의 단서로만 씀 — 정당 지지 문항이고 조사 두 건뿐"},
    "sample_size": 1000,
    "reps": 100,
    "bootstrap_B": 50,
    "scenarios": [
        {"id": "S1", "name": "무작위 응답", "age_response": False, "mA": 1.0, "mB": 1.0, "recall": 0.0,
         "note": "누구나 같은 확률로 답함 — 모든 방법이 맞아야 하는 기준선"},
        {"id": "S2", "name": "나이 치우침만", "age_response": True, "mA": 1.0, "mB": 1.0, "recall": 0.0,
         "note": "고령층만 더 잘 답함 — 인구통계 가중으로 고쳐지는 세계"},
        {"id": "S3", "name": "양쪽 강성층 과다", "age_response": True, "mA": 2.0, "mB": 2.0, "recall": 0.0,
         "note": "강성층이 양쪽 모두 2배로 답함"},
        {"id": "S4", "name": "A쪽 강성층 과다 (ARS형)", "age_response": True, "mA": "calib", "mB": 1.3, "recall": 0.0,
         "note": "A쪽 강성 배율을 ARS·전화면접 격차 차이(9.9%p)에 맞춰 계산"},
        {"id": "S5", "name": "B쪽 강성층 과다 (ARS형 반대)", "age_response": True, "mA": 1.3, "mB": "calib", "recall": 0.0,
         "note": "S4와 방향만 반대"},
        {"id": "S6", "name": "ARS형 + 기억 착오", "age_response": True, "mA": "calib", "mB": 1.3, "recall": 0.3,
         "note": "S4에 더해, 지난번 B계열을 찍은 중도층 30%가 A계열이라고 답함"},
        {"id": "S7", "name": "B쪽 과다 + 기억 착오", "age_response": True, "mA": 1.3, "mB": "calib", "recall": 0.3,
         "note": "S5에 같은 기억 착오를 더함 — 착오가 치우침과 같은 방향일 때"},
    ],
    "backtest": {"elections": 6, "bias_mean_pp": 2.0, "bias_sd_pp": 1.5, "house_effects_pp": [2.0, -1.0, 0.5, -1.5],
                 "anchor": "assume", "note": "⑤ 여러 조사 합치기·선거 단위 교차검증용 가상 선거들"},
    "sources": {
        "frame_v0": "사후층화 표 v0 (이 저장소 data/)",
        "exitpoll": "방송3사 출구조사 연령·성별 (머니투데이 2025-06-03)",
        "region": "시도별 득표 (노컷뉴스 2025-06-04 외, scripts/region_2025.py 출처 표시)",
        "ars_gap": "문화일보 2023-10-23 「조사협회 “ARS는 비과학적”」",
    },
}


def load(path=None):
    cfg = copy.deepcopy(DEFAULT)
    if path:
        user = json.loads(Path(path).read_text(encoding="utf-8"))
        cfg.update(user)
    return cfg
