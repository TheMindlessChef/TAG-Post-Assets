#!/usr/bin/env python3
"""Contact sheets per variant. Adds a 'STAND-IN LOGO' note on the sheet (never on the assets) while the
logo is not the approved master."""
import sys; sys.path.insert(0, '/workspace/tag-brand/day1-v2/src')
from PIL import Image, ImageDraw, ImageFont
from render import NAMES, ROOT, FONTS, VARIANTS, logo_asset
f_lab = ImageFont.truetype(FONTS['INTER'], 22); f_note = ImageFont.truetype(FONTS['INTER'], 26)
def sheet(var, ig):
    tw, th = (760, 950) if ig else (1000, 563)
    cols, gap, pad, top = 3, 32, 48, 110
    rows = 2
    W = pad*2 + cols*tw + (cols-1)*gap; Hh = top + rows*(th+50) + (rows-1)*gap + pad
    sh = Image.new('RGB', (W, Hh), (24, 24, 26)); d = ImageDraw.Draw(sh)
    title = f'TAG day 1 v2 · Variant {var}: {VARIANTS[var]["name"]} · {"Instagram 1080x1350" if ig else "X/Facebook 1600x900"} · DRAFT'
    d.text((pad, 40), title, font=f_note, fill=(242, 240, 235))
    if logo_asset()[1]:
        note = 'STAND-IN LOGO (derived from X avatar, not approved master)'
        w = d.textlength(note, font=f_note)
        d.rectangle((W-pad-w-28, 28, W-pad, 80), fill=(255, 214, 0)); d.text((W-pad-w-14, 40), note, font=f_note, fill=(0, 0, 0))
    for i, n in enumerate(sorted(NAMES)):
        name = f'{NAMES[n]}-{var}' + ('-ig' if ig else '')
        im = Image.open(f'{ROOT}/{"ig/" if ig else ""}{name}.png').convert('RGB').resize((tw, th), Image.LANCZOS)
        x = pad + (i % cols)*(tw+gap); y = top + (i//cols)*(th+50+gap)
        sh.paste(im, (x, y)); d.rectangle((x-1, y-1, x+tw, y+th), outline=(70, 70, 74))
        d.text((x, y+th+12), name + '.png', font=f_lab, fill=(200, 200, 200))
    out = f'{ROOT}/{"ig/contact-sheet-ig-" if ig else "contact-sheet-"}{var}.png'
    sh.save(out); print(out)
for v in 'AB':
    sheet(v, False); sheet(v, True)
