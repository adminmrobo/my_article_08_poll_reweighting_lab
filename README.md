# 여론조사 보정 연구실 (특별편 X1)

강성 지지층이 더 많이 답하는 여론조사로 유권자 전체의 생각을 추정하는 방법을 다루는 저장소입니다.
글 · 안상선 ((주)M-Robo 대표) · AI 보조 제작

| 파일 | 내용 |
|---|---|
| `index.html` | 첫 화면 (GitHub Pages) |
| `X1_poll_reweighting.html` | 해설 페이지 v2 — 보정법 다섯 단계 + 배경 문헌 + 가상 세계 설정·현실성 점검 + 프로그램 비교 결과 + 공표 점검표 (단일 HTML) |
| `pollcal/` | 보정법 비교 프로그램 (Python). `python -m pollcal run` |
| `results/results.json`, `results/benchmark.csv` | 프로그램 실행 결과 (7 시나리오 × 100번 × 방법 7). 해설 페이지가 이 파일을 그대로 싣는다 |
| `frame_v0.html` | 사후층화 표 v0 결과 페이지 (임시판) |
| `data/frame_v0_with_pastvote.csv` | 연령 6 × 성별 2 × 시도 17 × 2025 대선 지난 투표 5 = 1,020칸 |
| `data/frame_v0_age_sex_prov_edu.csv` | 연령 6 × 성별 2 × 시도 17 × 학력 4 = 816칸 |
| `data/frame_v0_checks.json` | 맞춤 오차, 전국 재현값, 출구조사 대비, 시도별 출처 표시, 가정 |
| `data/kep_exitpoll_2025_age_sex.csv` | 방송3사 출구조사 연령·성별 득표 (보도 기준) |
| `scripts/build_frame.py` | 사후층화 표 만들기 |
| `scripts/region_2025.py` | 시도별 득표·투표율 (출처 표시 포함, 선관위 원본으로 교체 예정) |
| `scripts/make_poststrat_frame.py` | 가상 한국인 원자료에서 정확한 표 만들기 (PC에서 실행) |
| `scripts/make_frame_page.py`, `scripts/frame_page_template.html` | `frame_v0.html` 다시 만들기 |
| `docs/IMG_X1_poll_reweighting.md` | 해설 페이지 이미지 제작 명세서 |
| `docs/KG_00_registry_X1_additions.json` | 지식 그래프 등록부 추가분 |

## 보정법 비교 프로그램 (pollcal)

```bash
pip install -r requirements.txt
python -m pollcal run --out results          # 전체 비교, 약 2분
python -m pollcal quick --out results_quick  # 반복 10회 점검
```

- 설정은 `pollcal/config.py` 한 곳에 있고, 값마다 근거(자료 / 맞춤 / 가정)를 표시했다.
- 비교하는 방법: 원시 평균, 사후층화, 레이킹(지난 투표), MRP(라플라스 근사 베이지안), XGBoost·LightGBM + 사후층화, 원래 working paper의 3단계 가중식(기준선).
- 평가: 참값 대비 평균 오차·평균 제곱근 오차, 95% 구간 포함률, 유효 표본, 계산 시간(실행 환경 기록), 기여 분해, 선거 단위 교차검증, 공개 결과표 점검 예시.

## 사후층화 표 다시 만들기

```bash
git clone https://github.com/eopchang/nemotron-personas-korea-audit   # 변수 쌍별 집계표 사용
pip install numpy
python scripts/build_frame.py ../nemotron-personas-korea-audit
python scripts/make_frame_page.py
```

## 주의

- `frame_v0`은 임시판입니다. 가상 한국인 결합 분포는 변수 쌍별 집계표 6개로 근사했고, 시도별 득표 일부는 출구조사로 보충했습니다. 각 값의 출처는 `frame_v0.html`과 `data/frame_v0_checks.json`에 표시되어 있습니다.
- 가상 한국인 데이터에는 정치 성향 변수가 없습니다. 지난 투표 층은 시도별 득표와 출구조사로 추정한 값입니다.
- 이 표로 만든 수치를 실제 여론조사 결과처럼 공표하지 마세요.

## 출처와 라이선스

- NVIDIA, Nemotron-Personas-Korea (CC BY 4.0)
- Kim, Chang-Eop (2026), nemotron-personas-korea-audit (보고서·집계 CC BY 4.0)
- 캐릭터 그림: adminmrobo/fruitfly-lab-expressions (ea5da3f)
- 선거 수치: 노컷뉴스·디지털타임스·머니투데이·한국경제 보도 (2025-06), 원본은 중앙선거관리위원회
