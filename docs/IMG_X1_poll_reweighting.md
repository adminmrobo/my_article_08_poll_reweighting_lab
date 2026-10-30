# X1번 「목소리 큰 응답자, 조용한 유권자 — 여론조사 보정의 사다리」 이미지 제작 명세서

| 항목 | 내용 |
|---|---|
| 페이지 | X1_poll_reweighting.html |
| 모드 / 주 앵커 | 교과서 / B 연구실: 밤의 연구실 전경 (시료 선반, 봉인된 봉투 상자) |
| 시즌 | 기본 |
| 대결 | 3,000명 원시 평균 대 1,000명 + 지난 투표 가중 → 결과 F, 평균 절대 오차 2.32%p 대 8.10%p (차이 5.8%p) |
| 새로 그릴 그림 | P1 2장 · P2 3장 · P3 1장 |
| 제작 경로 | 직접 3장 (sc_x1_outro 합성본은 페이지 안, thumb_x1·og_x1은 파일) · 외부 의뢰 3장 (bg_x1, sc_x1_hero, doc_scale) |
| 의뢰 도구 | Genspark (기본) |
| 진행 | 받음 0 / 의뢰 3 · 마지막 반영 아직 |
| 캐릭터 팩 표정 | 96px 27장 + 192px 9장 (팩 커밋 ea5da3f) |
| 재사용 | 0장 (시리즈 기존 장면 목록을 받지 못함) |
| 그림이 없을 때 | 페이지는 캐릭터 팩 표정과 CSS 배경으로 이미 완성 상태 |

## 1. 그림체와 고정 외형
- 스타일: SKILL 18-3 (16비트 SNES 시대 픽셀 아트, 굵은 외곽선, 디더링 음영)
- 캐릭터 고정 외형: SKILL 18-4 표 그대로 (공식 저장소 `CHARACTER_CORE_EN`)
- 이 페이지 장소: 밤의 연구실 전경. 원심분리로 층이 갈라진 시료가 든 시험관 선반, 봉인된 봉투 상자(지난 선거 = 정답지), 실험 노트 더미, 글자 없는 칠판, 작은 서버 랙
- 장소 영어 묘사: *wide night laboratory with test tube racks holding layered two-tone samples, a box of sealed envelopes, stacks of lab notebooks, a blank chalkboard, a small server rack*
- 정치 중립: 정당을 떠올리게 하는 색 조합(파랑 대 빨강)을 소품의 짝으로 쓰지 않는다. 시료의 두 층은 민트와 구리색으로.

## 2. 필요한 그림 전체

| # | 키 | 판 | 크기 | 상태 | 제작 | 우선 | 들어가는 곳 | 대신 쓰는 그림 |
|---|---|---|---|---|---|---|---|---|
| 1 | bg_x1 | F | 1920×720 | 의뢰 | 외부 | P1 | 히어로 배경 | CSS 그라데이션 + 벌집 무늬 |
| 2 | sc_x1_hero | E | 1200×800 | 의뢰 | 외부 | P1 | 히어로 무대 | 팩 캐릭터 4명 CSS 무대 합성 |
| 3 | sc_x1_outro | E | 1200×800 | 넣음 (합성본) | 직접 → 외부 선택 | P2 | 아웃트로 | 팩 캐릭터 CSS 무대 합성 (초파리 앞·크게) |
| 4 | thumb_x1 | I | 600×400 | 넣음 (파일) | 직접 (CSS 배경 + 팩 2명) | P2 | 목차 카드 | 색 카드 |
| 5 | og_x1 | K | 1200×630 | 넣음 (파일) | 직접 (CSS 배경 + 팩 3명 + 제목) | P3 | 공유 미리보기 | 없음 |
| 6 | doc_scale → doc_e13 | A | 팩 96 | 팩 (저울 그림 없음) | 외부 (선택) | P2 | 대결 무승부 판정 (이번 결과에서는 안 쓰임) | doc_e13 |
| 7 | doc_think → doc_e09 | A | 팩 96 | 팩 | — | — | 히어로 대화창·무대 | — |
| 8 | doc_front → doc_e08 | A | 팩 96 | 팩 | — | — | 등장인물 카드 | — |
| 9 | doc_board → doc_e07 | A | 팩 96 | 팩 | — | — | 큰 그림 말풍선 | — |
| 10 | doc_magic → doc_e16 | A | 팩 96 | 팩 | — | — | ③ 말풍선, 아웃트로 | — |
| 11 | doc_judge → doc_e10 | A | 팩 96 | 팩 | — | — | 대결 판정, 정리 말풍선 | — |
| 12 | asst_smile → asst_e13 | B | 팩 96 | 팩 | — | — | 히어로, 등장인물, 무승부 | — |
| 13 | asst_e07 | B | 팩 96 | 팩 | — | — | ② 숫자 발표 | — |
| 14 | asst_e10 | B | 팩 96 | 팩 | — | — | 꾸러미 섹션 | — |
| 15 | asst_firm → asst_e12 | B | 팩 96 | 팩 | — | — | 대결 결과 전 | — |
| 16 | asst_spark → asst_e01 | B | 팩 96 | 팩 | — | — | 대결 결과 후, 아웃트로 | — |
| 17 | asst_shock → asst_e24 | B | 팩 96 | 팩 | — | — | 대결 실격 (이번 결과에서는 안 쓰임) | — |
| 18 | fly_clip → fly_e10 | C | 팩 96 | 팩 | — | — | 등장인물 카드 | — |
| 19 | fly_magnify → fly_e07 | C | 팩 96 | 팩 | — | — | ① 말풍선 | — |
| 20 | fly_type → fly_e09 | C | 팩 96 | 팩 | — | — | ⑤ 말풍선 | — |
| 21 | fly_point → fly_e08 | C | 팩 96·192 | 팩 | — | — | 히어로, 대결 전 (`data-face="right"`) | — |
| 22 | fly_arms → fly_e16 | C | 팩 96·192 | 팩 | — | — | 대결 후 (F), 아웃트로 | — |
| 23 | fly_coffee → fly_e13 | C | 팩 192 | 팩 | — | — | 대결 후 (R 소차·D) | — |
| 24 | fly_cry → fly_e21 | C | 팩 192 | 팩 | — | — | 대결 후 (R 10%p 이상) | — |
| 25 | robo_smile → robo_e13 | D | 팩 96 | 팩 | — | — | 등장인물 카드 | — |
| 26 | robo_chart → robo_e07 | D | 팩 96 | 팩 | — | — | "왜" 말풍선 | — |
| 27 | robo_calc → robo_e09 | D | 팩 96 | 팩 | — | — | ④ 말풍선 | — |
| 28 | robo_coin → robo_e16 | D | 팩 96·192 | 팩 | — | — | 히어로, 대결 전 (`data-face="left"`) | — |
| 29 | robo_sigh → robo_e20 | D | 팩 192 | 팩 | — | — | 대결 후 (F) | — |
| 30 | robo_happy → robo_e12 | D | 팩 192 | 팩 | — | — | 대결 후 (R) | — |
| 31 | robo_meh → robo_e18 | D | 팩 192 | 팩 | — | — | 대결 후 (D) | — |
| 32 | robo_blush → robo_e14 | D | 팩 96·192 | 팩 | — | — | 대결 후 (X), 아웃트로 | — |
| — | 행동으로 보기 5개, NPC | — | — | 코드 | 직접 | — | 캔버스 점·시험관·막대 | — |

컷(G판)은 넣지 않았다. 다섯 칸 모두 캔버스 도식이 개념을 보여 주므로 R5 조건("개념을 장면으로 보여 줄 때만")에 해당하는 칸이 없다.

## 3. 새로 그릴 그림 상세

### 3-1. `bg_x1` — 층이 갈라진 시료와 봉인된 정답지가 있는 밤의 연구실
| 항목 | 내용 |
|---|---|
| 판 · 크기 | F · 1920×720 (정수배 가능) |
| 제작 경로 | 외부: Genspark |
| 배경 | 그림 전체 |
| 구도 | 왼쪽 45%는 어두운 벽과 빈 칠판만(제목 자리). 오른쪽에 시험관 선반(두 층으로 갈라진 시료, 위층에 피펫이 꽂혀 있음), 그 옆 책상 위 봉인된 봉투 상자에 조명이 모인다 |
| 표정·몸짓 | 인물 없음 |
| 소품 | 시험관 선반, 피펫, 봉인된 봉투 상자, 실험 노트, 작은 서버 랙 (글자 없음) |
| 빛·분위기 | 남보라 어둠, 보라 천장 조명, 모니터 청록 불빛, 시료의 민트·구리색 층이 작게 빛남 |
| 피할 것 | 글자·숫자, 투표함·정당 상징, 파랑 대 빨강 짝 |
| 대체 글 (alt) | 밤의 연구실, 시료 선반과 봉인된 봉투 상자가 보이는 배경 |
| 대신 쓰는 그림 | CSS 배경 |

**프롬프트 (복사해서 사용)**
```
detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, cheerful comedy mood, consistent with the reference images, cozy night laboratory mood, purple light, soft magenta and green fluorescent accents, wide 8:3 background, left side simple and calm for title text, details on the right, wide night laboratory with test tube racks holding layered two-tone samples in mint green and copper orange, a pipette dipped only into the top layer of one tube, a box of sealed envelopes on a desk lit by a small spotlight, stacks of lab notebooks, a blank chalkboard on the left wall, a small server rack with teal lights, no characters, no text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands
```

### 3-2. `sc_x1_hero` — 넷이 시험관 하나를 두고 서로 다른 반응
| 항목 | 내용 |
|---|---|
| 판 · 크기 | E · 1200×800 |
| 제작 경로 | 외부: Genspark |
| 배경 | 그림 전체 |
| 구도 | 가운데 아래에 위층만 빨아올린 피펫과 시험관. 초파리는 왼쪽에서 오른쪽을 보며 시험관을 가리킴, Money-Robo는 오른쪽에서 왼쪽을 보며 옆에 금화 더미(더 많은 시험관을 원함), 박사는 가운데 뒤에서 턱에 손, 하루는 한쪽 옆에서 클립보드. 중요한 것은 위쪽 62% 안에 |
| 표정·몸짓 | 초파리 E08 안내(가리킴, 의심), 박사 E09 생각, 하루 E13 기본, 로봇 E16 뿌듯함(금화) |
| 소품 | 층이 갈라진 시험관, 피펫, 금화 더미, 클립보드 (글자 없음) |
| 빛·분위기 | 시험관에 시선이 모이는 스포트라이트 |
| 피할 것 | 승패 암시, 글자, 정당 색 짝 |
| 대체 글 (alt) | 네 캐릭터가 연구실에서 여론조사 표본 시험관을 바라보는 장면 |
| 대신 쓰는 그림 | 팩 캐릭터 CSS 무대 합성 |

**프롬프트 (복사해서 사용)**
```
detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, cheerful comedy mood, consistent with the reference images, cozy night laboratory mood, purple light, soft magenta and green fluorescent accents, 3:2 landscape scene, medium brightness, wide night laboratory with test tube racks, the Professor, a chibi male scientist with a big head, dark charcoal spiky hair with a white streak at the front, a small low ponytail at the back, very thick bold black eyebrows, teal-framed rectangular glasses, light peach skin, white lab coat over a black vest, black tie and black slacks, standing at the back center with a hand on his chin and a small question mark; the Fruit Fly, a tiny expressive cartoon fruit fly researcher with a dark charcoal-black segmented insect body, large glossy red compound eyes, a retro dark blue helmet with a yellow-white center stripe and small round side bolts, colorful dangling cables in magenta, purple and blue curving from the back of the helmet, a tiny white lab coat over a black vest, translucent veined wings, six thin black legs with the front pair used like hands, on the left looking right and pointing suspiciously at a test tube; MONEY-ROBO, a cute small floating chibi robot with a large glossy rounded-square white head and a small rounded white body with thick black outlines, a black pill-shaped screen face showing golden-yellow pixel eyes and mouth, a small round knob antenna on a short stem, stubby rounded fingerless arms, no legs, a black oval chest panel with a bright cyan pill-shaped core light, hovering above a small dark oval shadow, on the right looking left with a smug grin beside a small pile of gold coins; Haru, a cute anime girl lab assistant, long straight pink hair with navy blue streaks including a thick navy streak down the center of the bangs, two round messy hair buns on top of the head, a small ahoge, big bright blue eyes, light peach skin, wearing a lavender hoodie with white drawstrings over a white t-shirt, under an open white knee-length lab coat, at the side holding a blank clipboard; in the center foreground a glass test tube with a mint green top layer and a copper orange bottom layer, a pipette drawing liquid only from the top layer, a soft spotlight on the tube, no text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands
```

### 3-3. `sc_x1_outro` — 대결 뒤 (초파리 승)
| 항목 | 내용 |
|---|---|
| 판 · 크기 | E · 1200×800 |
| 제작 경로 | 직접 (페이지 안 CSS 무대 합성, 넣음) → 외부 선택 |
| 배경 | 그림 전체 |
| 구도 | 초파리가 앞·크게 팔짱, 작은 시험관 하나(1,000명). Money-Robo는 옆에서 큰 시험관 세 개(3,000명)를 안고 머쓱한 표정, 인정하는 몸짓. 박사가 가운데 뒤에서 보랏빛 불꽃, 하루가 옆에서 반짝이며 웃음 |
| 표정·몸짓 | 초파리 E16, 로봇 E14, 박사 E16, 하루 E01 |
| 소품 | 시험관 넷, 봉인이 뜯긴 봉투 하나 (글자 없음) |
| 빛·분위기 | 따뜻해진 연구실 조명 |
| 피할 것 | 로봇 조롱, 글자 |
| 대체 글 (alt) | 대결 뒤 초파리 연구원이 앞에서 팔짱을 끼고, Money-Robo가 옆에서 머쓱해하는 연구실 장면 |
| 대신 쓰는 그림 | 팩 캐릭터 CSS 무대 합성 |

**프롬프트 (외부 의뢰를 고를 때)**
```
detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, cheerful comedy mood, consistent with the reference images, cozy night laboratory mood, purple light, soft magenta and green fluorescent accents, 3:2 landscape scene, medium brightness, the Fruit Fly, a tiny expressive cartoon fruit fly researcher with large glossy red compound eyes, a retro dark blue helmet with a yellow-white center stripe and small round side bolts, magenta, purple and blue cables, a tiny white lab coat over a black vest, in the front left, larger, arms crossed with a proud sparkle, beside one small test tube; MONEY-ROBO, a small floating chibi robot with a glossy rounded-square white head, a black pill-shaped screen face with golden-yellow pixel eyes showing droopy embarrassed eyes and pink blush lines, a cyan chest core light, on the right hugging three large test tubes, sheepishly accepting the result; the Professor, chibi scientist with charcoal spiky hair with a white streak, very thick black eyebrows, teal-framed rectangular glasses, white lab coat over black vest and tie, at the back center holding purple flames in both hands and laughing; Haru, anime girl lab assistant with long straight pink hair with navy streaks and two round hair buns, lavender hoodie under an open white lab coat, at the side smiling with sparkles; an opened sealed envelope on the desk, no text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands
```

### 3-4. `thumb_x1` — 목차 카드 썸네일
| 항목 | 내용 |
|---|---|
| 판 · 크기 | I · 600×400 |
| 제작 경로 | 직접: CSS 배경 + 팩 192px 초파리(E08, 뒤집어 오른쪽을 봄)·로봇(E16) + 제목. `bg_x1`을 받으면 3:2로 잘라 다시 만든다 |
| 대체 글 (alt) | X1 여론조사 보정 페이지 카드 |
| 상태 | 넣음 (파일 `thumb_x1.png`) |

### 3-5. `og_x1` — 공유 미리보기
| 항목 | 내용 |
|---|---|
| 판 · 크기 | K · 1200×630 |
| 제작 경로 | 직접: CSS 배경 + 팩 초파리·박사·로봇 + 제목·부제 |
| 대체 글 (alt) | X1번 여론조사 보정 페이지 미리보기 |
| 상태 | 넣음 (파일 `og_x1.png`). 공개 주소가 정해지면 `<meta property="og:image">`에 연결 |

### 3-6. `doc_scale` — 저울을 든 박사 (새 표정 후보 E25)
| 항목 | 내용 |
|---|---|
| 판 · 크기 | A · 약 390×390 (저장소 원본과 같게) |
| 제작 경로 | 외부 (선택): 저장소 표정 명세 형식으로 |
| 배경 | 연회색 단색 (안 되면 #00ff00) |
| 구도 | 저장소 E13과 같은 크기·위치, 허리 위 치비 |
| 표정·몸짓 | 차분한 미소, 수평인 놋쇠 저울을 두 손으로 |
| 대신 쓰는 그림 | doc_e13 |
| 비고 | 이 페이지의 대결 결과(F)에서는 쓰이지 않는다. 시리즈 공용 후보 |

**프롬프트**: 저장소 `specs/doctor/expressions/`의 E13 항목 `prompt_en`을 복사해 얼굴·몸짓 구절만 *calm gentle smile, holding a level brass balance scale with both hands* 로 바꾼다. 참고 이미지 `images/doctor/E13_neutral.png`, `refs/original/doctor_sheet.png`.

## 4. 일관성 지침
- 참고 이미지: 공식 저장소 `refs/original/keyart_rivals.png`(넷이 함께) + 장면에 나오는 캐릭터의 팩 표정 원본 PNG (`images/fruitfly/E08_guiding.png`, `images/doctor/E09_thinking.png`, `images/haru/E13_neutral.png`, `images/money_robo/E16_proud.png`)
- 같은 캐릭터는 같은 세션에서, 시드 고정 가능하면 고정: 박사 1101, 조수 1102, 초파리 1103, 로봇 1104
- 표정만 바꿀 때 추가 문장: *same character, same size and position, only change the facial expression and pose to ...*
- 투명 배경이 안 되면: *solid flat #00ff00 background*

## 5. 넘겨받은 뒤 처리
SKILL 18-15 절차 그대로 (키 맞추기 → 눈으로 검수 → `--ingest` → 페이지에 넣기 → 새 표정이면 저장소용 파일 → 상태 갱신 → 점검 → 전달).
```bash
python3 build_character_pack.py --ingest 받은폴더/ --plates bg_x1=F,sc_x1_hero=E,sc_x1_outro=E --out received_x1
```
페이지 그림 합계: 현재 표정만 약 300 KB(base64). `bg_x1`(약 75 KB)과 `sc_x1_hero`(약 110 KB)를 넣으면 400 KB를 넘으므로, 그때는 192px 대결 표정 9장을 `--quality 70`으로 다시 뽑거나 96px로 내린다.

## 6. 체크리스트
- [x] HTML의 모든 `data-img` 키가 명세서에 있음 (bg_x1, sc_x1_hero, sc_x1_outro + 팩 키 27)
- [x] 대결 결과 후 표정이 5-8절 표와 일치 (F: fly_arms, robo_sigh, asst_spark, doc_judge)
- [x] 결과 전 그림에 승패 암시 없음 (fly_point, robo_coin, asst_firm)
- [x] 팩에 있는 표정을 "새로 그림"에 넣지 않음
- [x] 장소가 주 앵커(B 연구실)와 일치, 초파리 해부·현미경 소품 없음
- [x] 외부 의뢰 그림마다 참고 이미지 경로, 받는 파일 이름, 배경 지시
- [x] P1 2장 (6장 이하)
- [ ] 외부 그림을 넣은 뒤 그림 합계 400 KB 재확인

## 8. 외부 의뢰 묶음 (Genspark 에 그대로 붙여 넣기)

같은 세션에서 이 순서대로: 배경 → 히어로 장면 → (선택) 아웃트로 장면.

### 의뢰 1/3 · `bg_x1`
- **올릴 참고 이미지:** 없음 (배경만). 분위기 맞춤용으로 `refs/original/keyart_rivals.png` 한 장은 넣어도 됨
- **크기·비율:** 1920×720 (8:3) 이상
- **배경:** 그림 전체
- **받을 파일 이름:** `bg_x1.png`
- **프롬프트:** 3-1의 프롬프트 그대로
- **네거티브:** `blurry, smooth vector art, 3D render, photorealistic, anti-aliased painting, text, letters, watermark, ballot box, party logo`
- **확인할 것:** 왼쪽 45%가 단순한지, 시료 두 층이 파랑·빨강으로 나오지 않았는지

### 의뢰 2/3 · `sc_x1_hero`
- **올릴 참고 이미지:** `refs/original/keyart_rivals.png`, `images/fruitfly/E08_guiding.png`, `images/doctor/E09_thinking.png`, `images/money_robo/E16_proud.png`
- **크기·비율:** 1200×800 (3:2) 이상
- **배경:** 그림 전체
- **받을 파일 이름:** `sc_x1_hero.png`
- **프롬프트:** 3-2의 프롬프트 그대로
- **네거티브:** `blurry, smooth vector art, 3D render, photorealistic, anti-aliased painting, inconsistent character, off-model, text, letters, watermark`
- **확인할 것:** 박사 안경이 둥글게 나오면 다시. 금화에 "B"나 글자가 있으면 다시

### 의뢰 3/3 · `sc_x1_outro` (선택)
- **올릴 참고 이미지:** `refs/original/keyart_rivals.png`, `images/fruitfly/E16_proud.png`, `images/money_robo/E14_awkward.png`, `images/doctor/E16_proud.png`, `images/haru/E01_joy.png`
- **크기·비율:** 1200×800 (3:2) 이상
- **배경:** 그림 전체
- **받을 파일 이름:** `sc_x1_outro.png`
- **프롬프트:** 3-3의 프롬프트 그대로
- **네거티브:** 의뢰 2와 같음
- **확인할 것:** 로봇이 조롱당하는 구도가 아니라 인정하는 몸짓인지

(저장소 파일 이름의 슬러그는 저장소 실제 이름에 맞춰 고칠 것. 이번 작업에서는 저장소 폴더 목록을 직접 보지 않았다.)

## 7. 매니페스트
```json
{
  "page": "X1_poll_reweighting",
  "anchor": "B:night-lab-layered-samples",
  "season": "default",
  "duel": {"result": "F", "gap": 0.058, "metric": "mean absolute error (%p), lower is better", "fly": 2.32, "robo": 8.10},
  "images": [
    {"key":"bg_x1","plate":"F","size":[1920,720],"maker":"external","tool":"genspark","status":"requested","priority":"P1","slot":"hero-bg","fallback":"css","alt":"밤의 연구실, 시료 선반과 봉인된 봉투 상자가 보이는 배경"},
    {"key":"sc_x1_hero","plate":"E","size":[1200,800],"maker":"external","tool":"genspark","status":"requested","priority":"P1","slot":"hero-stage","fallback":"composite","alt":"네 캐릭터가 연구실에서 여론조사 표본 시험관을 바라보는 장면"},
    {"key":"sc_x1_outro","plate":"E","size":[1200,800],"maker":"claude","status":"placed","priority":"P2","slot":"outro","fallback":"composite","alt":"대결 뒤 초파리 연구원이 앞에서 팔짱을 끼고, Money-Robo가 옆에서 머쓱해하는 연구실 장면","note":"외부 의뢰 선택"},
    {"key":"thumb_x1","plate":"I","size":[600,400],"maker":"claude","status":"placed","priority":"P2","slot":"index-card","alt":"X1 여론조사 보정 페이지 카드"},
    {"key":"og_x1","plate":"K","size":[1200,630],"maker":"claude","status":"placed","priority":"P3","slot":"og","alt":"X1번 여론조사 보정 페이지 미리보기"},
    {"key":"doc_scale","pack":"doc_e13","plate":"A","size":96,"status":"pack-substitute","priority":"P2","slot":"duel-draw","alt":""},
    {"key":"doc_think","pack":"doc_e09","plate":"A","size":96,"status":"pack","slot":"hero-dialog","alt":""},
    {"key":"fly_point","pack":"fly_e08","plate":"C","size":192,"status":"pack","slot":"duel-before","alt":""},
    {"key":"robo_coin","pack":"robo_e16","plate":"D","size":192,"status":"pack","slot":"duel-before","alt":""},
    {"key":"fly_arms","pack":"fly_e16","plate":"C","size":192,"status":"pack","slot":"duel-after","alt":""},
    {"key":"robo_sigh","pack":"robo_e20","plate":"D","size":192,"status":"pack","slot":"duel-after","alt":""},
    {"key":"asst_spark","pack":"asst_e01","plate":"B","size":96,"status":"pack","slot":"duel-result","alt":""},
    {"key":"doc_judge","pack":"doc_e10","plate":"A","size":96,"status":"pack","slot":"duel-verdict","alt":""}
  ],
  "character_pack": {"repo":"adminmrobo/fruitfly-lab-expressions","commit":"ea5da3f"},
  "status_values": "pack | placed(직접, 넣음) | requested(의뢰) | received(받음) | applied(반영) | rejected(다시 의뢰)"
}
```

## v2 추가 (2026-10-29)
- 새 섹션 말풍선 4개: 배경 `fly_e08`(fly_point), 가상 세계 `asst_e10`, 비교 결과 `doc_e07`(doc_board), 점검표 `asst_e07` — 모두 팩 표정, 새로 그릴 그림 없음
- 192px 팩과 겹치는 96px 표정 10장을 빼서 페이지 크기를 줄임 (566 KB)
