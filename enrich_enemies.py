#!/usr/bin/env python3
"""补齐敌人图鉴：名称/描述/分组/图标（来自 PRTS 缓存页 + enemy_handbook_table）。"""
import csv, html, json, os, re, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(ROOT, "raw")
DATA = os.path.join(ROOT, "data")
ASSETS = os.path.join(ROOT, "assets", "enemies", "special")

HANDBOOK = os.path.join(RAW, "enemy_handbook_table.json")
CACHE = "/tmp/eh3.json"

DMG = {"PHYSIC": "物理", "PHYSICAL": "物理", "MAGIC": "法术", "TRUE": "真实", "NONE": "无", "NO_DAMAGE": "无伤"}
LEVEL = {"NORMAL": "普通", "ELITE": "精英", "BOSS": "领袖"}


def load_handbook():
    path = HANDBOOK if os.path.exists(HANDBOOK) else CACHE
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)["enemyData"]


def parse_wiki():
    text = json.load(open(os.path.join(RAW, "wiki_parse_text.json"), encoding="utf-8"))["parse"]["text"]
    i = text.find('id="战术特训敌人"')
    seg = text[i:]
    j = seg.find("<h3", 10)
    seg = seg[:j] if j > 0 else seg
    meta, group_desc = {}, {}
    for r in re.findall(r"<tr>(.*?)</tr>", seg, re.S):
        tds = re.findall(r"<td[^>]*>(.*?)</td>", r, re.S)
        if len(tds) < 2:
            continue
        m = re.search(r"<br\s*/?>\s*([^<]+)\s*$", tds[0])
        g = html.unescape(m.group(1)).strip() if m else ""
        tip = re.search(r'data-size="\d+"[^>]*>([^<]+)</span>', tds[0])
        if g and tip:
            group_desc[g] = html.unescape(tip.group(1)).strip()
        for blk in re.findall(r'class="enemyicon">(.*?)</div>', tds[1], re.S):
            nm = re.search(r'title="([^"]+)"', blk)
            src = re.search(r'<img src="([^"]+)"', blk)
            if nm and src:
                meta.setdefault(nm.group(1), {"g": g, "u": src.group(1)})
    return meta, group_desc


def parse_bosses():
    text = json.load(open(os.path.join(RAW, "wiki_parse_text.json"), encoding="utf-8"))["parse"]["text"]
    i = text.find('id="领袖"')
    seg = text[i:text.find('id="战术特训敌人"', i)]
    out = {}
    for r in re.findall(r"<tr>(.*?)</tr>", seg, re.S):
        tds = re.findall(r"<td[^>]*>(.*?)</td>", r, re.S)
        if len(tds) < 5:
            continue
        nm = re.search(r'title="([^"]+)"', tds[0])
        src = re.search(r'<img src="([^"]+)"', tds[0])
        first = re.sub(r"<[^>]+>", " ", tds[1]).split()
        if not nm or not first:
            continue
        num = re.sub(r"[^\d]", "", first[0])
        if num:
            out[int(num)] = (nm.group(1), src.group(1) if src else "")
    return out


def icon_url(u):
    return u.replace("/60px-", "/120px-")


def dl(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 500:
        return True
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    for _ in range(4):
        r = subprocess.run(["curl", "-sL", "-A", "Mozilla/5.0", "-e", "https://prts.wiki/",
                            "--max-time", "30", url, "-o", dest], capture_output=True)
        if os.path.exists(dest) and os.path.getsize(dest) > 500:
            return True
    return False


def main():
    eh = load_handbook()
    meta, group_desc = parse_wiki()
    s = json.load(open(os.path.join(RAW, "activity_table.json"), encoding="utf-8"))
    s = s["activity"]["AUTOCHESS"]["act3autochess"]["V3_1"]
    old = {r["id"]: r for r in csv.DictReader(open(os.path.join(DATA, "enemies.csv"), encoding="utf-8-sig"))}

    bosses = parse_bosses()
    rows = []
    for eid, e in s["bossInfoDict"].items():
        hp = e["bloodDataDict"].get("mode_multi_funny", "")
        name, icon = bosses.get(int(hp), ("未公开领袖", ""))
        dest = ""
        if icon:
            dest = os.path.join("assets", "enemies", "boss", f"{hp}.png")
            dl(icon_url(icon), os.path.join(ROOT, dest))
            if not os.path.exists(os.path.join(ROOT, dest)):
                dest = ""
        rows.append({
            "类型": "领袖", "分组": "", "敌人": name, "id": eid, "敌人等级": "BOSS",
            "伤害类型": "", "技能": "", "普通敌人": "", "精英敌人": "",
            "标准模拟": hp,
            "险境模拟": e["bloodDataDict"].get("mode_multi_normal", ""),
            "绝境模拟": e["bloodDataDict"].get("mode_multi_hard", ""),
            "终极模拟": e["bloodDataDict"].get("mode_multi_abyss", ""),
            "描述": f"隐秘核心（mode_single_20）血量 {e['bloodDataDict'].get('mode_single_20','—')}",
            "图标": dest,
        })

    downloaded = 0
    for eid, e in s["specialEnemyInfoDict"].items():
        info = eh.get(eid, {})
        name = info.get("name", eid)
        m = meta.get(name, {})
        dest = os.path.join("assets", "enemies", "special", eid + ".png")
        if m.get("u") and dl(icon_url(m["u"]), os.path.join(ROOT, dest)):
            downloaded += 1
        abilities = "；".join(a.get("text", "") for a in (info.get("abilityList") or []) if a.get("text"))
        att_n = [ (eh.get(k) or {}).get("name", k) for k in (e.get("attachedNormalEnemyKeys") or []) ]
        att_e = [ (eh.get(k) or {}).get("name", k) for k in (e.get("attachedEliteEnemyKeys") or []) ]
        rows.append({
            "类型": "战术特训敌人", "分组": m.get("g", ""), "敌人": name, "id": eid,
            "敌人等级": LEVEL.get(info.get("enemyLevel", ""), info.get("enemyLevel", "")),
            "伤害类型": "/".join(DMG.get(d, d) for d in (info.get("damageType") or [])),
            "技能": abilities,
            "普通敌人": " / ".join(att_n), "精英敌人": " / ".join(att_e),
            "标准模拟": "", "险境模拟": "", "绝境模拟": "", "终极模拟": "",
            "描述": info.get("description", ""),
            "图标": dest if os.path.exists(os.path.join(ROOT, dest)) else "",
        })

    fields = ["类型", "分组", "敌人", "id", "敌人等级", "伤害类型", "技能",
              "普通敌人", "精英敌人", "标准模拟", "险境模拟", "绝境模拟", "终极模拟", "描述", "图标"]
    with open(os.path.join(DATA, "enemies.csv"), "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    with open(os.path.join(DATA, "enemy_groups.json"), "w", encoding="utf-8") as fh:
        json.dump(group_desc, fh, ensure_ascii=False, indent=2)
    print(f"敌人 {len(rows)} 行，下载图标 {downloaded} 个；分组 {len(group_desc)} 个")


if __name__ == "__main__":
    main()
