from seasonal import get_theme
from seasonal_scene import build_scene

DARK = dict(base="#191724", surface="#1f1d2e", overlay="#26233a", hi_low="#21202e",
            muted="#6e6a86", subtle="#908caa", text="#e0def4",
            gold="#f6c177", rose="#ea9a97", pine="#31748f", foam="#9ccfd8", iris="#c4a7e7")
LIGHT = dict(base="#faf4ed", surface="#fffaf3", overlay="#f2e9e1", hi_low="#f4ede8",
             muted="#9893a5", subtle="#797593", text="#575279",
             gold="#ea9d34", rose="#d7827e", pine="#286983", foam="#56949f", iris="#907aa9")

W, H = 980, 150
FONT_UI = "Sora, 'Segoe UI', -apple-system, sans-serif"

THEME_LABELS = {
    "halloween": "Happy Halloween",
    "christmas": "Merry Christmas",
    "newyear": "Happy New Year",
    "easter": "Happy Easter",
    "winter": "Winter",
    "spring": "Spring",
    "summer": "Summer",
    "autumn": "Autumn",
}

def build_svg(p, theme):
    inner = build_scene(theme, p, W, H)
    label = THEME_LABELS.get(theme, "")
    parts = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg">']
    parts.append('<defs>')
    parts.append(f'<clipPath id="sceneClip"><rect x="0" y="0" width="{W}" height="{H}" rx="14"/></clipPath>')
    parts.append('</defs>')
    parts.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="14" fill="{p["base"]}" stroke="{p["overlay"]}" stroke-width="1.5"/>')
    parts.append(f'<g clip-path="url(#sceneClip)">{inner}</g>')
    parts.append(f'<text x="16" y="20" font-family="{FONT_UI}" font-size="11" fill="{p["subtle"]}" opacity="0.8">{label}</text>')
    parts.append('</svg>')
    return "".join(parts)

def main():
    theme = get_theme()
    with open("season-dark.svg", "w") as f:
        f.write(build_svg(DARK, theme))
    with open("season-light.svg", "w") as f:
        f.write(build_svg(LIGHT, theme))
    print("theme:", theme)

if __name__ == "__main__":
    main()
