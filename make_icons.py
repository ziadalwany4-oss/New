import os
import sys
from PIL import Image

src, res = sys.argv[1], sys.argv[2]
img = Image.open(src).convert("RGBA")

DENSITIES = [
    ("mdpi", 48, 108),
    ("hdpi", 72, 162),
    ("xhdpi", 96, 216),
    ("xxhdpi", 144, 324),
    ("xxxhdpi", 192, 432),
]

for name, legacy, layer in DENSITIES:
    folder = os.path.join(res, "mipmap-" + name)
    os.makedirs(folder, exist_ok=True)
    for fname in ("ic_launcher.png", "ic_launcher_round.png"):
        img.resize((legacy, legacy), Image.LANCZOS).save(os.path.join(folder, fname))
    inner = int(layer * 0.66)
    canvas = Image.new("RGBA", (layer, layer), (0, 0, 0, 0))
    icon = img.resize((inner, inner), Image.LANCZOS)
    off = (layer - inner) // 2
    canvas.paste(icon, (off, off), icon)
    canvas.save(os.path.join(folder, "hisn_fg.png"))

os.makedirs(os.path.join(res, "values"), exist_ok=True)
with open(os.path.join(res, "values", "hisn_colors.xml"), "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
            '    <color name="hisn_bg">#0b3c29</color>\n</resources>\n')

ADAPTIVE = ('<?xml version="1.0" encoding="utf-8"?>\n'
            '<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
            '    <background android:drawable="@color/hisn_bg"/>\n'
            '    <foreground android:drawable="@mipmap/hisn_fg"/>\n'
            '</adaptive-icon>\n')
folder = os.path.join(res, "mipmap-anydpi-v26")
os.makedirs(folder, exist_ok=True)
for fname in ("ic_launcher.xml", "ic_launcher_round.xml"):
    with open(os.path.join(folder, fname), "w", encoding="utf-8") as f:
        f.write(ADAPTIVE)

for d in os.listdir(res):
    if d.startswith("drawable"):
        p = os.path.join(res, d, "ic_launcher_foreground.xml")
        if os.path.exists(p):
            os.remove(p)

print("icons written")
