import math
from datetime import date, timedelta

def easter_date(year):
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19*a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2*e + 2*i - h - k) % 7
    m = (a + 11*h + 22*l) // 451
    month = (h + l - 7*m + 114) // 31
    day = ((h + l - 7*m + 114) % 31) + 1
    return date(year, month, day)

def get_theme(d=None):
    d = d or date.today()
    m, day = d.month, d.day
    easter = easter_date(d.year)
    if abs((d - easter).days) <= 4:
        return "easter"
    if (m == 10 and day >= 22) or (m == 11 and day <= 2):
        return "halloween"
    if m == 12 and day >= 14:
        return "christmas"
    if m == 1 and day <= 6:
        return "newyear"
    # astronomical seasons (approx equinox/solstice dates), not calendar months
    y = d.year
    spring_start = date(y, 3, 20)
    summer_start = date(y, 6, 21)
    autumn_start = date(y, 9, 22)
    winter_start = date(y, 12, 21)
    if spring_start <= d < summer_start:
        return "spring"
    if summer_start <= d < autumn_start:
        return "summer"
    if autumn_start <= d < winter_start:
        return "autumn"
    return "winter"

def snowflake(cx, cy, s, color):
    out = []
    for ang in (0, 60, 120):
        rad = math.radians(ang)
        dx, dy = math.cos(rad) * s, math.sin(rad) * s
        out.append(f'<line x1="{cx-dx:.1f}" y1="{cy-dy:.1f}" x2="{cx+dx:.1f}" y2="{cy+dy:.1f}" '
                   f'stroke="{color}" stroke-width="1" stroke-linecap="round"/>')
    return "".join(out)

def star4(cx, cy, s, color):
    d = (f"M{cx} {cy-s} Q{cx+s*0.18} {cy-s*0.18} {cx+s} {cy} "
         f"Q{cx+s*0.18} {cy+s*0.18} {cx} {cy+s} Q{cx-s*0.18} {cy+s*0.18} {cx-s} {cy} "
         f"Q{cx-s*0.18} {cy-s*0.18} {cx} {cy-s} Z")
    return f'<path d="{d}" fill="{color}"/>'

def pumpkin(cx, cy, s, color):
    out = [f'<ellipse cx="{cx}" cy="{cy}" rx="{s}" ry="{s*0.8:.1f}" fill="{color}" opacity="0.85"/>']
    for dx in (-s*0.42, 0, s*0.42):
        out.append(f'<path d="M{cx+dx:.1f} {cy-s*0.75:.1f} Q{cx+dx-1.5:.1f} {cy:.1f} {cx+dx:.1f} {cy+s*0.75:.1f}" '
                   f'fill="none" stroke="{color}" stroke-width="0.8" opacity="0.45"/>')
    out.append(f'<line x1="{cx}" y1="{cy-s*0.78:.1f}" x2="{cx}" y2="{cy-s*1.15:.1f}" stroke="{color}" stroke-width="1.3"/>')
    return "".join(out)

def bat(cx, cy, s, color):
    d = (f"M{cx-s} {cy} Q{cx-s*0.4} {cy-s} {cx} {cy-s*0.15} Q{cx+s*0.4} {cy-s} {cx+s} {cy} "
         f"Q{cx+s*0.4} {cy-s*0.25} {cx} {cy-s*0.05} Q{cx-s*0.4} {cy-s*0.25} {cx-s} {cy} Z")
    return f'<path d="{d}" fill="{color}"/>'

def egg(cx, cy, s, color):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{s*0.72:.1f}" ry="{s}" fill="{color}" opacity="0.85"/>'
           f'<path d="M{cx-s*0.4:.1f} {cy-s*0.2:.1f} q{s*0.4:.1f} {s*0.25:.1f} {s*0.8:.1f} 0" '
           f'fill="none" stroke="{color}" stroke-width="1" opacity="0.4"/>')

def flower(cx, cy, s, color):
    out = []
    for k in range(5):
        ang = math.radians(72*k - 90)
        px, py = cx + math.cos(ang)*s*0.55, cy + math.sin(ang)*s*0.55
        out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{s*0.4:.1f}" fill="{color}" opacity="0.8"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{s*0.3:.1f}" fill="{color}"/>')
    return "".join(out)

def leaf(cx, cy, s, color):
    d = f"M{cx} {cy-s} Q{cx+s} {cy-s*0.3} {cx} {cy+s} Q{cx-s} {cy-s*0.3} {cx} {cy-s} Z"
    return (f'<path d="{d}" fill="{color}" opacity="0.82"/>'
           f'<line x1="{cx}" y1="{cy-s*0.7:.1f}" x2="{cx}" y2="{cy+s*0.8:.1f}" stroke="{color}" stroke-width="0.6" opacity="0.5"/>')

def sun(cx, cy, s, color):
    out = [f'<circle cx="{cx}" cy="{cy}" r="{s*0.5:.1f}" fill="{color}"/>']
    for k in range(8):
        ang = math.radians(45*k)
        x1, y1 = cx + math.cos(ang)*s*0.7, cy + math.sin(ang)*s*0.7
        x2, y2 = cx + math.cos(ang)*s, cy + math.sin(ang)*s
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="1" stroke-linecap="round"/>')
    return "".join(out)

def firework(cx, cy, s, color):
    out = []
    for k in range(6):
        ang = math.radians(60*k + 15)
        x2, y2 = cx + math.cos(ang)*s, cy + math.sin(ang)*s
        out.append(f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="1" stroke-linecap="round"/>')
        out.append(f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="1" fill="{color}"/>')
    return "".join(out)

THEME_ICONS = {
    "halloween": [pumpkin, bat],
    "christmas": [snowflake, star4],
    "newyear": [firework, star4],
    "easter": [egg, flower],
    "winter": [snowflake],
    "spring": [flower, leaf],
    "summer": [sun],
    "autumn": [leaf],
}

def render_seasonal_row(p, colors, x_start, x_end, cy, theme=None):
    """Returns an SVG snippet: a row of small animated seasonal icons.
    colors: list of hex colors (from the existing palette) to cycle through."""
    theme = theme or get_theme()
    icon_fns = THEME_ICONS.get(theme, [leaf])
    span = x_end - x_start
    n = max(4, min(9, int(span / 46)))
    out = [f'<!-- seasonal:{theme} -->']
    for i in range(n):
        cx = x_start + span * (i + 0.5) / n
        fn = icon_fns[i % len(icon_fns)]
        color = colors[i % len(colors)]
        s = 6.5
        begin = i * 0.35
        period = 3.4 + (i % 3) * 0.4
        out.append(f'<g transform="translate(0,0)">'
                   f'<animateTransform attributeName="transform" type="translate" '
                   f'values="0 0;0 -2.4;0 0" keyTimes="0;0.5;1" begin="{begin}s" dur="{period}s" repeatCount="indefinite"/>'
                   f'<g opacity="0.85">'
                   f'<animate attributeName="opacity" values="0.55;0.95;0.55" begin="{begin}s" dur="{period}s" repeatCount="indefinite"/>'
                   f'{fn(cx, cy, s, color)}'
                   f'</g></g>')
    return "".join(out)
