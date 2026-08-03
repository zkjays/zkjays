# -*- coding: utf-8 -*-
import numpy as np

ASSETS = r"C:\Users\Jays\AppData\Local\Temp\claude\C--Users-Jays-Documents-Second-Brain-zkjays\9916058f-aa43-41f2-a91d-295529fd98a2\scratchpad\pathode\assets"
OUT = r"C:\Users\Jays\AppData\Local\Temp\claude\C--Users-Jays-Documents-Second-Brain-zkjays\9916058f-aa43-41f2-a91d-295529fd98a2\scratchpad\pathode"

W, H = 1180, 610
MARGIN = 4
RX = 14
HEADER_H = 40
LEFT_W = 445

PAD = 22

# timeline (seconds)
T_HOLD_PORTRAIT_END = 3.0
T_TRANS1_END = 4.3
T_HOLD_MINA_END = 6.3
T_TRANS2_END = 7.6
T_HOLD_DR_END = 9.6
T_TRANS3_END = 10.9
T_HOLD_X_END = 12.9
T_TOTAL = 14.2

POS_TIMES = [0.0, T_HOLD_PORTRAIT_END, T_TRANS1_END, T_HOLD_MINA_END, T_TRANS2_END,
             T_HOLD_DR_END, T_TRANS3_END, T_HOLD_X_END, T_TOTAL]
OPACITY_TIMES = [0.0, T_HOLD_PORTRAIT_END, T_TRANS1_END, T_HOLD_X_END, T_TOTAL]

ROWS = [
    ("Subject", "zkJays"),
    ("Role", "Mina Ambassador / Darkroom Founder"),
    ("Origin", "France"),
    ("Status", "Building systems that run without me"),
    ("ToolChain", "Claude Code, Next.js, Vercel"),
    ("Core.Lang", "TypeScript, Python"),
    ("Core.Frontend", "Next.js, React, Tailwind"),
    ("Core.Backend", "Next.js API, Supabase, NextAuth"),
    ("Core.Database", "Supabase (Postgres)"),
    ("Core.Infra", "Vercel"),
    ("Grid.Mail", "jayalls.contact@gmail.com"),
    ("Grid.GitHub", "github.com/zkjays"),
    ("Grid.X", "@zkjays"),
]

PALETTES = {
    "dark": dict(
        bg="#0A101F", panel_bg="#0D1424", chrome="#22D3EE", chrome_dim="#22D3EE",
        text="#F8FAFC", muted="#94A3B8", accent="#10B981", portrait="#A78BFA",
        red="#F87171", border="#1E293B",
    ),
    "light": dict(
        bg="#FFFFFF", panel_bg="#F8FAFC", chrome="#0891B2", chrome_dim="#0891B2",
        text="#0F172A", muted="#475569", accent="#059669", portrait="#7C3AED",
        red="#DC2626", border="#E2E8F0",
    ),
}


def fmt(v):
    return f"{v:.2f}".rstrip('0').rstrip('.') if '.' in f"{v:.2f}" else f"{v:.2f}"


def keytimes_str(times, total):
    return ";".join(fmt(t / total) for t in times)


def values_str(vals):
    return ";".join(fmt(v) for v in vals)


def build_row_markup(x0, x1, y, label, value, muted, text_color, font_size=14):
    total_width = x1 - x0
    dot_count = 46
    label_part = f"{label} "
    dots = "." * dot_count
    content_label = label_part + dots + " "
    esc_value = (value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    esc_label = (content_label.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    return (
        f'<text x="{x0}" y="{y}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
        f'font-size="{font_size}" textLength="{total_width}" lengthAdjust="spacingAndGlyphs">'
        f'<tspan fill="{muted}">{esc_label}</tspan><tspan fill="{text_color}">{esc_value}</tspan>'
        f'</text>'
    )


def build_dense_circles(pts, cx, cy, scale, r=1.15):
    parts = []
    for x, y in pts:
        px = cx + x * scale
        py = cy + y * scale
        parts.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r}"/>')
    return "".join(parts)


def build_travelers(channel_portrait, channel_mina, channel_dr, channel_x, cx, cy, scale, r=1.7):
    parts = []
    n = len(channel_portrait)
    kt = keytimes_str(POS_TIMES, T_TOTAL)
    splines = " ".join([".42 0 .58 1"] * (len(POS_TIMES) - 1))
    for i in range(n):
        p = channel_portrait[i]
        m = channel_mina[i]
        d = channel_dr[i]
        xx = channel_x[i]
        cxs = [
            cx + p[0] * scale, cx + p[0] * scale, cx + m[0] * scale, cx + m[0] * scale,
            cx + d[0] * scale, cx + d[0] * scale, cx + xx[0] * scale, cx + xx[0] * scale,
            cx + p[0] * scale,
        ]
        cys = [
            cy + p[1] * scale, cy + p[1] * scale, cy + m[1] * scale, cy + m[1] * scale,
            cy + d[1] * scale, cy + d[1] * scale, cy + xx[1] * scale, cy + xx[1] * scale,
            cy + p[1] * scale,
        ]
        cx_vals = ";".join(f"{v:.0f}" for v in cxs)
        cy_vals = ";".join(f"{v:.0f}" for v in cys)
        parts.append(
            f'<circle r="{r}">'
            f'<animate attributeName="cx" values="{cx_vals}" keyTimes="{kt}" dur="{T_TOTAL}s" '
            f'repeatCount="indefinite"/>'
            f'<animate attributeName="cy" values="{cy_vals}" keyTimes="{kt}" dur="{T_TOTAL}s" '
            f'repeatCount="indefinite"/>'
            f'</circle>'
        )
    return "".join(parts)


def build_banner(theme):
    pal = PALETTES[theme]
    dense_pts = np.load(f"{ASSETS}\\dense_pts.npy")
    ch_portrait = np.load(f"{ASSETS}\\channel_portrait.npy")
    ch_mina = np.load(f"{ASSETS}\\channel_mina.npy")
    ch_dr = np.load(f"{ASSETS}\\channel_darkroom.npy")
    ch_x = np.load(f"{ASSETS}\\channel_x.npy")

    box_x0 = MARGIN + PAD
    box_x1 = MARGIN + LEFT_W - PAD
    box_y0 = MARGIN + HEADER_H + 34
    box_y1 = H - MARGIN - 16
    box_cx = (box_x0 + box_x1) / 2
    box_cy = (box_y0 + box_y1) / 2
    box_w = box_x1 - box_x0
    box_h = box_y1 - box_y0
    fit_scale = 0.86 * min(box_w, box_h)

    dense_color = pal["portrait"]
    dense_group = build_dense_circles(dense_pts, box_cx, box_cy, fit_scale)
    traveler_group = build_travelers(ch_portrait, ch_mina, ch_dr, ch_x, box_cx, box_cy, fit_scale)

    dense_op_vals = values_str([1, 1, 0, 0, 1])
    trav_op_vals = values_str([0, 0, 1, 1, 0])
    op_kt = keytimes_str(OPACITY_TIMES, T_TOTAL)

    right_x0 = MARGIN + LEFT_W + 24
    right_x1 = W - MARGIN - 22
    rows_markup = []
    row_y0 = MARGIN + HEADER_H + 56
    row_h = 24
    for i, (label, value) in enumerate(ROWS):
        y = row_y0 + i * row_h
        rows_markup.append(build_row_markup(right_x0, right_x1, y, label, value, pal["muted"], pal["text"]))
    rows_svg = "".join(rows_markup)

    clip_id = f"term-clip-{theme}"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<clipPath id="{clip_id}"><rect x="{MARGIN}" y="{MARGIN}" width="{W - 2*MARGIN}" height="{H - 2*MARGIN}" rx="{RX}"/></clipPath>
<style>
  text {{ dominant-baseline: alphabetic; }}
  .mono {{ font-family: ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; }}
</style>
</defs>
<rect x="{MARGIN}" y="{MARGIN}" width="{W - 2*MARGIN}" height="{H - 2*MARGIN}" rx="{RX}" fill="{pal['bg']}" stroke="{pal['border']}" stroke-width="1.5"/>
<g clip-path="url(#{clip_id})">
  <rect x="{MARGIN}" y="{MARGIN}" width="{W - 2*MARGIN}" height="{HEADER_H}" fill="{pal['panel_bg']}"/>
  <line x1="{MARGIN}" y1="{MARGIN + HEADER_H}" x2="{W - MARGIN}" y2="{MARGIN + HEADER_H}" stroke="{pal['border']}" stroke-width="1"/>
  <line x1="{MARGIN + LEFT_W}" y1="{MARGIN + HEADER_H}" x2="{MARGIN + LEFT_W}" y2="{H - MARGIN}" stroke="{pal['border']}" stroke-width="1"/>

  <circle cx="{MARGIN + 20}" cy="{MARGIN + HEADER_H/2}" r="4" fill="{pal['muted']}" opacity="0.5"/>
  <circle cx="{MARGIN + 34}" cy="{MARGIN + HEADER_H/2}" r="4" fill="{pal['muted']}" opacity="0.5"/>
  <circle cx="{MARGIN + 48}" cy="{MARGIN + HEADER_H/2}" r="4" fill="{pal['muted']}" opacity="0.5"/>
  <text x="{MARGIN + 68}" y="{MARGIN + HEADER_H/2 + 5}" class="mono" font-size="13" fill="{pal['chrome']}">profile.sh --live</text>

  <g>
    <circle cx="{W - MARGIN - 128}" cy="{MARGIN + HEADER_H/2}" r="4" fill="{pal['red']}">
      <animate attributeName="opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/>
    </circle>
    <text x="{W - MARGIN - 118}" y="{MARGIN + HEADER_H/2 + 4}" class="mono" font-size="12" fill="{pal['red']}" letter-spacing="1">LIVE</text>
  </g>
  <rect x="{W - MARGIN - 92}" y="{MARGIN + 9}" width="76" height="22" rx="11" fill="none" stroke="{pal['chrome']}" stroke-width="1" opacity="0.6"/>
  <text x="{W - MARGIN - 54}" y="{MARGIN + HEADER_H/2 + 4}" class="mono" font-size="12" fill="{pal['text']}" text-anchor="middle">@zkjays</text>

  <text x="{MARGIN + PAD}" y="{MARGIN + HEADER_H + 22}" class="mono" font-size="13" fill="{pal['chrome']}" letter-spacing="1.5">VISUAL.MAP</text>
  <text x="{MARGIN + LEFT_W + 24}" y="{MARGIN + HEADER_H + 22}" class="mono" font-size="13" fill="{pal['chrome']}" letter-spacing="1.5">SYSTEM.INFO</text>

  <g fill="{dense_color}" opacity="1">
    <animate attributeName="opacity" values="{dense_op_vals}" keyTimes="{op_kt}" dur="{T_TOTAL}s" repeatCount="indefinite"/>
    {dense_group}
  </g>
  <g fill="{dense_color}" opacity="0">
    <animate attributeName="opacity" values="{trav_op_vals}" keyTimes="{op_kt}" dur="{T_TOTAL}s" repeatCount="indefinite"/>
    {traveler_group}
  </g>

  {rows_svg}
</g>
</svg>'''
    return svg


for theme in ("dark", "light"):
    svg = build_banner(theme)
    path = f"{OUT}\\{theme}.svg"
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    import os
    print(theme, "bytes", os.path.getsize(path))
