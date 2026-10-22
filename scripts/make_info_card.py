
from pathlib import Path
from html import escape

# Output file in the repository root
root = Path(__file__).resolve().parent.parent
output_file = root / "info-card.svg"

# Customize your information here
details = [
    ("Education", "BSc Computer Science | Year 3"),
    ("University", "University of Angers, France"),
    ("Focus", "Data Analytics, Data Science & Data Engineering"),
    ("Languages", "Python, SQL, R, JavaScript, Java, C++"),
    ("Tools", "Pandas, Numpy, PostgreSQL, Git"),
    ("Projects", "Intelligent-Agricultural-Resource-Optimization, RE-WEAR, Enterprise-Sales-Data-Warehouse"),
]

width = 650
height = 330

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{width}" height="{height}" '
    f'viewBox="0 0 {width} {height}">',
    '<rect width="100%" height="100%" rx="14" fill="#0d1117"/>',
    '<rect x="1" y="1" width="648" height="328" rx="14" '
    'fill="none" stroke="#30363d"/>',
    '<style>',
    'text { font-family: monospace; font-size: 15px; }',
    '.key { fill: #58a6ff; }',
    '.value { fill: #e6edf3; }',
    '@keyframes fadeIn {',
    'from { opacity: 0; transform: translateY(4px); }',
    'to { opacity: 1; transform: translateY(0); }',
    '}',
    '@keyframes blink { 50% { opacity: 0; } }',
    '</style>',
    '<text x="25" y="42" fill="#58a6ff" '
    'font-size="17">salma@github:~$ whoami</text>',
    '<text x="25" y="78" fill="#e6edf3" '
    'font-size="17">Computer Science Student</text>'
]

# Add each line with a progressive animation
for i, (key, value) in enumerate(details):
    y = 112 + i * 31
    delay = 0.3 + i * 0.25

    svg.append(
        f'<g style="opacity:0;animation:fadeIn 0.4s '
        f'ease {delay:.2f}s forwards">'
        f'<text class="key" x="25" y="{y}">'
        f'{escape(key)}:</text>'
        f'<text class="value" x="145" y="{y}">'
        f'{escape(value)}</text>'
        f'</g>'
    )

# Animated terminal cursor
svg.append(
    '<text x="25" y="313" fill="#58a6ff" '
    'style="animation:blink 1s infinite">❯ _</text>'
)

svg.append("</svg>")

output_file.write_text("\n".join(svg), encoding="utf-8")

print("Animated information card generated!")
print(f"Saved to: {output_file}")
