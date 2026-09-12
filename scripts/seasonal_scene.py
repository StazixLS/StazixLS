import math
import random

def leaf_shape(color, seed=0):
    r = random.Random(seed)
    hue = r.choice([0, 1])
    d = "M0,-7 Q6,-2 0,7 Q-6,-2 0,-7 Z"
    return f'<path d="{d}" fill="{color}" opacity="0.85"/>'

def snow_shape(color, seed=0):
    return f'<circle r="2.4" fill="{color}" opacity="0.9"/>'

def petal_shape(color, seed=0):
    d = "M0,-5 Q4,-3 3,2 Q0,5 -3,2 Q-4,-3 0,-5 Z"
    return f'<path d="{d}" fill="{color}" opacity="0.88"/>'

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

def scene_pumpkin(cx, cy, s, color, glow, begin=0):
    period = 2.2 + (begin % 1)
    return (
        f'<g transform="translate({cx},{cy})">'
        f'<ellipse cx="0" cy="0" rx="{s}" ry="{s*0.8:.1f}" fill="{color}"/>'
        f'<path d="M{-s*0.42:.1f},{-s*0.7:.1f} Q{-s*0.55:.1f},0 {-s*0.42:.1f},{s*0.7:.1f}" fill="none" stroke="{glow}" stroke-width="0.8" opacity="0.4"/>'
        f'<path d="M0,{-s*0.75:.1f} Q{-s*0.13:.1f},0 0,{s*0.75:.1f}" fill="none" stroke="{glow}" stroke-width="0.8" opacity="0.4"/>'
        f'<path d="M{s*0.42:.1f},{-s*0.7:.1f} Q{s*0.55:.1f},0 {s*0.42:.1f},{s*0.7:.1f}" fill="none" stroke="{glow}" stroke-width="0.8" opacity="0.4"/>'
        f'<line x1="0" y1="{-s*0.78:.1f}" x2="0" y2="{-s*1.15:.1f}" stroke="{color}" stroke-width="1.6"/>'
        f'<path d="M{-s*0.32:.1f},{-s*0.1:.1f} L{-s*0.16:.1f},{s*0.12:.1f} L0,{-s*0.1:.1f} L{s*0.16:.1f},{s*0.12:.1f} L{s*0.32:.1f},{-s*0.1:.1f}" '
        f'fill="none" stroke="{glow}" stroke-width="1.4" stroke-linejoin="round">'
        f'<animate attributeName="opacity" values="0.35;1;0.35" begin="{begin}s" dur="{period:.1f}s" repeatCount="indefinite"/>'
        f'</path>'
        f'<circle r="{s*1.5:.1f}" fill="{glow}" opacity="0">'
        f'<animate attributeName="opacity" values="0;0.18;0" begin="{begin}s" dur="{period:.1f}s" repeatCount="indefinite"/>'
        f'</circle>'
        f'</g>'
    )

def scene_bat(y, color, dur=9, begin=0):
    d = "M-7,0 Q-3,-6 0,-1 Q3,-6 7,0 Q3,-1.5 0,-0.4 Q-3,-1.5 -7,0 Z"
    return (
        f'<g transform="translate(-20,{y})">'
        f'<animateTransform attributeName="transform" type="translate" additive="sum" '
        f'values="0 0;1040 -14;1040 -14" keyTimes="0;0.999;1" begin="{begin}s" dur="{dur}s" repeatCount="indefinite"/>'
        f'<g><animateTransform attributeName="transform" type="scale" values="1,1;1,0.6;1,1" begin="{begin}s" dur="0.5s" repeatCount="indefinite"/>'
        f'<path d="{d}" fill="{color}"/></g></g>'
    )

def scene_tree(cx, base_y, s, trunk, green, lights):
    trunk_h = s * 0.22
    trunk_w = s * 0.16
    out = [f'<rect x="{cx-trunk_w/2:.1f}" y="{base_y-trunk_h:.1f}" width="{trunk_w:.1f}" height="{trunk_h:.1f}" fill="{trunk}"/>']

    tiers = 3
    tier_h = s * 0.4
    overlap = 0.45  # each tier sinks into the one below by this fraction of tier_h
    # bottom-most tier's base sits right on top of the trunk
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
        frac = rng.uniform(0.25, 0.92)  # 0 = apex, 1 = base
        ly = apex_y + frac * (base_yy - apex_y)
        half_w_here = (w / 2) * frac
        lx = cx + rng.uniform(-1, 1) * half_w_here * 0.85
        c = lights[i % len(lights)]
        out.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="1.7" fill="{c}">'
                   f'<animate attributeName="opacity" values="1;0.25;1" begin="{i*0.28:.2f}s" dur="1.6s" repeatCount="indefinite"/></circle>')
    return "".join(out)

def scene_santa(y, color, accent, dur=13, begin=0):
    return (
        f'<g transform="translate(-40,{y})">'
        f'<animateTransform attributeName="transform" type="translate" additive="sum" '
        f'values="0 0;1060 -18;1060 -18" keyTimes="0;0.999;1" begin="{begin}s" dur="{dur}s" repeatCount="indefinite"/>'
        f'<path d="M0,0 Q10,-9 24,-2 L22,3 Q10,-2 2,4 Z" fill="{color}"/>'
        f'<circle cx="6" cy="-2" r="3.2" fill="{accent}"/>'
        f'<line x1="-2" y1="2" x2="-14" y2="6" stroke="{color}" stroke-width="1.4"/>'
        f'<line x1="-6" y1="4" x2="-16" y2="9" stroke="{color}" stroke-width="1.4"/>'
        f'</g>'
    )

def scene_sun(cx, cy, s, color):
    out = [f'<circle cx="{cx}" cy="{cy}" r="{s*0.62:.1f}" fill="{color}"/>']
    for k in range(10):
        ang = math.radians(36*k)
        x1, y1 = cx+math.cos(ang)*s*0.78, cy+math.sin(ang)*s*0.78
        x2, y2 = cx+math.cos(ang)*s*1.05, cy+math.sin(ang)*s*1.05
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="1.6" stroke-linecap="round"/>')
    return (f'<g transform="translate(0,0)">'
           f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="40s" repeatCount="indefinite"/>'
           f'{"".join(out)}</g>')

def scene_beachball(cx, base_y, s, colors):
    wedges = []
    for k in range(6):
        a0, a1 = math.radians(60*k), math.radians(60*(k+1))
        x0, y0 = math.cos(a0)*s, math.sin(a0)*s
        x1, y1 = math.cos(a1)*s, math.sin(a1)*s
        wedges.append(f'<path d="M0,0 L{x0:.1f},{y0:.1f} A{s},{s} 0 0,1 {x1:.1f},{y1:.1f} Z" fill="{colors[k%len(colors)]}"/>')
    ball = f'<circle r="{s}" fill="{colors[-1]}"/>' + "".join(wedges)
    return (
        f'<g transform="translate({cx},{base_y-s})">'
        f'<animateTransform attributeName="transform" type="translate" additive="sum" '
        f'values="0 0;0 {-s*0.55:.1f};0 0" keyTimes="0;0.5;1" dur="1.8s" repeatCount="indefinite"/>'
        f'<g><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="3.6s" repeatCount="indefinite"/>{ball}</g>'
        f'</g>'
    )

def scene_egg(cx, cy, s, color, accent):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{s*0.72:.1f}" ry="{s}" fill="{color}"/>'
           f'<circle cx="{cx-s*0.2:.1f}" cy="{cy-s*0.3:.1f}" r="{s*0.14:.1f}" fill="{accent}" opacity="0.7"/>'
           f'<circle cx="{cx+s*0.15:.1f}" cy="{cy+s*0.1:.1f}" r="{s*0.1:.1f}" fill="{accent}" opacity="0.7"/>')

def scene_bunny(stops, dur, color):
    xs = ";".join(f"{x:.1f}" for x, y in stops) + f";{stops[0][0]:.1f}"
    n = len(stops) + 1
    kt = ";".join(str(round(i/(n-1), 4)) for i in range(n))
    hop_h = 10
    ys_base = [y for x, y in stops] + [stops[0][1]]
    return (
        f'<g>'
        f'<animate attributeName="opacity" values="1" dur="{dur}s"/>'
        f'<g transform="translate({stops[0][0]:.1f},{stops[0][1]:.1f})">'
        f'<animateTransform attributeName="transform" type="translate" calcMode="discrete" '
        f'values="{" ".join(f"{x:.1f},{y:.1f};" for x,y in stops+[stops[0]])[:-1]}" '
        f'keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
        f'<g>'
        f'<animateTransform attributeName="transform" type="translate" '
        f'values="0 0;0 {-hop_h};0 0" keyTimes="0;0.5;1" dur="0.5s" repeatCount="indefinite"/>'
        f'<ellipse cx="0" cy="0" rx="6" ry="5" fill="{color}"/>'
        f'<ellipse cx="0" cy="-8" rx="3.6" ry="3.6" fill="{color}"/>'
        f'<path d="M-2,-11 Q-3,-18 -1,-11" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round"/>'
        f'<path d="M2,-11 Q3,-18 1,-11" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round"/>'
        f'</g></g></g>'
    )

def scene_firework(cx, cy, s, color, begin):
    lines = []
    for k in range(8):
        ang = math.radians(45*k)
        x2, y2 = cx+math.cos(ang)*s, cy+math.sin(ang)*s
        lines.append(f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="1.2" stroke-linecap="round"/>')
    return (f'<g opacity="0" transform="translate(0,0) scale(0.2)" transform-origin="{cx} {cy}">'
           f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.15;0.6;1" begin="{begin}s" dur="2.6s" repeatCount="indefinite"/>'
           f'<animateTransform attributeName="transform" type="scale" values="0.3;1;1.15" keyTimes="0;0.4;1" '
           f'begin="{begin}s" dur="2.6s" repeatCount="indefinite" additive="sum"/>'
           f'{"".join(lines)}</g>')


def build_scene(theme, p, W=980, H=150):
    out = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{p["surface"]}"/>']
    ground_y = H - 14

    if theme == "autumn":
        colors = [p["rose"], p["gold"], p["iris"]]
        out.append(falling_particles("leaf", 22, W, H, colors, seed=11, dur_range=(6, 10)))
    elif theme == "winter":
        colors = [p["text"], p["foam"], p["subtle"]]
        out.append(falling_particles("snow", 34, W, H, colors, seed=22, dur_range=(7, 13), size_range=(0.6, 1.3), sway=10))
    elif theme == "spring":
        colors = [p["rose"], p["gold"]]
        out.append(falling_particles("petal", 20, W, H, colors, seed=33, dur_range=(6.5, 10.5)))
    elif theme == "summer":
        out.append(scene_sun(70, 46, 34, p["gold"]))
        out.append(scene_beachball(W*0.5, ground_y, 16, [p["rose"], p["foam"], p["iris"], p["gold"]]))
        out.append(scene_beachball(W*0.82, ground_y, 12, [p["iris"], p["rose"], p["foam"], p["gold"]]))
    elif theme == "halloween":
        xs = [W*0.22, W*0.5, W*0.78]
        for i, x in enumerate(xs):
            out.append(scene_pumpkin(x, ground_y - 14, 20, p["rose"], p["gold"], begin=i*0.6))
        out.append(scene_bat(30, p["muted"], dur=10, begin=0))
        out.append(scene_bat(50, p["subtle"], dur=8.5, begin=3))
    elif theme == "christmas":
        out.append(scene_tree(W*0.24, ground_y, 60, p["muted"], p["pine"], [p["rose"], p["gold"], p["foam"], p["iris"]]))
        out.append(scene_santa(40, p["text"], p["rose"], dur=13, begin=1))
    elif theme == "newyear":
        pts = [(W*0.18, 40), (W*0.5, 30), (W*0.82, 45), (W*0.35, 55), (W*0.68, 60)]
        colors = [p["rose"], p["gold"], p["iris"], p["foam"]]
        for i, (x, y) in enumerate(pts):
            out.append(scene_firework(x, y, 22, colors[i % len(colors)], begin=i*0.9))
    elif theme == "easter":
        eggs = [(W*0.2, ground_y-10), (W*0.42, ground_y-8), (W*0.62, ground_y-11), (W*0.8, ground_y-9)]
        egg_colors = [p["rose"], p["foam"], p["gold"], p["iris"]]
        for i, (x, y) in enumerate(eggs):
            out.append(scene_egg(x, y, 11, egg_colors[i % len(egg_colors)], p["base"]))
        out.append(scene_bunny(eggs, dur=9.0, color=p["text"]))
    else:
        out.append(falling_particles("leaf", 14, W, H, [p["muted"]], seed=1))

    return "".join(out)
