# TAG brand assets: clean transparent PNGs

Made on 3 Nov 2026 (Europe/London) from Neil's approved files in `/workspace/tag-brand/approved/`. The originals were not touched (md5s checked before and after).

**Rules followed.** Only backgrounds were removed. Nothing was redrawn, recoloured, sharpened or AI-regenerated. Every fully opaque pixel in every output is byte-identical to the source (checked in code). The only colour changes are in semi-transparent edge pixels. Where the background was black, those edge pixels were un-premultiplied (RGB ÷ alpha) to remove the black halo, which is standard edge decontamination. Fully transparent pixels have their hidden RGB set to 0. Every file is trimmed to its content plus about 1% transparent padding (at least 8 px).

Working scripts: `/workspace/tagwork/` (`cut.py`, `glyph.py`, `assemble.py`).

## Alpha audit of the sources

| Source | Mode | Background found |
|---|---|---|
| tag-logo-metallic.jpg | RGB, 100% opaque | Solid black |
| haggis-casual.png | RGB, 100% opaque | Solid black |
| haggis-squatting-on-black.jpg | RGB, 100% opaque | Solid black |
| haggis-standing / squatting / arms-out / arms-crossed.png | RGBA, 50–79% fully transparent | None. Edges are clean with no fringe. **But the body alpha is 250–254, not 255** (median 253, under 0.1% of pixels fully opaque), so the subject is about 1% see-through. |
| a4g-logo-blue.png | RGBA, 40% transparent | None. Clean edges. Body alpha is also mostly 250–254. |
| icon-*.png (6250×6250) | RGBA, 94.2% opaque, 4.2% transparent | Outside the rounded tile is **already truly transparent** (clean anti-aliased corners). The checkerboard **inside** the tile is a fake transparency checker baked into the pixels: it is the classic grey checker, darkened by the glass tint. Because it sits inside the tile, removing it would mean repainting the tile, so it was left alone. |

## Files

### tag-logo-metallic.png
- Source: `/workspace/tag-brand/approved/tag-logo-metallic.jpg`
- Size: 1361×601 px, 0.4 MB
- Method: Shape mask from BiRefNet-general (rembg). The edge band is re-keyed from luma (alpha-from-black, ramp max(RGB) 4→44) inside the dilated mask and then un-premultiplied. The interior is untouched.
- Quality / caveats: Clean, crisp bevel edges with no black halo. The dark outline around the letters is part of the artwork. JPEG source, so faint compression noise at the edges.

### haggis-casual.png
- Source: `/workspace/tag-brand/approved/haggis-casual.png`
- Size: 809×1528 px, 1.3 MB
- Method: BiRefNet-general mask with small holes filled. The interior is eroded 3 px and forced to alpha 255. In the edge band, alpha is multiplied by a near-black suppression term ((maxRGB−3)/12) and un-premultiplied against black.
- Quality / caveats: Fur, hood and headphone edges are clean on grey and white. One minor caveat: tiny dark wedges where the hair tuft meets the rope are source shadow, not background. The black gap between the legs was removed.

### haggis-squatting-on-black-cutout.png
- Source: `/workspace/tag-brand/approved/haggis-squatting-on-black.jpg`
- Size: 1183×1460 px, 1.1 MB
- Method: Same as haggis-casual. A BiRefNet low-confidence patch on the chest was filled.
- Quality / caveats: Good. The pom-pom edge keeps a thin dark-brown rim, which comes from the source's own dark fur edge. One stray hair wisp on top was kept. Note: this is a different render from haggis-squatting.png.

### haggis-standing.png
- Source: `/workspace/tag-brand/approved/haggis-standing.png`
- Size: 1061×1476 px, 1.1 MB
- Method: Already transparent. Trimmed and padded only.
- Quality / caveats: Clean edges, no fringe. Body alpha is about 253 (slightly see-through); left unchanged as instructed.

### haggis-squatting.png
- Source: `/workspace/tag-brand/approved/haggis-squatting.png`
- Size: 1123×1430 px, 1.6 MB
- Method: Already transparent. Trimmed and padded only.
- Quality / caveats: As above.

### haggis-arms-out.png
- Source: `/workspace/tag-brand/approved/haggis-arms-out.png`
- Size: 1054×1513 px, 0.7 MB
- Method: Already transparent. Trimmed and padded. 232k fully transparent pixels had leftover hidden colour (invisible), which was zeroed.
- Quality / caveats: As above. Body alpha max is 254, so nothing is fully opaque.

### haggis-arms-crossed.png
- Source: `/workspace/tag-brand/approved/haggis-arms-crossed.png`
- Size: 782×1706 px, 1.2 MB
- Method: Already transparent. Trimmed and padded only.
- Quality / caveats: As above.

### a4g-logo-blue.png
- Source: `/workspace/tag-brand/approved/a4g-logo-blue.png`
- Size: 1262×1243 px, 1.4 MB
- Method: Already transparent. Trimmed and padded only.
- Quality / caveats: Clean. Body alpha is about 253.

### icon-chemical-tile.png
- Source: `/workspace/tag-brand/approved/icon-chemical.png`
- Size: 6348×6374 px, 12.6 MB
- Method: The outside was already transparent, so this is the whole tile trimmed and padded. Pixels are unchanged.
- Quality / caveats: Clean rounded corners. The baked-in fake checkerboard is still visible inside the glass (it is in the source art). Full 6250-px resolution kept, but the source is an upscale and looks soft at 100%.

### icon-play-tile.png
- Source: `/workspace/tag-brand/approved/icon-play.png`
- Size: 6348×6374 px, 13.1 MB
- Method: The outside was already transparent, so this is the whole tile trimmed and padded. Pixels are unchanged.
- Quality / caveats: Clean rounded corners. The baked-in fake checkerboard is still visible inside the glass (it is in the source art). Full 6250-px resolution kept, but the source is an upscale and looks soft at 100%.

### icon-headphones-tile.png
- Source: `/workspace/tag-brand/approved/icon-headphones.png`
- Size: 6348×6374 px, 13.4 MB
- Method: The outside was already transparent, so this is the whole tile trimmed and padded. Pixels are unchanged.
- Quality / caveats: Clean rounded corners. The baked-in fake checkerboard is still visible inside the glass (it is in the source art). Full 6250-px resolution kept, but the source is an upscale and looks soft at 100%.

### icon-signal-tile.png
- Source: `/workspace/tag-brand/approved/icon-signal.png`
- Size: 6348×6374 px, 15.1 MB
- Method: The outside was already transparent, so this is the whole tile trimmed and padded. Pixels are unchanged.
- Quality / caveats: Clean rounded corners. The baked-in fake checkerboard is still visible inside the glass (it is in the source art). Full 6250-px resolution kept, but the source is an upscale and looks soft at 100%.

### icon-waveform-tile.png
- Source: `/workspace/tag-brand/approved/icon-waveform.png`
- Size: 6348×6374 px, 11.4 MB
- Method: The outside was already transparent, so this is the whole tile trimmed and padded. Pixels are unchanged.
- Quality / caveats: Clean rounded corners. The baked-in fake checkerboard is still visible inside the glass (it is in the source art). Full 6250-px resolution kept, but the source is an upscale and looks soft at 100%.

### icon-footsteps-tile.png
- Source: `/workspace/tag-brand/approved/icon-footsteps.png`
- Size: 6348×6374 px, 12.2 MB
- Method: The outside was already transparent, so this is the whole tile trimmed and padded. Pixels are unchanged.
- Quality / caveats: Clean rounded corners. The baked-in fake checkerboard is still visible inside the glass (it is in the source art). Full 6250-px resolution kept, but the source is an upscale and looks soft at 100%.

### icon-chemical-glyph.png
- Source: `/workspace/tag-brand/approved/icon-chemical.png`
- Size: 3565×3922 px, 2.4 MB
- Method: Hue/brightness keying, not AI. Alpha comes from cyan chroma (min(G,B)−R) relative to a locally estimated tile colour (ramp 16→120), plus a brightness term near the strokes so the white specular and pale-glass parts of the tubes are kept. The tube cores are closed and filled to solid alpha with untouched source pixels. Soft edge and glow pixels are unmixed from the dark tile colour, so the glow stays soft and cyan. The black drop shadow, the tile and the checker are removed. Fragments of the tile rim and faint specks were dropped.
- Quality / caveats: Clean. The source glow is short: these are mostly hard-edged glass tubes, not a wide neon bloom.

### icon-play-glyph.png
- Source: `/workspace/tag-brand/approved/icon-play.png`
- Size: 3698×3781 px, 3.4 MB
- Method: Hue/brightness keying, not AI. Alpha comes from cyan chroma (min(G,B)−R) relative to a locally estimated tile colour (ramp 16→120), plus a brightness term near the strokes so the white specular and pale-glass parts of the tubes are kept. The tube cores are closed and filled to solid alpha with untouched source pixels. Soft edge and glow pixels are unmixed from the dark tile colour, so the glow stays soft and cyan. The black drop shadow, the tile and the checker are removed. Fragments of the tile rim and faint specks were dropped.
- Quality / caveats: Clean. The top curve runs to the tile edge in the source, so it ends abruptly at the left. The source glow is short: these are mostly hard-edged glass tubes, not a wide neon bloom.

### icon-headphones-glyph.png
- Source: `/workspace/tag-brand/approved/icon-headphones.png`
- Size: 4855×3222 px, 4.3 MB
- Method: Hue/brightness keying, not AI. Alpha comes from cyan chroma (min(G,B)−R) relative to a locally estimated tile colour (ramp 16→120), plus a brightness term near the strokes so the white specular and pale-glass parts of the tubes are kept. The tube cores are closed and filled to solid alpha with untouched source pixels. Soft edge and glow pixels are unmixed from the dark tile colour, so the glow stays soft and cyan. The black drop shadow, the tile and the checker are removed. Fragments of the tile rim and faint specks were dropped.
- Quality / caveats: Good. The pale glass fill inside the ear cups and headband is kept. There is a faint pale edge on some outer contours. The source glow is short: these are mostly hard-edged glass tubes, not a wide neon bloom.

### icon-signal-glyph.png
- Source: `/workspace/tag-brand/approved/icon-signal.png`
- Size: 5076×5081 px, 5.1 MB
- Method: Hue/brightness keying, not AI. Alpha comes from cyan chroma (min(G,B)−R) relative to a locally estimated tile colour (ramp 16→120), plus a brightness term near the strokes so the white specular and pale-glass parts of the tubes are kept. The tube cores are closed and filled to solid alpha with untouched source pixels. Soft edge and glow pixels are unmixed from the dark tile colour, so the glow stays soft and cyan. The black drop shadow, the tile and the checker are removed. Fragments of the tile rim and faint specks were dropped.
- Quality / caveats: Clean. The source glow is short: these are mostly hard-edged glass tubes, not a wide neon bloom.

### icon-waveform-glyph.png
- Source: `/workspace/tag-brand/approved/icon-waveform.png`
- Size: 3949×4321 px, 1.7 MB
- Method: Hue/brightness keying, not AI. Alpha comes from cyan chroma (min(G,B)−R) relative to a locally estimated tile colour (ramp 16→120), plus a brightness term near the strokes so the white specular and pale-glass parts of the tubes are kept. The tube cores are closed and filled to solid alpha with untouched source pixels. Soft edge and glow pixels are unmixed from the dark tile colour, so the glow stays soft and cyan. The black drop shadow, the tile and the checker are removed. Fragments of the tile rim and faint specks were dropped.
- Quality / caveats: Clean. The source glow is short: these are mostly hard-edged glass tubes, not a wide neon bloom.

### icon-footsteps-glyph.png
- Source: `/workspace/tag-brand/approved/icon-footsteps.png`
- Size: 5605×5455 px, 3.1 MB
- Method: Hue/brightness keying, not AI. Alpha comes from cyan chroma (min(G,B)−R) relative to a locally estimated tile colour (ramp 16→120), plus a brightness term near the strokes so the white specular and pale-glass parts of the tubes are kept. The tube cores are closed and filled to solid alpha with untouched source pixels. Soft edge and glow pixels are unmixed from the dark tile colour, so the glow stays soft and cyan. The black drop shadow, the tile and the checker are removed. Fragments of the tile rim and faint specks were dropped.
- Quality / caveats: Clean. The square frame line is part of the glyph and is kept. The source glow is short: these are mostly hard-edged glass tubes, not a wide neon bloom.

## Contact sheet
`contact-sheet.png` shows every file above on a mid-grey checkerboard, labelled with its filename.

## Suggested follow-ups for Neil
1. The five pre-cut PNGs (four Haggis poses and the A4G logo) are about 1% translucent everywhere. If they should be solid, setting alpha ≥ 250 to 255 is a safe one-line fix that does not change any colours. This was not done because the brief said to leave those files alone.
2. The icon tiles contain a baked-in fake transparency checkerboard. If the tiles are meant to be plain dark glass, the tile art would need re-exporting from the designer. Painting it out here would break the 'no repainting' rule.
3. The icons are 6250 px upscales and are soft at 100%. Downscaling to 1024–2048 px for use is recommended.
