"""Regenerates stats-dark.svg / stats-light.svg from live GitHub data.
Stdlib only (urllib), so it runs in the Action with zero pip installs.
"""
import urllib.request
import json
import re
import html
import os
from datetime import datetime, timedelta

USER = "StazixLS"
TOKEN = os.environ.get("GH_TOKEN", "")
UA = {"User-Agent": "stats-generator", "Accept": "application/vnd.github+json"}
if TOKEN:
    UA["Authorization"] = f"Bearer {TOKEN}"

def fetch(url, headers=None):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8")

def get_repo_count():
    data = json.loads(fetch(f"https://api.github.com/users/{USER}"))
    return data.get("public_repos", 0), data.get("created_at", "")

def get_contribution_stats():
    page = fetch(f"https://github.com/users/{USER}/contributions")
    m = re.search(r'(\d[\d,]*)\s*\n\s*contributions', page)
    total = int(m.group(1).replace(",", "")) if m else 0
    pairs = re.findall(r'data-date="(\d{4}-\d{2}-\d{2})"[^>]*?data-level="(\d)"', page)
    days = {d: int(lvl) for d, lvl in pairs}
    if not days:
        return total, 0
    last_date = max(days.keys())
    cur = datetime.strptime(last_date, "%Y-%m-%d").date()
    streak = 0
    d = cur
    while days.get(d.isoformat(), 0) > 0:
        streak += 1
        d -= timedelta(days=1)
    return total, streak

# ---- palette (Ros\u00e9 Pine) ----
DARK = dict(base="#191724", surface="#1f1d2e", overlay="#26233a",
            muted="#6e6a86", subtle="#908caa", text="#e0def4",
            gold="#f6c177", rose="#ea9a97", pine="#31748f", foam="#9ccfd8", iris="#c4a7e7")
LIGHT = dict(base="#faf4ed", surface="#fffaf3", overlay="#f2e9e1",
             muted="#9893a5", subtle="#797593", text="#575279",
             gold="#ea9d34", rose="#d7827e", pine="#286983", foam="#56949f", iris="#907aa9")

W = 980
HEADER_H = 26
ROW_H = 96
H = HEADER_H + ROW_H
FONT_UI = "Sora, 'Segoe UI', -apple-system, sans-serif"

THEME_LABELS = {
    "halloween": "Halloween", "christmas": "Merry Christmas",
    "newyear": "Happy New Year", "easter": "Happy Easter",
    "winter": "Winter", "spring": "Spring", "summer": "Summer", "autumn": "Autumn",
    "labor_day": "Labor Day", "ve_day": "V-E Day", "music_day": "Music Day",
    "bastille_day": "Fete Nationale", "assumption": "Assumption",
    "toussaint": "All Saints' Day", "armistice": "Armistice Day",
    "epiphany": "Epiphany", "candlemas": "Candlemas", "mardi_gras": "Mardi Gras",
    "ascension": "Ascension", "pentecost": "Pentecost",
    "mothers_day": "Mother's Day", "fathers_day": "Father's Day",
    "valentines": "Valentine's Day", "chinese_new_year": "Chinese New Year",
}

def esc(s):
    return html.escape(s, quote=False)

def build_svg(p, stats, theme):
    from seasonal_scene import build_scene
    col_w = W / len(stats)
    parts = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg">']
    parts.append('<defs>')
    parts.append(f'<clipPath id="statsClip"><rect x="0" y="0" width="{W}" height="{H}" rx="14"/></clipPath>')
    parts.append('</defs>')
    parts.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="14" fill="{p["base"]}" stroke="{p["overlay"]}" stroke-width="1.5"/>')
    parts.append('<g clip-path="url(#statsClip)">')
    parts.append(f'<rect x="0" y="0" width="{W}" height="{HEADER_H}" fill="{p["surface"]}"/>')
    parts.append(f'<circle cx="16" cy="{HEADER_H/2}" r="3.5" fill="{p["foam"]}">'
                 f'<animate attributeName="opacity" values="1;0.35;1" dur="2s" repeatCount="indefinite"/></circle>')
    parts.append(f'<text x="26" y="{HEADER_H/2+4}" font-family="{FONT_UI}" font-size="11" fill="{p["subtle"]}">git log --stat --author={USER}</text>')
    parts.append(f'<text x="{W-16}" y="{HEADER_H/2+4}" font-family="{FONT_UI}" font-size="10.5" fill="{p["subtle"]}" '
                 f'text-anchor="end" opacity="0.75">{esc(THEME_LABELS.get(theme, ""))}</text>')
    parts.append(f'<line x1="0" y1="{HEADER_H}" x2="{W}" y2="{HEADER_H}" stroke="{p["overlay"]}" stroke-width="1"/>')

    # seasonal scene as a background layer, behind the numbers, same original panel size
    row_top = HEADER_H
    parts.append(f'<rect x="0" y="{row_top}" width="{W}" height="{ROW_H}" fill="{p["surface"]}"/>')
    parts.append(f'<g transform="translate(0,{row_top})" opacity="0.55">')
    parts.append(build_scene(theme, p, W, ROW_H))
    parts.append('</g>')

    for i, (value, label, color_key) in enumerate(stats):
        cx = col_w * i + col_w / 2
        color = p[color_key]
        begin = 0.15 + i * 0.12
        parts.append(f'<g opacity="0" transform="translate({cx},{row_top+ROW_H/2})">'
                     f'<animate attributeName="opacity" from="0" to="1" begin="{begin}s" dur="0.5s" fill="freeze"/>'
                     f'<animateTransform attributeName="transform" type="translate" '
                     f'from="{cx} {row_top+ROW_H/2+10}" to="{cx} {row_top+ROW_H/2}" begin="{begin}s" dur="0.5s" fill="freeze"/>'
                     f'<text x="0" y="-6" font-family="{FONT_UI}" font-size="30" font-weight="700" '
                     f'fill="{color}" text-anchor="middle">{esc(str(value))}</text>'
                     f'<text x="0" y="20" font-family="{FONT_UI}" font-size="11.5" '
                     f'fill="{p["subtle"]}" text-anchor="middle">{esc(label)}</text>'
                     f'</g>')
        if i > 0:
            parts.append(f'<line x1="{col_w*i}" y1="{row_top+18}" x2="{col_w*i}" y2="{H-18}" stroke="{p["overlay"]}" stroke-width="1"/>')
    parts.append('</g></svg>')
    return "".join(parts)

def main():
    from seasonal import get_theme
    repos, created_at = get_repo_count()
    total_contrib, streak = get_contribution_stats()
    since_year = created_at[:4] if created_at else "?"
    theme = get_theme()

    stats = [
        (f"{total_contrib}", "Contributions (1y)", "rose"),
        (f"{streak}", "Day streak", "gold"),
        (f"{repos}", "Repositories", "foam"),
        (since_year, "On GitHub since", "iris"),
    ]

    with open("stats-dark.svg", "w") as f:
        f.write(build_svg(DARK, stats, theme))
    with open("stats-light.svg", "w") as f:
        f.write(build_svg(LIGHT, stats, theme))
    print("Updated:", stats, "theme:", theme)

if __name__ == "__main__":
    main()
