"""data/ 의 사후층화 표 v0 결과로 frame_v0.html (단일 파일 결과 페이지)을 만든다.
사용: python scripts/make_frame_page.py   (저장소 맨 위 폴더에서)"""
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
checks = json.loads((D / "frame_v0_checks.json").read_text(encoding="utf-8"))
pv = [dict(r, share=float(r["share"])) for r in csv.DictReader(open(D / "frame_v0_with_pastvote.csv", encoding="utf-8-sig"))]
edu = [dict(r, share=float(r["share"])) for r in csv.DictReader(open(D / "frame_v0_age_sex_prov_edu.csv", encoding="utf-8-sig"))]
reg = {}
src = (ROOT / "scripts/region_2025.py").read_text(encoding="utf-8")
ns = {}; exec(compile(src, "region_2025", "exec"), ns)
for r in ns["table"](): reg[r["prov"]] = r
data = {"pv": [[r["age_grp"], r["sex"], r["province"], r["pastvote"], round(r["share"], 7)] for r in pv],
        "edu": [[r["age_grp"], r["sex"], r["province"], r["edu4"], round(r["share"], 7)] for r in edu],
        "checks": checks, "region": reg}
tpl = (ROOT / "scripts/frame_page_template.html").read_text(encoding="utf-8")
html = tpl.replace("/*__DATA__*/", "var DATA=" + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + ";")
(ROOT / "frame_v0.html").write_text(html, encoding="utf-8")
print("frame_v0.html", len(html.encode()) // 1024, "KB")
