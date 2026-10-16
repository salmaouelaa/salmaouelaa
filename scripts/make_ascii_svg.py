
from PIL import Image, ImageOps
from pathlib import Path
from html import escape

# File locations
root = Path(__file__).resolve().parent.parent
input_file = root / "scripts/assets/profile-prepped.png"
output_file = root / "avi-ascii.svg"

# ASCII characters ordered from dark to light
chars = "@%#*+=-:. "

# Load and resize the prepared portrait
image = Image.open(input_file).convert("L")
width = 58
height = max(1, round(image.height / image.width * width * 0.5))
image = image.resize((width, height))

# Convert pixels into ASCII lines
lines = []
for y in range(height):
    line = ""
    for x in range(width):
        brightness = image.getpixel((x, y))
        index = brightness * (len(chars) - 1) // 256
        line += chars[index]
    lines.append(line)

# SVG dimensions
font_size = 10
line_height = 11
svg_width = width * 6.2 + 24
svg_height = height * line_height + 30

# Create animated SVG
svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{svg_width}" height="{svg_height}" '
    f'viewBox="0 0 {svg_width} {svg_height}">',
    '<rect width="100%" height="100%" fill="#0d1117"/>',
    '<style>',
    'text { font-family: monospace; font-size: 10px; '
    'fill: #58a6ff; white-space: pre; }',
    '@keyframes appear { from { opacity: 0; } '
    'to { opacity: 1; } }',
    '</style>'
]

for i, line in enumerate(lines):
    y = 20 + i * line_height
    delay = i * 0.09

    svg.append(
        f'<text x="12" y="{y}" '
        f'style="opacity:0;animation:appear 0.1s '
        f'ease {delay:.2f}s forwards">'
        f'{escape(line)}</text>'
    )

svg.append("</svg>")

output_file.write_text("\n".join(svg), encoding="utf-8")

print("Animated ASCII portrait generated!")
print(f"Saved to: {output_file}")
