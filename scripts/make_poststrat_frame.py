"""
Nemotron-Personas-Korea → 여론조사 사후층화 표 (연령 × 성별 × 시도 × 학력)

사용법 (내 PC에서):
  1) 감사 저장소를 받아 데이터 내려받기
       git clone https://github.com/eopchang/nemotron-personas-korea-audit
       cd nemotron-personas-korea-audit
       pip install huggingface_hub polars pyarrow
       python scripts/01_download.py          # 약 2GB, data/raw/ 에 저장
  2) 이 파일을 저장소 맨 위 폴더에 두고 실행
       python make_poststrat_frame.py
  3) 만들어진 poststrat_frame/ 폴더(작은 CSV 3개 + JSON 1개)를 대화에 첨부

만드는 것:
  frame_age_sex_prov_edu.csv  연령 6 × 성별 2 × 시도 17 × 학력 4 = 최대 816칸, 칸별 인원(합 100만)
  frame_age_sex_prov.csv      학력을 뺀 408칸 (여론조사 공개 교차표 단위)
  frame_age_sex_edu.csv       시도를 뺀 48칸 (공식 교차표와 대조용)
  frame_meta.json             행 수, 범주 목록, 빈 칸 수, 주의 사항
"""
from __future__ import annotations

import json
from pathlib import Path

import polars as pl

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "poststrat_frame"
OUT.mkdir(exist_ok=True)

# 여론조사 공표 관행에 가까운 연령 구간 (데이터는 19세 이상이라 18세가 없음)
AGE_BREAKS = [30, 40, 50, 60, 70]
AGE_LABELS = ["19-29", "30-39", "40-49", "50-59", "60-69", "70+"]

EDU_MAP = {
    "무학": "중졸 이하", "초등학교": "중졸 이하", "중학교": "중졸 이하",
    "고등학교": "고졸",
    "2~3년제 전문대학": "전문대졸",
    "4년제 대학교": "대졸 이상", "대학원": "대졸 이상",
}
# 데이터의 시도 약칭 → 선관위·통계청 표기 (선거 결과와 붙일 때 씀)
PROV_FULL = {
    "서울": "서울특별시", "부산": "부산광역시", "대구": "대구광역시", "인천": "인천광역시",
    "광주": "광주광역시", "대전": "대전광역시", "울산": "울산광역시", "세종": "세종특별자치시",
    "경기": "경기도", "강원": "강원특별자치도", "충청북": "충청북도", "충청남": "충청남도",
    "전북": "전북특별자치도", "전라남": "전라남도", "경상북": "경상북도", "경상남": "경상남도",
    "제주": "제주특별자치도",
}


def main() -> None:
    files = sorted(RAW.rglob("*.parquet"))
    if not files:
        raise SystemExit("data/raw 에 parquet 파일이 없습니다. scripts/01_download.py 를 먼저 실행하세요.")
    df = pl.read_parquet([str(f) for f in files], columns=["age", "sex", "province", "education_level"])
    n_rows = df.height

    unknown_edu = sorted(set(df["education_level"].unique().to_list()) - set(EDU_MAP))
    unknown_prov = sorted(set(df["province"].unique().to_list()) - set(PROV_FULL))

    df = df.with_columns(
        pl.col("age").cut(breaks=AGE_BREAKS, labels=AGE_LABELS, left_closed=True).cast(pl.String).alias("age_grp"),
        pl.col("education_level").replace_strict(EDU_MAP, default="(미분류)").alias("edu4"),
        pl.col("province").replace_strict(PROV_FULL, default=pl.col("province")).alias("province_full"),
    )

    def save(keys: list[str], name: str) -> pl.DataFrame:
        t = (df.group_by(keys).agg(pl.len().alias("n")).sort(keys)
               .with_columns((pl.col("n") / n_rows).alias("share")))
        t.write_csv(OUT / name, include_bom=True)
        return t

    t4 = save(["age_grp", "sex", "province_full", "edu4"], "frame_age_sex_prov_edu.csv")
    save(["age_grp", "sex", "province_full"], "frame_age_sex_prov.csv")
    save(["age_grp", "sex", "edu4"], "frame_age_sex_edu.csv")

    possible = len(AGE_LABELS) * df["sex"].n_unique() * df["province_full"].n_unique() * 4
    meta = {
        "source": "nvidia/Nemotron-Personas-Korea (CC BY 4.0)",
        "rows": n_rows,
        "age_groups": AGE_LABELS,
        "sex": sorted(df["sex"].unique().to_list()),
        "edu4": ["중졸 이하", "고졸", "전문대졸", "대졸 이상"],
        "cells_possible": possible,
        "cells_nonempty": t4.height,
        "cells_under_30_rows": int((t4["n"] < 30).sum()),
        "unknown_education_values": unknown_edu,
        "unknown_province_values": unknown_prov,
        "caveats": [
            "데이터는 19세 이상만 포함 — 선거권이 있는 18세는 별도로 더해야 함",
            "합성 데이터의 칸 인원은 공식 통계의 근사치 — 연령·성·시도 칸은 공식 주민등록 인구로 다시 맞출 것",
            "감사 결과: 지역(시도)과 사람 속성의 결합은 약하게만 모델링됨 — 시도 × 학력 칸은 공식 교차표로 확인 필요",
            "정치 성향·투표 이력 변수는 없음",
        ],
    }
    (OUT / "frame_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False, indent=2))
    print(f"→ {OUT} 에 저장했습니다.")


if __name__ == "__main__":
    main()
