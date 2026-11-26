# -*- coding: utf-8 -*-
"""校验 AI 资料包：文件存在 / 链接可达 / JSON 合法 / 双份 PRD 一致 / 无敏感串。"""
import os, io, re, json, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AI = ROOT / "ai-context"
PRD = ROOT / "PRD_物业小程序一期_V0.3_2026-11-24.md"

def sha(p): return hashlib.sha256(io.open(p, "rb").read()).hexdigest()

# ---------- 1. 必需文件 ----------
REQUIRED = [
    "llms.txt", "AGENTS.md", "README.md", "AI_CONTEXT.md",
    "ai-context/00_INDEX.md", "ai-context/01_SUMMARY.md", "ai-context/02_PRD.md",
    "ai-context/03_DECISIONS.md", "ai-context/04_OPEN_QUESTIONS.md",
    "ai-context/05_GLOSSARY.md", "ai-context/06_CHANGELOG.md", "ai-context/07_EVIDENCE_MAP.md",
    "ai-context/08_DELIVERY_CONTRACT.md",
    "ai-context/data/requirements.json", "ai-context/data/fr_index.json",
    "ai-context/data/open_questions.json", "ai-context/data/versions.json",
]
missing = [f for f in REQUIRED if not (ROOT / f).exists()]
print("1) required files: %d/%d" % (len(REQUIRED) - len(missing), len(REQUIRED)))
if missing: print("   MISSING:", missing)

# ---------- 2. Markdown 相对链接可达 ----------
LINK = re.compile(r"\[[^\]]*\]\(([^)#][^)]*)\)")
bad, total_links = [], 0
md_files = [ROOT / f for f in REQUIRED if f.endswith(".md")] + [ROOT / "llms.txt"] + list(AI.glob("evidence/*.md"))
for f in md_files:
    s = io.open(f, encoding="utf-8").read()
    for m in LINK.finditer(s):
        target = m.group(1).strip()
        if target.startswith(("http://", "https://", "mailto:")): continue
        total_links += 1
        p = (f.parent / target).resolve()
        if not p.exists(): bad.append("%s -> %s" % (f.relative_to(ROOT), target))
print("2) links: %d checked, %d broken" % (total_links, len(bad)))
for b in bad: print("   BROKEN:", b)

# ---------- 3. JSON 合法 + 关键字段 ----------
def load(p): return json.loads(io.open(p, encoding="utf-8").read())
fr = load(AI / "data/fr_index.json")
uq = load(AI / "data/open_questions.json")
rq = load(AI / "data/requirements.json")
vs = load(AI / "data/versions.json")
ids = [x["id"] for x in fr["items"]]
uids = [x["id"] for x in uq["items"]]
print("3) JSON: fr=%d(unique %d, range %s..%s) | U=%d | req items=%d standards=%d answered=%d | versions=%d" % (
    len(ids), len(set(ids)), ids[0], ids[-1], len(uids),
    len(rq["items"]), len(rq["standards"]), len(rq["answered"]), len(vs["chain"])))
assert len(ids) == 93 and len(set(ids)) == 93 and ids[0] == "FR-01" and ids[-1] == "FR-93"
assert len(uids) == 13 and all(x["status"] == "OPEN" for x in uq["items"])
assert len(rq["items"]) == 31 and len(rq["standards"]) == 16 and len(rq["answered"]) == 18

# ---------- 4. PRD 双份一致 ----------
same = sha(PRD) == sha(AI / "02_PRD.md")
print("4) PRD mirror sha256 match:", same, "|", sha(AI / "02_PRD.md")[:16])

# ---------- 5. 敏感串 ----------
SENS = re.compile(r"(?i)(wx[0-9a-f]{16}|ltd-swan-[0-9a-z]+|C:\\\\?Users\\\\?DC|appsecret\s*=\s*[A-Za-z0-9]{8,})")
leaks = []
for dp, _, fns in os.walk(AI):
    for f in fns:
        p = Path(dp) / f
        if p.suffix not in (".md", ".json", ".txt"): continue
        if SENS.search(io.open(p, encoding="utf-8", errors="ignore").read()):
            leaks.append(str(p.relative_to(ROOT)))
for f in ("llms.txt", "AGENTS.md", "README.md", "AI_CONTEXT.md"):
    if SENS.search(io.open(ROOT / f, encoding="utf-8", errors="ignore").read()):
        leaks.append(f)
print("5) sensitive leaks:", len(leaks), leaks if leaks else "")

# ---------- 6. 状态标记与体量 ----------
total = 0
for dp, _, fns in os.walk(AI):
    for f in fns: total += os.stat(Path(dp) / f).st_size
print("6) ai-context size: %.1f KB | evidence=%d | data=%d" % (
    total / 1024, len(list((AI / "evidence").glob("*.md"))), len(list((AI / "data").glob("*.json")))))

# ---------- 7. V0.4 交付契约层 ----------
prd_txt = io.open(AI / "02_PRD.md", encoding="utf-8").read()
contract = {
    "§5.10 章节": prd_txt.count("### 5.10 ") == 1,
    "附录 K": prd_txt.count("## 附录 K ") == 1,
    "K.1~K.7": all(prd_txt.count("### K.%d " % i) == 1 for i in range(1, 8)),
    "P0 验收点 51 行": len(re.findall(r"^\| `FR-\d{2}` \|.*\| `TC-\d{3}` \|$", prd_txt, flags=re.M)) == 51,
    "RTM TC 编号": len(re.findall(r"`TC-\d{3}`", prd_txt)) >= 93,
    "08 速查": (AI / "08_DELIVERY_CONTRACT.md").exists(),
}
print("7) V0.4 contract:", "PASS" if all(contract.values()) else "FAIL",
      [k for k, ok in contract.items() if not ok] or "")
assert all(contract.values())

ok = not missing and not bad and same and not leaks and all(contract.values())
print("\nRESULT:", "PASS" if ok else "FAIL")
assert ok
