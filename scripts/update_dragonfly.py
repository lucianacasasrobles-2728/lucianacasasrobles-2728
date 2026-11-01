
import json
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from xml.sax.saxutils import escape

USERNAME = "lucianacasasrobles-2728"

url = f"https://api.github.com/users/{USERNAME}/events/public?per_page=100"

request = urllib.request.Request(
    url,
    headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "GitHub-Dragonfly"
    }
)

with urllib.request.urlopen(request, timeout=20) as response:
    events = json.load(response)

now = datetime.now(timezone.utc)
week_ago = now - timedelta(days=7)

commits = 0

for event in events:
    if event["type"] != "PushEvent":
        continue

    event_date = datetime.fromisoformat(
        event["created_at"].replace("Z", "+00:00")
    )

    if event_date >= week_ago:
        commits += 1


if commits >= 5:
    message = "Your dragonfly is glowing!"
    color = "#c084fc"
    dragonfly = "dragonfly_glowing.gif"
elif commits >= 1:
    message = "Your dragonfly is active!"
    color = "#7dd3fc"
    dragonfly = "dragonfly_active.gif"
else:
    message = "Your dragonfly is resting"
    color = "#a5b4fc"
    dragonfly = "dragonfly_resting.gif"

import shutil

shutil.copyfile(
    f"assets/{dragonfly}",
    "assets/dragonfly_current.gif"
)


svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
width="500" height="60" viewBox="0 0 500 60">
<rect width="500" height="60" rx="18" fill="#151225"/>
<circle cx="35" cy="30" r="7" fill="{color}"/>
<text x="55" y="36" fill="{color}"
font-size="18" font-family="Arial">
{escape(message)}
</text>
</svg>"""

Path("assets").mkdir(exist_ok=True)
Path("assets/activity.svg").write_text(
    svg, encoding="utf-8"
)

print(f"Recent public push events: {commits}")
