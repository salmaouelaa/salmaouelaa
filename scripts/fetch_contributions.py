
import json
import re
from pathlib import Path
from datetime import datetime, timezone
import requests
from bs4 import BeautifulSoup

USERNAME = "salmaouelaa"

root = Path(__file__).resolve().parent.parent
output = root / "data" / "contributions.json"
output.parent.mkdir(parents=True, exist_ok=True)

url = f"https://github.com/users/{USERNAME}/contributions"

response = requests.get(
    url,
    headers={"User-Agent": "GitHub-Profile-README"},
    timeout=30
)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
days = []

# GitHub's contribution calendar markup can change.
for cell in soup.select("td.ContributionCalendar-day"):
    date = cell.get("data-date")
    level = cell.get("data-level", "0")

    if date:
        try:
            level = int(level)
        except ValueError:
            level = 0

        days.append({
            "date": date,
            "level": level
        })

if not days:
    raise RuntimeError(
        "No contribution data found. "
        "GitHub may have changed its calendar HTML."
    )

output.write_text(
    json.dumps({
        "username": USERNAME,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "days": days
    }, indent=2),
    encoding="utf-8"
)

print(f"Saved {len(days)} contribution days to {output}")
