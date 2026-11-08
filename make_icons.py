"""Make the Android launcher icons from one square PNG.
usage: python3 make_icons.py icon-512.png android/app/src/main/res
Only overwrites icon files that already exist in the Capacitor template.
"""
import os
import sys
from PIL import Image

src, res = sys.argv[1], sys.argv[2]
img = Image.open(src).convert("RGBA")

# (folder, legacy launcher size, adaptive layer size)
DENSITIES = [
    ("mdpi", 48, 108),
    ("hdpi", 72, 162),
    ("xhdpi", 96, 216),
    ("xxhdpi", 144, 324),
    ("xxxhdpi", 192, 432),
]

changed = 0
for name, legacy, layer in DENSITIES:
    folder = os.path.join(res, "mipmap-" + name)
    if not os.path.isdir(folder):
        continue
    # legacy icons (square + round)
    for fname in ("ic_launcher.png", "ic_launcher_round.png"):
        path = os.path.join(folder, fname)
        if os.path.exists(path):
            img.resize((legacy, legacy), Image.LANCZOS).save(path)
            changed += 1
    # adaptive foreground: icon inside the safe zone (66%) on a transparent canvas
    path = os.path.join(folder, "ic_launcher_foreground.png")
    if os.path.exists(path):
        inner = int(layer * 0.66)
        canvas = Image.new("RGBA", (layer, layer), (0, 0, 0, 0))
        icon = img.resize((inner, inner), Image.LANCZOS)
        off = (layer - inner) // 2
        canvas.paste(icon, (off, off), icon)
        canvas.save(path)
        changed += 1

# adaptive background = the app's theme green
bg = os.path.join(res, "values", "ic_launcher_background.xml")
if os.path.exists(bg):
    with open(bg, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
                '    <color name="ic_launcher_background">#0b3c29</color>\n</resources>\n')
    changed += 1

print("icons updated:", changed)
