# day1-v2 build
python3 render.py [n ...]   # renders posts (default all) x variants A/B x sizes x/ig, + layout checks (margins, logo clear-space, IG bottom 10%)
python3 contact.py          # contact-sheet-A/B.png, ig/contact-sheet-ig-A/B.png (STAND-IN LOGO note while logo isn't approved)
python3 provenance.py       # ../provenance.md from manifest.json
Approved assets: logo = approved/tag-logo-metallic.jpg (placed unaltered; visible wordmark aligned to bottom-left margin). Haggis = HAGGIS dict in render.py (post 5: haggis-arms-crossed.png). Icons not delivered yet.
Icons (top-right slot, 72px / 64px IG): post1 *headphone* (not brain), post2 *waveform*, post3 *shield*/*protected*, post4 *signal*, post6 *play*, post5 none.
Edit ICONS in render.py to change mapping. Then re-run all three scripts.
Swapping to background-removed assets: render.py resolves every approved file via approved(): if
/workspace/tag-brand/approved/clean/<same stem>.png exists it is used, otherwise the original. So once
clean/tag-logo-metallic.png and clean/haggis-arms-crossed.png exist, just re-run render.py, contact.py, provenance.py.
(haggis-casual.png is not wired in; to use it, change HAGGIS in render.py.) Icons stay off: USE_ICONS = False.
