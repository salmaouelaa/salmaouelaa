
import json
from pathlib import Path
from datetime import date, timedelta
from html import escape

root = Path(__file__).resolve().parent.parent
input_file = root / "data" / "contributions.json"
output_file = root / "contrib-heatmap.svg"

data = json.loads(input_file.read_text(encoding="utf-8"))

levels = {
    item["date"]: max(0, min(4, int(item["level"])))
    for item in data["days"]
}

if not levels:
    raise RuntimeError("Contribution data is empty.")

colors = [
    "#21262d",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353"
]

dates = sorted(date.fromisoformat(d) for d in levels)
start = dates[0]
end = dates[-1]

# Align the first day to Sunday
start -= timedelta(days=(start.weekday() + 1) % 7)

cell = 11
gap = 3
step = cell + gap
left = 18
top = 52

weeks = ((end - start).days // 7) + 1
width = left + weeks * step + 22
height = top + 7 * step + 20

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{width}" height="{height}" '
    f'viewBox="0 0 {width} {height}">',
    '<rect width="100%" height="100%" '
    'rx="12" fill="#0d1117"/>',
    '<style>',
    'text { font-family: monospace; fill: #e6edf3; }',
    '@keyframes appear {',
    'from { opacity: 0.15; }',
    'to { opacity: 1; }',
    '}',
    '</style>',
    '<text x="18" y="28" font-size="16">'
    f'GitHub Contributions — {escape(data["username"])}'
    '</text>'
]

current = start
while current <= end:
    week = (current - start).days // 7
    weekday = (current.weekday() + 1) % 7

    x = left + week * step
    y = top + weekday * step

    level = levels.get(current.isoformat(), 0)
    delay = week * 0.025

    svg.append(
        f'<rect x="{x}" y="{y}" '
        f'width="{cell}" height="{cell}" rx="2" '
        f'fill="{colors[level]}" '
        f'style="animation:appear 0.5s ease '
        f'{delay:.2f}s both"/>'
    )

    current += timedelta(days=1)

svg.append("</svg>")

output_file.write_text("\n".join(svg), encoding="utf-8")

print(f"Heatmap generated: {output_file}")
