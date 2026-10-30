# X1 여론조사 보정 — Genspark 이미지 프롬프트 (v2)

## 쓰는 법
- **참고 이미지 첨부:** 캐릭터가 나오는 그림은 저장소 `adminmrobo/fruitfly-lab-expressions`의 `refs/original/` 캐릭터 시트 4장(박사·조수·초파리·로봇)을 함께 올려야 외형이 맞습니다.
- **비율:** 각 항목에 적힌 비율을 Genspark에서 고릅니다.
- **파일 이름:** 받은 그림은 표의 **키** 그대로(예: `cut_x1_world.png`) 저장해서 주세요. 그러면 들어갈 자리에 바로 넣습니다.
- **공통 금지:** 글자·숫자, 투표함·정당 상징, 파랑 대 빨강 짝. 시료의 두 층은 민트와 구리색입니다.
- 그림이 하나도 없어도 페이지는 지금처럼 동작합니다. 받은 것부터 넣습니다.

| 우선 | 키 | 비율 · 크기 | 들어갈 곳 | 장면 |
|---|---|---|---|---|
| P1 | bg_x1 | 8:3 · 1920×720 | 맨 위 배경 | 사람 없는 밤의 연구실 |
| P1 | sc_x1_hero | 3:2 · 1200×800 | 맨 위 무대 | 넷이 시험관 하나를 두고 서로 다른 반응 |
| P1 | cut_x1_why | 16:9 · 1200×675 | 왜 이 주제인가 | 엽서 산 위의 로봇, 봉투 하나 든 초파리 |
| P1 | cut_x1_mech | 16:9 · 1200×675 | 배경 | 울리는 전화에 달려드는 소수, 무심한 다수 |
| P1 | cut_x1_world | 16:9 · 1200×675 | 가상 세계 | 유리 돔 속 미니어처 도시와 조정판 |
| P2 | cut_x1_ladder | 16:9 · 1200×675 | 다섯 칸 시작 전 | 다섯 칸 사다리를 오르는 초파리 |
| P2 | cut_x1_bench | 16:9 · 1200×675 | 보정법 비교 | 시험관 일곱 개의 측정대, 초시계 든 하루 |
| P2 | cut_x1_duel | 16:9 · 1200×675 | 대결 | 작은 시험관+봉투 대 큰 시험관 셋, 가운데 박사 |
| P2 | cut_x1_check | 16:9 · 1200×675 | 공표 점검표 | 긴 결과표를 돋보기로 훑는 초파리 |
| P3 | sc_x1_outro | 3:2 · 1200×800 | 아웃트로 | 대결 뒤, 팔짱 낀 초파리와 머쓱한 로봇 |

---

## P1 — bg_x1 (8:3)
```
detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, cozy night laboratory mood, deep indigo darkness, purple ceiling light, soft magenta and green fluorescent accents, wide 8:3 background, left 45 percent simple and dark with only a blank chalkboard for title text, details on the right, test tube racks holding layered two-tone samples in mint green and copper orange glowing softly, a pipette dipped only into the top layer of one tube, a box of sealed envelopes on a desk lit by a small spotlight, stacks of lab notebooks, a small server rack with teal lights, no characters, no text, no letters, no numbers, no logos, no ballot box, no flags
```

## P1 — sc_x1_hero (3:2)
```
detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, cheerful comedy mood, consistent with the reference images, cozy night laboratory, purple light, soft magenta and green fluorescent accents, 3:2 landscape scene, all important elements in the upper 62 percent, the Professor, a chibi male scientist with a big head, dark charcoal spiky hair with a white streak at the front, a small low ponytail, very thick bold black eyebrows, teal-framed rectangular glasses, white lab coat over a black vest and black tie, standing at the back center with a hand on his chin and a small question mark; the Fruit Fly, a tiny cartoon fruit fly researcher with a charcoal-black segmented body, large glossy red compound eyes, a retro dark blue helmet with a yellow-white center stripe and round side bolts, magenta purple and blue cables from the back of the helmet, a tiny white lab coat over a black vest, translucent wings, on the left looking right and pointing suspiciously at a test tube; MONEY-ROBO, a small floating chibi robot with a glossy rounded-square white head, a black pill-shaped screen face with golden-yellow pixel eyes, a small knob antenna, stubby arms, no legs, a cyan core light on a black chest panel, on the right looking left with a smug grin beside a small pile of gold coins; Haru, an anime girl lab assistant with long straight pink hair with navy streaks, two round hair buns, big blue eyes, a lavender hoodie under an open white lab coat, at the side holding a blank clipboard; in the center foreground a glass test tube with a mint green top layer and a copper orange bottom layer, a pipette drawing liquid only from the top layer, a soft spotlight on the tube, no text, no letters, no numbers, no logos, no ballot box, no flags
```

## P1 — cut_x1_why (16:9)
"240만 장" 일화(크게 모았지만 한쪽으로 치우친 표본)를 보여 주는 그림입니다.
```
detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, cheerful comedy mood, consistent with the reference images, night laboratory, purple light, 16:9 landscape scene, on the right a huge towering mountain of blank paper postcards almost touching the ceiling, MONEY-ROBO, a small floating chibi robot with a glossy rounded-square white head, a black pill-shaped screen face with golden-yellow pixel eyes, a cyan chest core light, hovering proudly on top of the postcard mountain holding up a rising line chart sign with no numbers, the postcards on one side of the mountain are all the same copper orange color while very few are mint green, showing the pile is lopsided; on the left on the floor the Fruit Fly, a tiny cartoon fruit fly researcher with large glossy red compound eyes, a retro dark blue helmet with a yellow-white stripe, colorful cables, a tiny white lab coat, holding one small sealed envelope and a magnifying glass, looking up at the pile with a skeptical face, playful contrast of big versus small, no text, no letters, no numbers, no logos, no ballot box, no flags
```

## P1 — cut_x1_mech (16:9)
정치 관심이 큰 사람이 전화에 더 잘 답한다는 배경 섹션용입니다.
```
detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, warm gentle comedy mood, 16:9 landscape scene, a cozy miniature neighborhood diorama built on a long laboratory table, many tiny generic pixel townspeople in neutral grey beige and lavender clothes, an old-fashioned telephone in the middle of the diorama ringing with small motion lines, three or four tiny townspeople with very excited faces sprinting toward the phone waving their hands, while the many other townspeople keep doing everyday things, cooking, reading, sleeping on a bench, walking a dog, carrying groceries, calmly ignoring the ringing phone, in the background the Fruit Fly, a tiny cartoon fruit fly researcher with glossy red compound eyes, a retro dark blue helmet with a yellow-white stripe and a tiny white lab coat, leaning over the table edge watching with a notebook, soft purple night lab lighting, no party colors, no text, no letters, no numbers, no logos, no ballot box, no flags
```

## P1 — cut_x1_world (16:9)
참값을 아는 가상 세계(20만 명)를 만들어 두고 실험한다는 섹션용입니다.
```
detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, cheerful comedy mood, consistent with the reference images, night laboratory, purple light, 16:9 landscape scene, in the center a large glass dome on a pedestal containing a glowing miniature city with tiny houses, apartment blocks, roads and countless tiny dots of people, four districts of the city softly lit in slightly different pastel tones, thin glowing tubes running from the dome into a control console with sliders and round dials, Haru, an anime girl lab assistant with long straight pink hair with navy streaks, two round hair buns, a lavender hoodie under an open white lab coat, adjusting a slider on the console with focused eyes, the Professor, a chibi scientist with charcoal spiky hair with a white streak, very thick black eyebrows, teal-framed rectangular glasses and a white lab coat, standing behind the dome holding a sealed golden envelope labeled only with a star symbol meaning the true answer, no text, no letters, no numbers, no logos, no ballot box, no flags
```

## P2 — cut_x1_ladder (16:9)
다섯 단계 보정(원시 평균 → 사후층화 → 지난 투표 → 부분 풀링 → 여러 조사 합치기)을 시작하는 자리입니다.
```
detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, cheerful adventure mood, consistent with the reference images, night laboratory, purple light, 16:9 landscape scene, a tall wooden ladder with five glowing rungs leaning against a lab wall, each rung holds one small object: on the first rung a single plain beaker, on the second rung a tray of sorted small test tubes in a grid, on the third rung a sealed envelope with a wax seal, on the fourth rung several test tubes connected by thin tubes sharing liquid, on the fifth rung a small stack of overlapping line charts with no numbers, the Fruit Fly, a tiny cartoon fruit fly researcher with glossy red compound eyes, a retro dark blue helmet with a yellow-white stripe, colorful cables and a tiny white lab coat, climbing the ladder at the second rung and looking upward with determination, at the bottom MONEY-ROBO, a small floating white robot with a black screen face and golden-yellow pixel eyes, hovering and holding the ladder steady, no text, no letters, no numbers, no logos, no ballot box, no flags
```

## P2 — cut_x1_bench (16:9)
보정법 일곱 가지를 같은 조건에서 100번 돌려 오차를 잰 비교 섹션용입니다.
```
detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, cheerful comedy mood, consistent with the reference images, night laboratory, purple light, 16:9 landscape scene, a long measuring bench with seven identical glass test tubes standing in a row, each tube filled to a slightly different height with mint green liquid, a thin horizontal golden line glowing across all tubes marking the true level, some tubes close to the line and some far below it, a small dial gauge under each tube, Haru, an anime girl lab assistant with long straight pink hair with navy streaks, two round hair buns, a lavender hoodie under an open white lab coat, holding a stopwatch and a blank clipboard, the Fruit Fly, a tiny cartoon fruit fly researcher with glossy red compound eyes and a retro dark blue helmet, measuring one tube with a tiny ruler, precise and calm atmosphere, no text, no letters, no numbers, no logos, no ballot box, no flags
```

## P2 — cut_x1_duel (16:9)
대결(3,000명 원시 평균 대 1,000명 + 지난 투표 가중) 직전 장면입니다. 결과를 암시하지 않습니다.
```
detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, playful showdown mood like a retro fighting game select screen, consistent with the reference images, night laboratory arena with a purple spotlight from above, 16:9 landscape scene, on the left the Fruit Fly, a tiny cartoon fruit fly researcher with glossy red compound eyes, a retro dark blue helmet with a yellow-white stripe, magenta purple and blue cables and a tiny white lab coat, facing right, holding one small test tube and a sealed envelope with a wax seal, on the right MONEY-ROBO, a small floating chibi robot with a glossy rounded-square white head, a black pill-shaped screen face with golden-yellow pixel eyes, a cyan chest core light, facing left, hugging three large test tubes with a confident grin, in the center back the Professor, a chibi scientist with charcoal spiky hair with a white streak, very thick black eyebrows, teal-framed rectangular glasses and a white lab coat, as a referee raising one hand, a glowing lightning spark between the two sides, no winner shown, no text, no letters, no numbers, no logos, no ballot box, no flags
```

## P2 — cut_x1_check (16:9)
공표된 여론조사 결과표를 읽을 때 확인할 것(공표 점검표) 섹션용입니다.
```
detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, cheerful comedy mood, consistent with the reference images, night laboratory, purple light, 16:9 landscape scene, a very long paper scroll of a blank table with empty grid cells unrolled across a desk and hanging onto the floor, the Fruit Fly, a tiny cartoon fruit fly researcher with glossy red compound eyes, a retro dark blue helmet with a yellow-white stripe and a tiny white lab coat, walking along the table with a big magnifying glass, Haru, an anime girl lab assistant with long straight pink hair with navy streaks, two round hair buns, a lavender hoodie under an open white lab coat, following behind and stamping green check marks and one orange question mark on the margin with a rubber stamp, a sealed envelope and a coffee mug on the desk, no text, no letters, no numbers, no logos, no ballot box, no flags
```

## P3 — sc_x1_outro (3:2)
```
detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, cheerful comedy mood, consistent with the reference images, warm cozy night laboratory, purple light, 3:2 landscape scene, the Fruit Fly, a tiny cartoon fruit fly researcher with large glossy red compound eyes, a retro dark blue helmet with a yellow-white stripe, magenta purple and blue cables, a tiny white lab coat, in the front left and larger, arms crossed with a proud sparkle, beside one small test tube and an opened envelope; MONEY-ROBO, a small floating chibi robot with a glossy rounded-square white head, a black pill-shaped screen face with droopy embarrassed golden-yellow pixel eyes and pink blush lines, a cyan chest core light, on the right hugging three large test tubes and sheepishly accepting the result; the Professor, chibi scientist with charcoal spiky hair with a white streak, very thick black eyebrows, teal-framed rectangular glasses, white lab coat, at the back center holding small purple flames in both hands and laughing; Haru, anime girl lab assistant with long straight pink hair with navy streaks, two round hair buns, a lavender hoodie under an open white lab coat, at the side smiling with sparkles, no mocking, no text, no letters, no numbers, no logos, no ballot box, no flags
```
