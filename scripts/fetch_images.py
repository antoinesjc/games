"""Download the oracle bone glyphs and photos used by the games from Wikimedia Commons.

Run by .github/workflows/fetch-images.yml (GitHub's servers can reach Wikimedia).
Writes the files into oracle-bone/img/ and a credits.json with each file's license.
Missing files are reported in the log; the game falls back to its own sketches for them.
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request

UA = "MandarinZestGames/1.0 (https://www.mandarinzest.com; contact@mandarinzest.com)"
API = "https://commons.wikimedia.org/w/api.php"
ROOT = os.path.join(os.path.dirname(__file__), "..", "oracle-bone", "img")

# character -> candidate file names on Commons (first one found wins)
GLYPHS = {
    "日": ['日-oracle.svg'],
    "月": ['月-oracle.svg'],
    "山": ['山-oracle.svg'],
    "水": ['水-oracle.svg'],
    "雨": ['雨-oracle.svg'],
    "木": ['木-oracle.svg'],
    "今": ['今-oracle.svg'],
    "人": ['人-oracle.svg'],
    "女": ['女-oracle.svg'],
    "子": ['子-oracle.svg'],
    "口": ['口-oracle.svg'],
    "目": ['目-oracle.svg'],
    "耳": ['耳-oracle.svg'],
    "好": ['好-oracle.svg'],
    "卜": ['卜-oracle.svg'],
    "牛": ['牛-oracle.svg'],
    "羊": ['羊-oracle.svg'],
    "馬": ['馬-oracle.svg'],
    "魚": ['魚-oracle.svg'],
    "鳥": ['鳥-oracle.svg'],
    "龜": ['龜-oracle.svg'],
    "田": ['田-oracle.svg'],
    "車": ['車-oracle.svg'],
    "門": ['門-oracle.svg'],
    "刀": ['刀-oracle.svg'],
    "弓": ['弓-oracle.svg'],
    "舟": ['舟-oracle.svg'],
    "王": ['王-oracle.svg'],
    "大": ['大-oracle.svg'],
    "天": ['天-oracle.svg'],
    "火": ['火-oracle.svg'],
    "中": ['中-oracle.svg'],
    "宀": ['宀-oracle.svg'],
    "豕": ['豕-oracle.svg'],
    "家": ['家-oracle.svg'],
    "休": ['休-oracle.svg'],
    "明": ['明-oracle.svg'],
    "从": ['从-oracle.svg', '從-oracle.svg'],
    # Extra glyphs for the Mandarin Zest Club app's Calligraphy School course (chapters 6 and 7)
    "又": ['又-oracle.svg'],
    "止": ['止-oracle.svg'],
    "力": ['力-oracle.svg'],
    "立": ['立-oracle.svg'],
    "見": ['見-oracle.svg'],
    "生": ['生-oracle.svg'],
    "禾": ['禾-oracle.svg'],
    "米": ['米-oracle.svg'],
    "竹": ['竹-oracle.svg'],
    "酉": ['酉-oracle.svg'],
    "皿": ['皿-oracle.svg'],
    "鼎": ['鼎-oracle.svg'],
    "手": ['手-oracle.svg'],
    "步": ['步-oracle.svg'],
    "走": ['走-oracle.svg'],
    "黍": ['黍-oracle.svg'],
    "來": ['來-oracle.svg'],
    "麥": ['麥-oracle.svg'],
    "食": ['食-oracle.svg'],
    "秋": ['秋-oracle.svg'],
    "瓜": ['瓜-oracle.svg'],
    "采": ['采-oracle.svg'],
    "男": ['男-oracle.svg'],
    "林": ['林-oracle.svg'],
    "森": ['森-oracle.svg'],
    "炎": ['炎-oracle.svg'],
    "出": ['出-oracle.svg'],
    "正": ['正-oracle.svg'],
    "爵": ['爵-oracle.svg'],
    "豆": ['豆-oracle.svg'],
}
PHOTOS = {
    "scapula": ["Shang dynasty inscribed scapula.jpg"],
    "plastron": ["Shang dynasty inscribed tortoise plastron.jpg"],
}


def get(url):
    """GET with a polite pause and retries (Wikimedia answers 429 to fast bots)."""
    import time
    import urllib.error
    for attempt in range(6):
        time.sleep(2)
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 5:
                raise
            wait = int(e.headers.get("Retry-After") or 10 * (attempt + 1))
            print("  429, waiting %ss" % wait)
            time.sleep(min(wait, 60))


def info(title, width=None):
    q = {"action": "query", "format": "json", "prop": "imageinfo", "titles": "File:" + title,
         "iiprop": "url|extmetadata"}
    if width:
        q["iiurlwidth"] = str(width)
    data = json.loads(get(API + "?" + urllib.parse.urlencode(q)))
    page = next(iter(data["query"]["pages"].values()))
    if "imageinfo" not in page:
        return None
    return page["imageinfo"][0]


def clean(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html or "")).strip()


def main():
    os.makedirs(os.path.join(ROOT, "glyphs"), exist_ok=True)
    credits, missing = {}, []
    jobs = [("glyphs/%s.svg" % ch, names, None) for ch, names in GLYPHS.items()]
    jobs += [("%s.jpg" % key, names, 1000) for key, names in PHOTOS.items()]
    for out, names, width in jobs:
        for name in names:
            try:
                ii = info(name, width)
                if not ii:
                    continue
                url = ii.get("thumburl") if width else ii["url"]
                body = get(url)
            except Exception as e:  # keep going; report at the end
                print("ERROR   %-24s %s" % (out, e))
                continue
            with open(os.path.join(ROOT, out), "wb") as f:
                f.write(body)
            meta = ii.get("extmetadata", {})
            credits[out] = {
                "file": name,
                "source": ii.get("descriptionurl"),
                "license": clean(meta.get("LicenseShortName", {}).get("value")),
                "artist": clean(meta.get("Artist", {}).get("value")),
            }
            print("OK      %-24s <- %s (%s)" % (out, name, credits[out]["license"]))
            break
        else:
            missing.append(out)
            print("MISSING %-24s (tried %s)" % (out, ", ".join(names)))
    with open(os.path.join(ROOT, "credits.json"), "w", encoding="utf-8") as f:
        json.dump(credits, f, ensure_ascii=False, indent=1)
    print("\n%d downloaded, %d missing" % (len(credits), len(missing)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
