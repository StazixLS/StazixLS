import math
import random

# ---------- particle shapes (used by falling_particles) ----------

def leaf_shape(color, seed=0):
    d = ("M0,-10 C2.5,-9 4,-6.5 3.2,-4 C5.5,-3 6,0.5 4,2.5 "
         "C5.5,3.5 5,6.5 2.5,7.5 C1.5,6 0.5,6 0,7.5 "
         "C-0.5,6 -1.5,6 -2.5,7.5 C-5,6.5 -5.5,3.5 -4,2.5 "
         "C-6,0.5 -5.5,-3 -3.2,-4 C-4,-6.5 -2.5,-9 0,-10 Z")
    stem = f'<path d="M0,7.5 Q0.5,10 1.5,12" fill="none" stroke="{color}" stroke-width="0.9" stroke-linecap="round"/>'
    vein = f'<path d="M0,-9 Q0.5,0 0.5,7" fill="none" stroke="#00000030" stroke-width="0.5"/>'
    return f'<path d="{d}" fill="{color}"/>{vein}{stem}'

def snow_shape(color, seed=0):
    out = []
    for k in range(6):
        ang = math.radians(60 * k)
        x2, y2 = math.cos(ang) * 5, math.sin(ang) * 5
        out.append(f'<line x1="0" y1="0" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="0.7" stroke-linecap="round"/>')
        for frac in (0.5, 0.78):
            bx, by = math.cos(ang) * 5 * frac, math.sin(ang) * 5 * frac
            for sign in (-1, 1):
                bang = ang + sign * math.radians(40)
                bx2, by2 = bx + math.cos(bang) * 1.6, by + math.sin(bang) * 1.6
                out.append(f'<line x1="{bx:.1f}" y1="{by:.1f}" x2="{bx2:.1f}" y2="{by2:.1f}" stroke="{color}" stroke-width="0.6" stroke-linecap="round"/>')
    return "".join(out)

def petal_shape(color, seed=0):
    d = "M0,-6 C3,-5 3.5,-1.5 1.6,1.5 C1,2.6 -1,2.6 -1.6,1.5 C-3.5,-1.5 -3,-5 0,-6 Z"
    return f'<path d="{d}" fill="{color}"/>'

def note_shape(color, seed=0):
    return (f'<circle cx="0" cy="5" r="2.6" fill="{color}"/>'
           f'<line x1="2.4" y1="5" x2="2.4" y2="-8" stroke="{color}" stroke-width="1.1"/>'
           f'<path d="M2.4,-8 Q6,-7 5.6,-3.5" fill="none" stroke="{color}" stroke-width="1.1"/>')

def star_shape(color, seed=0):
    pts = []
    for k in range(5):
        ang = math.radians(90 + 72 * k)
        pts.append((math.cos(ang) * 4.4, -math.sin(ang) * 4.4))
        ang2 = ang + math.radians(36)
        pts.append((math.cos(ang2) * 1.8, -math.sin(ang2) * 1.8))
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"
    return f'<path d="{d}" fill="{color}"/>'

def cornflower_shape(color, center, seed=0):
    out = []
    for k in range(8):
        ang = math.radians(45 * k)
        x2, y2 = math.cos(ang) * 4.5, math.sin(ang) * 4.5
        out.append(f'<line x1="0" y1="0" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="1.6" stroke-linecap="round"/>')
    out.append(f'<circle cx="0" cy="0" r="1.3" fill="{center}"/>')
    return "".join(out)

def mum_shape(color, center, seed=0):
    out = []
    for k in range(12):
        ang = math.radians(30 * k)
        x2, y2 = math.cos(ang) * 4.2, math.sin(ang) * 4.2
        out.append(f'<line x1="0" y1="0" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="1.2" stroke-linecap="round"/>')
    out.append(f'<circle cx="0" cy="0" r="1.6" fill="{center}"/>')
    return "".join(out)

# ---------- generic falling particles ----------

def falling_particles(kind, n, W, H, colors, seed=1, dur_range=(5.5, 9.5), size_range=(0.7, 1.4), sway=14):
    rng = random.Random(seed)
    shape_fn = {"leaf": leaf_shape, "snow": snow_shape, "petal": petal_shape}[kind]
    out = []
    for i in range(n):
        x0 = rng.uniform(0, W)
        dur = rng.uniform(*dur_range)
        begin = rng.uniform(-dur, 0)
        scale = rng.uniform(*size_range)
        color = colors[i % len(colors)]
        rot0 = rng.uniform(0, 360)
        rot1 = rot0 + rng.choice([-1, 1]) * rng.uniform(120, 320)
        sway_dir = rng.choice([-1, 1]) * sway
        shape = shape_fn(color, seed=i)
        out.append(
            f'<g transform="translate({x0:.1f},-12) scale({scale:.2f})">'
            f'<animateTransform attributeName="transform" type="translate" additive="sum" '
            f'values="0 0;{sway_dir*0.4:.1f} {(H+24)*0.33:.1f};{-sway_dir*0.4:.1f} {(H+24)*0.66:.1f};0 {H+24:.1f}" '
            f'keyTimes="0;0.33;0.66;1" begin="{begin:.2f}s" dur="{dur:.2f}s" repeatCount="indefinite"/>'
            f'<g>'
            f'<animateTransform attributeName="transform" type="rotate" '
            f'from="{rot0:.0f}" to="{rot1:.0f}" begin="{begin:.2f}s" dur="{dur:.2f}s" repeatCount="indefinite"/>'
            f'{shape}'
            f'</g></g>'
        )
    return "".join(out)

def floating_up(kind, n, W, H, colors, seed=1, dur_range=(5, 8)):
    rng = random.Random(seed)
    shape_fn = {"note": note_shape}[kind]
    out = []
    for i in range(n):
        x0 = rng.uniform(20, W - 20)
        dur = rng.uniform(*dur_range)
        begin = rng.uniform(-dur, 0)
        scale = rng.uniform(0.9, 1.6)
        color = colors[i % len(colors)]
        sway = rng.uniform(10, 24) * rng.choice([-1, 1])
        shape = shape_fn(color, seed=i)
        out.append(
            f'<g transform="translate({x0:.1f},{H+10:.1f}) scale({scale:.2f})">'
            f'<animateTransform attributeName="transform" type="translate" additive="sum" '
            f'values="0 0;{sway*0.5:.1f} {-(H+20)*0.5:.1f};0 {-(H+20):.1f}" '
            f'keyTimes="0;0.5;1" begin="{begin:.2f}s" dur="{dur:.2f}s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="rotate" additive="sum" '
            f'values="-8;8;-8" begin="{begin:.2f}s" dur="{dur*0.6:.2f}s" repeatCount="indefinite"/>'
            f'{shape}</g>'
        )
    return "".join(out)

# ---------- Halloween ----------

def jack_o_lantern(cx, cy, s, body, glow, begin=0):
    ridges = []
    for dx in (-0.5, -0.17, 0.17, 0.5):
        ridges.append(f'<path d="M{cx+dx*s:.1f},{cy-s*0.62:.1f} Q{cx+dx*s*1.15:.1f},{cy:.1f} {cx+dx*s:.1f},{cy+s*0.62:.1f}" '
                      f'fill="none" stroke="{body}" stroke-width="1" opacity="0.55"/>')
    body_shape = f'<ellipse cx="{cx}" cy="{cy}" rx="{s*0.62:.1f}" ry="{s*0.5:.1f}" fill="{body}"/>'
    stem = f'<path d="M{cx-2:.1f},{cy-s*0.48:.1f} q2,-8 6,-9" fill="none" stroke="#5a7d3a" stroke-width="3" stroke-linecap="round"/>'
    face = (f'<path d="M{cx-s*0.16:.1f},{cy-s*0.12:.1f} l{s*0.09:.1f},{-s*0.16:.1f} l{s*0.09:.1f},{s*0.16:.1f} Z" fill="{glow}"/>'
           f'<path d="M{cx+s*0.08:.1f},{cy-s*0.12:.1f} l{s*0.09:.1f},{-s*0.16:.1f} l{s*0.09:.1f},{s*0.16:.1f} Z" fill="{glow}"/>'
           f'<path d="M{cx-s*0.22:.1f},{cy+s*0.16:.1f} q{s*0.22:.1f},{s*0.18:.1f} {s*0.44:.1f},0 '
           f'l{-s*0.06:.1f},{-s*0.08:.1f} q{-s*0.16:.1f},{s*0.1:.1f} {-s*0.32:.1f},0 Z" fill="{glow}"/>')
    period = 2.6
    glow_layer = f'<g><animate attributeName="opacity" values="0.5;1;0.5" begin="{begin}s" dur="{period}s" repeatCount="indefinite"/>{face}</g>'
    return f'<g>{"".join(ridges)}{body_shape}{stem}{glow_layer}</g>'

def bat_shape(cx, cy, s, color):
    d = (f"M{cx},{cy-s*0.15:.1f} "
        f"C{cx-s*0.15:.1f},{cy-s*0.5:.1f} {cx-s*0.55:.1f},{cy-s*0.75:.1f} {cx-s:.1f},{cy-s*0.35:.1f} "
        f"C{cx-s*0.7:.1f},{cy-s*0.3:.1f} {cx-s*0.55:.1f},{cy-s*0.15:.1f} {cx-s*0.42:.1f},{cy-s*0.18:.1f} "
        f"C{cx-s*0.55:.1f},{cy-s*0.05:.1f} {cx-s*0.62:.1f},{cy+s*0.15:.1f} {cx-s*0.4:.1f},{cy+s*0.05:.1f} "
        f"C{cx-s*0.25:.1f},{cy+s*0.22:.1f} {cx-s*0.1:.1f},{cy+s*0.12:.1f} {cx},{cy+s*0.3:.1f} "
        f"C{cx+s*0.1:.1f},{cy+s*0.12:.1f} {cx+s*0.25:.1f},{cy+s*0.22:.1f} {cx+s*0.4:.1f},{cy+s*0.05:.1f} "
        f"C{cx+s*0.62:.1f},{cy+s*0.15:.1f} {cx+s*0.55:.1f},{cy-s*0.05:.1f} {cx+s*0.42:.1f},{cy-s*0.18:.1f} "
        f"C{cx+s*0.55:.1f},{cy-s*0.15:.1f} {cx+s*0.7:.1f},{cy-s*0.3:.1f} {cx+s:.1f},{cy-s*0.35:.1f} "
        f"C{cx+s*0.55:.1f},{cy-s*0.75:.1f} {cx+s*0.15:.1f},{cy-s*0.5:.1f} {cx},{cy-s*0.15:.1f} Z")
    ears = (f'<path d="M{cx-s*0.08:.1f},{cy-s*0.2:.1f} l{-s*0.05:.1f},{-s*0.12:.1f} l{s*0.1:.1f},{s*0.02:.1f} Z '
           f'M{cx+s*0.08:.1f},{cy-s*0.2:.1f} l{s*0.05:.1f},{-s*0.12:.1f} l{-s*0.1:.1f},{s*0.02:.1f} Z" fill="{color}"/>')
    return f'<path d="{d}" fill="{color}"/>{ears}'

def scene_bat(y, color, dur=9, begin=0, s=16):
    return (
        f'<g transform="translate(-20,{y})">'
        f'<animateTransform attributeName="transform" type="translate" additive="sum" '
        f'values="0 0;1040 -14;1040 -14" keyTimes="0;0.999;1" begin="{begin}s" dur="{dur}s" repeatCount="indefinite"/>'
        f'<g><animateTransform attributeName="transform" type="scale" values="1,1;1,0.55;1,1" begin="{begin}s" dur="0.45s" repeatCount="indefinite"/>'
        f'{bat_shape(0, 0, s, color)}</g></g>'
    )

def scene_fog(W, H, color, seed=9):
    rng = random.Random(seed)
    out = []
    for i in range(3):
        y = rng.uniform(H * 0.55, H - 12)
        dur = rng.uniform(14, 20)
        begin = -rng.uniform(0, dur)
        out.append(f'<ellipse cx="0" cy="{y:.1f}" rx="120" ry="14" fill="{color}" opacity="0.10">'
                   f'<animate attributeName="cx" values="{-150};{W+150}" begin="{begin:.1f}s" dur="{dur:.1f}s" repeatCount="indefinite"/>'
                   f'</ellipse>')
    return "".join(out)

# ---------- Christmas ----------

def scene_tree(cx, base_y, s, trunk, green, lights):
    trunk_h = s * 0.22
    trunk_w = s * 0.16
    out = [f'<rect x="{cx-trunk_w/2:.1f}" y="{base_y-trunk_h:.1f}" width="{trunk_w:.1f}" height="{trunk_h:.1f}" fill="{trunk}"/>']
    tiers = 3
    tier_h = s * 0.4
    overlap = 0.45
    tier_geoms = []
    cur_base_y = base_y - trunk_h
    widths = [s * 0.98, s * 0.72, s * 0.46]
    for t in range(tiers):
        w = widths[t]
        apex_y = cur_base_y - tier_h
        tier_geoms.append((apex_y, cur_base_y, w))
        cur_base_y = apex_y + tier_h * overlap
    for apex_y, base_yy, w in tier_geoms:
        out.append(f'<path d="M{cx},{apex_y:.1f} L{cx+w/2:.1f},{base_yy:.1f} L{cx-w/2:.1f},{base_yy:.1f} Z" fill="{green}"/>')
    top_apex_y = tier_geoms[-1][0]
    out.append(f'<path d="M{cx},{top_apex_y-s*0.16:.1f} l{s*0.07:.1f},{s*0.16:.1f} l-{s*0.14:.1f},0 Z" fill="{lights[0]}"/>')
    rng = random.Random(3)
    for i in range(9):
        t = rng.randint(0, tiers - 1)
        apex_y, base_yy, w = tier_geoms[t]
        frac = rng.uniform(0.25, 0.92)
        ly = apex_y + frac * (base_yy - apex_y)
        half_w_here = (w / 2) * frac
        lx = cx + rng.uniform(-1, 1) * half_w_here * 0.85
        c = lights[i % len(lights)]
        out.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="1.7" fill="{c}">'
                   f'<animate attributeName="opacity" values="1;0.25;1" begin="{i*0.28:.2f}s" dur="1.6s" repeatCount="indefinite"/></circle>')
    return "".join(out)

def sleigh_group(color, accent, skin):
    # reindeer leads on the RIGHT (positive x) so it looks correct when the
    # whole group travels left-to-right (was backwards before)
    sleigh = (f'<path d="M2,10 L-34,10 Q-40,10 -40,4 L-40,-8 Q-40,-14 -34,-14 Q-30,-14 -30,-10 '
             f'L-30,4 L2,4 Q6,4 6,7 Q6,10 2,10 Z" fill="{color}"/>')
    santa = (f'<ellipse cx="-14" cy="-4" rx="9" ry="10" fill="{accent}"/>'
            f'<circle cx="-14" cy="-16" r="5.5" fill="{skin}"/>'
            f'<path d="M-9,-19 Q-14,-30 -22,-22 Q-17,-23 -14,-19 Z" fill="{accent}"/>'
            f'<circle cx="-22" cy="-22" r="2" fill="{color}"/>')
    rx = 34
    reindeer = (f'<ellipse cx="{rx}" cy="2" rx="11" ry="6" fill="{skin}"/>'
               f'<circle cx="{rx+13}" cy="-4" r="5" fill="{skin}"/>'
               f'<path d="M{rx+16},-8 L{rx+20},-16 M{rx+16},-8 L{rx+13},-17" stroke="{skin}" stroke-width="1.3"/>'
               f'<line x1="{rx-6}" y1="7" x2="{rx-6}" y2="14" stroke="{skin}" stroke-width="2"/>'
               f'<line x1="{rx+6}" y1="7" x2="{rx+6}" y2="14" stroke="{skin}" stroke-width="2"/>'
               f'<circle cx="{rx+18}" cy="-4" r="1.3" fill="{color}"/>')
    rein = f'<path d="M{rx+2},-2 Q10,-2 4,6" fill="none" stroke="{skin}" stroke-width="1" opacity="0.7"/>'
    return sleigh + santa + reindeer + rein

def scene_santa(y, color, accent, skin, dur=13, begin=0):
    g = sleigh_group(color, accent, skin)
    return (
        f'<g transform="translate(-70,{y}) scale(0.55)">'
        f'<animateTransform attributeName="transform" type="translate" additive="sum" '
        f'values="0 0;1900 -60;1900 -60" keyTimes="0;0.999;1" begin="{begin}s" dur="{dur}s" repeatCount="indefinite"/>'
        f'{g}</g>'
    )

# ---------- Summer ----------

def scene_sun(cx, cy, s, color):
    out = [f'<circle cx="{cx}" cy="{cy}" r="{s*0.62:.1f}" fill="{color}"/>']
    for k in range(10):
        ang = math.radians(36 * k)
        x1, y1 = cx + math.cos(ang) * s * 0.78, cy + math.sin(ang) * s * 0.78
        x2, y2 = cx + math.cos(ang) * s * 1.05, cy + math.sin(ang) * s * 1.05
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="1.6" stroke-linecap="round"/>')
    return (f'<g transform="translate(0,0)">'
           f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="40s" repeatCount="indefinite"/>'
           f'{"".join(out)}</g>')

def beachball_shape(s, colors):
    wedges = []
    for k in range(6):
        a0, a1 = math.radians(60 * k), math.radians(60 * (k + 1))
        x0, y0 = math.cos(a0) * s, math.sin(a0) * s
        x1, y1 = math.cos(a1) * s, math.sin(a1) * s
        wedges.append(f'<path d="M0,0 L{x0:.1f},{y0:.1f} A{s},{s} 0 0,1 {x1:.1f},{y1:.1f} Z" fill="{colors[k%len(colors)]}"/>')
    return f'<circle r="{s}" fill="{colors[-1]}"/>' + "".join(wedges)

def scene_beachball_pass(y0, y1, s, colors, x_start, x_end, dur, begin=0):
    ball = beachball_shape(s, colors)
    mid_y = min(y0, y1) - s * 2.6
    return (
        f'<g transform="translate({x_start},{y0})">'
        f'<animateTransform attributeName="transform" type="translate" additive="sum" '
        f'values="0 0;{(x_end-x_start)/2:.1f} {mid_y-y0:.1f};{x_end-x_start:.1f} {y1-y0:.1f};'
        f'{(x_end-x_start)/2:.1f} {mid_y-y0:.1f};0 0" '
        f'keyTimes="0;0.25;0.5;0.75;1" begin="{begin}s" dur="{dur}s" repeatCount="indefinite"/>'
        f'<g><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="{dur/2.2:.1f}s" repeatCount="indefinite"/>{ball}</g>'
        f'</g>'
    )

# ---------- Easter ----------

def scene_egg(cx, cy, s, color, accent):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{s*0.72:.1f}" ry="{s}" fill="{color}"/>'
           f'<circle cx="{cx-s*0.2:.1f}" cy="{cy-s*0.3:.1f}" r="{s*0.14:.1f}" fill="{accent}" opacity="0.7"/>'
           f'<circle cx="{cx+s*0.15:.1f}" cy="{cy+s*0.1:.1f}" r="{s*0.1:.1f}" fill="{accent}" opacity="0.7"/>')

def scene_bunny(stops, dur, color):
    """Hops smoothly between stops (continuous interpolated movement with a
    little arc per leg, not a teleport) and loops back to the first stop."""
    pts = stops + [stops[0]]
    n = len(pts)
    xs, ys, kt = [], [], []
    for i, (x, y) in enumerate(pts):
        kt.append(i / (n - 1))
        xs.append(x)
        ys.append(y)
        if i < n - 1:
            nx, ny = pts[i + 1]
            mx, my = (x + nx) / 2, min(y, ny) - 14  # hop apex, higher = further up
            kt.append((i + 0.5) / (n - 1))
            xs.append(mx)
            ys.append(my)
    key_times = ";".join(str(round(t, 4)) for t in kt)
    vals = ";".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    return (
        f'<g transform="translate({xs[0]:.1f},{ys[0]:.1f})">'
        f'<animateTransform attributeName="transform" type="translate" calcMode="linear" '
        f'values="{vals}" keyTimes="{key_times}" dur="{dur}s" repeatCount="indefinite"/>'
        f'<g>'
        f'<animateTransform attributeName="transform" type="scale" additive="sum" '
        f'values="1,1;1,0.85;1,1" dur="0.4s" repeatCount="indefinite"/>'
        f'<ellipse cx="0" cy="0" rx="6" ry="5" fill="{color}"/>'
        f'<ellipse cx="0" cy="-8" rx="3.6" ry="3.6" fill="{color}"/>'
        f'<path d="M-2,-11 Q-3,-18 -1,-11" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round"/>'
        f'<path d="M2,-11 Q3,-18 1,-11" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round"/>'
        f'</g></g>'
    )

# ---------- Fireworks / New Year / Bastille Day ----------

def scene_firework(cx, cy, s, color, begin, dur=2.6):
    lines = []
    for k in range(8):
        ang = math.radians(45 * k)
        x2, y2 = cx + math.cos(ang) * s, cy + math.sin(ang) * s
        lines.append(f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="1" stroke-linecap="round"/>')
        lines.append(f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="0.9" fill="{color}"/>')
    # small, stays put - just appears and disappears, no growth/movement
    return (f'<g opacity="0">'
           f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.2;0.7;1" begin="{begin}s" dur="{dur}s" repeatCount="indefinite"/>'
           f'{"".join(lines)}</g>')

def scene_banner(cx, cy, w, h, color, text_color, text, font="Sora, sans-serif"):
    notch = h * 0.5
    d = (f"M{cx-w/2},{cy-h/2} L{cx+w/2},{cy-h/2} L{cx+w/2-notch*0.5},{cy} L{cx+w/2},{cy+h/2} "
        f"L{cx-w/2},{cy+h/2} L{cx-w/2+notch*0.5},{cy} Z")
    return (f'<path d="{d}" fill="{color}"/>'
           f'<text x="{cx}" y="{cy+h*0.16:.1f}" font-family="{font}" font-size="{h*0.55:.1f}" '
           f'font-weight="700" fill="{text_color}" text-anchor="middle">{text}</text>')

def eiffel_tower(cx, base_y, s, color):
    top = base_y - s
    return (f'<path d="M{cx-s*0.42:.1f},{base_y:.1f} L{cx-s*0.06:.1f},{top:.1f} L{cx+s*0.06:.1f},{top:.1f} '
           f'L{cx+s*0.42:.1f},{base_y:.1f}" fill="none" stroke="{color}" stroke-width="{s*0.045:.1f}"/>'
           f'<line x1="{cx-s*0.30:.1f}" y1="{base_y-s*0.3:.1f}" x2="{cx+s*0.30:.1f}" y2="{base_y-s*0.3:.1f}" stroke="{color}" stroke-width="{s*0.03:.1f}"/>'
           f'<line x1="{cx-s*0.16:.1f}" y1="{base_y-s*0.65:.1f}" x2="{cx+s*0.16:.1f}" y2="{base_y-s*0.65:.1f}" stroke="{color}" stroke-width="{s*0.03:.1f}"/>')

def jet_patrol(y, dur, begin, trail_colors):
    """A small jet silhouette flying left-to-right trailing 3 colour smoke lines
    (bleu-blanc-rouge, like the Patrouille de France)."""
    jet = ('<path d="M0,0 L-14,4 L-10,0 L-14,-4 Z" fill="#8a8a95"/>'
          '<path d="M-4,0 L-9,7 L-6,7 L-2,1 Z" fill="#8a8a95"/>'
          '<path d="M-4,0 L-9,-7 L-6,-7 L-2,-1 Z" fill="#8a8a95"/>')
    trails = []
    for i, c in enumerate(trail_colors):
        dy = (i - 1) * 2.6
        trails.append(f'<path d="M-14,{dy:.1f} L-90,{dy:.1f}" stroke="{c}" stroke-width="2" opacity="0.55" stroke-linecap="round">'
                      f'<animate attributeName="opacity" values="0;0.55;0.55" keyTimes="0;0.08;1" '
                      f'begin="{begin}s" dur="{dur}s" repeatCount="indefinite"/></path>')
    return (
        f'<g transform="translate(-40,{y})">'
        f'<animateTransform attributeName="transform" type="translate" additive="sum" '
        f'values="0 0;1080 0;1080 0" keyTimes="0;0.999;1" begin="{begin}s" dur="{dur}s" repeatCount="indefinite"/>'
        f'{"".join(trails)}{jet}</g>'
    )

# ---------- Chinese New Year ----------

def paper_lantern(cx, cy, s, color, gold, begin):
    body = f'<ellipse cx="0" cy="0" rx="{s*0.55:.1f}" ry="{s*0.7:.1f}" fill="{color}"/>'
    caps = (f'<rect x="{-s*0.2:.1f}" y="{-s*0.78:.1f}" width="{s*0.4:.1f}" height="{s*0.1:.1f}" fill="{gold}"/>'
           f'<rect x="{-s*0.2:.1f}" y="{s*0.68:.1f}" width="{s*0.4:.1f}" height="{s*0.1:.1f}" fill="{gold}"/>')
    ribs = "".join(f'<line x1="{x:.1f}" y1="{-s*0.68:.1f}" x2="{x:.1f}" y2="{s*0.68:.1f}" stroke="{gold}" stroke-width="0.5" opacity="0.5"/>'
                   for x in (-s*0.3, 0, s*0.3))
    tassel = f'<line x1="0" y1="{s*0.78:.1f}" x2="0" y2="{s*1.05:.1f}" stroke="{gold}" stroke-width="1"/>'
    string = f'<line x1="0" y1="{-s*0.78:.1f}" x2="0" y2="{-s*1.1:.1f}" stroke="{gold}" stroke-width="0.8"/>'
    return (f'<g transform="translate({cx},{cy})">'
           f'<animateTransform attributeName="transform" type="rotate" values="-4;4;-4" '
           f'begin="{begin}s" dur="3.2s" repeatCount="indefinite" additive="sum"/>'
           f'{string}{body}{ribs}{caps}{tassel}</g>')

def firecracker_burst(cx, cy, s, color, begin):
    dots = []
    rng = random.Random(int(cx))
    for i in range(6):
        ang = rng.uniform(0, 6.28)
        r = s * rng.uniform(0.5, 1)
        dots.append(f'<circle cx="{math.cos(ang)*r:.1f}" cy="{math.sin(ang)*r:.1f}" r="1.1" fill="{color}"/>')
    return (f'<g transform="translate({cx},{cy})" opacity="0">'
           f'<animate attributeName="opacity" values="0;1;0" begin="{begin}s" dur="0.9s" repeatCount="indefinite"/>'
           f'{"".join(dots)}</g>')

# ---------- Chinese zodiac animals (simple shared body+head template) ----------

def _critter_base(cx, cy, s, color, ears, extras_back="", extras_front=""):
    body = f'<ellipse cx="{cx}" cy="{cy+s*0.35:.1f}" rx="{s*0.85:.1f}" ry="{s*0.62:.1f}" fill="{color}"/>'
    head = f'<circle cx="{cx}" cy="{cy-s*0.15:.1f}" r="{s*0.5:.1f}" fill="{color}"/>'
    return extras_back + body + ears + head + extras_front

def zodiac_rat(cx, cy, s, color):
    ears = f'<circle cx="{cx-s*0.38:.1f}" cy="{cy-s*0.5:.1f}" r="{s*0.22:.1f}" fill="{color}"/><circle cx="{cx+s*0.38:.1f}" cy="{cy-s*0.5:.1f}" r="{s*0.22:.1f}" fill="{color}"/>'
    tail = f'<path d="M{cx+s*0.8:.1f},{cy+s*0.5:.1f} Q{cx+s*1.6:.1f},{cy+s*0.1:.1f} {cx+s*2.1:.1f},{cy+s*0.5:.1f}" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round"/>'
    nose = f'<circle cx="{cx}" cy="{cy-s*0.05:.1f}" r="{s*0.08:.1f}" fill="#2a2733"/>'
    return _critter_base(cx, cy, s, color, ears, extras_back=tail, extras_front=nose)

def zodiac_ox(cx, cy, s, color):
    horns = (f'<path d="M{cx-s*0.15:.1f},{cy-s*0.5:.1f} Q{cx-s*0.65:.1f},{cy-s*0.6:.1f} {cx-s*0.55:.1f},{cy-s*1.0:.1f}" fill="none" stroke="{color}" stroke-width="{s*0.16:.1f}" stroke-linecap="round"/>'
             f'<path d="M{cx+s*0.15:.1f},{cy-s*0.5:.1f} Q{cx+s*0.65:.1f},{cy-s*0.6:.1f} {cx+s*0.55:.1f},{cy-s*1.0:.1f}" fill="none" stroke="{color}" stroke-width="{s*0.16:.1f}" stroke-linecap="round"/>')
    snout = f'<ellipse cx="{cx}" cy="{cy+s*0.1:.1f}" rx="{s*0.28:.1f}" ry="{s*0.18:.1f}" fill="#2a2733"/>'
    return _critter_base(cx, cy, s, color, horns, extras_front=snout)

def zodiac_tiger(cx, cy, s, color):
    ears = f'<path d="M{cx-s*0.42:.1f},{cy-s*0.42:.1f} l{-s*0.24:.1f},{-s*0.34:.1f} l{s*0.34:.1f},{s*0.06:.1f} Z" fill="{color}"/><path d="M{cx+s*0.42:.1f},{cy-s*0.42:.1f} l{s*0.24:.1f},{-s*0.34:.1f} l{-s*0.34:.1f},{s*0.06:.1f} Z" fill="{color}"/>'
    stripes = "".join(f'<line x1="{cx-s*0.55+i*s*0.35:.1f}" y1="{cy+s*0.05:.1f}" x2="{cx-s*0.42+i*s*0.35:.1f}" y2="{cy+s*0.8:.1f}" stroke="#2a2733" stroke-width="1.8"/>' for i in range(4))
    return _critter_base(cx, cy, s, color, ears, extras_back=stripes)

def zodiac_rabbit(cx, cy, s, color):
    ears = f'<ellipse cx="{cx-s*0.22:.1f}" cy="{cy-s*0.85:.1f}" rx="{s*0.14:.1f}" ry="{s*0.45:.1f}" fill="{color}"/><ellipse cx="{cx+s*0.22:.1f}" cy="{cy-s*0.85:.1f}" rx="{s*0.14:.1f}" ry="{s*0.45:.1f}" fill="{color}"/>'
    return _critter_base(cx, cy, s, color, ears)

def zodiac_snake(cx, cy, s, color):
    d = f"M{cx-s*1.4:.1f},{cy+s*0.3:.1f} Q{cx-s*0.7:.1f},{cy-s*0.5:.1f} {cx:.1f},{cy+s*0.3:.1f} Q{cx+s*0.7:.1f},{cy+s*1.1:.1f} {cx+s*1.2:.1f},{cy+s*0.3:.1f}"
    body_l = f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{s*0.42:.1f}" stroke-linecap="round"/>'
    head = f'<circle cx="{cx+s*1.3:.1f}" cy="{cy+s*0.25:.1f}" r="{s*0.28:.1f}" fill="{color}"/>'
    tongue = f'<line x1="{cx+s*1.55:.1f}" y1="{cy+s*0.2:.1f}" x2="{cx+s*1.8:.1f}" y2="{cy+s*0.15:.1f}" stroke="#e05a5a" stroke-width="1"/>'
    return body_l + head + tongue

def zodiac_horse(cx, cy, s, color):
    ears = f'<path d="M{cx-s*0.2:.1f},{cy-s*0.5:.1f} l{-s*0.08:.1f},{-s*0.2:.1f} l{s*0.18:.1f},{s*0.08:.1f} Z" fill="{color}"/><path d="M{cx+s*0.2:.1f},{cy-s*0.5:.1f} l{s*0.08:.1f},{-s*0.2:.1f} l{-s*0.18:.1f},{s*0.08:.1f} Z" fill="{color}"/>'
    mane = "".join(f'<line x1="{cx-s*0.15+i*s*0.15:.1f}" y1="{cy-s*0.45:.1f}" x2="{cx-s*0.2+i*s*0.15:.1f}" y2="{cy-s*0.78:.1f}" stroke="{color}" stroke-width="{s*0.11:.1f}" stroke-linecap="round"/>' for i in range(4))
    legs = "".join(f'<line x1="{cx-s*0.5+i*s*0.35:.1f}" y1="{cy+s*0.85:.1f}" x2="{cx-s*0.5+i*s*0.35:.1f}" y2="{cy+s*1.3:.1f}" stroke="{color}" stroke-width="{s*0.15:.1f}" stroke-linecap="round"/>' for i in range(3))
    snout = f'<ellipse cx="{cx}" cy="{cy+s*0.08:.1f}" rx="{s*0.18:.1f}" ry="{s*0.12:.1f}" fill="{color}"/>'
    return _critter_base(cx, cy, s, color, ears, extras_back=legs + mane, extras_front=snout)

def zodiac_goat(cx, cy, s, color):
    horns = (f'<path d="M{cx-s*0.1:.1f},{cy-s*0.5:.1f} Q{cx-s*0.5:.1f},{cy-s*0.45:.1f} {cx-s*0.5:.1f},{cy-s*0.9:.1f}" fill="none" stroke="{color}" stroke-width="{s*0.13:.1f}" stroke-linecap="round"/>'
             f'<path d="M{cx+s*0.1:.1f},{cy-s*0.5:.1f} Q{cx+s*0.5:.1f},{cy-s*0.45:.1f} {cx+s*0.5:.1f},{cy-s*0.9:.1f}" fill="none" stroke="{color}" stroke-width="{s*0.13:.1f}" stroke-linecap="round"/>')
    beard = f'<path d="M{cx-s*0.05:.1f},{cy+s*0.3:.1f} L{cx+s*0.05:.1f},{cy+s*0.3:.1f} L{cx:.1f},{cy+s*0.55:.1f} Z" fill="{color}"/>'
    return _critter_base(cx, cy, s, color, horns, extras_front=beard)

def zodiac_monkey(cx, cy, s, color):
    ears = f'<circle cx="{cx-s*0.48:.1f}" cy="{cy-s*0.2:.1f}" r="{s*0.2:.1f}" fill="{color}"/><circle cx="{cx+s*0.48:.1f}" cy="{cy-s*0.2:.1f}" r="{s*0.2:.1f}" fill="{color}"/>'
    face = f'<ellipse cx="{cx}" cy="{cy}" rx="{s*0.3:.1f}" ry="{s*0.26:.1f}" fill="#e8c9a0"/>'
    tail = f'<path d="M{cx+s*0.8:.1f},{cy+s*0.5:.1f} Q{cx+s*1.5:.1f},{cy+s*0.6:.1f} {cx+s*1.4:.1f},{cy-s*0.1:.1f}" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round"/>'
    return _critter_base(cx, cy, s, color, ears, extras_back=tail, extras_front=face)

def zodiac_rooster(cx, cy, s, color):
    comb = f'<path d="M{cx-s*0.2:.1f},{cy-s*0.55:.1f} q{s*0.05:.1f},{-s*0.3:.1f} {s*0.15:.1f},{-s*0.1:.1f} q{s*0.05:.1f},{-s*0.25:.1f} {s*0.15:.1f},{-s*0.05:.1f} q{s*0.05:.1f},{-s*0.22:.1f} {s*0.15:.1f},0" fill="none" stroke="#c0392b" stroke-width="{s*0.14:.1f}" stroke-linecap="round"/>'
    wattle = f'<path d="M{cx+s*0.15:.1f},{cy+s*0.05:.1f} q{s*0.1:.1f},{s*0.15:.1f} 0,{s*0.28:.1f}" fill="none" stroke="#c0392b" stroke-width="{s*0.1:.1f}" stroke-linecap="round"/>'
    tail = f'<path d="M{cx-s*0.75:.1f},{cy+s*0.3:.1f} Q{cx-s*1.3:.1f},{cy-s*0.3:.1f} {cx-s*1.1:.1f},{cy-s*0.8:.1f} M{cx-s*0.75:.1f},{cy+s*0.4:.1f} Q{cx-s*1.35:.1f},{cy:.1f} {cx-s*1.3:.1f},{cy-s*0.5:.1f}" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round"/>'
    beak = f'<path d="M{cx+s*0.42:.1f},{cy-s*0.1:.1f} l{s*0.18:.1f},{s*0.06:.1f} l{-s*0.16:.1f},{s*0.12:.1f} Z" fill="#e8a13a"/>'
    return _critter_base(cx, cy, s, color, comb, extras_back=tail, extras_front=wattle + beak)

def zodiac_dog(cx, cy, s, color):
    ears = f'<path d="M{cx-s*0.35:.1f},{cy-s*0.3:.1f} q{-s*0.35:.1f},{s*0.05:.1f} {-s*0.3:.1f},{s*0.45:.1f}" fill="none" stroke="{color}" stroke-width="{s*0.24:.1f}" stroke-linecap="round"/><path d="M{cx+s*0.35:.1f},{cy-s*0.3:.1f} q{s*0.35:.1f},{s*0.05:.1f} {s*0.3:.1f},{s*0.45:.1f}" fill="none" stroke="{color}" stroke-width="{s*0.24:.1f}" stroke-linecap="round"/>'
    tail = f'<path d="M{cx-s*0.8:.1f},{cy+s*0.4:.1f} Q{cx-s*1.3:.1f},{cy:.1f} {cx-s*1.1:.1f},{cy-s*0.4:.1f}" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round"/>'
    nose = f'<circle cx="{cx}" cy="{cy-s*0.05:.1f}" r="{s*0.08:.1f}" fill="#2a2733"/>'
    return _critter_base(cx, cy, s, color, ears, extras_back=tail, extras_front=nose)

def zodiac_pig(cx, cy, s, color):
    ears = f'<path d="M{cx-s*0.35:.1f},{cy-s*0.45:.1f} l{-s*0.15:.1f},{-s*0.22:.1f} l{s*0.28:.1f},{s*0.08:.1f} Z" fill="{color}"/><path d="M{cx+s*0.35:.1f},{cy-s*0.45:.1f} l{s*0.15:.1f},{-s*0.22:.1f} l{-s*0.28:.1f},{s*0.08:.1f} Z" fill="{color}"/>'
    snout = f'<ellipse cx="{cx}" cy="{cy+s*0.05:.1f}" rx="{s*0.22:.1f}" ry="{s*0.16:.1f}" fill="#e8a3a0"/>'
    nostrils = f'<circle cx="{cx-s*0.06:.1f}" cy="{cy+s*0.05:.1f}" r="{s*0.03:.1f}" fill="#2a2733"/><circle cx="{cx+s*0.06:.1f}" cy="{cy+s*0.05:.1f}" r="{s*0.03:.1f}" fill="#2a2733"/>'
    tail = f'<path d="M{cx+s*0.8:.1f},{cy+s*0.4:.1f} q{s*0.3:.1f},0 {s*0.25:.1f},{-s*0.25:.1f} q{-s*0.05:.1f},{-s*0.2:.1f} {s*0.15:.1f},{-s*0.15:.1f}" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round"/>'
    return _critter_base(cx, cy, s, color, ears, extras_back=tail, extras_front=snout + nostrils)

ZODIAC_SHAPES = {
    "rat": zodiac_rat, "ox": zodiac_ox, "tiger": zodiac_tiger, "rabbit": zodiac_rabbit,
    "snake": zodiac_snake, "horse": zodiac_horse, "goat": zodiac_goat, "monkey": zodiac_monkey,
    "rooster": zodiac_rooster, "dog": zodiac_dog, "pig": zodiac_pig,
}

def chinese_dragon(y, s, color, gold, dur, begin):
    segs = 7
    path_pts = []
    for i in range(segs):
        px = i * 90
        py = math.sin(i * 0.9) * 14
        path_pts.append((px, py))
    d = "M" + " ".join(f"{'L' if i else ''}{x},{y}" for i, (x, y) in enumerate(path_pts))
    body = f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{s:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
    bumps = "".join(f'<circle cx="{x}" cy="{yy}" r="{s*0.28:.1f}" fill="{gold}"/>' for x, yy in path_pts[::2])
    hx, hy = path_pts[0]
    head = (f'<circle cx="{hx-6}" cy="{hy}" r="{s*0.85:.1f}" fill="{color}"/>'
           f'<path d="M{hx-6-s*0.6:.1f},{hy-s*0.3:.1f} l-6,-6 M{hx-6-s*0.6:.1f},{hy+s*0.3:.1f} l-6,6" '
           f'stroke="{gold}" stroke-width="1.4" stroke-linecap="round"/>'
           f'<circle cx="{hx-6-s*0.3:.1f}" cy="{hy-s*0.15:.1f}" r="1.3" fill="{gold}"/>')
    return (
        f'<g transform="translate(-80,{y-y})">'
        f'<animateTransform attributeName="transform" type="translate" additive="sum" '
        f'values="0 0;1140 0;1140 0" keyTimes="0;0.999;1" begin="{begin}s" dur="{dur}s" repeatCount="indefinite"/>'
        f'<g transform="translate(0,{-y})">{body}{bumps}{head}</g></g>'
    )

def envelope_shape(cx, cy, s, color, gold):
    return (f'<rect x="{cx-s*0.4:.1f}" y="{cy-s*0.55:.1f}" width="{s*0.8:.1f}" height="{s*1.1:.1f}" rx="2" fill="{color}"/>'
           f'<path d="M{cx-s*0.4:.1f},{cy-s*0.55:.1f} L{cx:.1f},{cy:.1f} L{cx+s*0.4:.1f},{cy-s*0.55:.1f}" '
           f'fill="none" stroke="{gold}" stroke-width="0.8"/>'
           f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{s*0.12:.1f}" fill="{gold}"/>')

# ---------- Épiphanie / Chandeleur / Mardi Gras ----------

def galette(cx, cy, s, color, gold):
    base = f'<circle cx="{cx}" cy="{cy}" r="{s}" fill="{color}"/>'
    lattice = []
    for k in range(6):
        ang = math.radians(60 * k)
        x2, y2 = cx + math.cos(ang) * s * 0.85, cy + math.sin(ang) * s * 0.85
        lattice.append(f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{gold}" stroke-width="1" opacity="0.5"/>')
    ring = f'<circle cx="{cx}" cy="{cy}" r="{s*0.9:.1f}" fill="none" stroke="{gold}" stroke-width="1.4" opacity="0.7"/>'
    return base + "".join(lattice) + ring

def crown_shape(cx, cy, s, gold, jewel):
    d = (f"M{cx-s*0.6:.1f},{cy+s*0.3:.1f} L{cx-s*0.6:.1f},{cy-s*0.1:.1f} L{cx-s*0.3:.1f},{cy+s*0.15:.1f} "
        f"L{cx-s*0.12:.1f},{cy-s*0.35:.1f} L{cx:.1f},{cy+s*0.05:.1f} L{cx+s*0.12:.1f},{cy-s*0.35:.1f} "
        f"L{cx+s*0.3:.1f},{cy+s*0.15:.1f} L{cx+s*0.6:.1f},{cy-s*0.1:.1f} L{cx+s*0.6:.1f},{cy+s*0.3:.1f} Z")
    jewels = "".join(f'<circle cx="{cx+dx*s:.1f}" cy="{cy+s*0.15:.1f}" r="{s*0.08:.1f}" fill="{jewel}"/>' for dx in (-0.3, 0, 0.3))
    return f'<path d="{d}" fill="{gold}"/>{jewels}'

def crepe_pan(cx, cy, s, batter, pan_color, begin):
    pan = f'<ellipse cx="{cx}" cy="{cy+s*0.1:.1f}" rx="{s}" ry="{s*0.32:.1f}" fill="{pan_color}"/>'
    crepe = (f'<g transform="translate({cx},{cy-s*0.15:.1f})">'
            f'<animateTransform attributeName="transform" type="rotate" values="0;360" '
            f'begin="{begin}s" dur="2.6s" repeatCount="indefinite" additive="sum"/>'
            f'<ellipse cx="0" cy="0" rx="{s*0.82:.1f}" ry="{s*0.26:.1f}" fill="{batter}"/>'
            f'</g>')
    handle = f'<rect x="{cx+s*0.9:.1f}" y="{cy+s*0.02:.1f}" width="{s*0.7:.1f}" height="{s*0.16:.1f}" rx="3" fill="{pan_color}"/>'
    return pan + crepe + handle

def confetti_burst(W, H, colors, n=18, seed=5):
    rng = random.Random(seed)
    out = []
    for i in range(n):
        x0 = rng.uniform(0, W)
        dur = rng.uniform(4, 7)
        begin = rng.uniform(-dur, 0)
        c = colors[i % len(colors)]
        rot0 = rng.uniform(0, 360)
        rot1 = rot0 + rng.uniform(200, 500)
        out.append(
            f'<rect x="-2" y="-2" width="4" height="4" fill="{c}" transform="translate({x0:.1f},-10)">'
            f'<animateTransform attributeName="transform" type="translate" additive="sum" '
            f'values="0 0;0 {H+20:.1f}" begin="{begin:.2f}s" dur="{dur:.2f}s" repeatCount="indefinite"/>'
            f'</rect>'
        )
        out.append(
            f'<g transform="translate({x0:.1f},-10)">'
            f'<animateTransform attributeName="transform" type="translate" additive="sum" '
            f'values="0 0;0 {H+20:.1f}" begin="{begin:.2f}s" dur="{dur:.2f}s" repeatCount="indefinite"/>'
            f'<rect x="-2" y="-2" width="4" height="4" fill="{c}">'
            f'<animateTransform attributeName="transform" type="rotate" from="{rot0:.0f}" to="{rot1:.0f}" '
            f'begin="{begin:.2f}s" dur="{dur:.2f}s" repeatCount="indefinite"/>'
            f'</rect></g>'
        )
    return "".join(out)

def mask_shape(cx, cy, s, color, gold):
    d = (f"M{cx-s:.1f},{cy:.1f} Q{cx-s:.1f},{cy-s*0.7:.1f} {cx-s*0.2:.1f},{cy-s*0.5:.1f} "
        f"Q{cx:.1f},{cy-s*0.65:.1f} {cx+s*0.2:.1f},{cy-s*0.5:.1f} Q{cx+s:.1f},{cy-s*0.7:.1f} {cx+s:.1f},{cy:.1f} "
        f"Q{cx+s:.1f},{cy+s*0.5:.1f} {cx:.1f},{cy+s*0.4:.1f} Q{cx-s:.1f},{cy+s*0.5:.1f} {cx-s:.1f},{cy:.1f} Z")
    eyes = (f'<ellipse cx="{cx-s*0.4:.1f}" cy="{cy-s*0.05:.1f}" rx="{s*0.18:.1f}" ry="{s*0.12:.1f}" fill="none" stroke="{gold}" stroke-width="1"/>'
           f'<ellipse cx="{cx+s*0.4:.1f}" cy="{cy-s*0.05:.1f}" rx="{s*0.18:.1f}" ry="{s*0.12:.1f}" fill="none" stroke="{gold}" stroke-width="1"/>')
    swirl = f'<path d="M{cx-s*0.15:.1f},{cy-s*0.55:.1f} q{s*0.3:.1f},{-s*0.35:.1f} {s*0.5:.1f},{-s*0.1:.1f}" fill="none" stroke="{gold}" stroke-width="1.2"/>'
    return f'<path d="{d}" fill="{color}"/>{eyes}{swirl}'

# ---------- Hearts / flowers / gifts ----------

def heart_shape(color, seed=0):
    d = "M0,4 C-6,-2 -6,-7 -2,-7 C-0.7,-7 0,-5.5 0,-5 C0,-5.5 0.7,-7 2,-7 C6,-7 6,-2 0,4 Z"
    return f'<path d="{d}" fill="{color}"/>'

def gift_box(cx, cy, s, box_color, ribbon):
    body = f'<rect x="{cx-s*0.6:.1f}" y="{cy-s*0.4:.1f}" width="{s*1.2:.1f}" height="{s*0.9:.1f}" rx="2" fill="{box_color}"/>'
    lid = f'<rect x="{cx-s*0.68:.1f}" y="{cy-s*0.55:.1f}" width="{s*1.36:.1f}" height="{s*0.22:.1f}" rx="2" fill="{box_color}" opacity="0.85"/>'
    vband = f'<rect x="{cx-s*0.08:.1f}" y="{cy-s*0.55:.1f}" width="{s*0.16:.1f}" height="{s*0.85:.1f}" fill="{ribbon}"/>'
    bow = (f'<path d="M{cx:.1f},{cy-s*0.55:.1f} q{-s*0.3:.1f},{-s*0.32:.1f} {-s*0.5:.1f},{-s*0.05:.1f} '
          f'q{s*0.2:.1f},{s*0.2:.1f} {s*0.5:.1f},{s*0.05:.1f} q{s*0.3:.1f},{-s*0.15:.1f} {s*0.5:.1f},{-s*0.05:.1f} '
          f'q{-s*0.2:.1f},{-s*0.27:.1f} {-s*0.5:.1f},0.05 Z" fill="{ribbon}"/>')
    return body + lid + vband + bow

def necktie_shape(cx, top_y, s, color):
    return (f'<path d="M{cx-s*0.18:.1f},{top_y:.1f} L{cx+s*0.18:.1f},{top_y:.1f} L{cx+s*0.1:.1f},{top_y+s*0.25:.1f} '
           f'L{cx+s*0.32:.1f},{top_y+s*1.3:.1f} L{cx:.1f},{top_y+s*1.55:.1f} L{cx-s*0.32:.1f},{top_y+s*1.3:.1f} '
           f'L{cx-s*0.1:.1f},{top_y+s*0.25:.1f} Z" fill="{color}"/>')

def dove_shape(cx, cy, s, color):
    """Simple seagull/dove silhouette - two swept wing curves, universally read as 'bird'."""
    d = (f"M{cx-s:.1f},{cy:.1f} Q{cx-s*0.4:.1f},{cy-s*0.7:.1f} {cx:.1f},{cy:.1f} "
        f"Q{cx+s*0.4:.1f},{cy-s*0.7:.1f} {cx+s:.1f},{cy:.1f} "
        f"Q{cx+s*0.4:.1f},{cy-s*0.25:.1f} {cx:.1f},{cy-s*0.15:.1f} "
        f"Q{cx-s*0.4:.1f},{cy-s*0.25:.1f} {cx-s:.1f},{cy:.1f} Z")
    return f'<path d="{d}" fill="{color}"/>'

# ---------- gentle / respectful motifs ----------

def scene_flame(cx, cy, s, color, glow):
    return (f'<g transform="translate({cx},{cy})">'
           f'<path d="M0,{s} Q{-s*0.5},{s*0.2} 0,{-s} Q{s*0.5},{s*0.2} 0,{s} Z" fill="{color}">'
           f'<animate attributeName="d" dur="1.4s" repeatCount="indefinite" '
           f'values="M0,{s} Q{-s*0.5},{s*0.2} 0,{-s} Q{s*0.5},{s*0.2} 0,{s} Z;'
           f'M0,{s} Q{-s*0.35},{s*0.15} 0,{-s*0.85} Q{s*0.35},{s*0.15} 0,{s} Z;'
           f'M0,{s} Q{-s*0.5},{s*0.2} 0,{-s} Q{s*0.5},{s*0.2} 0,{s} Z"/>'
           f'</path>'
           f'<circle r="{s*1.6:.1f}" fill="{glow}" opacity="0.12"/>'
           f'</g>')

def muguet_sprig(cx, base_y, s, color, leaf_color, begin):
    bells = []
    for i in range(5):
        by = base_y - s * (0.35 + i * 0.13)
        bx = cx + (2 if i % 2 == 0 else -2)
        bells.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="{s*0.09:.1f}" fill="{color}"/>')
    stem = f'<path d="M{cx},{base_y} Q{cx+1},{base_y-s*0.5} {cx},{base_y-s*0.68}" fill="none" stroke="{leaf_color}" stroke-width="1"/>'
    leaf1 = f'<path d="M{cx-2},{base_y} Q{cx-s*0.35},{base_y-s*0.5} {cx-2},{base_y-s*0.9}" fill="none" stroke="{leaf_color}" stroke-width="{s*0.16:.1f}" stroke-linecap="round"/>'
    leaf2 = f'<path d="M{cx+2},{base_y} Q{cx+s*0.4},{base_y-s*0.45} {cx+3},{base_y-s*0.85}" fill="none" stroke="{leaf_color}" stroke-width="{s*0.14:.1f}" stroke-linecap="round"/>'
    return (f'<g transform="translate(0,0)">'
           f'<animateTransform attributeName="transform" type="rotate" values="-3;3;-3" '
           f'begin="{begin}s" dur="3.4s" repeatCount="indefinite"/>'
           f'{leaf1}{leaf2}{stem}{"".join(bells)}</g>')

def scene_light_rays(cx, top_y, s, color):
    out = []
    for i, dx in enumerate((-0.5, -0.2, 0.1, 0.4)):
        x = cx + dx * s
        out.append(f'<line x1="{x:.1f}" y1="{top_y}" x2="{x+dx*8:.1f}" y2="{top_y+s:.1f}" '
                   f'stroke="{color}" stroke-width="2" stroke-linecap="round" opacity="0.5">'
                   f'<animate attributeName="opacity" values="0.25;0.55;0.25" begin="{i*0.5}s" dur="3s" repeatCount="indefinite"/>'
                   f'</line>')
    return "".join(out)

def arc_de_triomphe(cx, base_y, s, color):
    w, h = s * 1.15, s
    top = base_y - h
    arch_top = top + h * 0.42
    arch_rx = w * 0.22
    outer = f"M{cx-w/2:.1f},{base_y:.1f} L{cx-w/2:.1f},{top:.1f} L{cx+w/2:.1f},{top:.1f} L{cx+w/2:.1f},{base_y:.1f} Z"
    inner = (f"M{cx-arch_rx:.1f},{base_y:.1f} L{cx-arch_rx:.1f},{arch_top:.1f} "
            f"A{arch_rx:.1f},{h*0.42:.1f} 0 0,1 {cx+arch_rx:.1f},{arch_top:.1f} "
            f"L{cx+arch_rx:.1f},{base_y:.1f} Z")
    return f'<path d="{outer} {inner}" fill="{color}" fill-rule="evenodd"/>'

def candle_shape(cx, base_y, s, wax, flame_color, begin):
    body = f'<rect x="{cx-s*0.18:.1f}" y="{base_y-s:.1f}" width="{s*0.36:.1f}" height="{s}" rx="1.5" fill="{wax}"/>'
    return body + scene_flame(cx, base_y - s - s*0.35, s*0.35, flame_color, flame_color)

def memorial_cross(cx, base_y, s, color):
    return (f'<rect x="{cx-s*0.08:.1f}" y="{base_y-s:.1f}" width="{s*0.16:.1f}" height="{s}" fill="{color}"/>'
           f'<rect x="{cx-s*0.32:.1f}" y="{base_y-s*0.72:.1f}" width="{s*0.64:.1f}" height="{s*0.14:.1f}" fill="{color}"/>')

def crescent_stars(cx, cy, s, moon_color, star_color):
    moon = f'<path d="M{cx+s*0.3:.1f},{cy-s:.1f} A{s},{s} 0 1,0 {cx+s*0.3:.1f},{cy+s:.1f} A{s*0.78:.1f},{s*0.78:.1f} 0 1,1 {cx+s*0.3:.1f},{cy-s:.1f} Z" fill="{moon_color}"/>'
    out = [moon]
    for i in range(7):
        ang = math.radians(360 / 7 * i - 90)
        r = s * 1.9
        sx, sy = cx + math.cos(ang) * r, cy + math.sin(ang) * r * 0.55
        out.append(f'<g transform="translate({sx:.1f},{sy:.1f})" opacity="0.85">{star_shape(star_color)}'
                   f'<animate attributeName="opacity" values="0.4;0.9;0.4" begin="{i*0.3}s" dur="2.4s" repeatCount="indefinite"/></g>')
    return "".join(out)

def sailboat(cx, base_y, s, hull_color, sail_color, begin=0):
    hull = f'<path d="M{cx-s*0.6:.1f},{base_y:.1f} Q{cx:.1f},{base_y+s*0.3:.1f} {cx+s*0.6:.1f},{base_y:.1f} Z" fill="{hull_color}"/>'
    mast = f'<line x1="{cx}" y1="{base_y}" x2="{cx}" y2="{base_y-s*1.3:.1f}" stroke="{hull_color}" stroke-width="1.4"/>'
    sail = f'<path d="M{cx:.1f},{base_y-s*1.2:.1f} L{cx:.1f},{base_y-s*0.1:.1f} L{cx-s*0.7:.1f},{base_y-s*0.2:.1f} Z" fill="{sail_color}"/>'
    boat = f'<g>{hull}{mast}{sail}</g>'
    return (f'<g transform="translate({cx},{base_y})">'
           f'<animateTransform attributeName="transform" type="translate" additive="sum" '
           f'values="0 0;3 -3;0 0;-3 3;0 0" begin="{begin}s" dur="3.4s" repeatCount="indefinite"/>'
           f'<g transform="translate({-cx},{-base_y})">'
           f'<animateTransform attributeName="transform" type="rotate" '
           f'values="-4 {cx} {base_y};4 {cx} {base_y};-4 {cx} {base_y}" begin="{begin}s" dur="3.4s" repeatCount="indefinite" additive="sum"/>'
           f'{boat}</g></g>')

def wave_line(W, y, color, amplitude, dur, begin):
    d = f"M-{W},{y} "
    for x in range(-int(W), int(W*2)+40, 40):
        d += f"Q{x+20},{y-amplitude} {x+40},{y} "
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2" opacity="0.5">'
           f'<animateTransform attributeName="transform" type="translate" values="0 0;-80 0" '
           f'begin="{begin}s" dur="{dur}s" repeatCount="indefinite"/></path>')

def palm_tree(cx, base_y, s, trunk, leaf):
    trunk_path = f'<path d="M{cx-2},{base_y} Q{cx+6},{base_y-s*0.6:.1f} {cx},{base_y-s:.1f}" fill="none" stroke="{trunk}" stroke-width="4" stroke-linecap="round"/>'
    fronds = []
    top_x, top_y = cx, base_y - s
    for ang in (-70, -35, 0, 35, 70):
        rad = math.radians(ang)
        ex, ey = top_x + math.sin(rad) * s * 0.55, top_y - math.cos(rad) * s * 0.4
        fronds.append(f'<path d="M{top_x},{top_y} Q{top_x+math.sin(rad)*s*0.3:.1f},{top_y-s*0.3:.1f} {ex:.1f},{ey:.1f}" '
                      f'fill="none" stroke="{leaf}" stroke-width="3" stroke-linecap="round"/>')
    return trunk_path + "".join(fronds)


def build_scene(theme, p, W=980, H=150):
    ground_y = H - 14
    out = []

    if theme == "autumn":
        colors = ["#c17a4e", "#b5654a", "#d9a441", "#a86b3f"]
        out.append(falling_particles("leaf", 20, W, H, colors, seed=11, dur_range=(6, 10)))
    elif theme == "winter":
        colors = [p["text"], p["foam"], p["subtle"]]
        out.append(falling_particles("snow", 30, W, H, colors, seed=22, dur_range=(7, 13), size_range=(0.7, 1.3), sway=10))
    elif theme == "spring":
        colors = ["#f4c2c2", "#f7d6d6", p["rose"]]
        out.append(falling_particles("petal", 20, W, H, colors, seed=33, dur_range=(6.5, 10.5)))
    elif theme == "summer":
        out.append(scene_sun(66, 34, 26, p["gold"]))
        out.append(wave_line(W, ground_y + 2, p["foam"], 5, 3.5, 0))
        out.append(wave_line(W, ground_y + 8, p["pine"], 4, 4.5, -1))
        out.append(palm_tree(W * 0.88, ground_y, 50, "#8a6a4a", p["pine"]))
        out.append(sailboat(W * 0.4, ground_y - 6, 20, p["subtle"], p["rose"], begin=0))
        out.append(sailboat(W * 0.62, ground_y - 2, 12, p["muted"], p["gold"], begin=1.2))
    elif theme == "halloween":
        out.append(scene_fog(W, H, p["muted"]))
        out.append(jack_o_lantern(W * 0.16, ground_y - 4, 28, "#e8823c", "#ffdb8a", begin=0))
        out.append(jack_o_lantern(W * 0.45, ground_y - 14, 36, "#d9711f", "#ffdb8a", begin=0.7))
        out.append(jack_o_lantern(W * 0.75, ground_y - 2, 24, "#e8823c", "#ffdb8a", begin=1.3))
        out.append(scene_bat(22, "#2a2733", dur=10, begin=0, s=17))
        out.append(scene_bat(62, "#413d4d", dur=8.5, begin=3, s=13))
    elif theme == "christmas":
        out.append(scene_tree(W * 0.24, ground_y, 60, p["muted"], p["pine"], [p["rose"], p["gold"], p["foam"], p["iris"]]))
        out.append(scene_santa(38, p["muted"], p["rose"], p["text"], dur=13, begin=1))
    elif theme == "newyear":
        pts = [(W*0.14,34,7),(W*0.4,20,10),(W*0.66,44,6),(W*0.86,28,9),(W*0.28,58,5),(W*0.55,64,6),(W*0.78,56,7),(W*0.5,42,11)]
        colors = [p["rose"], p["gold"], p["iris"], p["foam"]]
        for i, (x, y, s) in enumerate(pts):
            out.append(scene_firework(x, y, s, colors[i % len(colors)], begin=i * 0.5, dur=2.2 + (i % 3) * 0.3))
        year_text = str(__import__("datetime").date.today().year)
        out.append(scene_banner(W * 0.5, H - 8, 130, 22, p["iris"], p["base"], year_text))
    elif theme == "easter":
        eggs = [(W*0.18, ground_y-4), (W*0.4, ground_y-20), (W*0.63, ground_y-2), (W*0.84, ground_y-16)]
        egg_colors = [p["rose"], p["foam"], p["gold"], p["iris"]]
        for i, (x, y) in enumerate(eggs):
            out.append(scene_egg(x, y, 11, egg_colors[i % len(egg_colors)], p["base"]))
        out.append(scene_bunny(eggs, dur=8.0, color=p["text"]))
    elif theme == "labor_day":
        for i, (x, sc) in enumerate([(W*0.28, 0.85), (W*0.5, 1.1), (W*0.72, 0.9)]):
            out.append(muguet_sprig(x, ground_y, 34 * sc, "#faf6ee", p["pine"], begin=i*0.4))
    elif theme == "ve_day":
        out.append(arc_de_triomphe(W*0.5, ground_y, 64, p["subtle"]))
        out.append(scene_flame(W*0.5, ground_y - 6, 10, p["gold"], p["rose"]))
        for i, x in enumerate([W*0.3, W*0.7]):
            out.append(f'<g transform="translate({x},{ground_y-14})">{cornflower_shape("#4a6fa5", "#faf4ed")}</g>')
        out.append(f'<rect x="{W*0.5-40}" y="8" width="26.6" height="7" fill="#0055A4"/>'
                   f'<rect x="{W*0.5-13.3}" y="8" width="26.6" height="7" fill="#FFFFFF"/>'
                   f'<rect x="{W*0.5+13.3}" y="8" width="26.6" height="7" fill="#EF4135"/>')
    elif theme == "music_day":
        colors = [p["rose"], p["iris"], p["gold"], p["foam"]]
        out.append(floating_up("note", 14, W, H, colors, seed=44))
    elif theme == "bastille_day":
        out.append(eiffel_tower(W*0.82, ground_y, 60, p["subtle"]))
        out.append(jet_patrol(26, 9, 0, ["#0055A4", "#FFFFFF", "#EF4135"]))
        out.append(jet_patrol(44, 9, 0.15, ["#0055A4", "#FFFFFF", "#EF4135"]))
        out.append(jet_patrol(62, 9, 0.3, ["#0055A4", "#FFFFFF", "#EF4135"]))
        pts = [(W*0.15,44,7,'#EF4135'),(W*0.35,22,10,'#FFFFFF'),(W*0.55,48,6,'#0055A4'),(W*0.25,64,6,'#0055A4'),(W*0.45,36,8,'#EF4135')]
        for i, (x, y, s, c) in enumerate(pts):
            out.append(scene_firework(x, y, s, c, begin=4.5 + i*0.5, dur=2.2+(i%3)*0.3))
    elif theme == "assumption":
        out.append(crescent_stars(W*0.5, 55, 16, "#faf4ed", p["gold"]))
    elif theme == "toussaint":
        colors = ["#c9835a", "#b5654a", p["gold"], p["subtle"]]
        heights = [ground_y-8, ground_y-22, ground_y-4, ground_y-16]
        for i, x in enumerate([W*0.18, W*0.38, W*0.6, W*0.8]):
            out.append(f'<g transform="translate({x},{heights[i]:.1f})">'
                       f'<animateTransform attributeName="transform" type="rotate" values="-2;2;-2" '
                       f'begin="{i*0.5}s" dur="4s" repeatCount="indefinite" additive="sum"/>'
                       f'{mum_shape(colors[i%len(colors)], p["base"])}</g>')
        out.append(candle_shape(W*0.5, ground_y, 16, "#efe6d8", p["gold"], begin=0))
    elif theme == "armistice":
        out.append(memorial_cross(W*0.5, ground_y, 34, p["subtle"]))
        out.append(scene_flame(W*0.5, ground_y - 40, 9, p["gold"], p["rose"]))
        for i, x in enumerate([W*0.28, W*0.72]):
            out.append(f'<g transform="translate({x},{ground_y-14})">{cornflower_shape("#4a6fa5", p["gold"])}</g>')
    elif theme == "epiphany":
        out.append(galette(W*0.5, ground_y - 6, 30, "#e8b95c", "#c98a2e"))
        out.append(crown_shape(W*0.5, ground_y - 44, 26, p["gold"], p["rose"]))
    elif theme == "candlemas":
        out.append(crepe_pan(W*0.5, ground_y - 10, 32, "#f3d9a0", "#4a4550", begin=0))
    elif theme == "mardi_gras":
        out.append(confetti_burst(W, H, [p["rose"], p["iris"], p["gold"], p["foam"]], n=22, seed=5))
        out.append(mask_shape(W*0.28, ground_y - 26, 22, p["iris"], p["gold"]))
        out.append(mask_shape(W*0.68, ground_y - 10, 18, p["rose"], p["gold"]))
    elif theme == "ascension":
        out.append(scene_light_rays(W*0.5, 8, 55, p["gold"]))
        colors = ["#f4c2c2", "#f7d6d6", p["rose"]]
        out.append(falling_particles("petal", 8, W, H, colors, seed=33, dur_range=(7, 10)))
    elif theme == "pentecost":
        colors = ["#f4c2c2", "#f7d6d6", p["rose"]]
        out.append(falling_particles("petal", 10, W, H, colors, seed=33, dur_range=(6.5, 10.5)))
        out.append(f'<g transform="translate({W*0.5:.1f},40)">'
                   f'<animateTransform attributeName="transform" type="translate" additive="sum" '
                   f'values="0 0;14 -4;0 0;-14 4;0 0" dur="6s" repeatCount="indefinite"/>'
                   f'{dove_shape(0, 0, 22, "#faf4ed")}</g>')
    elif theme == "mothers_day":
        bouquet_x = W * 0.5
        for i, dx in enumerate([-16, 0, 16]):
            out.append(f'<g transform="translate({bouquet_x+dx:.1f},{ground_y - (10 if i==1 else 0):.1f})">'
                       f'{flower_full(p["rose"] if i != 1 else p["gold"], p["base"])}</g>')
        for i, x in enumerate([W*0.28, W*0.72]):
            out.append(f'<g transform="translate({x},{50+i*10})">'
                       f'<animateTransform attributeName="transform" type="translate" additive="sum" '
                       f'values="0 0;0 -6;0 0" begin="{i*0.5}s" dur="2s" repeatCount="indefinite"/>{heart_shape(p["rose"])}</g>')
    elif theme == "fathers_day":
        out.append(gift_box(W*0.35, ground_y - 14, 24, p["pine"], p["gold"]))
        out.append(necktie_shape(W*0.58, ground_y - 48, 16, p["iris"]))
        out.append(f'<g transform="translate({W*0.78:.1f},{ground_y-16:.1f}) rotate(20)">'
                   f'<rect x="-2.5" y="-16" width="5" height="24" rx="2" fill="{p["subtle"]}"/>'
                   f'<circle cx="0" cy="-16" r="6" fill="none" stroke="{p["subtle"]}" stroke-width="3"/></g>')
    elif theme == "valentines":
        colors = [p["rose"], "#e58fa0", p["gold"]]
        rng = random.Random(7)
        for i in range(10):
            x0 = rng.uniform(20, W-20)
            dur = rng.uniform(5, 8)
            begin = rng.uniform(-dur, 0)
            scale = rng.uniform(1.0, 1.8)
            c = colors[i % len(colors)]
            out.append(f'<g transform="translate({x0:.1f},{H+10}) scale({scale:.2f})">'
                       f'<animateTransform attributeName="transform" type="translate" additive="sum" '
                       f'values="0 0;0 {-(H+20):.1f}" begin="{begin:.2f}s" dur="{dur:.2f}s" repeatCount="indefinite"/>'
                       f'{heart_shape(c)}</g>')
    elif theme == "chinese_new_year":
        from seasonal import current_zodiac_year, zodiac_animal
        animal = zodiac_animal(current_zodiac_year())
        out.append(paper_lantern(W*0.1, 34, 18, "#c0392b", "#f1c40f", 0))
        out.append(paper_lantern(W*0.1, 68, 14, "#a93226", "#f1c40f", 0.5))
        out.append(paper_lantern(W*0.92, 30, 16, "#c0392b", "#f1c40f", 0.3))
        out.append(paper_lantern(W*0.92, 62, 13, "#a93226", "#f1c40f", 0.8))
        for i, x in enumerate([W*0.25, W*0.75]):
            out.append(firecracker_burst(x, 24 + i*14, 12, "#f1c40f", begin=i*0.8))
        out.append(envelope_shape(W*0.86, ground_y - 8, 18, "#c0392b", "#f1c40f"))
        if animal == "dragon":
            out.append(chinese_dragon(ground_y - 24, 11, "#c0392b", "#f1c40f", 9, 0))
        else:
            shape_fn = ZODIAC_SHAPES.get(animal)
            if shape_fn:
                cx, cy = W * 0.48, ground_y - 22
                out.append(f'<circle cx="{cx}" cy="{cy}" r="40" fill="#c0392b" opacity="0.25"/>')
                out.append(f'<circle cx="{cx}" cy="{cy}" r="40" fill="none" stroke="#f1c40f" stroke-width="1.5" opacity="0.6"/>')
                out.append(f'<g transform="translate({cx},{cy})">'
                           f'<animateTransform attributeName="transform" type="translate" additive="sum" '
                           f'values="0 0;0 -4;0 0" dur="2.4s" repeatCount="indefinite"/>'
                           f'{shape_fn(0, 0, 34, "#f1c40f")}</g>')
    else:
        out.append(falling_particles("leaf", 14, W, H, [p["muted"]], seed=1))

    return "".join(out)

def flower_full(petal_color, center):
    out = []
    for k in range(6):
        ang = math.radians(60 * k)
        px, py = math.cos(ang) * 6, math.sin(ang) * 6
        out.append(f'<g transform="translate({px:.1f},{py:.1f}) rotate({math.degrees(ang)+90:.0f})">{petal_shape(petal_color)}</g>')
    out.append(f'<circle cx="0" cy="0" r="2.4" fill="{center}"/>')
    stem = '<line x1="0" y1="8" x2="0" y2="26" stroke="#5a8a5a" stroke-width="2"/>'
    return "".join(out) + stem
