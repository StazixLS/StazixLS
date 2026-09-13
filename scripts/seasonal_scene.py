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

def spooky_hand(color, s=22):
    fingers = []
    for fx in (-0.38, -0.14, 0.12, 0.36):
        fingers.append(f'<path d="M{fx*s:.1f},{-s*0.62:.1f} L{fx*s*1.15:.1f},{-s*1.05:.1f}" '
                       f'stroke="{color}" stroke-width="{s*0.14:.1f}" stroke-linecap="round"/>')
    thumb = (f'<path d="M{-0.5*s:.1f},{-s*0.5:.1f} L{-0.75*s:.1f},{-s*0.68:.1f}" '
            f'stroke="{color}" stroke-width="{s*0.14:.1f}" stroke-linecap="round"/>')
    arm = f'<path d="M0,4 L0,{-s*0.65:.1f}" stroke="{color}" stroke-width="{s*0.22:.1f}" stroke-linecap="round"/>'
    return arm + thumb + "".join(fingers)

def scene_reaching_hand(cx, ground_y, s, color, begin):
    return (
        f'<g transform="translate({cx},{ground_y})">'
        f'<animateTransform attributeName="transform" type="translate" additive="sum" '
        f'values="0 0;0 -4;0 0" keyTimes="0;0.5;1" begin="{begin}s" dur="2.4s" repeatCount="indefinite"/>'
        f'<g>'
        f'<animateTransform attributeName="transform" type="rotate" '
        f'values="-6;6;-6" begin="{begin}s" dur="2.4s" repeatCount="indefinite"/>'
        f'{spooky_hand(color, s)}'
        f'</g></g>'
    )

def scene_skull(cx, cy, s, color, eye):
    period = 1.8
    cranium = f'<circle cx="0" cy="0" r="{s*0.55:.1f}" fill="{color}"/>'
    jaw = (f'<path d="M{-s*0.32:.1f},{s*0.28:.1f} Q0,{s*0.55:.1f} {s*0.32:.1f},{s*0.28:.1f} '
          f'L{s*0.28:.1f},{s*0.15:.1f} L{-s*0.28:.1f},{s*0.15:.1f} Z" fill="{color}"/>')
    eyes = (f'<circle cx="{-s*0.22:.1f}" cy="{-s*0.05:.1f}" r="{s*0.15:.1f}" fill="{eye}">'
           f'<animate attributeName="opacity" values="1;0.3;1" dur="{period}s" repeatCount="indefinite"/></circle>'
           f'<circle cx="{s*0.22:.1f}" cy="{-s*0.05:.1f}" r="{s*0.15:.1f}" fill="{eye}">'
           f'<animate attributeName="opacity" values="1;0.3;1" dur="{period}s" repeatCount="indefinite"/></circle>')
    nose = f'<path d="M0,{s*0.05:.1f} l{-s*0.08:.1f},{s*0.15:.1f} l{s*0.16:.1f},0 Z" fill="{eye}"/>'
    return f'<g transform="translate({cx},{cy})">{cranium}{jaw}{eyes}{nose}</g>'

def scene_bat(y, color, dur=9, begin=0):
    d = "M-7,0 Q-3,-6 0,-1 Q3,-6 7,0 Q3,-1.5 0,-0.4 Q-3,-1.5 -7,0 Z"
    return (
        f'<g transform="translate(-20,{y})">'
        f'<animateTransform attributeName="transform" type="translate" additive="sum" '
        f'values="0 0;1040 -14;1040 -14" keyTimes="0;0.999;1" begin="{begin}s" dur="{dur}s" repeatCount="indefinite"/>'
        f'<g><animateTransform attributeName="transform" type="scale" values="1,1;1,0.6;1,1" begin="{begin}s" dur="0.5s" repeatCount="indefinite"/>'
        f'<path d="{d}" fill="{color}"/></g></g>'
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
    sleigh = (f'<path d="M-2,10 L34,10 Q40,10 40,4 L40,-8 Q40,-14 34,-14 Q30,-14 30,-10 '
             f'L30,4 L-2,4 Q-6,4 -6,7 Q-6,10 -2,10 Z" fill="{color}"/>')
    santa = (f'<ellipse cx="14" cy="-4" rx="9" ry="10" fill="{accent}"/>'
            f'<circle cx="14" cy="-16" r="5.5" fill="{skin}"/>'
            f'<path d="M9,-19 Q14,-30 22,-22 Q17,-23 14,-19 Z" fill="{accent}"/>'
            f'<circle cx="22" cy="-22" r="2" fill="{color}"/>')
    rx = -34
    reindeer = (f'<ellipse cx="{rx}" cy="2" rx="11" ry="6" fill="{skin}"/>'
               f'<circle cx="{rx-13}" cy="-4" r="5" fill="{skin}"/>'
               f'<path d="M{rx-16},-8 L{rx-20},-16 M{rx-16},-8 L{rx-13},-17" stroke="{skin}" stroke-width="1.3"/>'
               f'<line x1="{rx-6}" y1="7" x2="{rx-6}" y2="14" stroke="{skin}" stroke-width="2"/>'
               f'<line x1="{rx+6}" y1="7" x2="{rx+6}" y2="14" stroke="{skin}" stroke-width="2"/>'
               f'<circle cx="{rx-18}" cy="-4" r="1.3" fill="{color}"/>')
    rein = f'<path d="M{rx-2},-2 Q-10,-2 -4,6" fill="none" stroke="{skin}" stroke-width="1" opacity="0.7"/>'
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
    n = len(stops) + 1
    kt = ";".join(str(round(i / (n - 1), 4)) for i in range(n))
    hop_h = 10
    vals = ";".join(f"{x:.1f},{y:.1f}" for x, y in stops + [stops[0]])
    return (
        f'<g transform="translate({stops[0][0]:.1f},{stops[0][1]:.1f})">'
        f'<animateTransform attributeName="transform" type="translate" calcMode="discrete" '
        f'values="{vals}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
        f'<g>'
        f'<animateTransform attributeName="transform" type="translate" '
        f'values="0 0;0 {-hop_h};0 0" keyTimes="0;0.5;1" dur="0.5s" repeatCount="indefinite"/>'
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
        lines.append(f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="1.2" stroke-linecap="round"/>')
        lines.append(f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="1" fill="{color}"/>')
    return (f'<g opacity="0">'
           f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.15;0.6;1" begin="{begin}s" dur="{dur}s" repeatCount="indefinite"/>'
           f'<animateTransform attributeName="transform" type="scale" values="0.25;1;1.2" keyTimes="0;0.4;1" '
           f'begin="{begin}s" dur="{dur}s" repeatCount="indefinite"/>'
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
        out.append(scene_sun(66, 40, 30, p["gold"]))
        balls = [p["rose"], p["foam"], p["iris"], p["gold"]]
        out.append(scene_beachball_pass(ground_y - 10, ground_y - 26, 13, balls, W * 0.25, W * 0.75, dur=3.2, begin=0))
        out.append(scene_beachball_pass(ground_y - 8, ground_y - 30, 10, balls[::-1], W * 0.62, W * 0.92, dur=4.6, begin=0.6))
    elif theme == "halloween":
        out.append(scene_fog(W, H, p["muted"]))
        out.append(scene_reaching_hand(W * 0.22, ground_y + 4, 22, p["subtle"], begin=0))
        out.append(scene_reaching_hand(W * 0.7, ground_y + 4, 18, p["muted"], begin=0.8))
        out.append(scene_skull(W * 0.47, ground_y - 8, 30, p["text"], p["base"]))
        out.append(scene_bat(28, p["muted"], dur=10, begin=0))
        out.append(scene_bat(48, p["subtle"], dur=8.5, begin=3))
    elif theme == "christmas":
        out.append(scene_tree(W * 0.24, ground_y, 60, p["muted"], p["pine"], [p["rose"], p["gold"], p["foam"], p["iris"]]))
        out.append(scene_santa(38, p["muted"], p["rose"], p["text"], dur=13, begin=1))
    elif theme == "newyear":
        pts = [(W*0.14,38,26),(W*0.4,26,34),(W*0.66,42,22),(W*0.86,32,30),(W*0.28,55,18),(W*0.55,60,20),(W*0.78,58,24)]
        colors = [p["rose"], p["gold"], p["iris"], p["foam"]]
        for i, (x, y, s) in enumerate(pts):
            out.append(scene_firework(x, y, s, colors[i % len(colors)], begin=i * 0.55, dur=2.6 + (i % 3) * 0.4))
        year_text = str(__import__("datetime").date.today().year)
        out.append(scene_banner(W * 0.5, H - 8, 130, 22, p["iris"], p["base"], year_text))
    elif theme == "easter":
        eggs = [(W*0.2, ground_y-10), (W*0.42, ground_y-8), (W*0.62, ground_y-11), (W*0.8, ground_y-9)]
        egg_colors = [p["rose"], p["foam"], p["gold"], p["iris"]]
        for i, (x, y) in enumerate(eggs):
            out.append(scene_egg(x, y, 11, egg_colors[i % len(egg_colors)], p["base"]))
        out.append(scene_bunny(eggs, dur=9.0, color=p["text"]))
    elif theme == "labor_day":
        for i, x in enumerate([W*0.3, W*0.5, W*0.7]):
            out.append(muguet_sprig(x, ground_y, 34, "#faf6ee", p["pine"], begin=i*0.4))
    elif theme == "ve_day":
        out.append(scene_flame(W*0.5, ground_y-24, 16, p["gold"], p["rose"]))
        out.append(f'<rect x="{W*0.5-40}" y="{H-10}" width="26.6" height="8" fill="#0055A4"/>'
                   f'<rect x="{W*0.5-13.3}" y="{H-10}" width="26.6" height="8" fill="#FFFFFF"/>'
                   f'<rect x="{W*0.5+13.3}" y="{H-10}" width="26.6" height="8" fill="#EF4135"/>')
    elif theme == "music_day":
        colors = [p["rose"], p["iris"], p["gold"], p["foam"]]
        out.append(floating_up("note", 14, W, H, colors, seed=44))
    elif theme == "bastille_day":
        out.append(eiffel_tower(W*0.5, ground_y, 74, p["subtle"]))
        pts = [(W*0.15,34,'#EF4135',24),(W*0.5,22,'#FFFFFF',30),(W*0.85,36,'#0055A4',26),
               (W*0.3,55,'#0055A4',18),(W*0.7,58,'#EF4135',20)]
        for i, (x, y, c, s) in enumerate(pts):
            out.append(scene_firework(x, y, s, c, begin=i*0.5, dur=2.4+(i%3)*0.3))
    elif theme == "assumption":
        out.append(scene_light_rays(W*0.5, 10, 60, p["gold"]))
        for i, x in enumerate([W*0.3, W*0.5, W*0.7]):
            out.append(f'<g transform="translate({x},{40+i*6})" opacity="0.8">{star_shape(p["gold"])}'
                       f'<animate attributeName="opacity" values="0.4;0.9;0.4" begin="{i*0.6}s" dur="2.6s" repeatCount="indefinite"/></g>')
    elif theme == "toussaint":
        colors = ["#c9835a", "#b5654a", p["gold"], p["subtle"]]
        for i, x in enumerate([W*0.22, W*0.42, W*0.6, W*0.8]):
            out.append(f'<g transform="translate({x},{ground_y-12})">'
                       f'<animateTransform attributeName="transform" type="rotate" values="-2;2;-2" '
                       f'begin="{i*0.5}s" dur="4s" repeatCount="indefinite" additive="sum"/>'
                       f'{mum_shape(colors[i%len(colors)], p["base"])}</g>')
    elif theme == "armistice":
        out.append(scene_flame(W*0.5, ground_y-22, 14, p["gold"], p["rose"]))
        for i, x in enumerate([W*0.28, W*0.72]):
            out.append(f'<g transform="translate({x},{ground_y-16})">{cornflower_shape("#4a6fa5", p["gold"])}</g>')
    else:
        out.append(falling_particles("leaf", 14, W, H, [p["muted"]], seed=1))

    return "".join(out)
