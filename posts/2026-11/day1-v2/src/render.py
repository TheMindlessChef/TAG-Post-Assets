#!/usr/bin/env python3
"""TAG day-1 v2 renderer. HTML + inline SVG -> PNG via headless Chrome.
Usage: python3 render.py [post-number ...]   (no args = all six, both variants, both sizes)
Drop-in assets: anything placed in /workspace/tag-brand/approved/ is picked up automatically
(logo: *logo*/*wordmark*; icons by keyword, see ICONS). Until then the logo is the X avatar
(/workspace/tag-brand/avatar.jpg) pasted unmodified on a pure-black ground = STAND-IN, not the master."""
import glob, json, math, os, subprocess, sys, html as H

ROOT = '/workspace/tag-brand/day1-v2'
APPROVED = '/workspace/tag-brand/approved'
AVATAR = '/workspace/tag-brand/avatar.jpg'
BG, FG, ACC = '#000000', '#F2F0EB', '#1E7BFF'   # one neutral, one text colour, one accent
FONTS = {
  'SG':    '/usr/share/fonts/truetype/sand-box/google/Space Grotesk/SpaceGrotesk-VariableFont_wght.ttf',
  'INTER': '/usr/share/fonts/truetype/sand-box/google/Inter/Inter-VariableFont_opsz,wght.ttf',
  'PLEX':  '/usr/share/fonts/truetype/sand-box/google/IBM Plex Sans/IBMPlexSans-VariableFont_wdth,wght.ttf',
}
VARIANTS = {  # head family/weight, body family/weight, headline tracking
  'A': dict(head='SG', body='INTER', track='-0.035em', name='Space Grotesk Bold + Inter Regular'),
  'B': dict(head='PLEX', body='PLEX', track='-0.025em', name='IBM Plex Sans Bold + IBM Plex Sans Regular'),
}
# Which approved icon would drop into which post (slot is empty until the file exists)
ICONS = {1: (['headphone'], ['brain']), 2: (['waveform', 'wave'], []), 3: (['shield', 'protected'], []),
         4: (['signal'], []), 5: (None, []), 6: (['play'], [])}
NAMES = {1: 'post1-gta-preload-audio', 2: 'post2-footsteps-eq', 3: 'post3-obs33-checklist',
         4: 'post4-phasmo-resonance-radar', 5: 'post5-build-in-public-roadmap', 6: 'post6-twitch-recaps'}

def find_asset(keys, exclude=()):
    if not keys or not os.path.isdir(APPROVED): return None
    for f in sorted(glob.glob(APPROVED + '/**/*.png', recursive=True)):
        n = os.path.basename(f).lower()
        if 'haggis' in n or 'logo' in n: continue
        if any(k in n for k in keys) and not any(e in n for e in exclude): return f
    return None

CLEAN = APPROVED + '/clean'   # background-removed versions; preferred automatically once they exist
USE_ICONS = True              # approved neon glyphs (clean/*-glyph.png only, never tiles)
ICON_FILES = {1: CLEAN + '/icon-headphones-glyph.png', 2: CLEAN + '/icon-footsteps-glyph.png',
              4: CLEAN + '/icon-signal-glyph.png', 6: CLEAN + '/icon-play-glyph.png'}   # P3, P5: none
ICON_ORIG = {k: APPROVED + '/' + os.path.basename(v).replace('-glyph', '') for k, v in ICON_FILES.items()}
CAP = 0.698   # cap height / em of the headline faces (Plex 0.698, Space Grotesk 0.70): icon box <= cap height
CUR = {'icon': None}

def icon_box(fmt):
    return int(FMT[fmt]['hd'] * CAP) - 2          # X: 53px, IG: 70px square box

def icon_html(path, fmt):
    """Pre-downscale the large glyph with Lanczos (scale only, no other change) so its visible art fits the
    square box, cache it, and return an <img> at exact pixel size whose visible art is left-aligned to the
    margin and vertically centred in the kicker row."""
    from PIL import Image
    box = icon_box(fmt); M = FMT[fmt]['M']
    x0, y0, x1, y1, iw, ih = art_bbox(path)
    vw, vh = (x1-x0)*iw, (y1-y0)*ih
    sc = box / max(vw, vh)
    W, H = max(1, round(iw*sc)), max(1, round(ih*sc))
    os.makedirs(f'{ROOT}/src/icon-cache', exist_ok=True)
    out = f'{ROOT}/src/icon-cache/{os.path.splitext(os.path.basename(path))[0]}-{W}x{H}.png'
    if not os.path.exists(out):
        Image.open(path).resize((W, H), Image.LANCZOS).save(out)
    left = M - x0*W; top = M + (box - vh*sc)/2 - y0*H
    return f'<img src="file://{out}" style="position:absolute;left:{left:.1f}px;top:{top:.1f}px;width:{W}px;height:{H}px">', out
def approved(name):
    """Resolve an approved asset: clean/<stem>.png if present, else the original in approved/."""
    stem = os.path.splitext(name)[0]
    c = f'{CLEAN}/{stem}.png'
    return c if os.path.exists(c) else f'{APPROVED}/{name}'
LOGO_MASTER = approved('tag-logo-metallic.jpg')       # placed unaltered, proportional scale only
HAGGIS = {5: approved('haggis-arms-crossed.png')}     # approved transparent PNGs only; max 1-2 posts
def logo_asset():
    return (LOGO_MASTER, False) if os.path.exists(LOGO_MASTER) else (AVATAR, True)   # (path, is_stand_in)

def art_bbox(path):
    """Visible-artwork bbox as fractions of the file (alpha for PNG, non-black for JPG). Used only to
    position the untouched file so its visible artwork aligns to the grid; the file itself is never cropped."""
    from PIL import Image
    im = Image.open(path)
    bb = im.getchannel('A').getbbox() if im.mode == 'RGBA' else im.convert('L').point(lambda v: 255 if v > 8 else 0).getbbox()
    return bb[0]/im.width, bb[1]/im.height, bb[2]/im.width, bb[3]/im.height, im.width, im.height

def place(path, left=None, right=None, bottom=None, width=None, height=None, W=0, Hh=0):
    """Place file scaled proportionally so its VISIBLE art has given width/height, aligned by visible edges."""
    x0, y0, x1, y1, iw, ih = art_bbox(path)
    if width: sc = width/((x1-x0)*iw)
    else: sc = height/((y1-y0)*ih)
    w, h = iw*sc, ih*sc
    lx = left - x0*w if left is not None else (W-right) - x1*w
    ty = (Hh-bottom) - y1*h
    return f'<img src="file://{path}" style="position:absolute;left:{lx:.1f}px;top:{ty:.1f}px;width:{w:.1f}px;height:{h:.1f}px">', (lx, ty, w, h, sc)

# ---------- format geometry ----------
# S = visible logo wordmark width. LB = logo/Haggis baseline from bottom (IG: raised so nothing sits in bottom 10%).
# CB = lowest y for content graphics. small = minimum size for kickers / chart / plan labels (22 on X, 28 on IG).
FMT = {
  'x':  dict(W=1600, H=900,  M=128, LB=128, CB=772,  S=210, hd=80, sec=32, body=27, lab=24, kick=24, small=24),
  'ig': dict(W=1080, H=1350, M=88,  LB=138, CB=1040, S=190, hd=104, sec=32, body=28, lab=28, kick=28, small=28),
}

def esc(s): return H.escape(s)

def page(fmt, var, inner, icon_path, extra_art=''):
    g, v = FMT[fmt], VARIANTS[var]
    W, Hh, M, S = g['W'], g['H'], g['M'], g['S']
    logo, _ = logo_asset()
    logo_html, _ = place(logo, left=M, bottom=g['LB'], width=S, W=W, Hh=Hh)   # visible wordmark aligned to bottom-left margin
    icon_html = CUR['icon_html'] if CUR['icon'] else ''
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:SG;src:url("file://{FONTS['SG']}");font-weight:300 700}}
@font-face{{font-family:INTER;src:url("file://{FONTS['INTER']}");font-weight:100 900}}
@font-face{{font-family:PLEX;src:url("file://{FONTS['PLEX']}");font-weight:100 700}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{Hh}px;background:{BG};overflow:hidden;color:{FG}}}
.h{{font-family:{v['head']};font-weight:700;letter-spacing:{v['track']};line-height:1.02;font-feature-settings:"kern";text-wrap:balance}}
.b{{font-family:{v['body']};font-weight:400;letter-spacing:-0.005em;line-height:1.35;text-wrap:pretty}}
.kick{{font-size:{g['kick']}px;color:{ACC};letter-spacing:0.01em}}
.hd{{font-size:{g['hd']}px}}
.sec{{font-size:{g['sec']}px;line-height:1.3;text-wrap:balance}}
.body{{font-size:{g['body']}px}}
.lab{{font-size:{g['lab']}px;line-height:1.3}}
.acc{{color:{ACC}}}
svg text{{font-family:{v['body']};font-weight:400;fill:{FG}}}
svg .hs{{font-family:{v['head']};font-weight:700}}
.abs{{position:absolute}}
</style></head><body>{inner}{extra_art}{icon_html}{logo_html}<pre id="chk" style="display:none"></pre><script>{CHECK_JS}</script></body></html>'''

CHECK_JS = """document.fonts.ready.then(()=>{const r=[];document.querySelectorAll('.h,.b,svg text').forEach(e=>{
 if(e.children.length&&!(e.tagName=='text')&&[...e.children].some(c=>c.tagName=='DIV'))return;
 const range=document.createRange();range.selectNodeContents(e);const b=range.getBoundingClientRect();
 if(b.width>0)r.push({fs:parseFloat(getComputedStyle(e).fontSize),t:e.textContent.slice(0,40),x0:b.left,y0:b.top,x1:b.right,y1:b.bottom,lines:range.getClientRects().length});});
 document.getElementById('chk').textContent=JSON.stringify(r);});"""

# ---------- shared text block ----------
def kicker_row(fmt, kicker, absolute=False):
    """Kicker sits in a row one icon-box tall on every post so headlines align across the set; on posts with an
    icon the label starts after the icon box."""
    g = FMT[fmt]; box = icon_box(fmt); M = g['M']
    pad = box + 20 if CUR['icon'] else 0
    style = f'height:{box}px;display:flex;align-items:center;padding-left:{pad}px'
    if absolute: style += f';position:absolute;left:{M}px;top:{M}px'
    return f'<div class="b kick" style="{style}">{esc(kicker)}</div>'

def textblock(fmt, kicker, head, sec=None, extra='', x=None, y=None, w=None):
    g = FMT[fmt]; M = g['M']
    x = M if x is None else x; y = M if y is None else y
    w = (541 if fmt == 'x' else g['W'] - 2*M) if w is None else w
    s = f'<div class="abs" style="left:{x}px;top:{y}px;width:{w}px">'
    s += kicker_row(fmt, kicker)
    s += f'<div class="h hd" style="margin-top:{22 if fmt=="x" else 26}px">{head}</div>'
    if sec: s += f'<div class="b sec" style="margin-top:{28 if fmt=="x" else 32}px">{sec}</div>'
    s += extra + '</div>'
    return s

RX = 765          # 16:9 right column start (grid: left col 128-669, right col 765-1472)
RW = 1472 - RX

# ---------- Post 1 ----------
def post1(fmt):
    g = FMT[fmt]
    steps = [('01', 'Run the 3D Audio profile on YOUR headset'),
             ('02', 'Set a comfortable volume'),
             ('03', 'Then EQ: cut before YOU boost')]
    def steplist(w, numsz, txtsz, gap):
        s = f'<div style="width:{w}px">'
        for i, (n, t) in enumerate(steps):
            s += (f'<div style="display:flex;align-items:baseline;border-top:2px solid {FG};padding:{gap}px 0 {gap+4}px">'
                  f'<div class="h acc" style="font-size:{numsz}px;width:{numsz*2.4}px;flex:none;letter-spacing:0">{n}</div>'
                  f'<div class="b" style="font-size:{txtsz}px;line-height:1.25">{esc(t)}</div></div>')
        return s + '</div>'
    head = 'Sort YOUR audio first.'
    sec = 'GTA VI pre-load opens on PS5 on <span class="acc">10&nbsp;Nov</span>.'
    if fmt == 'x':
        tb = textblock(fmt, 'Pre-load · 10 Nov', head.replace('YOUR ', 'YOUR<br>'), sec)
        return tb + f'<div class="abs" style="left:{RX}px;top:{196}px">{steplist(RW, 30, 32, 26)}</div>'
    tb = textblock(fmt, 'Pre-load · 10 Nov', head.replace('YOUR ', 'YOUR<br>'), sec)
    return tb + f'<div class="abs" style="left:88px;top:{700}px">{steplist(904, 32, 36, 30)}</div>'

# ---------- Post 2: real EQ maths (RBJ biquads) ----------
def biquad_db(f, kind, f0, gain, q, fs=48000):
    A = 10**(gain/40); w0 = 2*math.pi*f0/fs; c, s = math.cos(w0), math.sin(w0); al = s/(2*q)
    if kind == 'peak':
        b = [1+al*A, -2*c, 1-al*A]; a = [1+al/A, -2*c, 1-al/A]
    else:  # low shelf
        sa = 2*math.sqrt(A)*al
        b = [A*((A+1)-(A-1)*c+sa), 2*A*((A-1)-(A+1)*c), A*((A+1)-(A-1)*c-sa)]
        a = [(A+1)+(A-1)*c+sa, -2*((A-1)+(A+1)*c), (A+1)+(A-1)*c-sa]
    w = 2*math.pi*f/fs
    z1 = complex(math.cos(-w), math.sin(-w)); z2 = z1*z1
    hz = (b[0]+b[1]*z1+b[2]*z2)/(a[0]+a[1]*z1+a[2]*z2)
    return 20*math.log10(abs(hz))

def eq_svg(w, h, fsz):
    pad_b = fsz*2.2; ph = h - pad_b; f_lo, f_hi = 20, 20000
    X = lambda f: (math.log10(f)-math.log10(f_lo))/(math.log10(f_hi)-math.log10(f_lo))*w
    rng = 8.0; Y = lambda db: ph/2 - db/rng*(ph/2)
    pts = []
    for i in range(400):
        f = f_lo*(f_hi/f_lo)**(i/399)
        db = biquad_db(f, 'shelf', 150, -3.0, 0.7) + biquad_db(f, 'peak', 3200, 2.5, 1.0)
        pts.append((X(f), Y(db)))
    path = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    s = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">'
    # frame + faint log grid (no numbers)
    for f in [50, 100, 200, 500, 1000, 2000, 5000, 10000]:
        s += f'<line x1="{X(f):.1f}" y1="0" x2="{X(f):.1f}" y2="{ph}" stroke="{FG}" stroke-opacity="{0.22 if f in (100,1000,10000) else 0.1}" stroke-width="1"/>'
    s += f'<line x1="0" y1="{ph/2}" x2="{w}" y2="{ph/2}" stroke="{FG}" stroke-opacity="0.5" stroke-width="1.5" stroke-dasharray="6 6"/>'
    s += f'<rect x="0.75" y="0.75" width="{w-1.5}" height="{ph-1.5}" fill="none" stroke="{FG}" stroke-opacity="0.35" stroke-width="1.5"/>'
    s += f'<path d="{path}" fill="none" stroke="{ACC}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>'
    # axis words
    for f, t, anc in [(f_lo, 'Lows', 'start'), (400, 'Mids', 'middle'), (3200, 'Upper mids', 'middle'), (f_hi, 'Highs', 'end')]:
        s += f'<text x="{X(f):.1f}" y="{ph+fsz*1.5}" font-size="{fsz}" text-anchor="{anc}">{t}</text>'
    s += f'<text x="14" y="{fsz*1.3}" font-size="{fsz}">Boost</text>'
    s += f'<text x="14" y="{ph-fsz*0.6}" font-size="{fsz}">Cut</text>'
    s += f'<text x="{w-14}" y="{ph/2-12}" font-size="{fsz}" text-anchor="end">Flat</text>'
    # annotations with leader lines
    xl, yl = X(45), Y(biquad_db(45,'shelf',150,-3,0.7)+biquad_db(45,'peak',3200,2.5,1))
    s += f'<circle cx="{xl:.1f}" cy="{yl:.1f}" r="7" fill="{BG}" stroke="{FG}" stroke-width="2.5"/>'
    s += f'<line x1="{xl:.1f}" y1="{yl+9:.1f}" x2="{xl:.1f}" y2="{yl+ph*0.16:.1f}" stroke="{FG}" stroke-width="1.5"/>'
    s += f'<text class="hs" x="{xl-6:.1f}" y="{yl+ph*0.16+fsz*1.1:.1f}" font-size="{fsz*1.1}">Trim lows</text>'
    xp = X(3200); yp = Y(biquad_db(3200,'shelf',150,-3,0.7)+2.5)
    s += f'<circle cx="{xp:.1f}" cy="{yp:.1f}" r="7" fill="{BG}" stroke="{FG}" stroke-width="2.5"/>'
    s += f'<line x1="{xp:.1f}" y1="{yp-9:.1f}" x2="{xp:.1f}" y2="{yp-ph*0.16:.1f}" stroke="{FG}" stroke-width="1.5"/>'
    s += f'<text class="hs" x="{xp:.1f}" y="{yp-ph*0.16-fsz*0.5:.1f}" font-size="{fsz*1.1}" text-anchor="middle">Lift upper mids</text>'
    return s + '</svg>'

def post2(fmt):
    head = 'More bass won’t save YOU.'
    sec = 'Footstep detail sits in the upper mids. Small moves beat big ones.'
    if fmt == 'x':
        tb = textblock(fmt, 'Footsteps EQ', 'More bass<br>won’t save YOU.', sec)
        return tb + f'<div class="abs" style="left:{RX}px;top:{128}px">{eq_svg(RW, 644, 24)}</div>'
    tb = textblock(fmt, 'Footsteps EQ', 'More bass<br>won’t save YOU.', sec)
    return tb + f'<div class="abs" style="left:88px;top:{600}px">{eq_svg(904, 440, 28)}</div>'

# ---------- Post 3 ----------
def post3(fmt):
    items = [('Export YOUR Profile + Scene Collection', 'Do it before YOU update.', True),
             ('Safe Mode if it misbehaves', 'It now skips third-party plugins and the WebSocket server.', False)]
    def checklist(w, tsz, ssz, box):
        s = f'<div style="width:{w}px">'
        for i, (t, sub, done) in enumerate(items):
            tick = (f'<svg width="{box}" height="{box}" viewBox="0 0 {box} {box}" style="flex:none">'
                    f'<rect x="1.5" y="1.5" width="{box-3}" height="{box-3}" fill="none" stroke="{FG}" stroke-width="3"/>'
                    + (f'<path d="M{box*.24},{box*.52} L{box*.43},{box*.7} L{box*.78},{box*.3}" fill="none" stroke="{ACC}" stroke-width="5" stroke-linecap="square"/>' if done else '')
                    + '</svg>')
            s += (f'<div style="display:flex;gap:{box*0.6}px;border-top:2px solid {FG};padding:30px 0 34px">{tick}'
                  f'<div><div class="h" style="font-size:{tsz}px;letter-spacing:-0.015em;line-height:1.12">{esc(t)}</div>'
                  f'<div class="b" style="font-size:{ssz}px;margin-top:12px">{esc(sub)}</div></div></div>')
        return s + '</div>'
    if fmt == 'x':
        tb = textblock(fmt, 'OBS 33 · Two habits', 'Before YOU<br>update OBS 33', 'Do these two things first.')
        return tb + f'<div class="abs" style="left:{RX}px;top:{196}px">{checklist(RW, 36, 33, 44)}</div>'
    tb = textblock(fmt, 'OBS 33 · Two habits', 'Before YOU<br>update OBS 33', 'Do these two things first.')
    return tb + f'<div class="abs" style="left:88px;top:{600}px">{checklist(904, 40, 28, 46)}</div>'

# ---------- Post 4: floor plan ----------
def plan_svg(w, h, fsz):
    u = lambda fx, fy: (fx*w, fy*h)
    sw = 3; op = 0.85
    s = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">'
    g = f'<g stroke="{FG}" stroke-opacity="{op}" stroke-width="{sw}" fill="none" stroke-linecap="square">'
    # walls as segments in unit coords (door gaps left open)
    segs = [ (0,0,1,0),(1,0,1,1),(1,1,0,1),(0,1,0,0),          # outer
             (0.42,0,0.42,0.30),(0.42,0.42,0.42,0.62),         # vertical wall w/ door
             (0,0.62,0.30,0.62),(0.40,0.62,0.70,0.62),(0.80,0.62,1,0.62),  # corridor top
             (0.62,0.62,0.62,1),                               # bottom split
             (0.42,0.36,0.62,0.36),(0.74,0.36,1,0.36),         # upper right split w/ door
           ]
    for x1,y1,x2,y2 in segs:
        a, b = u(x1,y1), u(x2,y2); g += f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>'
    s += g + '</g>'
    # looping sound (left room): steady, constant rings
    lx, ly = u(0.21, 0.27)
    s += f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="14" fill="{ACC}"/>'
    for r in (34, 54):
        s += f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="{r}" fill="none" stroke="{ACC}" stroke-width="3"/>'
    s += f'<text class="hs" x="{lx:.1f}" y="{ly+54+fsz*1.9:.1f}" font-size="{fsz*1.1}" text-anchor="middle">Looping sound</text>'
    s += f'<text x="{lx:.1f}" y="{ly+54+fsz*3.15:.1f}" font-size="{fsz}" text-anchor="middle">Stays on screen</text>'
    # one-off ping (upper-right room): rings fading out
    px, py = u(0.875 if fsz > 28 and w < 800 else 0.84, 0.18)
    s += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="8" fill="{FG}"/>'
    for r, o in [(24, .8), (42, .45), (60, .18)]:
        s += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r}" fill="none" stroke="{FG}" stroke-opacity="{o}" stroke-width="3"/>'
    tx = u(0.45 if fsz > 28 and w < 800 else 0.47, 0)[0]
    s += f'<text class="hs" x="{tx:.1f}" y="{py-fsz*0.15:.1f}" font-size="{fsz*1.1}">One-off sound</text>'
    s += f'<text x="{tx:.1f}" y="{py+fsz*1.15:.1f}" font-size="{fsz}">Pings and fades</text>'
    return s + '</svg>'

def post4(fmt):
    sec = 'Phasmophobia’s Resonance update reworks the Sound Sensor map. Late&nbsp;Nov.'
    if fmt == 'x':
        tb = textblock(fmt, 'Resonance update · Late\u00a0Nov', 'Sound is now<br>gameplay info.', sec)
        return tb + f'<div class="abs" style="left:{RX}px;top:{128}px">{plan_svg(RW, 644, 29)}</div>'
    tb = textblock(fmt, 'Resonance update · Late\u00a0Nov', 'Sound is now<br>gameplay info.', sec)
    return tb + f'<div class="abs" style="left:88px;top:{620}px">{plan_svg(904, 420, 28)}</div>'

# ---------- Post 5: typographic roadmap strip (approved by Neil 3 Nov 2026) ----------
def post5(fmt):
    """Typographic roadmap strip + Haggis (placed in build()). Approved by Neil 3 Nov 2026."""
    g = FMT[fmt]; M = g['M']
    kick = kicker_row(fmt, 'Build-in-public check-in', absolute=True)
    if fmt == 'x':
        y = 280; nx1 = 832; tx0, tx1 = 880, 1210      # NEXT column | THEN column | Haggis (right, 1271-1472)
        s = kick
        s += f'<div class="abs" style="left:{M}px;top:{y}px;width:{nx1-M}px;height:6px;background:{ACC}"></div>'
        s += f'<div class="abs" style="left:{tx0}px;top:{y+2}px;width:{tx1-tx0}px;height:2px;background:{FG}"></div>'
        s += f'<div class="abs h acc" style="left:{M}px;top:{y+44}px;width:{nx1-M}px;font-size:72px">NEXT:<br>A4G closed launch</div>'
        s += f'<div class="abs b" style="left:{tx0}px;top:{y+44}px;width:{tx1-tx0}px;font-size:34px;line-height:1.25">THEN:<br>MultiChat +<br>Studio Apps</div>'
        s += f'<div class="abs b sec" style="left:{M}px;top:{y+222}px">Built solo. Built in public.</div>'
        return s
    y = 300; cw = 520
    s = kick
    s += f'<div class="abs" style="left:{M}px;top:{y}px;width:904px;height:6px;background:{ACC}"></div>'
    s += f'<div class="abs h acc" style="left:{M}px;top:{y+44}px;width:904px;font-size:92px">NEXT:<br>A4G closed launch</div>'
    s += f'<div class="abs" style="left:{M}px;top:{y+330}px;width:{cw}px;height:2px;background:{FG}"></div>'
    s += f'<div class="abs b" style="left:{M}px;top:{y+370}px;width:{cw}px;font-size:40px;line-height:1.25">THEN:<br>MultiChat + Studio Apps</div>'
    s += f'<div class="abs b sec" style="left:{M}px;top:{y+530}px">Built solo. Built in public.</div>'
    return s

# ---------- Post 6: generic desktop window wireframe (desktop-first: no phone screens anywhere) ----------
def desktop_svg(w, h, fsz, clips=5, preview=True):
    lw = 3; bar = fsz*2.1; p = fsz*1.0
    if not preview:   # compact window: title bar + clip timeline only; height derived from content
        ch0 = ((w-2*p-(clips-1)*10)/clips)*0.56
        h = bar + p*1.2 + ch0 + fsz*0.8 + 14 + p*1.4
    s = f'<svg width="{w}" height="{h:.0f}" viewBox="0 0 {w} {h:.0f}" xmlns="http://www.w3.org/2000/svg">'
    s += f'<rect x="{lw/2}" y="{lw/2}" width="{w-lw}" height="{h-lw:.1f}" rx="10" fill="none" stroke="{FG}" stroke-width="{lw}"/>'
    s += f'<line x1="0" y1="{bar}" x2="{w}" y2="{bar}" stroke="{FG}" stroke-width="2"/>'
    s += f'<text class="hs" x="{p}" y="{bar/2+fsz*0.36}" font-size="{fsz}" style="fill:{ACC}">Recap</text>'
    # preview area
    tl_h = fsz*0.9 + (w-2*p)/clips*0.56 + fsz*1.2       # space for clip row + timeline
    pv_top = bar + p; pv_h = h - pv_top - tl_h - p*1.6
    if preview:
        s += f'<rect x="{p}" y="{pv_top:.1f}" width="{w-2*p:.1f}" height="{pv_h:.1f}" rx="6" fill="none" stroke="{FG}" stroke-opacity="0.4" stroke-width="2"/>'
    else:
        pv_top, pv_h = bar + p*0.3, 0
    # clip frames on a timeline, first clip blue
    gap = 10; cw = (w-2*p-(clips-1)*gap)/clips; ch = cw*0.56
    cy = pv_top + pv_h + p*0.9
    for i in range(clips):
        x = p + i*(cw+gap)
        if i == 0: s += f'<rect x="{x:.1f}" y="{cy:.1f}" width="{cw:.1f}" height="{ch:.1f}" rx="5" fill="{ACC}"/>'
        else: s += f'<rect x="{x+1:.1f}" y="{cy+1:.1f}" width="{cw-2:.1f}" height="{ch-2:.1f}" rx="5" fill="none" stroke="{FG}" stroke-width="2.5"/>'
    ty = cy + ch + fsz*0.8
    s += f'<line x1="{p}" y1="{ty:.1f}" x2="{w-p}" y2="{ty:.1f}" stroke="{FG}" stroke-width="2"/>'
    n = 40
    for i in range(n+1):
        x = p + i*(w-2*p)/n; tk = 10 if i % 5 == 0 else 5
        s += f'<line x1="{x:.1f}" y1="{ty:.1f}" x2="{x:.1f}" y2="{ty+tk:.1f}" stroke="{FG}" stroke-opacity="0.5" stroke-width="1.5"/>'
    # playhead at the end of the first clip
    px = p + cw
    s += f'<line x1="{px:.1f}" y1="{cy-6:.1f}" x2="{px:.1f}" y2="{ty+14:.1f}" stroke="{FG}" stroke-width="2.5"/>'
    return s + '</svg>'

def post6(fmt):
    # Wording follows Twitch's announcement (blog.twitch.tv/en/2026/10/20/stream-recaps/):
    # "A Stream Recap is a highlight reel of clips from a livestream" / "Your followers can find the Recap in a
    # shelf at the top of their mobile feed. Recaps also live on your channel page." / "By default, clips made by
    # you and your editors are included ... but you can easily remove, add or edit clips at any point."
    sec = 'A highlight reel of clips from YOUR stream, in a shelf at the top of followers’ mobile feed and on YOUR channel page.'
    tip = 'Clips by YOU and YOUR editors go in by default. Add, remove or edit them at any point.'
    head = 'When YOU go<br>offline, that’s<br>content.'
    fsz = 26 if fmt == 'x' else 30; clips = 5
    ww = RW if fmt == 'x' else 904
    p = fsz; wh = fsz*2.1 + p*1.2 + ((ww-2*p-(clips-1)*10)/clips)*0.56 + fsz*0.8 + 14 + p*1.4
    win = desktop_svg(ww, 0, fsz, clips, preview=False)
    if fmt == 'x':
        tb = textblock(fmt, 'Stream Recaps', head, None)
        top = 128 + icon_box(fmt) + 22 + 6      # window top aligns with the headline's top
        txt = (f'<div class="abs" style="left:{RX}px;top:{top+wh+44:.0f}px;width:{RW}px">'
               f'<div class="b sec" style="font-size:37px">{sec}</div><div class="b" style="font-size:32px;margin-top:20px">{tip}</div></div>')
        return tb + f'<div class="abs" style="left:{RX}px;top:{top}px">{win}</div>' + txt
    tb = textblock(fmt, 'Stream Recaps', head, sec, extra=f'<div class="b body" style="margin-top:20px">{tip}</div>')
    return tb + f'<div class="abs" style="left:88px;top:{FMT["ig"]["CB"]-wh:.0f}px">{win}</div>'

POSTS = {1: post1, 2: post2, 3: post3, 4: post4, 5: post5, 6: post6}

def shoot(html_path, png, W, Hh):
    subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
                    '--force-device-scale-factor=1', '--allow-file-access-from-files', f'--window-size={W},{Hh}',
                    '--virtual-time-budget=3000', f'--screenshot={png}', 'file://' + html_path],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def check(html_path, fmt, name):
    g = FMT[fmt]; W, Hh, M, S = g['W'], g['H'], g['M'], g['S']
    dom = subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu', '--allow-file-access-from-files',
                          f'--window-size={W},{Hh}', '--virtual-time-budget=3000', '--dump-dom', 'file://' + html_path],
                         capture_output=True, text=True).stdout
    import re
    m = re.search(r'<pre id="chk"[^>]*>(.*?)</pre>', dom, re.S)
    items = json.loads(H.unescape(m.group(1))) if m and m.group(1).strip() else []
    probs = []
    for it in items:
        if it['x0'] < M-1 or it['x1'] > W-M+1 or it['y0'] < M-6 or it['y1'] > Hh-g['LB']+1: probs.append(('outside margin', it))
        x0, y0, x1, y1, iw, ih = art_bbox(logo_asset()[0]); lh = S*(y1-y0)*ih/((x1-x0)*iw)
        if it['x0'] < M+S+lh and it['y1'] > Hh-g['LB']-2*lh: probs.append(('logo clear-space', it))
        if fmt == 'ig' and it['y1'] > Hh*0.9: probs.append(('bottom 10%', it))
        if it.get('fs', 99) < g['small'] - 0.01: probs.append((f'text {it["fs"]}px < {g["small"]}px', it))
    for p, it in probs: print(f'  !! {name}: {p}: {it["t"]!r} ({it["x0"]:.0f},{it["y0"]:.0f})-({it["x1"]:.0f},{it["y1"]:.0f})')
    return items

def build(nums):
    os.makedirs(f'{ROOT}/ig', exist_ok=True); os.makedirs(f'{ROOT}/src/html', exist_ok=True)
    manifest = {}
    for n in nums:
        icon = ICON_FILES.get(n) if USE_ICONS else None
        for var in 'AB':
            for fmt in ('x', 'ig'):
                g = FMT[fmt]
                CUR['icon'] = icon
                if icon: CUR['icon_html'], icon_cached = icon_html(icon, fmt)
                art = ''
                if n in HAGGIS and os.path.exists(HAGGIS[n]):
                    hh = g['H'] * (0.50 if fmt == 'x' else 0.46)   # 45-55% of frame height, feet on logo baseline
                    art, _ = place(HAGGIS[n], right=g['M'], bottom=g['LB'], height=hh, W=g['W'], Hh=g['H'])
                html = page(fmt, var, POSTS[n](fmt), icon, art)
                base = f'{NAMES[n]}-{var}' + ('-ig' if fmt == 'ig' else '')
                hp = f'{ROOT}/src/html/{base}.html'
                open(hp, 'w').write(html)
                out = f'{ROOT}/{"ig/" if fmt=="ig" else ""}{base}.png'
                shoot(hp, out, g['W'], g['H']); check(hp, fmt, base)
                manifest[out] = dict(post=n, variant=var, logo=logo_asset()[0], logo_stand_in=logo_asset()[1], icon=icon, icon_original=ICON_ORIG.get(n) if icon else None, icon_rendered=icon_cached if icon else None, haggis=HAGGIS.get(n) if n in HAGGIS and os.path.exists(HAGGIS[n]) else None,
                                     fonts=[FONTS[VARIANTS[var]['head']], FONTS[VARIANTS[var]['body']]])
                print(out)
    mp = f'{ROOT}/src/manifest.json'
    old = json.load(open(mp)) if os.path.exists(mp) else {}
    old.update(manifest); json.dump(old, open(mp, 'w'), indent=1)

if __name__ == '__main__':
    build([int(a) for a in sys.argv[1:]] or [1, 2, 3, 4, 5, 6])
